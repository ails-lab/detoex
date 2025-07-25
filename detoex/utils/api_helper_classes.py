from dataclasses import dataclass

from pydantic import BaseModel


class BaseRequest(BaseModel):
    language: str
    texts: list[str]


class BaseResponse(BaseModel):
    results: list[str]


@dataclass
class Match:
    term_uri: str
    term_literal: str
    issue_description: str
    categories: str
    text: str
    start_char: int
    end_char: int
    sentence_index: int | None
    word_id: int
