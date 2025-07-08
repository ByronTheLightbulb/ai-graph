import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from utils.settings import API_KEY, MODEL
from dataclasses import dataclass


@dataclass
class ProducerAgentOutput:
     
     
    instructions: str
    output_model_json: str
 
class AgentProducer:
    
    def __init__(self):
        self.id = uuid.uuid4()
        provider = GoogleProvider(api_key=API_KEY)
        model = GoogleModel(MODEL, provider=provider)
        agent = Agent(model)
        self.agent = Agent(
            model=MODEL,
            instructions="You are a producer agent. You will produce agents based on the input task provided and return the pydantic baseModel in json format that describes the output of the agent.",
            output_type=ProducerAgentOutput
        )