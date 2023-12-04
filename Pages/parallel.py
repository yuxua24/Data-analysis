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
    node_data = pd.read_csv("Dataset/MC1/community2/community_edge_node_stats_new.csv")
    edge_data = pd.read_csv("Dataset/MC1/Links.csv")
    parallel_data = pd.read_csv("Dataset/MC1/Parallel_coordinates/community_edge_node_stats_new.csv")

    # Filter nodes and edges based on the selected community
    filtered_nodes = node_data[node_data["Community"] == community_number]
    filtered_edges = edge_data[edge_data["source"].isin(filtered_nodes["id"]) & edge_data["target"].isin(filtered_nodes["id"])]
    filtered_parallel = parallel_data[parallel_data.iloc[:, 0] == community_number]

    # Depending on the chart type, display the respective chart
    if chart_type == "Graph":
        display_graph(filtered_nodes, filtered_edges)
    elif chart_type == "Parallel":
        display_parallel(filtered_parallel)

def display_graph(filtered_nodes, filtered_edges):
    # Prepare graph data
    nodes = [{"name": str(node), "symbolSize": 10} for node in filtered_nodes["id"]]
    links = [{"source": str(source), "target": str(target)} for source, target in zip(filtered_edges["source"], filtered_edges["target"])]

    # Create and display a graph
    g = Graph(init_opts=opts.InitOpts(width="100%", height="600px"))
    g.add("", nodes, links, repulsion=5000)
    g.set_global_opts(title_opts=opts.TitleOpts(title="Community Graph"))
    st_pyecharts(g)

def display_parallel(filtered_parallel):
    # Prepare parallel data
    schema = [opts.ParallelAxisOpts(dim=i, name=col) for i, col in enumerate(filtered_parallel.columns[3:])]
    data = filtered_parallel.iloc[:, 3:].values.tolist()

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
