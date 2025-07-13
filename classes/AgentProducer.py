import uuid
import json
import logging
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dataclasses import dataclass
from typing import Dict, Any

from utils.JsonToModel import JsonToModel
from utils.settings import SETTINGS
API_KEY =SETTINGS.api_key
MODEL=SETTINGS.model
DEPENDENCY_AGENT_PRODUCER_PROMPT=SETTINGS.dependency_agent_producer_prompt
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class ProducerAgentOutput:
    """
    Represents the structured output of an AI agent that generates a Pydantic BaseModel JSON schema.

    This class defines the expected structure of the agent's response, making it easier to work with
    and validate the output.

    Attributes:
        instructions (str): A string containing clear, actionable instructions for the AI model on how
                            to use the generated output model.
        output_model_json (str): A valid JSON string representing the Pydantic BaseModel schema. This
                                 JSON should be directly parsable into a Pydantic model.
    """
    instructions: str
    output_model_json: str

class AgentProducer:
    """
    A class responsible for producing AI agents with dynamically generated Pydantic models.

    The `AgentProducer` takes a task description, uses an AI model to generate a suitable
    Pydantic model for the task's output, and then creates a new AI agent configured
    with this dynamic model. This allows for flexible and task-specific agent generation.

    Attributes:
        id (uuid.UUID): A unique identifier for the AgentProducer instance.
        provider (GoogleProvider): The AI model provider (e.g., Google).
        model (GoogleModel): The specific AI model being used.
        agent (Agent): The initial AI agent responsible for generating the Pydantic model schema.
    """

    def __init__(self):
        """
        Initializes the AgentProducer, setting up the AI provider, model, and the initial agent.
        """
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)

        self.agent = Agent(
            model=self.model,
            instructions=DEPENDENCY_AGENT_PRODUCER_PROMPT,
            output_type=ProducerAgentOutput
        )

    def run(self, task: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Generates a new AI agent with a dynamically created Pydantic model based on the provided task.

        This method orchestrates the process of generating an agent definition, validating it, and
        then creating the final agent. It includes a retry mechanism to handle potential failures
        in generating a valid JSON schema.

        Args:
            task (str): The task description for which the agent and its output model are to be generated.
            max_retries (int): The maximum number of attempts to generate a valid agent definition.

        Returns:
            Dict[str, Any]: A dictionary containing the newly created agent and its definitions.
                            - "AGENT": The generated AI agent.
                            - "DEFINITIONS": The `ProducerAgentOutput` containing instructions and the JSON schema.

        Raises:
            ValueError: If a valid JSON schema cannot be generated after the maximum number of retries.
            RuntimeError: If the agent definition cannot be generated for other reasons.
        """
        generated_agent_definitions = None
        last_error_message = None

        for attempt in range(max_retries):
            logging.info(f"Attempt {attempt + 1} of {max_retries} to generate agent definition for task: '{task}'")

            prompt_for_agent = task
            if last_error_message:
                feedback = (
                    "The previous attempt failed. Please ensure 'output_model_json' is a perfectly valid "
                    f"and parsable JSON string for a Pydantic BaseModel. Error: {last_error_message}"
                )
                prompt_for_agent = f"{task}\n\n[CRITICAL FEEDBACK]: {feedback}"

            try:
                producer_output_wrapper = self.agent.run_sync(user_prompt=prompt_for_agent)
                generated_agent_definitions = producer_output_wrapper.output

                # Validate the generated JSON
                json.loads(generated_agent_definitions.output_model_json)
                logging.info("Successfully validated generated JSON schema.")
                break  # Exit loop on success

            except json.JSONDecodeError as e:
                logging.error(f"JSONDecodeError on attempt {attempt + 1}: {e}")
                last_error_message = str(e)
            except Exception as e:
                logging.error(f"An unexpected error occurred on attempt {attempt + 1}: {e}")
                last_error_message = str(e)

        if not generated_agent_definitions:
            raise RuntimeError(f"Failed to generate a valid agent definition after {max_retries} attempts.")

        self.generated_agent_definitions = generated_agent_definitions
        logging.info("Successfully generated agent definitions.")
        
        try:
            # Create the final agent with the dynamically generated output model
            generated_agent = Agent(
                model=self.model,
                instructions=self.generated_agent_definitions.instructions,
                output_type=JsonToModel(str(self.generated_agent_definitions.output_model_json))
            )
            logging.info("Successfully created the final agent with dynamic output model.")
        except Exception as e:
            logging.error(
                "Failed to create the final agent. This often means the JSON schema, while valid, "
                f"is not a valid Pydantic BaseModel schema. Error: {e}"
            )
            logging.error(f"Invalid JSON Schema: {self.generated_agent_definitions.output_model_json}")
            raise

        return {"AGENT": generated_agent, "DEFINITIONS": self.generated_agent_definitions}
 
    
 