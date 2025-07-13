# AI-Graph

AI-Graph is a powerful tool designed to break down high-level tasks into atomic sub-tasks, orchestrate their execution using specialized AI agents, and visualize the resulting execution plan. It provides a structured approach to complex problem-solving by leveraging AI capabilities to generate efficient and manageable workflows.

## Features

-   **Task Atomization**: Automatically decomposes complex, high-level tasks into smaller, atomic, and manageable sub-tasks.
-   **AI Agent Orchestration**: Generates a detailed execution plan, assigning specific AI agents to handle each atomic task.
-   **Multiple Output Formats**: Saves the generated execution plan in various formats, including JSON and Pickle, for easy integration and further processing.
-   **Visual Task Dependencies**: Creates an interactive Mermaid diagram (HTML) that visually represents the dependencies between atomic tasks, providing a clear overview of the workflow.

## Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/ByronTheLightbulb/ai-graph.git
    cd ai-graph
    ```

2.  **Install Dependencies**:

    This project requires Python 3.x. Install the necessary dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run AI-Graph, execute the `main.py` script with your desired task and output options.

```bash
python main.py --task "Your high-level task description here" \
               --output-json "output.json" \
               --output-pickle "output.pkl" \
               --output-diagram "mermaid_diagram.html"
```

**Example**:

```bash
python main.py --task "Find me suspicious transaction in my company's transaction history for the previous month" \
               --output-json "transaction_analysis.json" \
               --output-pickle "transaction_analysis.pkl" \
               --output-diagram "transaction_flow.html"
```

### Command-line Arguments:

-   `--task` (str, required): The high-level task to be accomplished. Enclose in quotes if it contains spaces.
-   `--output-json` (str, optional): The path to save the generated execution plan in JSON format. Defaults to `output.json`.
-   `--output-pickle` (str, optional): The path to save the generated execution plan in Pickle format. Defaults to `output.pkl`.
-   `--output-diagram` (str, optional): The path to save the Mermaid diagram HTML file. Defaults to `mermaid_diagram.html`.

## Project Structure

-   `main.py`: The main entry point of the application, orchestrating the task processing and output generation.
-   `classes/`: Contains core classes like `AtomicGenerator`, `AgentProducer`, `TaskAtomizer`, and `TaskConnector` that define the AI agent logic and task processing.
-   `prompts/`: Stores various prompt templates used by the AI agents for task understanding and generation.
-   `utils/`: Provides utility functions, including JSON serialization (`JsonToModel`), task sequencing (`sequencer`), settings management (`settings`), and visualization tools (`visualise`).

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[Specify your license here, e.g., MIT License, Apache 2.0 License, etc.]
