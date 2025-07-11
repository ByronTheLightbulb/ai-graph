import uuid 
from pydantic_ai import Agent  
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dataclasses import dataclass
import logging
from typing import Dict,List

from utils.settings import API_KEY, MODEL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



 
from pydantic import BaseModel
from typing import List, Tuple

class TaskConnectorOutput(BaseModel):
    tasks: List[Tuple[str, List[int]]]

    def to_dict(self) -> Dict[str, List[int]]:
        return dict(self.tasks)


class TaskConnector :
    def __init__(self):
        INSTRUCTION = """
You are an expert AI agent responsible for constructing a fully-connected dependency graph (DAG) of AI subtasks.

You will be given:
- A general task description  
- A list of atomic subtasks (each labeled with an integer ID and a short textual description)

Each task is an autonomous unit that may:
- Require the output of previous tasks as input  
- Enable the execution of other tasks upon completion

Your goal is to connect these atomic tasks into a valid Directed Acyclic Graph (DAG), where:
- Each task is represented by a key (its ID as a string)
- Each key maps to a list of IDs of other tasks that must precede it and whose output will be used as input to the task

Output Format:
Produce your output as a JSON dictionary:
{
  "1": [],
  "2": [1],
  "3": [1, 2]
}

This means:
- Task 1 has no dependencies and can run immediately.  
- Task 2 depends on task 1.  
- Task 3 depends on both tasks 1 and 2.

Requirements:
1. Directed: Dependencies must flow in one direction (no cycles).
2. Acyclic: A task must not eventually depend on itself.
3. Complete: All task IDs from the input must appear as keys, even if they have no dependencies.
4. Coherent: Dependencies must make semantic and functional sense based on the task descriptions.
5. Fully Connected:
   - Every task must eventually contribute (directly or indirectly) to a final output task.
   - No node may be a dead-end (i.e., have no outgoing edges), except for the final task(s) responsible for presenting or recording the final result.

How to Determine Dependencies:
- Semantic Precedence: If a task logically precedes another (e.g., validation before analysis), the latter should depend on the former.
- Data Requirements: If a task consumes data produced by another, it must depend on it.
- Validation before Use: No task should operate on unvalidated or uncleaned data.
- No Redundant Edges: Only include dependencies that are functionally required.
- Final Contribution: Ensure each task outputs to at least one other task, unless it is a final presentation/summarization/reporting task.

Do Not:
- Generate explanations or reasoning in the output
- Add any task IDs not explicitly listed in the input
- Leave any task disconnected from the main graph
- Create circular dependencies
"""

        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        
        self.agent = Agent(
            model=self.model,
            instructions=(INSTRUCTION),
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
            logging.info(f"Generated connections: {self.generated_graph.tasks}")
            return self.generated_graph
        except Exception as e:
            logging.error(f"Error during the connecting of tasks : {e}")
            return "TaskConnectorOutput()"   
 
     