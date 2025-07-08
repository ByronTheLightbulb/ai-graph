import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from utils.JsonToModel import JsonToModel

from utils.settings import API_KEY, MODEL
from dataclasses import dataclass


@dataclass
class ProducerAgentOutput:
     
     
    instructions: str
    output_model_json: str
 
class AgentProducer:
    
    def __init__(self):
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
         
        self.agent = Agent(
            model=self.model,
            instructions=(
"                    i will tell you a user task and you will create a pydantic basemodel as a json  that describes the output of an ai agent that performs that task"     ),
            output_type=ProducerAgentOutput
        )
    def run(self,task):
        self.generated_agent_definitions=self.agent.run_sync(user_prompt=task).output
        self.generated_agent = Agent(model=self.model,instructions=self.generated_agent_definitions.instructions,output_type=JsonToModel(self.generated_agent_definitions.output_model_json))
        return self.generated_agent
    
    def save(self):
        pass 