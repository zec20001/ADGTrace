# ADGTrace-Achieving-Adaptive-Trajectory-Synthesis-with-Generated-Data
User trajectory publication has promoted various location-based applications like user travel recommendation. However, possible privacy leakages have hindered more inclusive trajectory data analysis and utilization. Privacy-preserving trajectory synthesis is a popular approach to address the above privacy issues. Existing methods unavoidably produce low trajectory utility since they usually apply perturbed versions of human moving patterns. Worse still, they cannot adaptively adjust this synthesis according to the varying granularity demands of different users. This paper proposes a novel adaptive trajectory synthesis framework with generated data, namely ADGTrace. Our model achieves privacy preservation without introducing additional noise while maintaining high adaptation. ADGTrace directly synthesizes artiﬁcial trajectories that share the similar patterns with real ones through a generative and selective optimization process. Additionally, we present a grid granularity alignment strategy to achieve adaptive trajectory synthesis, satisfying varying user demands. Extensive experiments on real-world datasets demonstrate the superiority of ADGTrace over the stateof-the art methods under various utility metrics, maintaining strong attack resilience.
# ADGTrace

[![GitHub stars](https://img.shields.io/github/stars/zec20001/ADGTrace?style=social)](https://github.com/zec20001/ADGTrace/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zec20001/ADGTrace?style=social)](https://github.com/zec20001/ADGTrace/network)
[![GitHub issues](https://img.shields.io/github/issues/zec20001/ADGTrace)](https://github.com/zec20001/ADGTrace/issues)

> **ADGTrace** 是一个用于 **自适应轨迹合成（adaptive trajectory synthesis）** 的人工智能开源项目。通过生成数据，该模型无需额外噪声的情况下维护高适应性，同时实现隐私保护。

---

## 🚀 主要功能

- 📌 **Adaptive Trajectory Synthesis**：Automatically generates high-quality trajectories based on input data.
- 🔒 **Privacy Preservation**：Maintains model performance without introducing additional noise.
- ⚙️ **Extensible Architecture**：Suitable for research and engineering scenarios for further development.
- 🧠 **Trainable Modules**：Supports model training and evaluation.

---

## 📁 项目结构

```text
ADGTrace/
├── za          # Generates multiple pseudo-trajectories based on user trajectories
├── zb          # Uses FCNN model for training and prediction, selecting the most effective pseudo-trajectories
├── zc          # Aggregates trajectories across different grids
├── README.md   # Project description document
└── LICENSE     # License
