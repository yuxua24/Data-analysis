import streamlit as st
import pandas as pd


data = pd.DataFrame({
    'A': range(1, 101),
    'B': range(101, 201)
})

st.markdown(
    """
    <style>
    .scrolling-wrapper {
        border: 2px solid #9e9e9e;  
        border-radius: 5px;         
        overflow: auto;
        height: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scrolling-wrapper">' + data.to_html(index=True) + '</div>',
    unsafe_allow_html=True
)
