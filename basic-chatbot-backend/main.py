from fastapi import FastAPI, Query, status
from fastapi.responses import StreamingResponse
from models.prompt_response import PromptResponse
from models.prompt_request import PromptRequest
from dotenv import load_dotenv
from agents import Agent, Runner, trace, RunErrorDetails
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(override=True)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "Healthy"

@app.post(f"/prompt/", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def prompt_llm(prompt: PromptRequest):
    request = prompt.request_prompt
    response = PromptResponse()

    basic_request_agent = Agent(
        name="basic agent",
        instructions="Just answer the question.",
        model="gpt-4o-mini"
    )

    try:
        with trace("basic_request"):
            res = await Runner.run(basic_request_agent, request)
            response.response = res.final_output
    except RunErrorDetails as e:
        response.response = "Error occured when calling the llm"
        response.error = e
        response.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return response