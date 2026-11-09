权重空间编程综述：当前计划摘要
更新日期：2026-11-09
仓库：https://github.com/emecii/weight-space-programming-survey

一、当前目标与进度
当前交付是一页中文综述，已上传 PDF、中文正文、可编辑 JSON 和生成脚本；下一步是审阅并修订这一页。PDF 已检查页数、中文字体、版面和引用一致性，包含方法对照、关键证据及 8 项代表文献。
原先的 20–30 页长篇目标和约 28 页提纲保留为后续扩展方案，不是当前交付的页数要求。

PDF 原文件直链（不是 GitHub 文件预览页）：
https://raw.githubusercontent.com/emecii/weight-space-programming-survey/main/manuscript/survey-one-page-zh.pdf

二、综述范围
覆盖权重空间编程、零阶优化、激活／表征引导、神经架构搜索（NAS），并保留具身模型与机器人控制案例。重点起始材料为 Exploring Weight-Space Programming、Sparks of Weight-Space Programming 和 SteerAct；SteerScope 用于补充评估证据。

三、组织主线
围绕“修改哪里、如何提出或搜索修改、需要什么信息、怎样公平评估”组织内容：
1. 干预空间：激活、权重、架构。
2. 方法机制：统计构造、梯度、零阶查询、进化搜索、LLM 提案等，可多标签归类。
3. 信息条件：可否访问权重、激活、梯度、目标值与轨迹。
4. 评估协议：分别记录准备、搜索、部署和最终验证成本，比较目标收益、能力回退、泛化与副作用。
具身控制是应用场景；表征引导不等同于零阶优化，NAS 也不必然是无梯度方法。不同任务的分数不直接混合排名。

四、后续工作顺序
1. 先审阅单页 PDF，按反馈调整重点、术语与可读性，同步更新正文、JSON 和 PDF。
2. 核验并补充原始论文与作者资料；记录检索日期、版本、筛选依据和具体证据位置，纳入失败案例与相反结论。
3. 完善文献对照表：统一记录干预对象、信息访问、搜索机制、基线、预算、准备成本、迁移表现和副作用，标出不可直接比较的结果。
4. 对照已有综述全文，检验分类与综合分析是否提供额外价值，再确定贡献表述与长篇扩展结构。
5. 如后续扩展成长篇，沿用已有提纲完善论证、图表和参考文献；每次修订同步源码与 PDF，并在 GitHub 留下版本记录。

五、证据边界与待定事项
当前版本是基于已有文献的叙述性综述，未开展新实验，不声称已完成穷尽式系统综述或已证实创新优先权。实验仅在能解决明确比较问题且预算、协议确定后考虑，并非当前必需任务。正式标题、投稿场所、作者名单与许可证仍待确定。

六、文件位置
manuscript/survey-one-page-zh.pdf：单页中文 PDF。
manuscript/survey-one-page-zh.md：中文正文及构建说明。
manuscript/survey-one-page-zh.json：可编辑内容源。
manuscript/build_one_page_zh.py：PDF 生成脚本。
docs/PLAN.md：详细文献与交付流程，含早期长篇计划。
docs/OUTLINE.md：保留的长篇提纲。
docs/SCOPE.md：研究范围、边界和候选贡献。
literature/seed-papers.csv：种子文献与核验状态。
