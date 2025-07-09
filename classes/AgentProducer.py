import uuid
import json
import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from utils.JsonToModel import JsonToModel # Assuming this is correctly implemented
from utils.settings import API_KEY, MODEL
from dataclasses import dataclass
from typing import Dict, Any
from pydantic import BaseModel
import logging

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class ProducerAgentOutput:
    """
    Represents the output of an AI agent that generates a Pydantic BaseModel JSON schema.

    Attributes:
        instructions (str): A string containing instructions for the AI model on how to use the generated output model.
        output_model_json (str): A valid JSON string representing the Pydantic BaseModel schema.
    """
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
                "You are an expert AI agent that designs Pydantic BaseModel schemas. "
                "I will give you a user task. Your job is to create a Pydantic BaseModel "
                "as a **valid JSON schema** that describes the output of an AI agent "
                "that performs that task. "
                "Ensure the `output_model_json` field is a perfectly parsable JSON string. "
                "It must represent a valid Pydantic model definition (e.g., with 'title', 'properties', 'type')."
            ),
            output_type=ProducerAgentOutput
        )

    def run(self, task, save=False, save_folder='temp', max_retries=3):
        generated_agent_definitions = None # Initialize to None
        attempt = 0
        original_prompt = task
        last_error_message = None # Store the last error message here

        while attempt < max_retries:
            logging.info(f"Attempt {attempt + 1} to generate agent definition.")

            # Construct the prompt for the current attempt
            prompt_for_agent = original_prompt
            if last_error_message: # If there was a previous error, add feedback
                feedback = f"The last JSON output was invalid. Please ensure 'output_model_json' is a perfectly valid and parsable JSON string for a Pydantic BaseModel. Specific error: {last_error_message}"
                prompt_for_agent = f"{original_prompt}\n\n[CRITICAL FEEDBACK]: {feedback}"

            try:
                producer_output_wrapper = self.agent.run_sync(user_prompt=prompt_for_agent)
                generated_agent_definitions = producer_output_wrapper.output

                # Attempt to parse the generated JSON
                parsed_model_json = json.loads(generated_agent_definitions.output_model_json)
                logging.info("Successfully parsed generated output_model_json.")

                # If parsing is successful, break the loop
                break

            except json.JSONDecodeError as e:
                logging.error(f"JSONDecodeError on attempt {attempt + 1}: {e}")
                last_error_message = str(e) # Store the error message
                attempt += 1
                if attempt >= max_retries:
                    logging.error("Max retries reached. Failed to get valid JSON from producer agent.")
                    raise ValueError(f"Failed to get valid JSON from producer agent after {max_retries} attempts. Last error: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred on attempt {attempt + 1}: {e}")
                last_error_message = str(e) # Store the error message
                attempt += 1
                if attempt >= max_retries:
                    logging.error("Max retries reached due to unexpected error.")
                    raise

        if not generated_agent_definitions:
            raise RuntimeError("Agent definition could not be generated after multiple attempts.")

        self.generated_agent_definitions = generated_agent_definitions
        logging.info("Producer Agent Output Instructions:\n%s", self.generated_agent_definitions.instructions)
        logging.info("Producer Agent Output Model JSON:\n%s", self.generated_agent_definitions.output_model_json)

        # Proceed to create the new agent with the validated output
        try:
            self.generated_agent = Agent(
                model=self.model,
                instructions=self.generated_agent_definitions.instructions,
                output_type=JsonToModel(str(self.generated_agent_definitions.output_model_json))
            )
        except Exception as e:
            logging.error(f"Failed to create generated agent with dynamic output_type. "
                          f"This usually means the JSON schema, while valid JSON, "
                          f"is not a valid Pydantic BaseModel schema: {e}")
            logging.error(f"Invalid JSON Schema was: {self.generated_agent_definitions.output_model_json}")
            raise

        if save:
            save_obj = {
                "instructions": self.generated_agent_definitions.instructions,
                "output_model_json": self.generated_agent_definitions.output_model_json
            }
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, f"{uuid.uuid4()}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(save_obj, f, indent=4)
            logging.info(f"Agent definition saved to {file_path}")

        return self.generated_agent

    def save(self):
        # This method seems to be a placeholder
        pass