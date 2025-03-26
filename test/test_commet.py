import requests

from constant import model as MODEL_CONSTANT

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": '"Qwen/Qwen2-7B-Instruct',
    "messages": [
        {
            "role": "user",
            "content": "What opportunities and challenges will the Chinese large model industry face in 2025?"
        }
    ],
    "stream": False,
    "max_tokens": 512,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {"type": "json_object"},
    "tools": [

    ]
}
headers = {
    "Authorization": "Bearer " + MODEL_CONSTANT.API_KEY,
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
