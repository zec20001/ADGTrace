# ADGTrace-Achieving-Adaptive-Trajectory-Synthesis-with-Generated-Data
User trajectory publication has promoted various location-based applications like user travel recommendation. However, possible privacy leakages have hindered more inclusive trajectory data analysis and utilization. Privacy-preserving trajectory synthesis is a popular approach to address the above privacy issues. Existing methods unavoidably produce low trajectory utility since they usually apply perturbed versions of human moving patterns. Worse still, they cannot adaptively adjust this synthesis according to the varying granularity demands of different users. This paper proposes a novel adaptive trajectory synthesis framework with generated data, namely ADGTrace. Our model achieves privacy preservation without introducing additional noise while maintaining high adaptation. ADGTrace directly synthesizes artiﬁcial trajectories that share the similar patterns with real ones through a generative and selective optimization process. Additionally, we present a grid granularity alignment strategy to achieve adaptive trajectory synthesis, satisfying varying user demands. Extensive experiments on real-world datasets demonstrate the superiority of ADGTrace over the stateof-the art methods under various utility metrics, maintaining strong attack resilience.
# ADGTrace

[![GitHub stars](https://img.shields.io/github/stars/zec20001/ADGTrace?style=social)](https://github.com/zec20001/ADGTrace/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zec20001/ADGTrace?style=social)](https://github.com/zec20001/ADGTrace/network)
[![GitHub issues](https://img.shields.io/github/issues/zec20001/ADGTrace)](https://github.com/zec20001/ADGTrace/issues)

> **ADGTrace** 是一个用于 **自适应轨迹合成（adaptive trajectory synthesis）** 的人工智能开源项目。通过生成数据，该模型无需额外噪声的情况下维护高适应性，同时实现隐私保护。

---

## 🚀 主要功能

- 📌 **自适应轨迹合成**：根据输入数据自动生成高质量轨迹。
- 🔒 **隐私保护**：无需引入额外噪声，在保证隐私的前提下保持模型性能。
- ⚙️ **易扩展架构**：适合科研和工程场景进行二次开发。
- 🧠 **可训练模块**：支持模型训练与测试评估。

---

## 📁 项目结构

```text
ADGTrace/
├── your_module/          # 核心代码模块
├── notebooks/            # 示例与实验 notebook
├── data/                 # 示例数据
├── requirements.txt      # 依赖列表
├── main.py               # 运行入口
├── README.md             # 项目说明文档
└── LICENSE               # 许可证
