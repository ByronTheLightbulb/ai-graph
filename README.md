AI GRAPH
# Principle of atomicity

A task is defined as such if it can not be further subdivided to smaller tasks 

# Atomisation 

Sometimes it is not possible to formulate the solution to a real-world problem using perfectly atomised task , therefore the proccess by which the state of an AI-graph changes as to include agents which perform only atomic tasks , shall be called atomisation of the Graph. 

# Basic entities 

Each agentic entity may or may not contain inside it the graph-like structure defined here.  

## Master Agent : $A_{m}$ 

Initially the user should be able to define a *Master Agent* that  :

1. Holds the information  in its context of the general task at hand
2. Manages all the definitions of the *Atomic* and *Mediator* agents 
3. Is responsible for the creation or deletion of agents 

Every creation , deletion or edit of an *agent* performed by the *Master Agent* shall either further the atomisation of the graph or achieve a better performace with regards to the general task ,as measured by a <u>user-defined metric</u> .  

# Atomic task : $t_{i}$

An atomic task  $t_{i}$  is a task that can be performed by an agent , using the tools contained in the tool pool , adhering to the principle of atomicity

## Atomic Agent : $A_{t_{i}}$

An atomic agent $A_{t_{i}}$ is an agent that performs an atomic task $t_{i}$ using the tools contained in the tool pool . 

### Input of an agent 
$Inp(A_{{t_i}})$ :  Is the set of all the diffrent flows of information that the agent recieceves from tools or other agents 
### Output of an agent 
$Out(A_{{t_i}})$ :  Is the set of all the diffrent flows of information that the agent produces , each directed to a certain tool or agent  

### Codependence 

If for atomic agents $A_{{t_{i}}}$ and $A_{{t_j}}$ , $Inp(A_{t_{j}}) \cap out(A_{t_{i}}) \neq \emptyset$  then they are called codependent

## Mediator Agent : $A_{ij}$

A mediator agent $A_{ij}$ is an agent that manages the relationship between two codependent atomic agents $A_{{t_{i}}}$ and $A_{{t_j}}$  by : 

1. Changing the content of the input / output 
2. Changing the skills and definition of each Agent 

 
## Tool Pool 

A set of api's tools adhering to the MCP protocol 
 

