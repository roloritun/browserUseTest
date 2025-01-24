from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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


