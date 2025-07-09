import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from utils.settings import API_KEY, MODEL
from dataclasses import dataclass

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
            instructions=(
            "You will receive a user task. Your job is to decompose it into a list of atomic tasks. "
            "Each atomic task must be the smallest possible actionable step that cannot be further subdivided. "
            "Ensure each task is clear, precise, and can be executed independently by an agent (e.g., querying a database, calling an API, processing data). "
            "Do not group multiple actions together. Only output tasks that are truly indivisible."
            ),
            output_type=TaskAtomizerOutput
        )
    def run(self,task):
        self.generated_tasks=self.agent.run_sync(user_prompt=task).output
        return self.generated_tasks
     
     
if __name__=="__main__":
    TA = TaskAtomizer()
    print(TA.run("I want to look at my financial transactions for possible improvements for my business"))