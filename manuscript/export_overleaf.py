"""Deterministic Markdown -> editable XeLaTeX export, preserving reference numbers.
Run from any directory. No network; sources: survey-en.md and references-200.json.
"""
from pathlib import Path
import json,re,shutil,zipfile
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'overleaf'; OUT.mkdir(exist_ok=True)
MATH={'α':r'\alpha','θ':r'\theta','Δ':r'\Delta','λ':r'\lambda','Σ':r'\Sigma','≈':r'\approx','∈':r'\in','π':r'\pi','ε':r'\epsilon','∇':r'\nabla','η':r'\eta','σ':r'\sigma','→':r'\rightarrow','←':r'\leftarrow','↔':r'\leftrightarrow','ᵀ':r'{}^T'}
def esc(t):
 out=''
 for c in t:
  if c in MATH:out+=r'\ensuremath{'+MATH[c]+'}'
  elif c in '&%$#_{}':out+='\\'+c
  elif c=='\\':out+=r'\textbackslash{}'
  elif c=='~':out+=r'\textasciitilde{}'
  elif c=='^':out+=r'\textasciicircum{}'
  else:out+=c
 return out
cited=set()
def inline(t):
 t=esc(t.replace('`',''))
 def cite(m):
  nums=[]
  for part in m[1].split(','):
   if '-' in part:
    a,b=map(int,part.split('-'));nums.extend(range(a,b+1))
   else:nums.append(int(part))
  cited.update(nums);return r'\cite{'+','.join('r'+str(n) for n in nums)+'}'
 t=re.sub(r'\[(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)\]',cite,t)
 return re.sub(r'\*\*(.*?)\*\*',r'\\textbf{\1}',t)
def diagram(kind):
 if kind=='spaces':
  labels=['Inputs / prompts','Activations','Weights','Architecture']; note='Statistical construction, gradients, function-value search, or LLM proposals'
 else:labels=['Observation','Policy + intervention','Action execution','Feedback'];note='The environment evolves during inference and execution'
 return '\n'.join([r'\begin{center}\begin{tikzpicture}[every node/.style={font=\small}]']+[rf'\node[draw=teal,fill=teal!5,rounded corners,minimum width=3.3cm,minimum height=.8cm] (n{i}) at ({i*3.7},0) {{{l}}};' for i,l in enumerate(labels)]+([rf'\draw[->,teal] (n{i}) -- (n{i+1});' for i in range(3)] if kind!='spaces' else [])+[r'\end{tikzpicture}\par\small '+note+r'\end{center}'])
lines=(ROOT/'manuscript/survey-en.md').read_text().splitlines(); body=[];i=0
while i<len(lines):
 t=lines[i].strip();i+=1
 if not t:continue
 if t.startswith('$$ ') and t.endswith(' $$'):
  body.append(r'\['+t[3:-3]+r'\]');continue
 if t=='<!-- pagebreak -->':body.append(r'\clearpage');continue
 if t.startswith('<!-- figure:'):body.append(diagram(t.split(':')[1].split()[0]));continue
 if t.startswith('|'):
  raw=[t]
  while i<len(lines) and lines[i].strip().startswith('|'):raw.append(lines[i].strip());i+=1
  rows=[[v.strip() for v in r.strip('|').split('|')] for r in raw if not re.fullmatch(r'[|\s:\-]+',r)]
  n=len(rows[0]); widths=[1/n]*n
  spec=''.join(r'>{\raggedright\arraybackslash}p{'+str(round((15.8-.42*n)*w,2))+'cm}' for w in widths)
  b=[r'\begingroup\small\setlength{\tabcolsep}{5pt}\renewcommand{\arraystretch}{1.18}',r'\begin{longtable}{'+spec+'}',r'\toprule',' & '.join(r'\textbf{'+inline(x)+'}' for x in rows[0])+r'\\\midrule\endhead']
  for row in rows[1:]:b.append(' & '.join(inline(x) for x in row)+r'\\\addlinespace[3pt]')
  body.extend(b+[r'\bottomrule\end{longtable}\endgroup']);continue
 if t.startswith('# '):body.append(r'\begin{center}{\LARGE\bfseries '+inline(t[2:])+r'}\end{center}');continue
 if t.startswith('## '):body.append(r'\section*{'+inline(t[3:])+r'}');continue
 if t.startswith('### '):body.append(r'\subsection*{'+inline(t[4:])+r'}');continue
 if t.startswith('> '):t=t[2:]
 body.append(inline(t)+'\n')
refs=json.loads((ROOT/'literature/references-200.json').read_text())
bib=[r'\begin{thebibliography}{200}\small']
for r in refs:
 title=esc(r['title']);authors=esc(', '.join(r['authors'][:6])+(', et al.' if len(r['authors'])>6 else ''));url=r['url']
 bib.append(r'\bibitem{r'+str(r['number'])+'} '+authors+'. '+r'\href{'+url+'}{'+title+'}. '+str(r['year'])+'.'+(' DOI: '+esc(r['doi'])+'.' if r.get('doi') else ''))
bib.append(r'\end{thebibliography}')
(OUT/'body.tex').write_text('\n\n'.join(body))
(OUT/'references.tex').write_text('\n'.join(bib))
(OUT/'main.tex').write_text(r'''% !TeX program = xelatex
\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,xcolor,tikz}
\usepackage[unicode,colorlinks=true,linkcolor=teal,citecolor=teal,urlcolor=teal]{hyperref}
\usepackage{cite}
\usepackage{fancyhdr}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\linespread{1.08}
\setlength{\emergencystretch}{3em}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Weight-Space Programming}
\fancyhead[R]{\small Methods, Costs, and Limitations}
\fancyfoot[L]{\small English working draft}
\fancyfoot[R]{\thepage}
\setlength{\headheight}{15pt}
\begin{document}
\let\originalclearpage\clearpage
\let\clearpage\relax
\input{body}
\let\clearpage\originalclearpage
\clearpage
\input{references}
\end{document}
''')
(OUT/'latexmkrc').write_text("$pdf_mode = 5;\n$xelatex = 'xelatex -interaction=nonstopmode -synctex=1 %O %S';\n")
(OUT/'references-200.bib').write_text(re.sub(r'^  note = .*\n', '', (ROOT/'literature/references-200.bib').read_text(), flags=re.M))
(OUT/'README.md').write_text('''# Weight-Space Programming Survey — English manuscript

Overleaf: select XeLaTeX, main document `main.tex`, then Recompile.

Edit `body.tex` for manuscript text; `references.tex` preserves existing [1]–[200] numbering. `references-200.bib` is supplied for future venue conversion; the current build uses references.tex, not BibTeX.

Source of truth before collaborative editing: manuscript/survey-en.md and literature/references-200.json in GitHub. Run `python3 manuscript/export_overleaf.py` to regenerate this folder. Once editing on Overleaf starts, export and reconcile those edits before regenerating; do not overwrite collaborators' changes.

Author order, affiliations, funding, conflict-of-interest and author contribution declarations require team input. This is a narrative review with no new experiments. The baseline search date remains 2026-11-09. AI assistance was used for drafting, source cross-checking and formatting; authors must review the final text and venue-specific disclosure requirements.
''')
(OUT/'README.md').write_text((OUT/'README.md').read_text()+'\nOverleaf: https://www.overleaf.com/project/6afd33eb5393573dd5c55652\n')
assert cited <= {r['number'] for r in refs}
print('References:',len(refs),'cited:',len(cited),'uncited:',sorted(set(range(1,201))-cited))
