"""Build the Chinese survey from Markdown and checked bibliography metadata.

Dependencies: reportlab, pypdf. No network access required.
Defaults expect this script and manuscript in manuscript/, with literature/ next to it.
Chinese TrueType/TTC font paths are configurable; no fonts are redistributed.
"""
from pathlib import Path
import argparse, re, json, html, unicodedata
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, KeepTogether, Flowable, FrameBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,default=ROOT/'survey-zh-200.md')
ap.add_argument('--references',type=Path,default=ROOT.parent/'literature'/'references-200.json')
ap.add_argument('--output',type=Path,default=ROOT/'survey-zh-200.pdf')
ap.add_argument('--font',type=Path,default=Path('C:/Windows/Fonts/msyh.ttc'))
ap.add_argument('--bold-font',type=Path,default=Path('C:/Windows/Fonts/msyhbd.ttc'))
ap.add_argument('--latin-font',type=Path,default=Path('C:/Windows/Fonts/times.ttf'))
ap.add_argument('--latin-italic-font',type=Path,default=Path('C:/Windows/Fonts/timesi.ttf'))
args=ap.parse_args()
refs=json.loads(args.references.read_text(encoding='utf-8'))
assert len(refs)==200
pdfmetrics.registerFont(TTFont('CN',str(args.font),subfontIndex=0))
pdfmetrics.registerFont(TTFont('CN-Bold',str(args.bold_font),subfontIndex=0))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CN-Bold',italic='CN',boldItalic='CN-Bold')
pdfmetrics.registerFont(TTFont('Latin',str(args.latin_font)))
pdfmetrics.registerFont(TTFont('Latin-Italic',str(args.latin_italic_font)))
pdfmetrics.registerFontFamily('Latin',normal='Latin',bold='Latin',italic='Latin-Italic',boldItalic='Latin-Italic')
NAVY=colors.HexColor('#18374C'); TEAL=colors.HexColor('#12767C'); GRAY=colors.HexColor('#566672'); LIGHT=colors.HexColor('#F0F5F6'); RULE=colors.HexColor('#CCD9DD')
PW,PH=A4; M=44; WIDTH=PW-2*M
styles={
 'body':ParagraphStyle('body',fontName='CN',fontSize=10.5,leading=16.9,spaceAfter=8,wordWrap='CJK',textColor=colors.HexColor('#182631')),
 'title':ParagraphStyle('title',fontName='CN-Bold',fontSize=23,leading=32,spaceAfter=11,textColor=NAVY,wordWrap='CJK'),
 'h1':ParagraphStyle('h1',fontName='CN-Bold',fontSize=16,leading=23,spaceAfter=12,textColor=NAVY,wordWrap='CJK',keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='CN-Bold',fontSize=11.1,leading=17,spaceBefore=6,spaceAfter=7,textColor=TEAL,wordWrap='CJK',keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='CN',fontSize=9.3,leading=14.2,wordWrap='CJK',textColor=colors.HexColor('#182631')),
 'th':ParagraphStyle('th',fontName='CN-Bold',fontSize=9.3,leading=14.2,wordWrap='CJK',textColor=colors.white),
 'caption':ParagraphStyle('caption',fontName='CN',fontSize=8.3,leading=12.5,spaceBefore=5,spaceAfter=8,textColor=GRAY,wordWrap='CJK'),
 'equation':ParagraphStyle('equation',fontName='CN',fontSize=10.1,leading=17,spaceBefore=5,spaceAfter=11,leftIndent=10,rightIndent=10,backColor=LIGHT,borderPadding=9,wordWrap='CJK'),
 'ref':ParagraphStyle('ref',fontName='Latin',fontSize=9,leading=11.2,spaceAfter=5.5,leftIndent=21,firstLineIndent=-21,splitLongWords=True),
 'refhead':ParagraphStyle('refhead',fontName='CN-Bold',fontSize=12,leading=18,spaceAfter=10,textColor=NAVY,keepWithNext=True),
}
cited=set()
def clean(t):
    t=unicodedata.normalize('NFC',t).replace('–','-').replace('—','-').replace('‑','-').replace('\u200b','').replace('\ufeff','')
    t=t.replace('$\\pi_0$','pi_0').replace('$\\pi_{0}$','pi_0').replace('𝜋','pi').replace('π₀','pi_0')
    return t

def markup(t):
    t=html.escape(clean(t))
    t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t)
    def cite(m):
        parts=m.group(1).split(','); numbers=[]
        for p in parts:
            if '-' in p:
                a,b=map(int,p.split('-'));numbers.extend(range(a,b+1))
            else:numbers.append(int(p))
        assert all(1<=n<=200 for n in numbers),numbers
        cited.update(numbers)
        display=[]
        for p in parts:
            first=int(p.split('-')[0]);display.append(f'<link href="#r{first}" color="#12767C">{p}</link>')
        return '['+', '.join(display)+']'
    return re.sub(r'\[(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)\]',cite,t)

def P(t,sty='body'):return Paragraph(markup(t),styles[sty])

class Diagram(Flowable):
    def __init__(self,kind):
        super().__init__();self.kind=kind;self.width=WIDTH;self.height=137 if kind=='spaces' else 91
    def draw(self):
        c=self.canv
        def box(x,y,w,h,title,subtitle):
            c.setFillColor(LIGHT);c.setStrokeColor(RULE);c.roundRect(x,y,w,h,5,stroke=1,fill=1)
            c.setFillColor(NAVY);c.setFont('CN-Bold',9.5);c.drawCentredString(x+w/2,y+h-16,title)
            c.setFont('CN',8.1);c.setFillColor(GRAY);c.drawCentredString(x+w/2,y+10,subtitle)
        def arrow(x1,y1,x2,y2):
            c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(x1,y1,x2,y2)
            p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-5,y2+2.5);p.lineTo(x2-5,y2-2.5);p.close();c.setFillColor(TEAL);c.drawPath(p,fill=1,stroke=0)
        if self.kind=='spaces':
            gap=10;bw=(WIDTH-3*gap)/4
            for i,(t,s) in enumerate([('输入／提示','修改 x'),('激活／表征','修改 h'),('权重／参数','修改 θ'),('架构／计算图','修改 a')]):box(i*(bw+gap),82,bw,47,t,s)
            c.setFont('CN',9.3);c.setFillColor(TEAL);c.drawCentredString(WIDTH/2,62,'统计构造 · 梯度训练 · 零阶／演化搜索 · LLM 程序提案')
            c.setStrokeColor(RULE);c.line(15,50,WIDTH-15,50)
            c.setFillColor(NAVY);c.drawCentredString(WIDTH/2,31,'权限与预算 → 候选修改 → 反馈选择 → 独立验证／回退')
            c.setFont('CN',8.2);c.setFillColor(GRAY);c.drawCentredString(WIDTH/2,12,'同一种提案机制可作用于不同对象；语言和机器人是应用域')
        else:
            gap=20;bw=(WIDTH-3*gap)/4
            for i,(t,s) in enumerate([('观测','图像／状态'),('策略＋干预','门控与推理'),('动作执行','动作块／约束'),('环境反馈','成功／失败')]):
                box(i*(bw+gap),33,bw,48,t,s)
                if i<3:arrow(i*(bw+gap)+bw+2,57,(i+1)*(bw+gap)-3,57)
            c.setStrokeColor(TEAL);c.line(WIDTH-bw/2,30,WIDTH-bw/2,12);c.line(WIDTH-bw/2,12,bw/2,12);c.line(bw/2,12,bw/2,30)
            c.setFont('CN',8);c.setFillColor(GRAY);c.drawCentredString(WIDTH/2,18,'环境在推理与执行期间继续变化')

class SurveyDoc(BaseDocTemplate):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.headings=[];self.ref_start=None
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name in ('h1','title'):
            text=f.getPlainText();key='section'+str(len(self.headings));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,0,False);self.headings.append({'page':self.page,'title':text})
        if isinstance(f,Paragraph) and f.style.name=='refhead' and self.ref_start is None:self.ref_start=self.page

def decorate(c,doc):
    c.saveState();c.setStrokeColor(RULE);c.setLineWidth(.5);c.line(M,PH-36,PW-M,PH-36);c.line(M,35,PW-M,35)
    c.setFont('CN',7.2);c.setFillColor(GRAY);c.drawString(M,PH-27,'权重空间编程 · 方法、成本与局限');c.drawRightString(PW-M,PH-27,'200 篇文献 · 中文综述')
    c.drawString(M,22,'2026-11-09  |  叙述性综述 · 未开展新实验');c.drawRightString(PW-M,22,str(doc.page));c.restoreState()

doc=SurveyDoc(str(args.output),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=49,bottomMargin=46,
 title='权重空间编程：方法、成本与局限 - 200 篇文献中文综述',author='',subject='Weight-space programming, zeroth-order optimization, steering, NAS and embodied control',allowSplitting=1)
height=PH-49-46
frame=Frame(M,46,WIDTH,height,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='body')
gap=18;rw=(WIDTH-gap)/2
ref_frames=[Frame(M,46,rw,height,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='rleft'),Frame(M+rw+gap,46,rw,height,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='rright')]
doc.addPageTemplates([PageTemplate(id='body',frames=[frame],onPage=decorate),PageTemplate(id='refs',frames=ref_frames,onPage=decorate)])
story=[]
lines=args.source.read_text(encoding='utf-8').splitlines();i=0;table_count=0
while i<len(lines):
    line=lines[i].strip();i+=1
    if not line:continue
    if line=='<!-- pagebreak -->':story.append(PageBreak());continue
    if line.startswith('<!-- figure:'):
        story.append(Diagram(line.split(':')[1].split(' ')[0]));continue
    if line.startswith('### '):story.append(P(line[4:],'h2'));continue
    if line.startswith('## '):story.append(P(line[3:],'h1'));continue
    if line.startswith('# '):story.append(P(line[2:],'title'));continue
    if line.startswith('> '):story.append(P(line[2:],'equation'));continue
    if line.startswith('|'):
        table_count+=1;raw=[line]
        while i<len(lines) and lines[i].strip().startswith('|'):raw.append(lines[i].strip());i+=1
        rows=[[s.strip() for s in x.strip('|').split('|')] for x in raw if not re.fullmatch(r'[|\s:\-]+',x)]
        n=len(rows[0]);ratios={3:[.27,.35,.38],4:[.19,.28,.26,.27]}[n]
        if table_count==1:ratios=[.40,.12,.48]
        data=[[P(v,'th' if ri==0 else 'cell') for v in row] for ri,row in enumerate(rows)]
        tb=Table(data,colWidths=[WIDTH*x for x in ratios],repeatRows=1,hAlign='LEFT')
        tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[LIGHT,colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,-1),(-1,-1),.6,RULE)]))
        story.extend([tb,Spacer(1,9)]);continue
    para=[line]
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','<!--','|','>')):para.append(lines[i].strip());i+=1
    text=' '.join(para);story.append(P(text,'caption' if text.startswith(('图 1','图 2','版本：')) else 'body'))

assert cited==set(range(1,201)),f'Missing citations: {sorted(set(range(1,201))-cited)}'
story.extend([NextPageTemplate('refs'),PageBreak()])
ref_heights=[];col_height=0
for r in refs:
    n=r['number'];authors=r['authors'];author=authors[0]+(' et al.' if len(authors)>1 else '')
    if (n-1)%20==0:
        if n>1:ref_heights.append(round(col_height,1));story.append(FrameBreak())
        head=P(f'参考文献 {n}-{min(n+19,200)}','refhead');story.append(head);col_height=head.wrap(rw,height)[1]+styles['refhead'].spaceAfter
    title=clean(r['title']).replace('AtP$^*$','AtP*').replace('$','')
    url=html.escape(r['url'],quote=True)
    text=f'<a name="r{n}"/>[{n}] {html.escape(author)} ({r["year"]}). <link href="{url}" color="#174F66">{html.escape(title)}</link>. <font color="#566672">arXiv:{r["arxiv_id"]}</font>.'
    if n==131:text=f'<a name="r{n}"/>[{n}] {html.escape(author)} (2019). <link href="{url}" color="#174F66">{html.escape(title)}</link>. <i>JMLR</i> 20(55):1-21.'
    para=Paragraph(text,styles['ref']);col_height+=para.wrap(rw,height)[1]+styles['ref'].spaceAfter
    story.append(KeepTogether([para]))
ref_heights.append(round(col_height,1))
assert max(ref_heights)<height, (ref_heights,height)
args.output.parent.mkdir(parents=True,exist_ok=True)
doc.build(story)
reader=PdfReader(args.output)
metadata={'pages':len(reader.pages),'references':len(refs),'cited':len(cited),'reference_start_page':doc.ref_start,'headings':doc.headings,'tables':table_count,'figures':2,'reference_column_heights':ref_heights}
args.output.with_suffix('.build.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(metadata,ensure_ascii=False))
