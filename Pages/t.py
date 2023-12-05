from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

# 创建柱状图对象
bar = Bar()

# 数据
x_data = ["A", "B", "C", "D", "E"]
y_data = [5, 10, 15, 20, 25]

# 自定义颜色数组
bar_item_colors = ["red", "blue", "green", "orange", "purple"]

# 将 y_data 转换为包含样式的字典列表
y_data_with_style = [{"value": y, "itemStyle": {"color": color}} for y, color in zip(y_data, bar_item_colors)]

# 添加数据和颜色
bar.add_xaxis(x_data)
bar.add_yaxis("柱状图", y_data_with_style)

# 设置标题和其他样式
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="自定义柱状图颜色示例"),
    xaxis_opts=opts.AxisOpts(name="X轴"),
    yaxis_opts=opts.AxisOpts(name="Y轴"),
)

# 在 Streamlit 中渲染直方图
st_pyecharts(bar, height="400px", width="100%")
