import os

import requests
from langchain.llms.base import LLM
from langchain_community.llms.utils import enforce_stop_tokens
from pydantic import BaseModel
import json
# 设置API密钥和基础URL环境变量

from constant import model as model_constant


class SiliconFlow(LLM):
    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "siliconflow"

    def siliconflow_completions(self, model: str, prompt: str) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {model_constant.API_KEY}"
        }

        response = requests.post(model_constant.BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _call(self, prompt: str, stop: list = None, model: str = "default-model") -> str:
        response = self.siliconflow_completions(model=model, prompt=prompt)
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        return response