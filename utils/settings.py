import os 
import dotenv 

dotenv.load_dotenv()

API_KEY = os.environ["API_KEY"]  
MODEL = os.environ["MODEL"]

AGENT_PRODUCER_PROMPT = open('prompts/AGENT_PRODUCER_PROMPT.md','r').read()
TASK_ATOMIZER_PROMPT = open('prompts/TASK_ATOMIZER_PROMPT.md','r').read()
TASK_CONNECTOR_PROMPT = open('prompts/TASK_CONNECTOR_PROMPT.md','r').read()

if __name__ == "__main__":
    print(f"API_KEY: {API_KEY}")
    print(f"MODEL: {MODEL}")
    print(AGENT_PRODUCER_PROMPT)
    