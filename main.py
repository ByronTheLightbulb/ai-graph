import argparse
import json
import pickle
import logging
from pprint import pprint
from pydantic import BaseModel
import copy

from classes.AtomicGenerator import AtomicGenerator
from utils.visualise import generate_mermaid_diagram

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(task: str, output_json: str, output_pickle: str, output_diagram: str):
    """
    The main function for the AI-Graph application.

    This function orchestrates the entire process of taking a high-level task, generating a
    plan of execution with specialized AI agents, and saving the output to various formats.

    Args:
        task (str): The high-level task to be accomplished.
        output_json (str): The path to the output JSON file.
        output_pickle (str): The path to the output pickle file.
        output_diagram (str): The path to the output Mermaid diagram HTML file.
    """
    logging.info(f"Starting the AI-Graph process for task: '{task}'")

    # Initialize the AtomicGenerator
    atomic_generator = AtomicGenerator()

    # Generate the execution plan
    try:
        data = atomic_generator.generate(task)
        logging.info("Successfully generated the execution plan.")
    except Exception as e:
        logging.error(f"Failed to generate the execution plan: {e}")
        return

    # Generate the Mermaid diagram
    try:
        task_descriptions = [t["description"] for t in data["ATOMISED_TASKS"].values()]
        dependencies = [(k, v["dependencies"]) for k, v in data["ATOMISED_TASKS"].items()]
        generate_mermaid_diagram(task_descriptions, dependencies, output_diagram)
    except Exception as e:
        logging.error(f"Failed to generate the Mermaid diagram: {e}")

    # Save the output to JSON and pickle files
    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=lambda o: o.dict() if isinstance(o, BaseModel) else str(o))
        logging.info(f"Successfully saved the output to '{output_json}'.")

        # with open(output_pickle, "wb") as f:
        #     pickle.dump(data, f)
        # logging.info(f"Successfully saved the output to '{output_pickle}'.")
    except IOError as e:
        logging.error(f"Failed to save the output files: {e}")

    logging.info("AI-Graph process completed successfully.")
    pprint(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Graph: A tool for generating and visualizing AI agent execution plans.")
    parser.add_argument("--task", type=str, default="Find me suspicious transaction in my company's transaction history for the previous month", help="The high-level task to be accomplished.")
    parser.add_argument("--output-json", type=str, default="output.json", help="The path to the output JSON file.")
    parser.add_argument("--output-pickle", type=str, default="output.pkl", help="The path to the output pickle file.")
    parser.add_argument("--output-diagram", type=str, default="mermaid_diagram.html", help="The path to the output Mermaid diagram HTML file.")
    args = parser.parse_args()

    main(args.task, args.output_json, args.output_pickle, args.output_diagram)
