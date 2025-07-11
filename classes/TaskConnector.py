import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dataclasses import dataclass
import logging
from typing import Dict,List

from utils.settings import API_KEY, MODEL,TASK_CONNECTOR_PROMPT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



 
from pydantic import BaseModel
from typing import List, Tuple

class TaskConnectorOutput(BaseModel):
    tasks: List[Tuple[str, List[int]]]

    def to_dict(self) -> Dict[str, List[int]]:
        return dict(self.tasks)


class TaskConnector :
    def __init__(self):

        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        
        self.agent = Agent(
            model=self.model,
            instructions=(TASK_CONNECTOR_PROMPT),
            output_type=TaskConnectorOutput
        )
        
    def run(self,initial_task,tasks):
        logging.info(f"Attempting to create connections for the tasks")
        try:
            
            # Creating the prompt with the list of task with their id's
            user_prompt =f"General Task :{initial_task}\nIndividual Tasks: \n"
            for i in range(0,len(tasks)) :
                user_prompt+=f"{i}.{tasks[i]}"
            
            self.generated_graph=self.agent.run_sync(user_prompt=user_prompt).output
            logging.info(f"Generated connections" )
            return self.generated_graph.tasks
        except Exception as e:
            logging.error(f"Error during the connecting of tasks : {e}")
            return "TaskConnectorOutput()"   
 
     