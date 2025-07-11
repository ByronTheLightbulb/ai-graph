from pprint import pprint
import json 

from classes.AgentProducer import AgentProducer
from classes.TaskAtomizer import TaskAtomizer
from classes.TaskConnector import TaskConnector
from utils.visualise import create_mermaid_diagram


GENERAL_TASK ="Find me suspicious entries vehicle fleet routes data  "

TA = TaskAtomizer()
ATOMISED_TASKS = TA.run(GENERAL_TASK)
 

TC = TaskConnector()
DEPENDENCIES = TC.run(initial_task=GENERAL_TASK,tasks=ATOMISED_TASKS)
 

create_mermaid_diagram(task_descriptions=ATOMISED_TASKS,dependencies=DEPENDENCIES)

