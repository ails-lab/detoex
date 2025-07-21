from fastapi import FastAPI

from detoex.api_modules.main_module import detect_and_explain
from detoex.utils.api_helper_classes import *


app = FastAPI()


@app.post('/')
async def base_request(request: BaseRequest) -> BaseResponse:
    texts = request.texts
    language = request.language
    detoex = detect_and_explain(texts, language=language)
    return BaseResponse(
        results=detoex
    )
