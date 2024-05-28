import pydantic 

class LogSchema(pydantic.BaseModel):
    message: str
    level: str
    user: str
