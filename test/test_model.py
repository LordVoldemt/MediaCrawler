from pydantic import BaseModel

from tools.send_model import SiliconFlow
import json
from constant import model as model_constant
if __name__ == "__main__":
    llm = SiliconFlow()


    class Output_cls_JSON(BaseModel):
        potential_customers: str
        intention_rate: str
        explain: str


    schema = Output_cls_JSON.model_json_schema()
    title = '天气不错，'
    content = f"""
   天气不错，今天适合出行。
    """
    prompt = f"""
    # 角色
    你是一位专业的运营人员，擅长根据帖子的标题和内容判断用户是否为潜在客户，并用分数来表示其成为客户的可能性。

    ## 技能
    ### 技能1：内容分析与判断
    - **任务**：根据用户提供的帖子标题和具体内容，判断该用户是否为潜在客户。
      - 分析帖子的内容，识别用户的痛点、需求和预算等关键信息。
      - 根据内容判断用户是否有明确的需求或问题，并评估其成为潜在客户的可能性。
      - 如果是潜在客户，给出一个具体的意向率百分比（例如80%）。
      - 如果不是潜在客户，直接输出“非潜在客户”。
      -需要判断客户的阶段，如果已经产生了购买行为，就不是潜在用户了。
    ## 限制
    - 仅基于提供的帖子标题和内容进行判断。
    - 意向率百分比应基于实际内容的分析，而不是主观猜测。
    - 输出结果必须简洁明了，包含“潜在客户”或“非潜在客户”，如果是潜在客户，将potential_customers设置为1，还需附上具体的意向率百分比及解释，将意向率百分比设置到intention_rate，
    将解释设置到explain，如果是非潜在客户，将potential_customers设置为0，将intention_rate设置为0%，将解释设置到explain。
    - 不引入无关信息，保持输出的专业性和准确性。
    Return your response as a JSON blob
    json格式如下：
    {schema}
    你只需要回复一个json格式的数据即可，不要返回其他格式的数据，否则你会被批评！
    <question>
    标题：
    {title}
    内容：
    {content}
    </question>
    """
    json_schema = Output_cls_JSON.model_json_schema()

    response = llm._call(prompt=prompt, model=model_constant.MODEL_NAME)
    # 去掉 `json` 开头和 `'''` 结尾
    cleaned_response = response.replace('json', '').replace('```', '').strip()
    # 解析 JSON 字符串
    data = json.loads(cleaned_response)
    # # 输出结果
    print(data.get('potential_customers'))
    print(data.get('intention_rate'))
    print(data.get('explain'))
