from pydantic import BaseModel


class PromptRequest(BaseModel):
    request_prompt: str = ""

