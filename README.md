# 🧠 Agent Decomposition Framework

This project is part of a modular agentic system designed to dynamically generate executable agent graphs from a single high-level user prompt. Its core functionality centers on automating the decomposition, structuring, and coordination of tasks via large language models (LLMs), allowing agents to be instantiated and orchestrated automatically based on a derived task graph.

---

## 🧩 Components

### TaskAtomizer

`TaskAtomizer` is responsible for decomposing a high-level instruction into a linear list of atomic subtasks. It uses a Google-backed LLM via the `pydantic_ai` agent interface.

- **Input**: A single user instruction (string)
- **Output**: A structured list of subtasks (`list[str]`)
- **Use Case**: Preparing fine-grained steps for agent assignment or task routing

This forms the first stage of the pipeline — transforming an abstract goal into discrete executable actions.

---

### TaskConnector

`TaskConnector` infers logical and execution dependencies between subtasks, producing a task dependency graph.

- **Input**:
  - The general task description (string)
  - A list of atomic subtasks (`list[str]`)
- **Output**: A list of `(task_id: str, dependency_ids: List[int])` tuples representing a Directed Acyclic Graph (DAG)
- **Use Case**: Planning execution order, scheduling, agent graph construction

This enables construction of dynamic DAGs, which can be used to trigger agents conditionally based on completion of their prerequisite tasks.

---

## 🔁 Example Pipeline

1. **Decompose** the high-level prompt into atomic subtasks:
   - e.g., "Analyze telemetry data" → `["Load raw data", "Validate timestamps", "Aggregate by vehicle"]`

2. **Connect** those subtasks into a dependency structure:
   - Output: `[("0", []), ("1", [0]), ("2", [1])]`

3. **Generate** a task DAG and instantiate agents for each atomic node based on the graph topology.

---

## ⚙️ Configuration

Define the following settings in `utils/settings.py` or as environment variables:

```python
API_KEY = "your-google-api-key"
MODEL = "models/gemini-1.5-pro"
TASK_ATOMIZER_PROMPT = "...system prompt for task decomposition..."
TASK_CONNECTOR_PROMPT = "...system prompt for dependency inference..."
