from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool, StructuredTool
from datetime import datetime
import wikipedia

def save_to_file(filename: str, content: str):
    """Saves content to a file and returns the file path."""
    formatted_text = f"---Research Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})---\n\n{content}"
    with open(filename, "w") as file:
        file.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = StructuredTool.from_function(
    save_to_file,
    name="save_results",
    description="Saves the research summary to a specified file. Expects {filename: str, content: str}.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Useful for when you need to answer questions about current events or find specific information online.",
)

api_wrapper = WikipediaAPIWrapper(wiki_client=wikipedia, top_k_results=1, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)