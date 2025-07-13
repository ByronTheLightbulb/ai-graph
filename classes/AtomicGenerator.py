from pprint import pprint
import json
import pickle

from classes.AgentProducer import AgentProducer
from classes.TaskAtomizer import TaskAtomizer
from classes.TaskConnector import TaskConnector
from utils.sequencer import TaskSequencer

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



GENERAL_TASK = "Find me suspicious transaction in my company's transaction history for the previous month"

class AtomicGenerator:
    def __init__(self):
        self.TA = TaskAtomizer()
        self.TC = TaskConnector() 
        self.AP = AgentProducer()
    def generate(self,prompt):
         
        self.ATOMISED_TASKS = self.TA.run(prompt) 
        logging.info(f"ATOMISED_TASKS: '{self.ATOMISED_TASKS}'")
        self.DEPENDENCIES = self.TC.run(initial_task=prompt, tasks=self.ATOMISED_TASKS)
        logging.info(f"DEPENDENCIES: '{self.DEPENDENCIES}'")
        t= TaskSequencer(self.DEPENDENCIES)
        self.SEQUENCE = t.generate_sequence()
        logging.info(f"SEQUENCE: '{self.SEQUENCE}'")
        self.DATA = {
                "ATOMISED_TASKS": {}, 
                "SEQUENCE": self.SEQUENCE
            }
        for i in range(len(self.ATOMISED_TASKS)):
            deps = []
            for k, v in self.DEPENDENCIES:
                if k == str(i):
                    deps = [str(x) for x in v]
                    break
            self.DATA['ATOMISED_TASKS'][str(i)] = {
                "description": self.ATOMISED_TASKS[i],
                "instructions": None,
                "output_model_json": None,
                "agent": None,
                "dependencies": deps
            }
            
        for id in self.DATA['SEQUENCE']:
            task = self.DATA['ATOMISED_TASKS'][str(id)]
             
            description = task["description"]
            dependencies = [self.DATA['ATOMISED_TASKS'][dep_id] for dep_id in task["dependencies"]]
            
            prompt = f"{description}\n\n[PREVIOUS AGENTS]:"
            for idx, agent in enumerate(dependencies, start=1):
                prompt += f"""
                \nAGENT {idx}:
                \nINSTRUCTIONS: {agent['instructions']}
                \nOUTPUT_MODEL_JSON: {agent['output_model_json']}"""
                
            
            result = self.AP.run(task=prompt)
            logging.info(f'RESULT: {result}')
            self.DATA['ATOMISED_TASKS'][str(id)]['agent'] = result['AGENT']
            self.DATA['ATOMISED_TASKS'][str(id)]['instructions'] = result['DEFINITIONS'].instructions
            self.DATA['ATOMISED_TASKS'][str(id)]['output_model_json'] = result['DEFINITIONS'].output_model_json
        return self.DATA
    
 
    
# TA = TaskAtomizer()
# ATOMISED_TASKS = TA.run(GENERAL_TASK)

# TC = TaskConnector()
# DEPENDENCIES = TC.run(initial_task=GENERAL_TASK, tasks=ATOMISED_TASKS)

# SQ = sequencer(DEPENDENCIES)
# SEQUENCE = SQ.generate_sequence()
 
# DATA = {
#     "ATOMISED_TASKS": {}, 
#     "SEQUENCE": SEQUENCE
# }
 
# for i in range(len(ATOMISED_TASKS)):
#     deps = []
#     for k, v in DEPENDENCIES:
#         if k == str(i):
#             deps = [str(x) for x in v]
#             break
#     DATA['ATOMISED_TASKS'][str(i)] = {
#         "description": ATOMISED_TASKS[i],
#         "instructions": None,
#         "output_model_json": None,
#         "agent": None,
#         "dependencies": deps
#     }

 
 
# AP = AgentProducer()
# for id in DATA['SEQUENCE']:
#     task = DATA['ATOMISED_TASKS'][str(id)]
#     description = task["description"]
#     dependencies = [DATA['ATOMISED_TASKS'][dep_id] for dep_id in task["dependencies"]]
#     prompt = constructPrompt(task=task, dependencies=dependencies)
#     pprint(prompt)
#     result = AP.run(task=prompt)

#     #DATA['ATOMISED_TASKS'][str(id)]['agent'] = result['AGENT']
#     DATA['ATOMISED_TASKS'][str(id)]['instructions'] = result['DEFINITIONS'].instructions
#     DATA['ATOMISED_TASKS'][str(id)]['output_model_json'] = result['DEFINITIONS'].output_model_json

# Save to JSON
# with open("output.json", "w", encoding="utf-8") as json_file:
#     json.dump(DATA, json_file, indent=4, ensure_ascii=False)

# # Save to Pickle
# with open("output.pkl", "wb") as pickle_file:
#     pickle.dump(DATA, pickle_file)

# print("Data saved to 'output.json' and 'output.pkl'")
