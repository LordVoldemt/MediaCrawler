from pydantic import BaseModel

class Output_cls_JSON(BaseModel):
    desc: str
    cumster_flag: int
json_schema = Output_cls_JSON.model_json_schema()
print(json_schema)