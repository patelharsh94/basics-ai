from tkinter.constants import S
from pydantic import BaseModel


class PromptResponse(BaseModel):
    response: str = ""
    status: int = 200
    error: str = ""
