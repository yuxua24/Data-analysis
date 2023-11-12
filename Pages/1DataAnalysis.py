import streamlit as st
import pandas as pd

st.header("Data Analysis")
st.write("---")

"""
### Dataset Description
###### Earlier data was in JSON format and to make a sense out of it, JSON data was divided into two two DataFrames:
- 1. Nodes: Collection of all graph nodes in which ID column is unique.
- 2. Links: Collection of source and target edges.

###### To enhance the data quality, a unified DataFrame was created using joining node Dataframe with link DataFrame using: 
"""

code1 = "links = links.merge(nodes[['id', 'country']], how='left', left_on='source', right_on='id')"
st.code(code1, language="python", line_numbers=False)

code2 = "links = links.merge(nodes[['id', 'country']], how='left', left_on='target', right_on='id')"
st.code(code1, language="python", line_numbers=False)

"""
###### this enhancement in data helped in extracting the key factors from the knowledge graphs.

###### The uniform DataFrame looks like this:  
"""

links = pd.read_csv('Dataset/Links.csv')

st.write(links)