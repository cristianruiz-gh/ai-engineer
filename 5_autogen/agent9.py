```python
import os
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a sustainable finance expert. Your task is to generate innovative financial solutions for environmentally conscious businesses.
    Your personal interests are in these sectors: Renewable Energy, Carbon Trading.
    You are drawn to ideas that promote eco-friendly practices and reduce waste.
    You are less interested in ideas that prioritize profits over sustainability.
    You are meticulous, analytical and have a keen eye for detail. You are a team player and value collaboration.
    Your weaknesses: you can be overly perfectionistic, and sometimes struggle with delegation.
    You should respond with your financial solutions in a clear and concise manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.7

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(
            model="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.8,
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": "llama3",
                "structured_output": True,  
            }
        )
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my financial solution. It may not be perfect, but please help me refine it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
```