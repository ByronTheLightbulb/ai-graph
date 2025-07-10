import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from utils.settings import API_KEY, MODEL
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
            instructions=(
                "You are an hyper-detailed, meticulous project manager and data analyst. Your core function is to decompose any user task into the absolute smallest, most fundamental, and independently executable atomic steps. "
                "For *every* part of the user's request, you must break it down into the most minute, single, distinct actions. "
                "Think step-by-step, as if you are preparing a precise checklist for an automated system with very limited capabilities per step. "
                "Each atomic task must represent a single, indivisible operation that, once completed, allows the next single step to proceed. "
                "**Crucial Rule: If a step can be logically broken down into two or more distinct sub-steps, it is NOT atomic and MUST be further subdivided.** "
                "Consider the entire lifecycle: from data acquisition, through cleaning, structuring, specific calculations, different types of analysis, interpretation, to concrete recommendation formulation and presentation. "
                "Examples of atomic vs. non-atomic breakdown for common analytical tasks: "
                "- 'Analyze data' is NON-ATOMIC. Break it into: 'Calculate average X', 'Identify max Y', 'Filter data by Z', 'Compare A to B', 'Plot trend of C'. "
                "- 'Generate report' is NON-ATOMIC. Break it into: 'Compile findings for Section 1', 'Draft conclusion statement', 'Format report layout'. "
                "- 'Make recommendations' is NON-ATOMIC. Break it into: 'Identify specific problem P', 'Propose solution S for problem P', 'State rationale for solution S', 'Quantify potential impact of solution S'. "
                "Ensure every generated task is crystal clear, singularly focused, actionable, and can be performed without any hidden sub-steps. "
                "List all fundamental component actions explicitly, leaving absolutely no implicit actions or assumptions."
            ),
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