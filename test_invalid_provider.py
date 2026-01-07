import os
os.environ['STRIX_LLM'] = 'invalid-provider/model'
from strix.llm import LLM
from strix.llm.config import LLMConfig
config = LLMConfig()
llm = LLM(config)
print('Testing invalid provider...')
try:
    import asyncio
    asyncio.run(llm.generate([{'role': 'user', 'content': 'test'}]))
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
