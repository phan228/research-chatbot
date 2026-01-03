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

def main():
    parser_cli = argparse.ArgumentParser(description="Research assistant")
    parser_cli.add_argument("--tools-only", action="store_true", help="Run tools directly without LLM")
    parser_cli.add_argument("--save", type=str, default=None, help="Optional file to save the summary")
    args_cli = parser_cli.parse_args()

    user_query = input("What can I help you research today? ")

    if args_cli.tools_only:
        # Direct tool execution path (no LLM call)
        try:
            search_result = search_tool.invoke(user_query)
            wiki_result = wiki_tool.invoke(user_query)
            # Extract URLs from search result for references
            refs = list(dict.fromkeys(re.findall(r"https?://\S+", str(search_result))))
            tools_used = [search_tool.name, getattr(wiki_tool, "name", "Wikipedia")]
            summary = (str(wiki_result) or "")
            if search_result:
                snippet = str(search_result)
                summary = (summary + "\n\nSearch highlights:\n" + snippet)[:1500]
            resp = ResearchResponse(
                topic=user_query,
                summary=summary,
                references=refs,
                tools_used=tools_used,
            )
            print(resp)
if __name__ == "__main__":
    main()