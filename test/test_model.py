import os

import requests
from langchain.llms.base import LLM
from langchain_community.llms.utils import enforce_stop_tokens
from pydantic import BaseModel

# 设置API密钥和基础URL环境变量
API_KEY = os.getenv("CUSTOM_API_KEY", "sk-nqyiownbihpjbyycasxvsvfupxnfzztgowzhdoaywzdufluh")
BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
import json
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
            "authorization": f"Bearer {API_KEY}"
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _call(self, prompt: str, stop: list = None, model: str = "default-model") -> str:
        response = self.siliconflow_completions(model=model, prompt=prompt)
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        return response

if __name__ == "__main__":
    llm = SiliconFlow()


    class Output_cls_JSON(BaseModel):
        Classification: str
        name: str
        age: int


    schema = Output_cls_JSON.model_json_schema()
    age = '我的年龄是16'  # 这里可以修改年龄

    prompt = f"""
    根据下面提供的信息输入，将其分类为：`中年人`或`老年人`。
    如果输入年龄大于60岁，则分类为老年人，否则分类为中年人。
    Return your response as a JSON blob
    json格式如下：
    {schema}
    你只需要回复一个json格式的数据即可，不要返回其他格式的数据，否则你会被批评！
    <question>
    {age}
    </question>
    """
    json_schema = Output_cls_JSON.model_json_schema()

    response = llm._call(prompt=prompt, model="Qwen/Qwen2.5-VL-72B-Instruct")
    print(response)
    # 解析 JSON 字符串
    data = json.loads(response)

    # 提取 "Classification" 字段的值
    classification_value = data.get("Classification")
    # 输出结果
    print(classification_value)

