# 定向增量检索：2026-11-17

查询：`site:arxiv.org "weight-space programming" November 2026`；`site:arxiv.org "SteerAct" "2610.25632"`。工具：网页检索，原始来源为 arXiv 摘要记录。不是全领域检索；未更新 200 篇基线样本或其 62/138 核验计数。

| 候选与发布日期 | 摘要级发现 | 对综述的意义／待核验 |
| --- | --- | --- |
| [iWSP](https://arxiv.org/abs/2611.18114)，11-13 | 通过代码显式构造可解释权重和特征，包含神经编码模型 | 补充科学模型构造分支；全文检查解释性评价、外部先验与验证划分 |
| [Compiling Known Rules into Compact Neural Agents](https://arxiv.org/abs/2611.16981)，11-12 | 提供已知游戏规则，比较写权重、代码策略及架构约束 | 直接支持信息权限与最终实现对象的比较；核验源代码访问、留出数据与计算限制 |
| [Replicating and Extending Weight-Space Programming](https://arxiv.org/abs/2611.21449)，11-16 | 报告复现，并将写权重与程序编译、读权重与输入层线索相联系 | 优先全文核验独立复现及替代解释，不直接采信摘要中的普适结论 |
| [Weight-Space Programming for Medical Imaging](https://arxiv.org/abs/2611.12066)，11-09 | 比较直接构造小型分类器与少样本训练，报告训练优势及失败案例 | 检查是否漏于基线截止时间；核验数据权限、公平对照与失败，不作临床建议 |

初始筛选时优先安排复现与游戏编译两篇；后续核验结果见下方更新记录。SteerAct 的本次查询没有形成可确认的版本变更记录；不能据此声称没有更新。

## Full-text follow-up

Relevant passages of arXiv:2611.21449v1 and arXiv:2611.16981v1 were checked on November 17 and incorporated into English Section 4.3 as supplemental references [201–202]. See `wsp-update-evidence-2026-11-17.md` for exact reading scopes and unresolved checks. The other two candidates remain abstract-screened. This update does not alter the baseline corpus or its 62/138 counts.
