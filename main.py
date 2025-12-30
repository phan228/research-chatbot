from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from langchain.agents import create_agent, AgentExecutor
import re
import os

load_dotenv()  # Load environment variables from .env file

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    references: list[str]
    tools_used: list[str]

default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#gpt = init_chat_model("gpt-4.1")
gpt = ChatOpenAI(model=default_model, temperature=0)
#claude = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# Parse the response into a ResearchResponse object to use
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

system_prompt = (
    "You are a research assistant that provides detailed summaries on various topics. "
    "Answer the user query and use necessary tools to gather information. "
    f"Wrap the response in this format and provide no other text:\n{parser.get_format_instructions()}"
)
