from classes.AgentProducer import AgentProducer
from utils.JsonToModel import JsonToModel
from pprint import pprint
import json 

task = "you are an agent that recieves a topic from the user and analysis it from all angles "
generated_agent = AgentProducer().run(task)


print(generated_agent.run_sync("tell me about gothic literature").output.model_dump_json())