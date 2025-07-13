import os
import logging
import dotenv
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Settings:
    """
    A data class to hold the application settings.

    Attributes:
        api_key (str): The API key for the AI model provider.
        model (str): The name of the AI model to be used.
        agent_producer_prompt (str): The prompt for the AgentProducer.
        task_atomizer_prompt (str): The prompt for the TaskAtomizer.
        task_atomizer_prompt_v2 (str): The version 2 prompt for the TaskAtomizer.
        task_connector_prompt (str): The prompt for the TaskConnector.
        dependency_agent_producer_prompt (str): The prompt for the DependencyAgentProducer.
    """
    api_key: str
    model: str
    agent_producer_prompt: str
    task_atomizer_prompt: str
    task_atomizer_prompt_v2: str
    task_connector_prompt: str
    dependency_agent_producer_prompt: str

def load_settings() -> Settings:
    """
    Loads the application settings from environment variables and prompt files.

    This function loads the .env file, retrieves the API key and model name from environment
    variables, and reads the content of the various prompt files. It then returns a
    Settings object containing all the loaded configuration.

    Returns:
        Settings: A data class containing the loaded settings.

    Raises:
        ValueError: If any of the required environment variables or prompt files are not found.
    """
    logging.info("Loading application settings.")
    
    # Load environment variables from .env file
    dotenv.load_dotenv()

    # Load individual settings
    try:
        api_key = os.environ["API_KEY"]
        model = os.environ["MODEL"]
        
        prompts = {
            "agent_producer_prompt": 'prompts/AGENT_PRODUCER_PROMPT.md',
            "task_atomizer_prompt": 'prompts/TASK_ATOMIZER_PROMPT.md',
            "task_atomizer_prompt_v2": 'prompts/TASK_ATOMIZER_PROMPT_v2.md',
            "task_connector_prompt": 'prompts/TASK_CONNECTOR_PROMPT.md',
            "dependency_agent_producer_prompt": 'prompts/DEPENDENCY_AGENT_PRODUCER_PROMPT.md'
        }

        loaded_prompts = {}
        for name, path in prompts.items():
            with open(path, 'r', encoding='utf8') as f:
                loaded_prompts[name] = f.read()

    except KeyError as e:
        logging.error(f"Environment variable not set: {e}")
        raise ValueError(f"Please set the {e} environment variable.") from e
    except FileNotFoundError as e:
        logging.error(f"Prompt file not found: {e}")
        raise ValueError(f"Please make sure the prompt file exists: {e.filename}") from e

    settings = Settings(
        api_key=api_key,
        model=model,
        **loaded_prompts
    )

    logging.info("Successfully loaded all settings.")
    return settings

# Load settings on module import
SETTINGS = load_settings()

if __name__ == "__main__":
    print("Application Settings:")
    print(f"  API Key: {SETTINGS.api_key}")
    print(f"  Model: {SETTINGS.model}")
    print(f"  Task Atomizer V2 Prompt: \n{SETTINGS.task_atomizer_prompt_v2[:200]}...")
    