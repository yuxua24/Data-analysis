import streamlit as st

# 在边栏创建一个下拉选择框，用于页面导航
page = st.sidebar.selectbox("", ["首页", "页面 1", "页面 2"])

# 根据选择的页面显示不同的内容
if page == "首页":
    st.write("这是首页")
    # 在这里添加首页的内容
elif page == "页面 1":
    st.write("欢迎来到页面 1")
    # 在这里添加页面 1 的内容
elif page == "页面 2":
    st.write("现在你在页面 2")
    # 在这里添加页面 2 的内容
