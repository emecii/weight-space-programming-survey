# 中文长文与重建

`survey-zh-200.pdf` 为 20 页版本：正文 15 页、参考文献 5 页。正文有 12 张比较表、2 张由构建脚本绘制的矢量示意图。编号 [1]-[200] 对应 `../literature/references-200.json`。

编辑 `survey-zh-200.md` 和相应文献 JSON，然后在仓库根目录运行：

```shell
python -m pip install reportlab pypdf
python manuscript/build_survey_zh.py
```

脚本使用 ReportLab 离线构建，附加参考文献、内部引用链接及 PDF 书签；不会访问网络。Markdown 是正文源文件，参考文献由 JSON 自动附加。`<!-- pagebreak -->` 是分页标记；`<!-- figure:spaces -->` 与 `<!-- figure:loop -->` 调用脚本中的原创矢量图。

默认使用 Windows 微软雅黑与 Times New Roman。其他系统需指定有授权的 TrueType/TTC 字体，字体不随仓库分发：

```shell
python manuscript/build_survey_zh.py --font /path/CJK-Regular.ttf --bold-font /path/CJK-Bold.ttf --latin-font /path/Serif-Regular.ttf --latin-italic-font /path/Serif-Italic.ttf
```

不同字体会改变换行与分页。构建后会输出 `.build.json` 记录页数、标题页码和参考文献栏高；须重新渲染检查，不能仅以脚本运行成功作为版面验收。

本版已检查 20 页、200 条唯一参考文献、对应链接、中文字体、页边界、表格和示意图。`survey-zh-200.qa.json` 记录核验结果。未开展新实验或独立复现。

前期单页中文 PDF、正文与构建脚本保留，用于快速阅读与历史比较。
