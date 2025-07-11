import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from utils.settings import API_KEY, MODEL,TASK_ATOMIZER_PROMPT
from dataclasses import dataclass
import logging
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
            instructions=(TASK_ATOMIZER_PROMPT),
            output_type=TaskAtomizerOutput
        )
    def run(self,task):
        logging.info(f"Attempting to atomize task: '{task}'")
        try:
            self.generated_tasks=self.agent.run_sync(user_prompt=task).output
            logging.info(f"Generated tasks: {self.generated_tasks.tasks}")
            return self.generated_tasks
        except Exception as e:
            logging.error(f"Error during task atomization: {e}")
            return TaskAtomizerOutput(tasks=[])  
               
if __name__=="__main__":
    TA = TaskAtomizer()
    print(TA.run("I want to tell me 10 jokes and explain me to them and categorize them"))