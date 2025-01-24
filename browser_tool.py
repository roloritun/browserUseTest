from typing import Any, Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from browser_use import Agent, AgentHistoryList, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from constants import MAX_STEPS
import uuid

from constants import MAX_STEPS
from llm_manager import LLM
from pprint import pprint


class BrowseUseTool(BaseTool):
    name: str
    description: str
    args_schema: Type[BaseModel]
    prompt_query: Optional[str] = None
    return_direct: bool = True
    llm: Any
    stamp: str = uuid.uuid4().hex

    async def _arun(self, task: str):
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
                save_conversation_path=f"conversations/conversation{self.stamp}.json",
                browser=browser,
                generate_gif=True,
            )
            result: AgentHistoryList = await agent.run(max_steps=MAX_STEPS)
            final_result = result.final_result()

            print('Final Result:')
            pprint(result.final_result(), indent=4)

            print('\nErrors:')
            pprint(result.errors(), indent=4)

            print('\nModel Outputs:')
            pprint(result.model_outputs(), indent=4)

            print('\nThoughts:')
            pprint(result.model_thoughts(), indent=4) 

            print('\nModel Actions:')
            pprint(result.model_actions(), indent=4)

            print('\nActions Names:')
            pprint(result.action_names(), indent=4)

            print("\nUrls:")
            pprint(result.urls(), indent=4)

            # print("\nScreenshots:")
            # pprint(result.screenshots(), indent=4)

            return final_result
        except Exception as e:
            print(f"Error running task: {e}")
            return {"error": str(e)}
        finally:
            try:
                await browser.close()
            except Exception as e:
                print(f"Error closing browser: {e}")

    def _run(self, task: str):
        raise NotImplementedError("supports only async")
