"""
This script processes JSON data and matches it with directories containing attack technique logs.
"""

import pandas as pd
import os
from typing import List, Dict


def read_input_data(json_path: str) -> pd.DataFrame:
    """Read and initialize the DataFrame with required columns."""
    df = pd.read_json(json_path)
    df["tools"] = "-"
    df["log_name"] = "-"
    df["log_details"] = df.apply(lambda x: [], axis=1)
    return df


def read_log_file(log_path: str) -> str:
    """Read and return the contents of a log file."""
    try:
        with open(log_path, "r", encoding="utf8") as log_file:
            return log_file.read()
    except Exception as e:
        print(f"Error reading log file {log_path}: {e}")
        return ""


def update_dataframe(
    df: pd.DataFrame,
    technique_id: str,
    log_name: str,
    log_content: str,
    tool_name: str = None,
) -> None:
    """Update the DataFrame with log file information.

    Args:
        df (pd.DataFrame): The DataFrame to update.
        technique_id (str): Identifier for the technique being processed.
        log_name (str): Name of the log file.
        log_content (str): Contents of the log file.
        tool_name (str, optional): The name of tools that used to generate the logs.  Defaults to None.
    """
    existing_log = df.loc[df["Technique ID"] == technique_id, "log_name"].values[0]

    # Update log name
    if existing_log == "-":
        df.loc[df["Technique ID"] == technique_id, "log_name"] = log_name
    else:
        df.loc[df["Technique ID"] == technique_id, "log_name"] += f", {log_name}"

    # Update tool name if provided
    if tool_name:
        df.loc[df["Technique ID"] == technique_id, "tools"] = tool_name

    # Update log details
    idx = df.index[df["Technique ID"] == technique_id][0]
    df.at[idx, "log_details"].append(log_content)


def process_technique_directory(
    df: pd.DataFrame, tech_path: str, technique_id: str
) -> None:
    """
    Process a technique directory and its subdirectories for log files.
    The function searches through a technique directory and its subdirectories for .log files,
    reads their contents, and updates a DataFrame with the extracted information.
    Args:
      df (pd.DataFrame): The DataFrame to update with log file information.
      tech_path (str): Path to the technique directory to process.
      technique_id (str): Identifier for the technique being processed.
    Returns:
      None: The function modifies the DataFrame in-place.
    Example:
      >>> df = pd.DataFrame()
      >>> process_technique_directory(df, '/path/to/technique', 'T001')
    """
    for item in os.listdir(tech_path):
        item_path = os.path.join(tech_path, item)

        if item.endswith(".log"):
            # Process log file in main directory
            log_content = read_log_file(item_path)
            update_dataframe(df, technique_id, item, log_content)

        elif os.path.isdir(item_path):
            # Process log files in subdirectory
            for log_file in os.listdir(item_path):
                if log_file.endswith(".log"):
                    log_path = os.path.join(item_path, log_file)
                    log_content = read_log_file(log_path)
                    update_dataframe(df, technique_id, log_file, log_content, item)


def main():
    # File paths
    json_path = "../Reconnaissance/Reconnaissance.json"
    attack_path = "../attack_data_/attack_data/datasets/attack_techniques/"

    # Read and initialize data
    df = read_input_data(json_path)

    # Process each technique
    for technique in df.to_dict(orient="records"):
        technique_id = technique["Technique ID"]

        for directory in os.listdir(attack_path):
            if technique_id == directory.upper():
                tech_path = os.path.join(attack_path, directory)
                process_technique_directory(df, tech_path, technique_id)

    # Save results
    df.to_csv("../data/data.csv", index=False)
    df.to_json("../data/data.json", orient="records")


if __name__ == "__main__":
    main()
  