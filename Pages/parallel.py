import pandas as pd
import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Graph, Parallel
from streamlit.components.v1 import html

def main():
    st.set_page_config(layout="wide")
    
    # Streamlit application layout
    st.title("Community Visualization")

    # Controls for community selection and chart type, placed at the top
    community_number = st.selectbox("Select a Community Number", range(16))
    chart_type = st.radio("Select Chart Type", ("Graph", "Parallel"))

    # Load data
    node_data = pd.read_csv("Dataset/MC1/Parallel coordinates/community_node_stats.csv")
    edge_data = pd.read_csv("Dataset/MC1/Links.csv")
    parallel_data = pd.read_csv("Dataset/MC1/Parallel coordinates/community_stats.csv")

    # Suspected nodes list
    suspected_nodes = ["Mar de la Vida OJSC", "979893388",
                    "Oceanfront Oasis Inc Carriers", "8327"]  

    # Filter nodes and edges based on the selected community
    filtered_nodes = node_data[node_data["Community"] == community_number]
    filtered_edges = edge_data[edge_data["source"].isin(filtered_nodes["id"]) & edge_data["target"].isin(filtered_nodes["id"])]
    filtered_parallel = parallel_data[parallel_data.iloc[:, 0] == community_number]

    # Depending on the chart type, display the respective chart
    if chart_type == "Graph":
        display_graph(filtered_nodes, filtered_edges)
    elif chart_type == "Parallel":
        display_parallel(filtered_parallel, suspected_nodes)

def display_graph(filtered_nodes, filtered_edges):
    # Define categories and their respective colors
    categories_list = [
        "person", "political_organization", "organization", "event", "company", 
        "location", "vessel", "movement", "Uncategorized"
    ]
    colors = ["#df493f", "#f9d580", "#e4a2b8", "#54beaa", "#fcf1f0", "#b0d992", "#99b9e9", "#af8fd0", "#eca680"]
    categories = [{"name": category, "itemStyle": {"color": color}} for category, color in zip(categories_list, colors)]

    # Create a mapping from type to category index
    type_to_category = {type_: index for index, type_ in enumerate(categories_list)}

    # Prepare graph data
    nodes = []
    for _, node in filtered_nodes.iterrows():
        category_index = type_to_category.get(node["type"], len(categories_list) - 1)
        node_color = categories[category_index]["itemStyle"]["color"]
        nodes.append({
            "name": str(node["id"]),
            "symbolSize": 10,
            "category": category_index,
            "itemStyle": {"color": node_color},
            "label": {"show": True, "color": "black"}  # Set label color to black
        })

    links = [{"source": str(source), "target": str(target)} for source, target in zip(filtered_edges["source"], filtered_edges["target"])]

    # Create and display a graph
    g = Graph(init_opts=opts.InitOpts(width="100%", height="600px"))
    g.add("", nodes, links, repulsion=5000, categories=categories)
    g.set_global_opts(title_opts=opts.TitleOpts(title="Community Graph"))
    st_pyecharts(g)




def display_parallel(filtered_parallel, suspected_nodes):
    # Convert suspected_nodes to a set for faster lookup
    suspected_nodes_set = set(suspected_nodes)
    
    # Prepare parallel data
    schema = [opts.ParallelAxisOpts(dim=i, name=col) for i, col in enumerate(filtered_parallel.columns[4:])]
    ids = filtered_parallel["id"].tolist()  # Extract ids for performance
    data = []
    
    for i, row in enumerate(filtered_parallel.itertuples()):
        is_suspected = ids[i] in suspected_nodes_set
        color = 'red' if is_suspected else 'gray'
        line_width = 3 if is_suspected else 1
        data.append({
            "value": list(row)[5:],  # Skip index and first 4 columns
            "lineStyle": {"color": color, "width": line_width}
        })

    # Create and display a parallel chart
    parallel = Parallel(init_opts=opts.InitOpts(width="100%", height="600px"))
    parallel.add_schema(schema)
    parallel.add("parallel", data)
    parallel.set_global_opts(title_opts=opts.TitleOpts(title="Community Parallel Coordinates"))
    st_pyecharts(parallel)


def st_pyecharts(chart):
    # Render a Pyecharts chart in Streamlit
    raw_html = chart.render_embed()
    html(raw_html, width=1600, height=600)

if __name__ == "__main__":
    main()
