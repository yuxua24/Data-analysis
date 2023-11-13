import json

# Function to flatten "children" if it has nested lists
def flatten_children(json_data):
    if "children" in json_data:
        # Check if 'children' is a list of lists
        if isinstance(json_data["children"], list) and json_data["children"] and isinstance(json_data["children"][0], list):
            # Flatten the list
            json_data["children"] = [item for sublist in json_data["children"] for item in sublist]
    # Recursively apply to all dictionary elements
    for key, value in json_data.items():
        if isinstance(value, dict):
            flatten_children(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    flatten_children(item)
    return json_data

# Function to read, transform, and save the JSON file
def process_json_file(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    
    # Transform the JSON data
    transformed_json = flatten_children(json_data)
    
    # Write the transformed JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(transformed_json, file, indent=4)

# Example usage:
# Replace 'path_to_json_file.json' with your actual file path
process_json_file('tree_data_8327.json')
