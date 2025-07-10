from classes.AgentProducer import AgentProducer
from pprint import pprint
import json 
from classes.TaskAtomizer import TaskAtomizer

TA = TaskAtomizer()
for i in range(10):
    print(f"TRY {i}: ")
    atomised_tasks = TA.run("manage my tinder account for maximum matches").tasks
    for n in range(0,len(atomised_tasks)):
        print(f'{n+1}.{atomised_tasks[n]}')
    
# AP = AgentProducer()
# Agents = [AP.run(task,save=True) for task in atomised_tasks]
