"""Explicit model routing; provider credentials never fall back across origins."""
import os
import re
from urllib.parse import urlsplit
from .core import public_url

OPTIONS = ('CHAT_PROVIDER', 'LLM_BASE_URL', 'LLM_MODEL')

def validate_option(key, value):
    if not isinstance(value, str) or not value or len(value) > 512:
        raise ValueError('Model configuration must be nonempty text (at most 512 characters)')
    if key == 'CHAT_PROVIDER':
        if value not in ('blockrun', 'custom'):
            raise ValueError('Select BlockRun or an OpenAI-compatible model API')
    elif key == 'LLM_BASE_URL':
        try:
            public_url(value)
            parsed = urlsplit(value)
            if parsed.query or parsed.fragment or not re.fullmatch(r'https://[A-Za-z0-9.:-]+(?:/[A-Za-z0-9._~-]+)*/?', value):
                raise ValueError()
        except ValueError:
            raise ValueError('Base URL must be a public HTTPS API root without credentials, query or fragment') from None
        value = value.rstrip('/')
    elif key == 'LLM_MODEL':
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./:@+-]{0,199}', value):
            raise ValueError('Enter a valid model ID (at most 200 characters)')
    else:
        raise ValueError('Unknown model configuration field')
    return value

def model_options(environ=None):
    env = os.environ if environ is None else environ
    return {key: env.get(key, 'blockrun' if key == 'CHAT_PROVIDER' else '') for key in OPTIONS}

def model_route(environ=None):
    env = os.environ if environ is None else environ
    provider = validate_option('CHAT_PROVIDER', env.get('CHAT_PROVIDER', 'blockrun'))
    if provider == 'custom':
        missing = [key for key in ('LLM_API_KEY', 'LLM_BASE_URL', 'LLM_MODEL') if not env.get(key)]
        if missing:
            raise ValueError('Missing configuration: ' + ', '.join(missing))
        base = validate_option('LLM_BASE_URL', env['LLM_BASE_URL'])
        model = validate_option('LLM_MODEL', env['LLM_MODEL'])
        return 'model', base, 'LLM_API_KEY', model
    if not env.get('BLOCKRUN_API_KEY'):
        raise ValueError('Missing configuration: BLOCKRUN_API_KEY (or select your own model API)')
    return 'blockrun', 'https://api.blockrun.ai/v1', 'BLOCKRUN_API_KEY', env.get('CHAT_MODEL', 'openai/gpt-4o-mini')
