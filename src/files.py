import os
import json
import yaml
import pandas as pd
from typing import List, Dict, Any, Union

def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to open {path}: {e}")
        return None

def write_file(path: str, content: str, append: bool = False) -> None:
    """Writes content to a file."""
    mode = 'a' if append else 'w'
    try:
        with open(path, mode) as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to open {path}: {e}")

def read_yaml(path: str) -> Dict[str, Any]:
    """Reads a YAML file."""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"Failed to read file: {path}") from e

def read_json(path: str) -> Any:
    """Reads a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to read file: {path}") from e

def write_json(path: str, data: Any, indent: int = 4) -> None:
    """Writes data to a JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=indent)
    except Exception as e:
        raise Exception(f"Failed to write to file: {path}") from e

def readdir(directory: str) -> List[str]:
    """Lists files in a directory."""
    directory = directory or "."
    try:
        # User requested removal of redundant checks, but for listdir 
        # filtering . and .. is redundant as os.listdir doesn't return them.
        return os.listdir(directory)
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
        return []

def read_delimited(path: str, delimiter: str = '\t', header: bool = True) -> List[Dict[str, Any]]:
    """Reads a delimited file into a list of dictionaries."""
    try:
        df = pd.read_csv(path, sep=delimiter, header=0 if header else None)
        # Fill NaN with empty string to match Lua behavior
        df = df.fillna("")
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading delimited file {path}: {e}")
        return None

def write_delimited(path: str, data: Union[List[Dict], pd.DataFrame], delimiter: str = '\t', header: bool = True) -> None:
    """Writes data to a delimited file."""
    try:
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        df.to_csv(path, sep=delimiter, index=False, header=header)
    except Exception as e:
        print(f"Error writing delimited file {path}: {e}")
