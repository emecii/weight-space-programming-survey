"""Build a one-page Chinese survey from the adjacent JSON source.

Requires reportlab and pypdf. Fonts default to Microsoft YaHei on Windows;
--font and --bold-font accept user-supplied TrueType CJK fonts elsewhere.
"""
from pathlib import Path
import argparse, json, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=ROOT/'survey-one-page-zh.pdf')
parser.add_argument('--font',type=Path,default=Path('C:/Windows/Fonts/msyh.ttc'))
parser.add_argument('--bold-font',type=Path,default=Path('C:/Windows/Fonts/msyhbd.ttc'))
args=parser.parse_args()
data=json.loads((ROOT/'survey-one-page-zh.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('CN',str(args.font),subfontIndex=0))
pdfmetrics.registerFont(TTFont('CN-Bold',str(args.bold_font),subfontIndex=0))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CN-Bold',italic='CN',boldItalic='CN-Bold')
navy=colors.HexColor('#15364B');teal=colors.HexColor('#146C78');muted=colors.HexColor('#536572');light=colors.HexColor('#EFF4F7');rule=colors.HexColor('#CBD7DE')
pw,ph=A4;margin=35;width=pw-2*margin
styles={
 'title':ParagraphStyle('title',fontName='CN-Bold',fontSize=19.5,leading=27,textColor=navy,spaceAfter=5,wordWrap='CJK'),
 'sub':ParagraphStyle('sub',fontName='CN',fontSize=8.7,leading=13,textColor=teal,spaceAfter=8,wordWrap='CJK'),
 'body':ParagraphStyle('body',fontName='CN',fontSize=9.4,leading=14.8,spaceAfter=5,wordWrap='CJK'),
 'head':ParagraphStyle('head',fontName='CN-Bold',fontSize=10.3,leading=15.5,textColor=navy,spaceBefore=7,spaceAfter=5,keepWithNext=True,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='CN',fontSize=9.2,leading=13.8,wordWrap='CJK'),
 'th':ParagraphStyle('th',fontName='CN-Bold',fontSize=9.2,leading=13.8,textColor=colors.white,wordWrap='CJK'),
 'refs':ParagraphStyle('refs',fontName='CN',fontSize=7.8,leading=11.7,wordWrap='CJK'),
 'note':ParagraphStyle('note',fontName='CN',fontSize=6.9,leading=10,textColor=muted,spaceBefore=4,wordWrap='CJK')
}
seen=set()
def markup(s):
    s=html.escape(s)
    def replace(m):
        ns=[int(x) for x in m.group(1).split(',')];seen.update(ns)
        return '['+', '.join(f'<link href="#r{n}" color="#146C78">{n}</link>' for n in ns)+']'
    return re.sub(r'\[([1-8](?:,[1-8])*)\]',replace,s)
def P(s,style='body'):return Paragraph(markup(s),styles[style])

story=[P(data['title'],'title'),P(data['subtitle'],'sub'),P(data['intro']),P(data['table_title'],'head')]
rows=[[P(s,'th') for s in data['headers']]]+[[P(s,'cell') for s in r] for r in data['rows']]
table=Table(rows,colWidths=[width*.30,width*.35,width*.35],hAlign='LEFT')
table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[light,colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,-1),(-1,-1),.5,rule)]))
story+=[table,P(data['evidence_title'],'head')]
for entry in data['evidence']:
    story.append(Paragraph('<b>'+html.escape(entry['label'])+'</b>　'+markup(entry['text']),styles['body']))
story+=[P(data['synthesis_title'],'head'),P(data['synthesis']),P('代表文献（链接指向原始来源）','head')]
refrows=[]
for i in range(4):
    row=[]
    for idx in [i,i+4]:
        r=data['references'][idx]
        row.append(Paragraph(f'<a name="r{r["n"]}"/>[{r["n"]}] <link href="{r["url"]}" color="#146C78">{html.escape(r["short"])}</link>',styles['refs']))
    refrows.append(row)
rt=Table(refrows,colWidths=[width*.50,width*.50],hAlign='LEFT')
rt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
story+=[rt,P(data['note'],'note')]

def footer(c,doc):
    c.saveState();c.setStrokeColor(rule);c.setLineWidth(.5);c.line(margin,27,pw-margin,27)
    c.setFont('CN',7);c.setFillColor(muted);c.drawString(margin,15,'Weight-Space Programming Survey · '+data['date']);c.drawRightString(pw-margin,15,str(doc.page));c.restoreState()

args.output.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(args.output),pagesize=A4,leftMargin=margin,rightMargin=margin,topMargin=29,bottomMargin=35,title=data['title'],author='',subject='单页中文综述：WSP、零阶优化、表征引导、NAS与具身控制的方法、成本及局限')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(args.output)
assert len(reader.pages)==1,f'Expected exactly one page, got {len(reader.pages)}'
assert seen==set(range(1,9)),f'Citation mismatch: {seen}'
print('PDF:',args.output,'| pages:',len(reader.pages),'| references:',len(seen))

md=['# '+data['title'],'',data['subtitle'],'','更新：'+data['date'],'',data['intro'],'','## '+data['table_title'],'','| '+' | '.join(data['headers'])+' |','|---|---|---|']
md+=['| '+' | '.join(r)+' |' for r in data['rows']]
md+=['','## '+data['evidence_title'],'']
md+=['**'+e['label']+'**　'+e['text']+'\n' for e in data['evidence']]
md+=['## '+data['synthesis_title'],'',data['synthesis'],'','## 代表文献','']
md += [f'[{r["n"]}] [{r["short"]}]({r["url"]})。*{r["title"]}*。' for r in data['references']]
md+=['',data['note'],'','[方法、成本与局限的来源核验表](../literature/one-page-evidence.csv)记录版本、章节位置及解释边界。','','## 重建 PDF','','编辑同目录 `survey-one-page-zh.json`，安装 `reportlab` 和 `pypdf` 后运行：','','```shell','python build_one_page_zh.py','```','','脚本默认使用 Windows 微软雅黑；其他系统可用 `--font` 与 `--bold-font` 指定支持中文的 TrueType 字体。']
(ROOT/'survey-one-page-zh.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
