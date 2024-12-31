import os
import asyncio
from typing import Optional
from openai import AsyncAzureOpenAI, AsyncOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from utils.logging import time_logger

class OpenAIClient:
    def __init__(self, model: str):

        use_azure = os.environ.get("USE_AZURE_OPENAI", 'False').lower() == 'true'
        use_azure_auth = os.environ.get("USE_AZURE_OPENAI_AUTH", 'False').lower() == 'true'

        if use_azure_auth:
            token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

        if use_azure:
            self.client = AsyncAzureOpenAI(
                api_key= os.environ.get("AZURE_OPENAI_API_KEY") if not use_azure_auth else None,
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
                azure_ad_token_provider=token_provider if use_azure_auth else None,
            )
                
        else:
            self.client = AsyncOpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )

        self.model = model

    @time_logger()
    async def get_response(self, system_prompt: str, query: str, history: Optional[list[dict]] = None):
        system_prompt = {"role": "system", "content": system_prompt}

        query = {"role": "user", "content": query}

        # add system prompt
        messages = [system_prompt]

        # add history
        if history:
            for h in history:
                if h.get("role") and h.get("content"):
                    messages.append({"role": h.get("role"), "content": h.get("content")})
        
        # add query
        messages.append(query)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content