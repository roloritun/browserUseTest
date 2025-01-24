from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from pydantic import BaseModel, Field

from browser_tool import BrowseUseTool
from llm_manager import LLM
from constants import AGENT_EXECUTOR_VERBOSE, RETURN_INTERMIDIATE_STEPS

from prompt import (
    get_prompt_for_openai_functions_agent,
)


class Task(BaseModel):
    task: str = Field(description="Task to be performed")


def create_browser_tool():
    tool = BrowseUseTool(
        name="browser",
        description="Use browser to perform tasks",
        args_schema=Task,
        llm=LLM,
    )
    return tool


def create_langchain_agent():
    all_tools = []
    llm = LLM

    all_tools =  [create_browser_tool()]

    prompt = get_prompt_for_openai_functions_agent()
    agent = create_openai_functions_agent(llm=llm, tools=all_tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=AGENT_EXECUTOR_VERBOSE,
        handle_parsing_errors=True,
        # max_iterations=3,
        return_intermediate_steps=RETURN_INTERMIDIATE_STEPS,
        early_stopping_method="generate",
    )
    return agent_executor


async def run_task(task: str):
    agent = create_langchain_agent()
    return await agent.ainvoke({"input": task})    
