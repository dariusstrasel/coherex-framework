#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def validate_rpg_structure(repo_root: Path) -> list[str]:
    """
    Validates the RPG structure defined in rpg/index.json against the filesystem.
    Ensures all specified paths and key files exist relative to the repository root.

    Args:
        repo_root (Path): The absolute path to the root of the repository.

    Returns:
        list[str]: A list of error messages. Returns an empty list if validation passes.
    """
    errors: list[str] = []
    rpg_index_path = repo_root / "rpg" / "index.json"

    if not rpg_index_path.exists():
        errors.append(f"RPG index file not found at: {rpg_index_path}")
        return errors

    try:
        with open(rpg_index_path, 'r', encoding='utf-8') as f:
            rpg_data = json.load(f)
    except json.JSONDecodeError:
        errors.append(f"Error decoding JSON from {rpg_index_path}. Please check its syntax.")
        return errors
    except Exception as e:
        errors.append(f"Error reading {rpg_index_path}: {e}")
        return errors

    # Validate primary documentation files
    if "primary_docs" in rpg_data and isinstance(rpg_data["primary_docs"], list):
        for doc_path_str in rpg_data["primary_docs"]:
            doc_path = repo_root / Path(doc_path_str)
            if not doc_path.exists():
                errors.append(f"Primary documentation file '{doc_path_str}' not found at: {doc_path}")
    else:
        errors.append("Missing or malformed 'primary_docs' list in rpg/index.json.")

    # Validate 'structure' sections and their key files
    if "structure" in rpg_data and isinstance(rpg_data["structure"], dict):
        for section_name, section_details in rpg_data["structure"].items():
            if not isinstance(section_details, dict):
                errors.append(f"Section '{section_name}' in rpg/index.json is malformed (not a dictionary).")
                continue

            if "path" in section_details:
                relative_path = Path(section_details["path"])
                absolute_path = repo_root / relative_path

                if not absolute_path.exists():
                    errors.append(f"Path specified for '{section_name}' in RPG ({relative_path}) does not exist on filesystem at: {absolute_path}.")
                elif "key_files" in section_details and isinstance(section_details["key_files"], list):
                    for key_file_relative_str in section_details["key_files"]:
                        key_file_relative = Path(key_file_relative_str)
                        key_file_absolute = absolute_path / key_file_relative
                        if not key_file_absolute.exists():
                            errors.append(f"Key file '{key_file_relative_str}' for section '{section_name}' does not exist at: {key_file_absolute}.")
                elif "key_files" in section_details and not isinstance(section_details["key_files"], list):
                    errors.append(f"Key files for section '{section_name}' must be a list in rpg/index.json.")
            else:
                errors.append(f"Section '{section_name}' in rpg/index.json is missing a 'path' key.")
    else:
        errors.append("Missing or malformed 'structure' dictionary in rpg/index.json.")

    return errors

if __name__ == "__main__":
    current_script_path = Path(__file__).resolve()
    project_root = current_script_path.parent.parent # Assumes scripts/ is at repo root

    validation_errors = validate_rpg_structure(project_root)

    if validation_errors:
        print("RPG validation failed:", file=sys.stderr)
        for error in validation_errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print("RPG structure valid.", file=sys.stdout)
        sys.exit(0)