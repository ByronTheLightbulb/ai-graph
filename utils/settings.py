import os 
import dotenv 

dotenv.load_dotenv()

API_KEY = os.environ["API_KEY"]  
MODEL = os.environ["MODEL"]


if __name__ == "__main__":
    print(f"API_KEY: {API_KEY}")
    print(f"MODEL: {MODEL}")