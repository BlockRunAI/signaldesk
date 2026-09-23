import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from signaldesk.settings import update_settings

class SettingsTests(unittest.TestCase):
    def test_session_only_never_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'.env';env={}
            result=update_settings({'keys':{'X_BEARER_TOKEN':'test-token-123'}},path,env)
            self.assertFalse(path.exists());self.assertTrue(result['configured']['X_BEARER_TOKEN'])
            self.assertNotIn('test-token-123',str(result))
    def test_private_atomic_save_preserves_other_settings_and_blank(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'.env';path.write_text('CHAT_MODEL=example\nX_BEARER_TOKEN=old-token\n')
            env={'TYPESAFE_API_KEY':'keep-token'}
            update_settings({'keys':{'X_BEARER_TOKEN':'new-token','TYPESAFE_API_KEY':''},'persist':True},path,env)
            self.assertEqual(path.stat().st_mode & 0o777,0o600)
            self.assertIn('CHAT_MODEL=example',path.read_text());self.assertNotIn('old-token',path.read_text())
            self.assertEqual(env['TYPESAFE_API_KEY'],'keep-token')
    def test_rejects_injection_without_mutation(self):
        for payload in [{'keys':{'OTHER':'secret-value'}},{'keys':{'X_BEARER_TOKEN':'abc\nEVIL=1'}},{'keys':{'X_BEARER_TOKEN':'secret-value'},'remove':['X_BEARER_TOKEN']}]:
            env={}
            with self.assertRaises(ValueError):update_settings(payload,Path('/unused'),env)
            self.assertEqual(env,{})
    def test_disk_failure_does_not_change_session(self):
        with tempfile.TemporaryDirectory() as folder:
            env={'X_BEARER_TOKEN':'old-token'}
            with patch('signaldesk.settings.os.replace',side_effect=OSError):
                with self.assertRaises(OSError):update_settings({'keys':{'X_BEARER_TOKEN':'new-token'},'persist':True},Path(folder)/'.env',env)
            self.assertEqual(env['X_BEARER_TOKEN'],'old-token')
    def test_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);(p/'target').write_text('preserve');(p/'.env').symlink_to(p/'target')
            with self.assertRaises(ValueError):update_settings({'keys':{'X_BEARER_TOKEN':'new-token'},'persist':True},p/'.env',{})
            self.assertEqual((p/'target').read_text(),'preserve')
