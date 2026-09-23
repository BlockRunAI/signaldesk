"""Local-only credential configuration. Secrets are never returned to the UI."""
import os
from pathlib import Path
import tempfile

KEYS = ('BLOCKRUN_API_KEY', 'TYPESAFE_API_KEY', 'X_BEARER_TOKEN', 'TWITTERAPI_KEY')

def configured(environ=None):
    env = os.environ if environ is None else environ
    return {key: bool(env.get(key)) for key in KEYS}

def update_settings(payload, env_path, environ=None):
    env = os.environ if environ is None else environ
    if not isinstance(payload, dict) or set(payload) - {'keys', 'remove', 'persist'}:
        raise ValueError('Invalid settings fields')
    values = payload.get('keys', {})
    remove = payload.get('remove', [])
    persist = payload.get('persist', False)
    if not isinstance(values, dict) or set(values) - set(KEYS):
        raise ValueError('Unknown credential field')
    if not isinstance(remove, list) or any(key not in KEYS for key in remove):
        raise ValueError('Unknown credential to remove')
    if not isinstance(persist, bool):
        raise ValueError('Invalid persistence setting')
    changes = {}
    for key, value in values.items():
        if not isinstance(value, str):
            raise ValueError('Credentials must be text')
        if not value:  # Blank means keep the current value.
            continue
        if not 8 <= len(value) <= 4096 or any(c.isspace() or ord(c) < 33 or ord(c) > 126 for c in value) or any(c in value for c in '\"\'\\'):
            raise ValueError('Credentials must be 8–4096 printable characters without spaces or quotes')
        changes[key] = value
    if set(changes) & set(remove):
        raise ValueError('Cannot save and remove the same credential')
    for key in remove:
        changes[key] = None
    if persist and changes:
        path = Path(env_path)
        # Refuse symlinks, preserve unrelated configuration, atomically replace with mode 0600.
        if path.is_symlink():
            raise ValueError('Settings file must not be a symbolic link')
        lines = path.read_text().splitlines() if path.exists() else []
        lines = [line for line in lines if line.partition('=')[0].strip() not in changes]
        lines += [f'{key}={value}' for key, value in changes.items() if value is not None]
        fd, temporary = tempfile.mkstemp(prefix='.signaldesk-env-', dir=path.parent)
        try:
            with os.fdopen(fd, 'w') as out:
                out.write('\n'.join(lines) + '\n')
            os.chmod(temporary, 0o600)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    for key, value in changes.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    return {'configured': configured(env), 'storage': 'local file and current session' if persist else 'current session only'}
