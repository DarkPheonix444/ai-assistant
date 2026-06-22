from pydantic import BaseModel


class CodeFile(BaseModel):

    path: str

    content: str


class CodeResponse(BaseModel):

    files: list[CodeFile]