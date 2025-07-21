from pydantic import BaseModel


class BaseRequest(BaseModel):
    language: str
    texts: list[str]


class BaseResponse(BaseModel):
    results: list[str]
    