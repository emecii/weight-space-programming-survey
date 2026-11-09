# 权重空间编程：方法、成本与局限

单页中文综述 · 零阶优化 / 表征引导 / 架构搜索 / 具身控制

更新：2026-11-09

权重空间编程（WSP）让推理模型检查、构造或直接修改网络权重[1,2]。本页按干预对象、信息访问和搜索机制，对照相邻方法的成本与边界：类别可重叠，表征引导不等同于零阶优化，NAS 也不必然无梯度；具身控制是应用场景。

## 方法对照：成本发生在哪里，结论受什么限制

| 方法与信息条件 | 主要成本（口径与阶段） | 局限与适用边界 |
|---|---|---|
| WSP：推理式权重编辑[1,2]。需权重读写；可结合激活诊断与任务反馈。 | 搜索：LLM 推理、工具调用、候选评测。部署：直接写入权重的编辑可沿用原计算图。 | 适合可定位的局部故障；少改参数不代表发现成本低。结果随任务、模型和搜索轨迹变化。 |
| 零阶优化（MeZO）[3]：随机双边扰动权重，用函数值估计更新，无需反向传播。 | 基本单方向更新需 2 次批次函数评估，另有扰动开销；原地实现显存接近推理，调参与验证另计。 | 适合反向传播显存受限；省显存不保证省总计算。受目标噪声、步数与有效维度影响，仍需可扰动权重。 |
| 表征引导（CAA）[4]：对比样本的平均激活差构造方向；需访问并干预隐藏状态。 | 准备：采集激活、选层与调强度。部署：在指定位置加向量，开销随序列长度与干预层数变化。 | 可灵活调整行为；强干预可能损害文本质量。目标收益、能力保留和分布外副作用需共同评估[7]。 |
| NAS（DARTS）[5,8]：架构连续松弛、双层梯度优化；需训练权重与架构参数。 | CIFAR-10（单位：GPU·天）：搜索一阶 1.5、二阶 4；另计选择 1、最终重训 1.5[5]。 | 受预设搜索空间与代理评估约束；松弛后须离散化、重训验证。上述成本限于原文硬件与实验协议。 |
| 具身引导（SteerAct）[6]：用 SAE 特征及参考轨迹调节干预时机和强度；需隐藏状态。 | 准备：训练 SAE、默认每任务 24 条带结果标签的仿真参考轨迹。部署：时序描述、参考匹配与门控。 | 受参考覆盖和 SAE 质量约束，不能消除主模型能力缺口；冻结主模型仍有准备成本和在线时延。 |

## 证据与反例：收益不等于稳定、无副作用的改进

**发现可靠性**　Exploring WSP 的一个 0.8B 数学案例修改 1,023 个参数，留出集 MATH-500 提升 29.45 个百分点；但共 16 条搜索轨迹中有 6 条最终保留原权重[2]。应同时报告成功收益、失败轨迹与总搜索预算。

**收益与副作用**　SteerScope 在两个 Gemma-2 规模的匹配评估及默认聚合下，所测激活方法未能在不增加综合副作用的同时超过提示词引导[7]。这是特定设置下的权衡，不构成对所有引导方法的否定。

## 比较原则与研究重点（本文综合）

成本分准备、搜索、部署、独立验证四阶段，记录 GPU·时、峰值显存、LLM token/API 费用、样本/轨迹数及单次时延，不混加不同单位。比较须匹配任务、信息访问、硬件和预算，保留未修改模型、提示词与简单搜索基线，并报告跨任务回退、分布外表现及多次运行波动。下一步重点检验：推理式提案在同编辑空间、同预算下是否优于简单搜索，以及收益能否覆盖部署与验证成本。

## 代表文献

[1] [Takehi 等，Sparks of WSP（2026，作者博客）](https://rikiyat.github.io/blog/weight-space-programming/)。*Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights*。
[2] [Hu 等，Exploring WSP（2026） · 2611.09382v1](https://arxiv.org/abs/2611.09382v1)。*Exploring Weight-Space Programming: Capabilities, Generalization, and Limitations*。
[3] [Malladi 等，MeZO（2023） · 2305.17333v3](https://arxiv.org/abs/2305.17333v3)。*Fine-Tuning Language Models with Just Forward Passes*。
[4] [Panickssery 等，CAA（2023） · 2312.06681v4](https://arxiv.org/abs/2312.06681v4)。*Steering Llama 2 via Contrastive Activation Addition*。
[5] [Liu 等，DARTS（2018） · 1806.09055v2](https://arxiv.org/abs/1806.09055v2)。*DARTS: Differentiable Architecture Search*。
[6] [Zhou 等，SteerAct（2026） · 2610.25632v1](https://arxiv.org/abs/2610.25632v1)。*SteerAct: Unlocking Action Models through Few-Shot Temporal Steering*。
[7] [Yang 等，SteerScope（2026） · 2610.07722v1](https://arxiv.org/abs/2610.07722v1)。*Does Steering Break Your Model? A Multi-Dimensional Evaluation Suite for LLM Steering Methods*。
[8] [Elsken 等，Neural Architecture Search: A Survey（2019）](https://jmlr.org/papers/v20/18-598.html)。*Neural Architecture Search: A Survey*。

SAE：稀疏自编码器。核验日期：2026-11-09；8 项代表来源可点击，非穷尽检索。表中成本项为机制归纳，数值限于所引实验；未开展新实验。AI 辅助整理。

[方法、成本与局限的来源核验表](../literature/one-page-evidence.csv)记录版本、章节位置及解释边界。

## 重建 PDF

编辑同目录 `survey-one-page-zh.json`，安装 `reportlab` 和 `pypdf` 后运行：

```shell
python build_one_page_zh.py
```

脚本默认使用 Windows 微软雅黑；其他系统可用 `--font` 与 `--bold-font` 指定支持中文的 TrueType 字体。
