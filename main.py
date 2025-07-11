from classes.AgentProducer import AgentProducer
from pprint import pprint
import json 
from classes.TaskAtomizer import TaskAtomizer
from classes.TaskConnector import TaskConnector
from utils.visualise import create_mermaid_diagram
GENERAL_TASK ="i want proper outputs for "

TA = TaskAtomizer()
 
ATOMISED_TASKS = TA.run(GENERAL_TASK).tasks
 
# for n in range(0,len(ATOMISED_TASKS)):
#     print(f'{n+1}.{ATOMISED_TASKS[n]}')
print(ATOMISED_TASKS)
TC = TaskConnector()
DEPENDENCIES = TC.run(initial_task=GENERAL_TASK,tasks=ATOMISED_TASKS)
 

create_mermaid_diagram(task_descriptions=ATOMISED_TASKS,dependencies=DEPENDENCIES)
# AP = AgentProducer()
# Agents = [AP.run(task,save=True) for task in atomised_tasks]
