"""Bounded Replit Gemini calls; no credentials, prompts or responses are logged."""
import asyncio,json,os
from urllib.parse import urlsplit
from httpx import TimeoutException
from google import genai
from google.genai import types

class ModelFailure(Exception):
    def __init__(self,reason):self.reason=reason

def configuration():
    key=os.getenv('AI_INTEGRATIONS_GEMINI_API_KEY','').strip()
    base=os.getenv('AI_INTEGRATIONS_GEMINI_BASE_URL','').strip()
    model=os.getenv('GEMINI_MODEL','gemini-2.5-flash').strip() or 'gemini-2.5-flash'
    return key,base,model

def status():
    key,base,model=configuration()
    valid=False
    try:
        url=urlsplit(base)
        valid=url.scheme=='https' and bool(url.hostname) and not(url.username or url.password or url.query or url.fragment)
    except ValueError:pass
    return {'configured':bool(key and valid),'model':model,'provider':'replit','configuration_only':True}

async def generate(instruction,payload,schema):
    key,base,model=configuration()
    if not key or not base:raise ModelFailure('unconfigured')
    if not status()['configured']:raise ModelFailure('configuration_error')
    try:
        async def call():
            async with genai.Client(api_key=key,http_options=types.HttpOptions(base_url=base,api_version='',timeout=12000,retry_options=types.HttpRetryOptions(attempts=1))).aio as client:
                response=await client.models.generate_content(model=model,contents=json.dumps(payload,ensure_ascii=False),config=types.GenerateContentConfig(system_instruction=instruction,response_mime_type='application/json',response_json_schema=schema,temperature=0,max_output_tokens=1800,thinking_config=types.ThinkingConfig(thinking_budget=0)))
                if not response.text or len(response.text)>16000:raise ModelFailure('invalid_response')
                return json.loads(response.text)
        return await asyncio.wait_for(call(),timeout=15)
    except ModelFailure:raise
    except (asyncio.TimeoutError,TimeoutError,TimeoutException):raise ModelFailure('timeout') from None
    except (ValueError,TypeError):raise ModelFailure('invalid_response') from None
    except Exception as error:
        code=getattr(error,'code',None)
        reason='authentication_error' if code in (401,403) else 'rate_limited' if code==429 else 'unavailable'
        raise ModelFailure(reason) from None
