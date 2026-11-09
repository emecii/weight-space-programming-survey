# Weight-Space Programming Survey

当前交付：**《权重空间编程：方法、成本与局限》20 页中文综述，纳入 200 篇去重论文／预印本**（2026-11-09）。正文 15 页，参考文献 5 页；包含 12 张比较表、2 张原创示意图，以及逐篇中文文献笔记。重点比较方法原理、信息条件、准备／搜索／部署／验证成本和局限。

**[直接打开 20 页 PDF](https://raw.githubusercontent.com/emecii/weight-space-programming-survey/main/manuscript/survey-zh-200.pdf)** · **[200 篇文献及逐篇笔记](literature/corpus-200.csv)** · **[当前计划摘要](readme.txt)**

## 范围与结构

用户指定的主题为 **weight-space programming**，覆盖权重空间学习、知识编辑与合并、零阶优化、表征引导、神经架构搜索，以及具身模型与闭环控制。本文按“修改哪里、如何提案、能访问什么信息、怎样验证”连接各分支，保留它们的机制差异。

正文依次讨论文献协议、统一描述框架、WSP、权重学习与合并、知识编辑、ZO 原理与系统成本、引导机制与副作用、NAS 与可靠比较、机器人闭环、成本账本和后续实验问题。详细页码见 [结构说明](docs/OUTLINE.md)。

## 文献与证据

本轮 16 组 arXiv 查询返回 528 条去重候选，结合 77 条种子／补检记录后得到 590 条唯一候选，按代表性和分支覆盖纳入 200 篇。分组为权重空间与编辑 50、ZO 35、表征引导 45、NAS 45、具身控制 25。

**62 篇核验了全文相关章节，138 篇完成元数据及摘要筛选。**“相关章节核验”不表示逐页精读全部论文；摘要级记录只用于机制和范围定位。200 篇均有中文方法笔记、成本／局限笔记、原始链接及核验深度。本文是叙述性综述，未开展新实验，不声称穷尽检索、双人独立筛选、元分析或已验证的创新优先权。

- [完整文献矩阵](literature/corpus-200.csv) / [BibTeX](literature/references-200.bib) / [结构化元数据](literature/references-200.json)
- [精确检索记录](literature/search-log.csv) / [590 条候选的选择记录](literature/screening-log.csv)
- [关键论断、原文位置与解释边界](literature/evidence-ledger.csv)
- [文献字段与筛选说明](literature/README.md)

新近 WSP 文献中的实验、机制审计与技术猜想分别标记；不将猜想数字当作已验证结果。比较保留 WSP 搜索回退、知识编辑一致性、引导副作用、NAS 代理偏差与机器人恢复／延迟问题。

## 稿件与重建

- [长文 PDF 原文件](https://raw.githubusercontent.com/emecii/weight-space-programming-survey/main/manuscript/survey-zh-200.pdf)
- [可编辑中文正文](manuscript/survey-zh-200.md)
- [PDF 构建脚本](manuscript/build_survey_zh.py) / [构建说明](manuscript/README.md)
- [版面与引用检查记录](manuscript/survey-zh-200.qa.json)
- [范围](docs/SCOPE.md) / [当前执行计划](docs/PLAN.md)

前期 [单页中文摘要 PDF](https://raw.githubusercontent.com/emecii/weight-space-programming-survey/main/manuscript/survey-one-page-zh.pdf) 保留，长文是本轮主要交付。现有单页文件和证据表未被覆盖。

## 起始材料

- [Exploring Weight-Space Programming](https://arxiv.org/abs/2611.09382v1)，本轮文献 [1]。
- [SteerAct](https://arxiv.org/abs/2610.25632v1)，本轮文献 [176]；SteerScope 是补充评估来源。
- [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/)，原作者博客作为背景，**不计入 200 篇学术文献**。

仓库只发布本项目文本、脚本、自制图表、元数据和原文链接；不分发第三方论文 PDF、完整摘要、字体或私人聊天材料。作者名单、机构、投稿场所及许可证尚未指定。
