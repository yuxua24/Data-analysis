# VAST Challenge 2023 - MC1 & MC3 Solutions

这个仓库包含了VAST Challenge 2023的MC1和MC3任务的解决方案。我们实现了一个交互式分析系统，旨在提供直观、高效的数据可视化和分析工具。

## 快速开始

要运行这个项目，请确保您已安装所有必要的依赖，然后在终端中执行以下命令：

```bash
streamlit run Introduction.py
```

## 功能概览

### MC1 - 分析页面 (MC1-Analysis)

MC1-Analysis页面提供了MC1任务的可视化展示和交互式分析系统。主要功能包括：

- **快速选择**：对4个怀疑实体的快速选择功能。
- **邻接图绘制**：绘制选定节点的邻接图。
- **信息筛选**：筛选节点和边的信息。
- **饼图统计**：使用饼图统计图中各种类型节点和边的数量。
- **节点详情显示**：点击图中节点以显示节点的详细信息。
- **怀疑集合管理**：将节点添加到怀疑集合中。
- **社区可视化**：对社区内部进行详细的可视化展示。

![MC1-Analysis](images/MC1-Analysis.png)

![MC1-community-Analysis](images/community.png)


[MC1-Analysis 演示视频](video/MC1-Analysis.mp4)

### MC1 - 异常度评估系统 (MC1-Anomaly)

MC1-Anomaly页面提供了MC1的异常度评估系统。功能特点包括：

- **评判标准设定**：设置多项评判标准。
- **权重和K值自定义**：用户可自定义每项标准的权重和K值。
- **异常度排名**：系统返回可疑度最高的前K个节点。

![MC1-Anomaly](images/MC1-Anomaly.png)

[MC1-Anomaly 演示视频](video/MC1-Anomaly.mp4)

### MC3 - 分析页面 (MC3-Analysis)

MC3-Analysis页面专注于MC3任务的可视化展示和交互式分析。包括以下功能：

- **热力图展示**：直观展示数据热点。
- **柱状图展示**：通过柱状图展示数据分布。
- **有向图展示**：展示数据间的关系和流向。
- **互动功能**：点击热力图中的方块并添加到有向图中；点击有向图节点时，柱状图对应柱子标红。

![MC3-Analysis](images/MC3-Analysis.png)

[MC3-Analysis 演示视频](video/MC3-Analysis.mp4)

### MC3 - 相似性分析页面 (MC3-Similarity)

MC3-Similarity页面是针对相似性分析的交互式界面，其特点包括：

- **权重调节**：调节相应权重。
- **K值设定**：设置返回结果的数量（前K个节点）。
- **相似性分析**：返回相似性最高的节点。

![MC3-Similarity](images/MC3-Similarity.png)

[MC3-Similarity 演示视频](video/MC3-Similarity.mp4)

## 如何贡献

我们欢迎并鼓励社区成员对此项目做出贡献。请阅读我们的[贡献指南](CONTRIBUTING.md)了解更多信息。

## 许可证

此项目根据[MIT 许可证](LICENSE)授权。
