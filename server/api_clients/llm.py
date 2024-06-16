import os
import asyncio
from typing import Optional
from openai import AsyncAzureOpenAI

class OpenAIClient:
    def __init__(self, model: str):
        self.client = AsyncAzureOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            azure_endpoint=os.environ.get("OPENAI_ENDPOINT"),
            api_version=os.environ.get("OPENAI_API_VERSION", "2023-12-01-preview")
        )
        self.model = model

    async def get_response(self, system_prompt: str, query: str, history: Optional[list[str]] = None):
        system_prompt = {"role": "system", "content": system_prompt}

        query = {"role": "user", "content": query}

        # add system prompt
        messages = [system_prompt]

        # add history
        if history:
            messages.extend(history)
        
        # add query
        messages.append(query)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content