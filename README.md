## TaskAtomizer

`TaskAtomizer` is a lightweight wrapper around a `pydantic_ai.Agent` that transforms a high-level user instruction into a list of atomic subtasks using a Google LLM backend.

---

### Description

It takes a single input string (task description) and returns a structured output in the form of a list of subtasks (`list[str]`). It's designed to be integrated into larger agent-based workflows or orchestration pipelines.

---

### Code Overview

```python
@dataclass
class TaskAtomizerOutput:
    tasks: list[str]

class TaskAtomizer:
    def __init__(self):
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        self.agent = Agent(
            model=self.model,
            instructions=TASK_ATOMIZER_PROMPT,
            output_type=TaskAtomizerOutput
        )

    def run(self, task: str) -> TaskAtomizerOutput:
        return self.agent.run_sync(user_prompt=task).output

## TaskConnector

`TaskConnector` is an agent wrapper that infers task dependencies from a list of subtasks derived from a high-level task description. It uses a Google LLM via `pydantic_ai` to return a structured dependency graph.

---

### Description

Given:
- A general task description (e.g., _"Process raw telemetry data"_), and
- A list of subtasks (e.g., ["Validate records", "Filter nulls", "Order data by timestamp"]),

the `TaskConnector` produces a list of `(task_id: str, dependency_ids: List[int])` pairs, which describe which tasks depend on which others.

---

### Code Overview

```python
class TaskConnectorOutput(BaseModel):
    tasks: List[Tuple[str, List[int]]]

    def to_dict(self) -> Dict[str, List[int]]:
        return dict(self.tasks)

class TaskConnector:
    def __init__(self):
        self.id = uuid.uuid4()
        self.provider = GoogleProvider(api_key=API_KEY)
        self.model = GoogleModel(MODEL, provider=self.provider)
        self.agent = Agent(
            model=self.model,
            instructions=TASK_CONNECTOR_PROMPT,
            output_type=TaskConnectorOutput
        )

    def run(self, initial_task: str, tasks: List[str]) -> List[Tuple[str, List[int]]]:
        user_prompt = f"General Task :{initial_task}\nIndividual Tasks:\n"
        for i, task in enumerate(tasks):
            user_prompt += f"{i}.{task}\n"

        return self.agent.run_sync(user_prompt=user_prompt).output.tasks

