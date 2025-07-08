import uuid 
from pydantic import BaseModel
from Agent import Agent 
from pprint import pprint
 
class dimension(BaseModel) :
    id:uuid.UUID
    label: str 

class Node(BaseModel) :
    id : uuid.UUID 
    data: str 

class connection(BaseModel):
    id: uuid.UUID
    id_from : uuid.UUID 
    id_to : uuid.UUID
    dimension: uuid.UUID
    
class Graph(BaseModel):
    nodes:list[Node]
    connections:list[connection]
    dimensions:list[dimension]

# class GraphContainer:
    
#     def __init__(self,json_definition) :
#         self.dict_definition =self.parse_json(json_definition)

#     def parse_json(self ,json_definition):
        
#         pass 
    
    
if __name__=="__main__":
    print(Node(id=uuid.uuid4(),data="Agent()"))
    nodes=[Node(id=uuid.uuid4(),data="Agent()"),Node(id=uuid.uuid4(),data="Agent()")]
    dimensions=[dimension(id=uuid.uuid4(),label="test")]
    connections=[connection(id=uuid.uuid4(),id_from=nodes[0].id,id_to=nodes[1].id,dimension=dimensions[0].id)]
    g = Graph(
                nodes= nodes,
                dimensions= dimensions,
                connections= connections)
    pprint(g.model_dump_json(),indent=3)