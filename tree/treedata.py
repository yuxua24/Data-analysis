import pandas as pd
import json

# Load data
nodes_df = pd.read_csv('Nodes.csv')
links_df = pd.read_csv('Links.csv')

# Filter to include only 'ownership' type relationships
links_df = links_df[links_df['type'] == 'ownership']

# Define a function to build a tree based on a node id
def build_tree(node_id, direction, depth, visited):
    if depth == 0 or node_id in visited:
        return None

    visited.add(node_id)

    if direction == 'up':
        child_nodes = links_df[links_df['target_id'] == node_id]
        direction_col = 'source_id'
    else:
        child_nodes = links_df[links_df['source_id'] == node_id]
        direction_col = 'target_id'

    children = []
    for _, row in child_nodes.iterrows():
        child_id = row[direction_col]
        node_info = nodes_df[nodes_df['id'] == child_id].iloc[0]
        child_tree = build_tree(child_id, direction, depth-1, visited)
        children.append({
            'name': node_info['id'],  # Changed from 'type' to 'id' as per the request
            'id': node_info['id'],
            'country': node_info['country'],
            'children': [child_tree] if child_tree else []
        })

    return children

# Specify node ids
node_ids = ['Mar de la Vida OJSC', '979893388', 'Oceanfront Oasis Inc Carriers', '8327']

# Build trees and save as separate JSON files
for node_id in node_ids:
    visited_up = set()
    visited_down = set()
    up_tree = build_tree(node_id, 'up', 5, visited_up)
    down_tree = build_tree(node_id, 'down', 5, visited_down)
    tree = {
        'name': node_id,  # Changed 'Root' to the node_id itself
        'id': node_id,
        'children': up_tree + down_tree if up_tree and down_tree else (up_tree or down_tree)
    }

    # Convert to JSON format
    tree_json = json.dumps(tree, indent=4)

    # Save the JSON data to a local file
    output_filename = f'tree_data_{node_id}.json'
    with open(output_filename, 'w') as outfile:
        outfile.write(tree_json)

    print(f"Data has been saved to {output_filename}")
