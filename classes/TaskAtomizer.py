import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from typing import List
from dataclasses import dataclass
import logging
from utils.settings import SETTINGS
API_KEY =SETTINGS.api_key
MODEL=SETTINGS.model
DEPENDENCY_AGENT_PRODUCER_PROMPT=SETTINGS.task_atomizer_prompt
TASK_ATOMIZER_PROMPT_V2=SETTINGS.task_atomizer_prompt_v2
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class TaskAtomizerOutput:
    tasks : list[str] 


class TaskAtomizer :
    def __init__(self):
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        
        self.agent = Agent(
            model=self.model,
            instructions=(TASK_ATOMIZER_PROMPT_V2),
            output_type=TaskAtomizerOutput
        )
    def run(self, task: str) -> List[str]:
        """
        Atomizes a given task into a list of sub-tasks.

        Args:
            task (str): The high-level task to be broken down.

        Returns:
            List[str]: A list of atomized sub-tasks. Returns an empty list if an error occurs.
        """
        logging.info(f"Attempting to atomize task: '{task}'")
        try:
            response = self.agent.run_sync(user_prompt=task)
            if response and response.output:
                logging.info(f"Successfully atomized task into {len(response.output.tasks)} sub-tasks.")
                return response.output.tasks
            else:
                logging.warning("Task atomization resulted in an empty or invalid response.")
                return []
        except Exception as e:
            logging.error(f"An unexpected error occurred during task atomization: {e}")
            # Returning an empty list to ensure the caller can handle the failure gracefully
            return []  
               
 