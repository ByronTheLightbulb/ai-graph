from classes.AgentProducer import AgentProducer
from pprint import pprint
import json 
from classes.TaskAtomizer import TaskAtomizer
TA = TaskAtomizer()
atomised_tasks = TA.run("I want to look at my financial transactions for possible improvements for my business").tasks
print(atomised_tasks)
AP = AgentProducer()
Agents = [AP.run(task,save=True) for task in atomised_tasks]
