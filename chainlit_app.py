import chainlit as cl
import logging
import os
import warnings

from dotenv import load_dotenv
from langchain_community.chat_models import ChatLiteLLM

from salesgpt.agents import SalesGPT

load_dotenv()  # loads .env file

# Suppress warnings
warnings.filterwarnings("ignore")

# Suppress logging
logging.getLogger().setLevel(logging.CRITICAL)

# LangSmith settings section, set TRACING_V2 to "true" to enable it
# or leave it as it is, if you don't need tracing (more info in README)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "tshortGPT"  # insert your project name here

@cl.on_chat_start
def main():
    llm = ChatLiteLLM(temperature=0.2, model_name="gpt-3.5-turbo")
    print("No agent config specified, using a standard config")
    # keep boolean as string to be consistent with JSON configs.
    sales_agent_kwargs = {
        "verbose": True,
        "use_tools": True,
    }

    sales_agent_kwargs.update(
        {
            "product_catalog": "examples/t_short_full_catalog.txt",
            "salesperson_name": "Motilda Sergeevna",
        }
    )

    sales_agent = SalesGPT.from_llm(llm, **sales_agent_kwargs)
    sales_agent.seed_agent()

    # Store the chain in the user session
    cl.user_session.set("sales_agent", sales_agent)


@cl.on_message
async def handle_message(message: cl.Message):
    # Retrieve the chain from the user session
    human_input = message.content
    sales_agent = cl.user_session.get("sales_agent")
    sales_agent.human_step(human_input)
    sales_agent.step()
    last_ai_message = sales_agent.conversation_history[-1]
    # Send the last AI message back to the user
    if "<END_OF_CALL>" in last_ai_message:
        await cl.Message(
            content=f"Sales Agent determined it is time to end this conversation.",
        ).send()
    else:
        await cl.Message(content=last_ai_message.replace("<END_OF_TURN>", "")).send()




