import uuid
import logging
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from typing import List, Tuple, Dict

from utils.settings import SETTINGS
API_KEY =SETTINGS.api_key
MODEL=SETTINGS.model
TASK_CONNECTOR_PROMPT=SETTINGS.task_connector_prompt
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TaskConnectorOutput(BaseModel):
    """
    Represents the output of the TaskConnector, defining the dependencies between tasks.

    Attributes:
        tasks (List[Tuple[str, List[int]]]): A list of tuples where each tuple contains a task ID (str)
                                             and a list of IDs (int) of tasks it depends on.
    """
    tasks: List[Tuple[str, List[int]]]

class TaskConnector:
    """
    A class for determining the dependencies between a set of atomized tasks.

    This class uses an AI agent to analyze a list of tasks and identify the relationships
    between them, representing these relationships as a directed graph.

    Attributes:
        id (uuid.UUID): A unique identifier for the TaskConnector instance.
        provider (GoogleProvider): The AI model provider (e.g., Google).
        model (GoogleModel): The specific AI model being used.
        agent (Agent): The AI agent configured to perform task connection.
    """

    def __init__(self):
        """
        Initializes the TaskConnector, setting up the AI provider, model, and agent.
        """
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        
        self.agent = Agent(
            model=self.model,
            instructions=TASK_CONNECTOR_PROMPT,
            output_type=TaskConnectorOutput
        )
        
    def run(self, initial_task: str, tasks: List[str]) -> List[Tuple[str, List[int]]]:
        """
        Determines the dependencies between a list of tasks.

        Args:
            initial_task (str): The original high-level task description.
            tasks (List[str]): A list of atomized sub-tasks.

        Returns:
            List[Tuple[str, List[int]]]: A list of tuples representing the dependency graph.
                                         Returns an empty list if an error occurs.
        """
        logging.info("Attempting to create connections for the given tasks.")
        
        # Construct the prompt for the agent
        user_prompt = f"General Task: {initial_task}\n\nIndividual Tasks:\n"
        for i, task in enumerate(tasks):
            user_prompt += f"{i}. {task}\n"
        
        try:
            response = self.agent.run_sync(user_prompt=user_prompt)
            if response and response.output:
                logging.info("Successfully generated task connections.")
                return response.output.tasks
            else:
                logging.warning("Task connection resulted in an empty or invalid response.")
                return []
        except Exception as e:
            logging.error(f"An unexpected error occurred during task connection: {e}")
            return []   
 
     