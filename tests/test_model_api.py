import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from signaldesk.providers import API
from signaldesk.model_config import model_route, validate_option
from signaldesk.settings import update_settings
from signaldesk.workflow import execute
from test_workflow import FakeAPI, post, response

CUSTOM={'CHAT_PROVIDER':'custom','LLM_API_KEY':'model-test-key','LLM_BASE_URL':'https://models.example/v1','LLM_MODEL':'test-model','TYPESAFE_API_KEY':'jev-test-key'}

class Reply:
    status=200
    headers={'x-blockrun-cost-usd':'999'}  # A different provider cannot report BlockRun costs.
    def __init__(self, body):self.body=body
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,limit):return json.dumps(self.body).encode()

class ModelAPITests(unittest.TestCase):
    @patch.dict(os.environ,CUSTOM,clear=True)
    def test_full_custom_workflow_without_blockrun(self):
        api=API();requests=[]
        def open_request(req,timeout):
            requests.append(req);body=json.loads(req.data)
            if req.full_url=='https://api.typesafe.ai/v1/systemone':
                self.assertEqual(req.get_header('Authorization'),'Bearer jev-test-key')
                return Reply(response(body['state']['posts']))
            self.assertEqual(req.full_url,'https://models.example/v1/chat/completions')
            self.assertEqual(req.get_header('Authorization'),'Bearer model-test-key')
            self.assertEqual(body['model'],'test-model')
            data=json.loads(body['messages'][1]['content'])
            output=FakeAPI().chat('',data,'draft' if 'posts' in data else 'company')
            return Reply({'choices':[{'finish_reason':'stop','message':{'content':json.dumps(output)}}]})
        with tempfile.TemporaryDirectory() as d,patch('signaldesk.workflow.ROOT',Path(d)),patch.object(api.opener,'open',side_effect=open_request):
            run=execute({'url':'https://example.com','provider':'import','brief':'Travel data eSIM for Japan. Requires a compatible unlocked phone.','days':365,'limit':10,'posts':[post()]},api=api)
            self.assertEqual(run['status'],'complete',run.get('error'))
            self.assertEqual(len(requests),3)
            self.assertEqual([c['service'] for c in api.calls],['model','jev','model'])
            self.assertTrue(all(c['cost_usd'] is None for c in api.calls if c['service']=='model'))
            self.assertNotIn('model-test-key',json.dumps(run))
    @patch.dict(os.environ,{**CUSTOM,'BLOCKRUN_API_KEY':'do-not-forward'},clear=True)
    def test_incomplete_custom_route_does_not_fall_back(self):
        del os.environ['LLM_API_KEY']
        with self.assertRaisesRegex(ValueError,'LLM_API_KEY'):model_route()
    @patch.dict(os.environ,CUSTOM,clear=True)
    def test_missing_extraction_or_search_key_fails_before_calls(self):
        for provider,brief in [('x',''),('exa','Product facts'),('x','Product facts')]:
            api=API()
            with self.assertRaises(ValueError):execute({'url':'https://example.com','provider':provider,'brief':brief},api=api)
            self.assertEqual(api.calls,[])
    def test_unsafe_base_urls_are_rejected(self):
        for url in ['http://models.example/v1','https://user:secret@models.example/v1','https://127.0.0.1/v1','https://models.example/v1?key=secret','https://models.example/v1#fragment','https://models.example/v1\nINJECT=1','https://host.internal/v1']:
            with self.assertRaises(ValueError):validate_option('LLM_BASE_URL',url)
        self.assertEqual(validate_option('LLM_BASE_URL','https://models.example/api/v1/'),'https://models.example/api/v1')
    def test_endpoint_change_requires_explicit_new_key_and_is_atomic(self):
        env=dict(CUSTOM)
        payload={'options':{'LLM_BASE_URL':'https://different.example/v1'}}
        with self.assertRaisesRegex(ValueError,'new model API key'):update_settings(payload,Path('/unused'),env)
        self.assertEqual(env,CUSTOM)
        with tempfile.TemporaryDirectory() as d:
            payload.update(keys={'LLM_API_KEY':'different-test-key'},persist=True)
            result=update_settings(payload,Path(d)/'.env',env)
            self.assertEqual(result['options']['LLM_BASE_URL'],'https://different.example/v1')
            self.assertNotIn('different-test-key',str(result))
    @patch.dict(os.environ,{'BLOCKRUN_API_KEY':'legacy-key'},clear=True)
    def test_existing_blockrun_setup_is_preserved(self):
        self.assertEqual(model_route(),('blockrun','https://api.blockrun.ai/v1','BLOCKRUN_API_KEY','openai/gpt-4o-mini'))
