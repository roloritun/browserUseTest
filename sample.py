from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

# import asyncio
import uuid
from dotenv import load_dotenv

# from langchain_openai import (
#     AzureChatOpenAI,
#     AzureOpenAIEmbeddings,
# )

# from logger_config import setup_logger, get_logger

# Configure logging
# setup_logger()
# logger = get_logger()

load_dotenv()

# LLM = AzureChatOpenAI(
#      azure_deployment="4o-mini-deploy")

LLM = ChatOpenAI(model="gpt-4o-mini")


async def run_task(task: str):
    browser_context_config = BrowserContextConfig(save_recording_path="recordings/")
    try:
        browser = Browser(
            config=BrowserConfig(
                headless=True,
                disable_security=True,
                new_context_config=browser_context_config,
            )
        )
    except Exception as e:
        print(f"Error initializing browser: {e}")
        return {"error": f"Error initializing browser: {e}"}

    try:
        print(f"Starting task: {task}")
        agent = Agent(
            task=task,
            llm=LLM,
            validate_output=True,
            save_conversation_path=f"conversations/conversation{uuid.uuid4().hex}.json",
            browser=browser,
            generate_gif=True,
        )
        result = await agent.run()
        final_result = result
        print(f"Task completed successfully: {final_result}")
        print(f"screenshots: {result.screenshots()}")
        print(f"model thoughts: {result.model_thoughts()}")
        print(f"action results: {result.action_results()}")
        print(f"is done: {result.is_done()}")
        print(f"has errors: {result.has_errors()}")
        return final_result
    except Exception as e:
        print(f"Error running task: {e}")
        return {"error": str(e)}
    finally:
        try:
            await browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")

""" async def main():
    agent = Agent(
        task="Find a one-way flight from Bali to Oman on 25 January 2025 on Google Flights. Return me the cheapest option.",
        llm=LLM,
    )
    result = await agent.run()
    print(result)


asyncio.run(main())
 """
