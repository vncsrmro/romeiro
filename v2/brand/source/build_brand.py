from pathlib import Path
import math, json, shutil, zipfile, html
from fontTools.ttLib import TTFont as Font
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.reportLabPen import ReportLabPen
from fontTools.pens.basePen import BasePen
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader, simpleSplit
from PIL import Image, ImageDraw
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
BRAND=ROOT/'brand'; OUT=ROOT/'output/pdf'; TMP=ROOT/'tmp/pdfs'; ASSETS=ROOT/'assets'
for p in [BRAND/'logos',BRAND/'fonts',BRAND/'templates',BRAND/'pages',OUT,TMP]:p.mkdir(parents=True,exist_ok=True)
INK='#242520'; PAPER='#EDEDE5'; LIME='#D7FF3F'; DARK='#20231F'; MUTED='#62665A'; LINE='#C9CCBE'; WHITE='#FFFFFF'
for w,name in [(400,'Space-Regular'),(500,'Space-Medium'),(700,'Space-Bold')]:
    f=Font(ASSETS/'fonts/SpaceGrotesk.ttf');f=instantiateVariableFont(f,{'wght':w},inplace=False);f.save(BRAND/'fonts'/f'{name}.ttf');pdfmetrics.registerFont(TTFont(name,str(BRAND/'fonts'/f'{name}.ttf')))
f=Font(ASSETS/'fonts/CormorantGaramond-Italic.ttf')
if 'fvar' in f:f=instantiateVariableFont(f,{'wght':400},inplace=False)
f.save(BRAND/'fonts/Editorial-Italic.ttf');pdfmetrics.registerFont(TTFont('Editorial',str(BRAND/'fonts/Editorial-Italic.ttf')))
shutil.copy(ASSETS/'fonts/MrsSaintDelafield-Regular.ttf',BRAND/'fonts/Signature.ttf')
pdfmetrics.registerFont(TTFont('Signature',str(BRAND/'fonts/Signature.ttf')))
for f in (ASSETS/'fonts').glob('OFL*'):shutil.copy(f,BRAND/'fonts'/f.name)
font=Font(BRAND/'fonts/Space-Bold.ttf');glyphs=font.getGlyphSet();cmap=font.getBestCmap();units=font['head'].unitsPerEm
positions=[];advance=0
for ch in 'romeiro':
    positions.append((cmap[ord(ch)],advance));advance+=font['hmtx'][cmap[ord(ch)]][0]-units*.079
LOGOW=advance+130;LOGOH=770

class CanvasPen(BasePen):
    def __init__(self,glyphset,canvas):super().__init__(glyphset);self.path=canvas.beginPath()
    def _moveTo(self,p):self.path.moveTo(*p)
    def _lineTo(self,p):self.path.lineTo(*p)
    def _curveToOne(self,p1,p2,p3):self.path.curveTo(*p1,*p2,*p3)
    def _closePath(self):self.path.close()

def spark(c,x,y,r,color):
    c.setStrokeColor(HexColor(color));c.setLineWidth(max(.6,r*.095))
    for a in [0,45,90,135]:
        d=math.radians(a);dx=math.cos(d)*r;dy=math.sin(d)*r;c.line(x-dx,y-dy,x+dx,y+dy)

def logo(c,x,top,width,color=INK,outline=False):
    c.saveState();s=width/LOGOW;c.translate(x,600-top-LOGOH*s);c.scale(s,s);c.setFillColor(HexColor(color))
    for g,px in positions:
        c.saveState();c.translate(px,0);pen=CanvasPen(glyphs,c);glyphs[g].draw(pen);c.setStrokeColor(HexColor(color));c.setLineWidth(5);c.drawPath(pen.path,fill=not outline,stroke=outline);c.restoreState()
    spark(c,LOGOW-35,660,52,color);c.restoreState()

def logo_svg(color):
    paths=[]
    for g,x in positions:
        p=SVGPathPen(glyphs);glyphs[g].draw(p);paths.append(f'<path transform="translate({x} 0)" d="{p.getCommands()}"/>')
    lines=[]
    for a in [0,45,90,135]:
        d=math.radians(a);dx=math.cos(d)*52;dy=math.sin(d)*52;cx=LOGOW-35;cy=660;lines.append(f'<path d="M{cx-dx},{cy-dy} L{cx+dx},{cy+dy}" fill="none" stroke="{color}" stroke-width="5"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 {LOGOW+35} {LOGOH}" role="img" aria-label="Romeiro"><g fill="{color}" transform="translate(0 {LOGOH}) scale(1 -1)">'+''.join(paths+lines)+'</g></svg>'

for name,color in [('grafite',INK),('marfim',PAPER),('lima',LIME)]:
    (BRAND/'logos'/f'romeiro-{name}.svg').write_text(logo_svg(color),encoding='utf8')
    p=TMP/f'logo-{name}.pdf';lc=canvas.Canvas(str(p),pagesize=(1500,500));lc.setPageSize((1500,500));lc.translate(0,-100);logo(lc,35,25,1430,color);lc.save()
    doc=pdfium.PdfDocument(str(p));img=doc[0].render(scale=1,fill_color=(0,0,0,0)).to_pil();img.save(BRAND/'logos'/f'romeiro-{name}.png');doc.close()

rp=SVGPathPen(glyphs);glyphs[cmap[ord('r')]].draw(rp)
icon=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="{LIME}"/><g transform="translate(20 77) scale(.10 -.10)" fill="{INK}"><path d="{rp.getCommands()}"/></g><path d="M69 25v14m-7-7h14m-12-5 10 10m0-10-10 10" fill="none" stroke="{INK}" stroke-width="1.6"/></svg>'
(BRAND/'logos/romeiro-icone.svg').write_text(icon,encoding='utf8');shutil.copy(BRAND/'logos/romeiro-icone.svg',ROOT/'favicon.svg')
tokens={'brand':'Romeiro','version':'1.0','colors':{'paper':PAPER,'ink':INK,'lime':LIME,'dark':DARK,'body':MUTED},'typography':{'primary':'Space Grotesk','editorial':'Cormorant Garamond Italic','signature':'Mrs Saint Delafield'},'spacing':[4,8,16,24,32,48,64,96],'radius':{'card':3,'button':999},'motion':{'microMs':220,'revealMs':700,'staggerMs':90,'easing':'cubic-bezier(.22,1,.36,1)','reducedMotion':True}}
(BRAND/'romeiro-tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2),encoding='utf8')
(BRAND/'romeiro-tokens.css').write_text(':root{--romeiro-paper:#edede5;--romeiro-ink:#242520;--romeiro-lime:#d7ff3f;--romeiro-dark:#20231f;--romeiro-body:#62665a;--romeiro-font:"Space Grotesk",sans-serif;--romeiro-editorial:"Cormorant Garamond",serif;--romeiro-radius:3px;--romeiro-motion:700ms cubic-bezier(.22,1,.36,1)}',encoding='utf8')

W,H=960,600
pdf=OUT/'Romeiro-Manual-da-Marca-v1.pdf';c=canvas.Canvas(str(pdf),pagesize=(W,H));c.setTitle('Romeiro | Manual da Marca 1.0');c.setAuthor('Vinicius Romeiro');c.setSubject('Identidade visual e verbal, diretrizes digitais e aplicações')
page=0;titles=[];bg=PAPER;fg=INK
def rect(x,top,w,h,color,stroke=None):
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color));c.rect(x,H-top-h,w,h,fill=1,stroke=bool(stroke))
def line(x,top,x2,top2,color=LINE,width=.7):
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x,H-top,x2,H-top2)
def text(value,x,top,size=14,font='Space-Regular',color=None):
    c.setFillColor(HexColor(color or fg));c.setFont(font,size);c.drawString(x,H-top-size*.8,value)
def para(value,x,top,width,size=14,color=None,font='Space-Regular',leading=None):
    leading=leading or size*1.55
    y=top
    for block in value.split('\n'):
        for row in simpleSplit(block,font,size,width):text(row,x,y,size,font,color);y+=leading
        y+=leading*.25
    return y
def heading(value,x=60,top=95,size=46,width=840,color=None,font='Space-Medium'):
    return para(value,x,top,width,size,color,font,size*1.08)
def label(value,x=60,top=40,color=None):text(value,x,top,9,'Space-Medium',color)
def begin(title,dark=False):
    global page,bg,fg
    if page:c.showPage()
    page+=1;titles.append(title);bg=DARK if dark else PAPER;fg=PAPER if dark else INK;rect(0,0,W,H,bg)
    label('ROMEIRO / MANUAL DA MARCA',color='#B5BAAA' if dark else MUTED);text(title.upper(),550,40,9,'Space-Medium','#B5BAAA' if dark else MUTED)
    line(60,556,900,556,'#444B3D' if dark else LINE);text('DESIGN APURADO. CÓDIGO À ALTURA.',60,574,8,'Space-Regular','#A3AD94' if dark else MUTED);text(f'V.1.0 / OUTUBRO 2026    {page:02d}',750,574,8,'Space-Regular','#A3AD94' if dark else MUTED)
def photo(file,x,top,w,h,fit='cover'):
    p=ASSETS/file;im=Image.open(p).convert('RGB');ratio=max(w/im.width,h/im.height) if fit=='cover' else min(w/im.width,h/im.height);rw,rh=im.width*ratio,im.height*ratio
    c.saveState();clip=c.beginPath();clip.rect(x,H-top-h,w,h);c.clipPath(clip,stroke=0,fill=0);c.drawImage(ImageReader(im),x+(w-rw)/2,H-top-h+(h-rh)/2,rw,rh);c.restoreState()
def smallcard(x,top,w,h,num,title,body):
    line(x,top,x+w,top);text(num,x,top+18,10,'Space-Medium',MUTED);para(title,x,top+48,w,24,INK,'Space-Medium',27);para(body,x,top+119,w,12,MUTED)

begin('Identidade visual e verbal',True)
label('VINICIUS ROMEIRO',60,105,LIME);logo(c,52,190,840,PAPER);text('O olhar cria.',62,413,31,'Space-Regular');text('O código transforma.',62,450,39,'Editorial',LIME);text('DIRETRIZES DE MARCA / EDIÇÃO 01',650,475,9,'Space-Medium')
begin('Como usar este manual')
heading('Uma marca.\nUm jeito de construir.',size=45)
para('Este manual organiza a identidade da Romeiro a partir da direção visual aprovada para o portfólio V2. Use como referência ao criar peças, interfaces e apresentações.',60,225,360,14,MUTED)
for i,(a,b,p) in enumerate([('01','Essência e linguagem','03-06'),('02','Sistema de assinatura','07-12'),('03','Cor, tipo e composição','13-19'),('04','Expressão e aplicações','20-28'),('05','Entrega e consistência','29-30')]):
    y=112+i*78;line(510,y+52,900,y+52);text(a,510,y,12,'Space-Medium',MUTED);text(b,550,y,17);text(p,852,y+3,10,'Space-Regular',MUTED)
begin('Essência')
label('A IDEIA QUE CONECTA TUDO.',60,100)
heading('O olhar cria.',60,153,71);heading('O código transforma.',60,240,78,font='Editorial')
para('A Romeiro une sensibilidade visual e capacidade de execução. Uma marca pessoal para quem desenha experiências, constrói software e conecta inteligência artificial ao produto.',60,385,570,17,MUTED)
spark(c,800,H-415,65,INK)
begin('Posicionamento')
heading('Design, tecnologia\ne negócio na mesma conversa.',size=45)
para('Para empresas e fundadores que precisam transformar uma ideia em marca, experiência e produto digital, Romeiro oferece visão integrada e execução cuidadosa.',60,220,795,17,MUTED)
for x,n,t,b in [(60,'01','Olhar experiente','Mais de 10 anos de design, incluindo trabalhos para Bosch e Dachser.'),(355,'02','Execução integrada','Design de produto, desenvolvimento full-stack e soluções com IA.'),(650,'03','Visão de fundador','Cofundador da InovaSys e da Make Solutions Happen. Produto e negócio conectados.')]:smallcard(x,330,250,180,n,t,b)
begin('Personalidade',True)
heading('Precisão com\npersonalidade.',size=53)
for i,(title,body) in enumerate([('CURIOSA','Investiga, conecta referências e questiona o que pode melhorar.'),('CRITERIOSA','Cada escolha visual e técnica tem uma razão para existir.'),('DIRETA','Comunica com clareza. Faz o complexo ficar compreensível.'),('AUTORAL','Tem um ponto de vista, sem deixar de servir ao projeto.')]):
    x=60+(i%2)*445;y=290+(i//2)*120;line(x,y,x+395,y,'#4D5646');text(title,x,y+19,12,'Space-Medium',LIME);para(body,x,y+46,380,13,'#B9C1AF')
begin('Voz e linguagem')
heading('Clareza também\né design.',size=49)
para('Fale em primeira pessoa na marca pessoal e em primeira pessoa do plural quando o projeto foi construído em equipe. Prefira ações concretas a superlativos.',60,217,820,15,MUTED)
for x,title,examples in [(60,'COMO SOA',['O olhar cria. O código transforma.','Uma ideia com forma e função.','Vamos construir o próximo passo.']),(500,'O QUE EVITAR',['Promessas de resultados sem evidência.','Jargão técnico sem contexto para o leitor.','Adjetivos genéricos no lugar de entregas.'])]:
    line(x,320,x+400,320);text(title,x,338,11,'Space-Medium');
    for i,item in enumerate(examples):para(item,x,380+i*45,390,14,MUTED)
begin('Assinatura principal')
heading('Simples para reconhecer.\nForte para permanecer.',size=44)
logo(c,145,270,670,INK)
para('A assinatura principal combina o nome em caixa-baixa com um pequeno asterisco de oito raios. O ritmo compacto e o traço sem serifa preservam a personalidade do logo aprovado no site.',150,460,660,13,MUTED)
begin('Construção e elementos')
logo(c,90,135,775,INK)
line(100,370,800,370);line(100,370,100,402);line(800,370,800,402)
text('01 / LETTERING',60,428,11,'Space-Medium');para('Base em Space Grotesk Bold, com espaçamento compacto fixado em contornos. Use os arquivos vetoriais; não redigite o logotipo.',60,455,420,13,MUTED)
text('02 / ASTERISCO',560,428,11,'Space-Medium');para('Sinal de conexão entre olhar e construção. É um elemento gráfico da marca, sem indicação de registro marcário.',560,455,340,13,MUTED)
begin('Área de proteção')
heading('Espaço é parte\nda assinatura.',size=43)
logo(c,240,294,470,INK)
c.setStrokeColor(HexColor(MUTED));c.setDash(4,4);c.rect(190,H-245-205,580,205,fill=0,stroke=1);c.setDash()
line(190,265,240,265,MUTED);text('0,5x',199,243,11,'Space-Medium');text('x = altura do corpo da letra o',270,481,12,'Space-Regular',MUTED)
para('Reserve no mínimo 0,5x em cada lado. Na composição, amplie essa margem sempre que possível. Nenhum texto, foto ou borda deve ocupar essa área.',560,110,320,14,MUTED)
begin('Versões cromáticas')
heading('Três versões.\nA mesma identidade.',size=43)
for x,fill,col,caption in [(60,PAPER,INK,'GRAFITE / FUNDO MARFIM'),(350,INK,PAPER,'MARFIM / FUNDO GRAFITE'),(640,INK,LIME,'LIMA / USO DE DESTAQUE')]:
    rect(x,280,260,150,fill,LINE if fill==PAPER else None);logo(c,x+22,324,216,col);text(caption,x,450,9,'Space-Medium',MUTED)
para('A versão grafite é a principal. A negativa mantém presença em fundos escuros. A versão lima é um acento, usada com intenção em aberturas e assinaturas especiais.',60,491,820,12,MUTED)
begin('Redução e assinatura compacta')
heading('Reconhecível\nem qualquer escala.',size=43)
logo(c,65,305,240,INK);text('PRINCIPAL',65,407,11,'Space-Medium');para('Largura mínima digital: 120 px.\nLargura mínima impressa: 30 mm.',65,438,345,14,MUTED)
rect(555,255,150,150,LIME);text('r',585,260,128,'Space-Bold');spark(c,674,H-288,11,INK)
text('ÍCONE COMPACTO',555,433,11,'Space-Medium');para('Mínimo digital: 24 px.\nEm 16 px, simplifique o asterisco.',555,460,340,14,MUTED)
begin('Usos incorretos')
heading('A consistência\nprotege o reconhecimento.',size=42)
for i,(title,kind) in enumerate([('Não esticar','stretch'),('Não inclinar','rotate'),('Não alterar as cores','color'),('Não usar contorno','outline'),('Não aplicar sombra','shadow'),('Não reduzir o contraste','contrast')]):
    x=60+(i%3)*290;y=260+(i//3)*133;rect(x,y,260,95,'#E0E2D7');c.saveState()
    if kind=='stretch':c.translate(x,0);c.scale(1.35,1);logo(c,15,y+29,165,INK)
    elif kind=='rotate':c.translate(x+130,H-y-47);c.rotate(9);c.translate(-(x+130),-(H-y-47));logo(c,x+25,y+20,210,INK)
    elif kind=='color':logo(c,x+20,y+28,220,'#7B58BA')
    elif kind=='outline':logo(c,x+20,y+28,220,INK,outline=True)
    elif kind=='shadow':logo(c,x+24,y+32,220,'#A3A992');logo(c,x+20,y+28,220,INK)
    else:logo(c,x+20,y+28,220,'#B9BEAE')
    c.restoreState();text(title,x,y+105,11,'Space-Medium',MUTED)
begin('Paleta cromática')
heading('Neutros que respiram.\nUm acento que acende.',size=45)
colors=[('MARFIM',PAPER,'237 / 237 / 229','0 / 0 / 3 / 7'),('GRAFITE',INK,'36 / 37 / 32','3 / 0 / 14 / 85'),('LIMA',LIME,'215 / 255 / 63','16 / 0 / 75 / 0'),('MUSGO',MUTED,'98 / 102 / 90','4 / 0 / 12 / 60')]
for i,(name,co,rgb,cmyk) in enumerate(colors):
    x=60+i*215;rect(x,263,195,130,co,LINE if i==0 else None);text(name,x,413,13,'Space-Medium');text(co,x,440,11);text('RGB '+rgb,x,462,9,'Space-Regular',MUTED);text('CMYK* '+cmyk,x,483,9,'Space-Regular',MUTED)
text('*Conversões iniciais aproximadas. Ajustar ao perfil de impressão e validar em prova física.',60,525,9,'Space-Regular',MUTED)
begin('Proporção e contraste visual')
heading('O verde marca\no que merece atenção.',size=47)
for x,w,co,txt in [(60,546,PAPER,'65% / MARFIM'),(606,210,INK,'25% / GRAFITE'),(816,84,LIME,'10%')]:rect(x,270,w,120,co,LINE if co==PAPER else None);text(txt,x+14,317,10,'Space-Medium',PAPER if co==INK else INK)
para('As proporções são um ponto de partida. Em áreas de portfólio, o grafite pode ser dominante para dar espaço aos trabalhos. O lima fica reservado a ações, destaques e momentos de assinatura.',60,430,410,14,MUTED)
para('Evite preencher todas as peças com verde. O contraste entre pausa e energia dá ritmo à marca. As cores dos projetos continuam pertencendo a cada projeto.',525,430,375,14,MUTED)
def luminance(h):
    vals=[int(h[i:i+2],16)/255 for i in (1,3,5)];vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals];return sum(a*b for a,b in zip(vals,[.2126,.7152,.0722]))
def contrast(a,b):
    ls=sorted([luminance(a),luminance(b)]);return (ls[1]+.05)/(ls[0]+.05)
begin('Legibilidade digital')
heading('Contraste é cuidado.',size=53)
para('As combinações abaixo foram calculadas em sRGB. Para texto comum, adote pelo menos 4,5:1; use também tamanho confortável, foco visível e informação além da cor.',60,179,820,14,MUTED)
for i,(fc,bc,name) in enumerate([(INK,PAPER,'Grafite sobre marfim'),(PAPER,INK,'Marfim sobre grafite'),(INK,LIME,'Grafite sobre lima'),(MUTED,PAPER,'Musgo sobre marfim')]):
    y=270+i*60;rect(60,y,80,44,bc,LINE);text('Aa',80,y+8,25,'Space-Medium',fc);text(name,170,y+11,16);text(f'{contrast(fc,bc):.2f}:1',695,y+11,17,'Space-Medium');text('APROVADO',800,y+15,9,'Space-Medium',MUTED)
begin('Sistema tipográfico')
text('Space Grotesk',60,110,65,'Space-Medium');text('A voz principal.',63,188,14,'Space-Regular',MUTED)
text('Cormorant Garamond',60,259,58,'Editorial');text('O contraste editorial.',63,328,14,'Space-Regular',MUTED)
text('Vinicius Romeiro',60,388,65,'Signature');text('Mrs Saint Delafield / assinatura pessoal.',63,475,13,'Space-Regular',MUTED)
para('400 / textos\n500 / títulos\n700 / marca e ênfase',710,130,190,14,MUTED)
para('Itálico apenas em títulos curtos. Não usar em parágrafos ou controles.',710,277,190,13,MUTED)
para('Uso pontual, com contraste. Não substitui o logo Romeiro.',710,427,190,13,MUTED)
begin('Hierarquia tipográfica')
heading('Ritmo antes\nde tamanho.',size=44)
for y,title,size,desc in [(278,'Título principal',48,'88-138 px / entrelinha 0,94-1,02 / peso 500'),(366,'Título de seção',31,'48-80 px / entrelinha 1,02 / peso 400-500'),(427,'Texto de leitura',19,'16-18 px / entrelinha 1,5-1,8 / peso 400'),(488,'RÓTULOS E METADADOS',10,'10-12 px / caixa-alta / tracking +0,10em')]:
    text(title,60,y,size,'Space-Medium');text(desc,510,y+10,10,'Space-Regular',MUTED)
begin('Grid e espaçamento')
heading('Uma estrutura.\nMuitas composições.',size=43)
for i in range(12):rect(60+i*70,260,54,165,'#DDE1D1')
for y in [260,300,340,380,425]:line(60,y,884,y,'#BFC5B2')
para('DESKTOP\n12 colunas. Margens a partir de 64 px. Gaps de 24-32 px. A assimetria nasce dentro do grid.',60,456,250,12,MUTED)
para('MOBILE\n4 colunas. Margens de 22-24 px. Imagens em uma coluna e títulos com quebra natural.',355,456,250,12,MUTED)
para('ESCALA\n4 / 8 / 16 / 24 / 32 / 48 / 64 / 96. Relações claras entre detalhes e áreas de respiro.',650,456,250,12,MUTED)
begin('Elementos gráficos',True)
heading('Sinais, não enfeites.',size=52)
spark(c,158,H-330,60,LIME);c.setStrokeColor(HexColor(PAPER));c.setLineWidth(2);c.circle(455,H-330,61,fill=0,stroke=1);line(425,360,485,300,PAPER,2);line(455,300,485,300,PAPER,2);line(485,300,485,330,PAPER,2)
for y in [283,330,377]:line(685,y,875,y,'#AAB49A',.5)
for x,title,body in [(60,'ASTERISCO','Conexão, possibilidades e autoria. Pode girar de forma discreta.'),(360,'SETAS E CÍRCULOS','Indicam ação e continuidade. Linhas leves, sem excesso de ícones.'),(660,'FIOS E MARCADORES','Organizam, separam e criam ritmo. Bordas sutis, cantos quase retos.')]:text(title,x,439,11,'Space-Medium',LIME);para(body,x,465,240,12,'#B7C0AA')
begin('Direção fotográfica')
photo(Path('vinicius-about.png'),60,108,320,415)
heading('Presença humana.\nTratamento contido.',430,112,42,470)
para('Retratos em preto e branco, contraste natural e fundo limpo. Enquadramentos próximos comunicam autoria e presença. A assinatura em lima pode acompanhar o retrato quando houver contraste.',430,254,450,15,MUTED)
para('Nos projetos, preserve as cores das marcas. Não aplique filtros que alterem a identidade do cliente. Imagens geradas são peças autorais; não devem ser usadas como prova documental de eventos.',430,398,450,13,MUTED)
begin('Direção dos cases')
heading('O projeto é\no protagonista.',size=45)
photo(Path('cases/stival.webp'),60,257,525,246,'contain')
para('01 / CONTEXTO\nExplique o problema e sua participação.\n02 / PROCESSO\nMostre estudos, decisões e sistemas.\n03 / ENTREGA\nRevele as interfaces e aplicações.\n04 / EVIDÊNCIA\nResultados mensurados só com fonte.',625,251,260,13,MUTED)
begin('Vídeo e movimento',True)
heading('Movimento com\nintenção.',size=52)
para('O vídeo segue a mesma linguagem do site: fundos planos, tipografia editorial, cortes suaves e imagens grandes. Sem molduras luminosas, painéis genéricos ou efeitos que disputem atenção com o trabalho.',60,241,790,17,'#BCC4B0')
for i,(big,small) in enumerate([('200-300 ms','INTERAÇÕES'),('600-750 ms','ENTRADAS'),('6 segundos','LOOP DE CASE')]):
    x=60+i*285;line(x,391,x+240,391,'#515A46');text(big,x,417,30,'Space-Regular',LIME);text(small,x,465,9,'Space-Medium')
text('Respeite movimento reduzido. Vídeos sem áudio automático e com controles nas páginas de case.',60,520,10,'Space-Regular','#B6C0A7')
begin('Aplicação no website')
rect(60,112,840,382,PAPER,LINE);logo(c,85,126,117,INK);text('TRABALHOS     SOBRE     CONTATO',640,143,9,'Space-Regular',MUTED);line(80,170,875,170)
text('O olhar cria.',90,211,45,'Space-Medium');text('O código',90,261,45,'Space-Medium');text('transforma.',90,307,52,'Editorial');para('Design, desenvolvimento e IA,\npensados juntos desde o início.',90,396,330,13,MUTED)
photo(Path('vinicius-about.png'),605,195,248,264);spark(c,852,H-209,21,INK);rect(605,440,248,28,INK);text('Vinicius Romeiro',646,438,27,'Signature',LIME)
text('COMPOSIÇÃO DE REFERÊNCIA / DESKTOP',60,518,10,'Space-Medium',MUTED)
begin('Cartão e papelaria')
heading('Presença fora da tela.',size=49)
rect(60,260,400,230,INK);logo(c,92,309,325,PAPER);label('DESIGN APURADO. CÓDIGO À ALTURA.',94,445,LIME)
rect(500,260,400,230,LIME);text('Vinicius Romeiro',530,291,24,'Space-Medium');text('DESIGN / DESENVOLVIMENTO / IA',530,333,9,'Space-Medium');line(530,384,870,384,INK);text('Contato via InovaSys',530,413,13);text('+55 19 96000-3434',530,442,13)
text('Formato sugerido: 90 × 50 mm. Margem de segurança: 4 mm. Sangria: 3 mm. Validar prova e acabamento.',60,518,10,'Space-Regular',MUTED)
begin('Sistema para redes sociais')
heading('Conteúdo com assinatura.',size=47)
for i in range(3):
    x=60+i*288;rect(x,220,260,304,[INK,LIME,PAPER][i],LINE if i==2 else None)
    if i==0:logo(c,x+20,242,120,PAPER);text('Uma ideia.',x+20,313,29,'Space-Medium',PAPER);text('Um universo.',x+20,352,32,'Editorial',LIME);text('PROJETO / STIVAL',x+20,488,9,'Space-Medium',PAPER)
    if i==1:label('PROCESSO CRIATIVO',x+20,246,INK);text('O cuidado',x+20,309,30,'Space-Medium',INK);text('mora no',x+20,348,30,'Space-Medium',INK);text('detalhe.',x+20,383,42,'Editorial',INK);logo(c,x+20,478,114,INK)
    if i==2:photo(Path('vinicius-about.png'),x+12,232,236,202);text('Por trás do projeto.',x+18,454,21,'Editorial',INK);logo(c,x+18,488,110,INK)
begin('Apresentações e propostas')
rect(60,110,840,410,INK);logo(c,96,143,170,PAPER);label('ROMEIRO / APRESENTAÇÃO DE PROJETO',96,221,LIME)
text('Ideias fortes.',96,283,57,'Space-Medium',PAPER);text('Produtos memoráveis.',96,350,60,'Editorial',LIME);text('ESTRATÉGIA / DESIGN / TECNOLOGIA',98,477,10,'Space-Medium',PAPER)
spark(c,800,H-214,47,LIME)
begin('Assinatura e comunicação')
heading('Autoria, sem ruído.',size=49)
text('Vinicius Romeiro',60,222,25,'Space-Medium');text('Design, desenvolvimento & IA',60,263,14,'Space-Regular',MUTED);line(60,307,470,307);logo(c,60,339,190,INK);text('InovaSys / WhatsApp: +55 19 96000-3434',60,425,12,'Space-Regular',MUTED)
para('E-MAIL E DOCUMENTOS\nAssinatura compacta, links claros e texto selecionável. Não transformar toda a assinatura em imagem.',575,222,310,14,MUTED)
para('ASSINATURA PESSOAL\nUse a caligrafia como elemento editorial. Em fotografias escuras, prefira lima ou marfim. Reserve o logo para identificar a marca.',575,366,310,14,MUTED)
begin('Ícones e pequenas superfícies')
heading('Poucos elementos.\nReconhecimento rápido.',size=45)
for i,(sz,x) in enumerate([(170,70),(100,310),(60,480),(32,610)]):
    y=310;rect(x,y,sz,sz,LIME);text('r',x+sz*.18,y+sz*.03,sz*.95,'Space-Bold',INK);spark(c,x+sz*.72,H-y-sz*.27,sz*.08,INK);text(f'{[128,64,32,24][i]} px',x,y+sz+15,10,'Space-Regular',MUTED)
para('O ícone usa a inicial e o asterisco. Não substitui a assinatura principal em capas, propostas e materiais institucionais. Use em favicon, avatar compacto ou indicação de autoria.',720,310,180,13,MUTED)
begin('Kit e controle de qualidade')
heading('Pronto para continuar.',size=49)
for x,title,body in [(60,'ARQUIVOS','SVG / vetores em contornos\nPNG / versões transparentes\nPDF / manual completo\nTTF / fontes e licenças\nCSS + JSON / tokens\nSVG + HTML / aplicações editáveis'),(510,'ANTES DE PUBLICAR','Conferir contraste e legibilidade.\nRespeitar a área de proteção.\nEvitar deformar a assinatura.\nPreservar as cores dos projetos.\nTestar mobile, teclado e movimento reduzido.\nConfirmar links e informações de contato.')]:
    text(title,x,239,11,'Space-Medium');para(body,x,280,370,15,MUTED,leading=33)
begin('Construir com intenção',True)
label('A IDENTIDADE É O COMEÇO.',60,112,LIME);heading('O próximo projeto\nainda está por vir.',60,175,62,780,PAPER,'Editorial');logo(c,58,383,535,PAPER);spark(c,817,H-421,62,LIME)
c.save()

# Editable application assets use vector outlines for the wordmark.
inner=logo_svg(INK).split('>',1)[1].rsplit('</svg>',1)[0]
def svg_template(name,w,h,body):
    (BRAND/'templates'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>@font-face{{font-family:Space;src:url(../fonts/Space-Medium.ttf)}}text{{font-family:Space,Arial,sans-serif}}</style>{body}</svg>',encoding='utf8')
svg_template('post-editorial-1080x1350.svg',1080,1350,f'<rect width="1080" height="1350" fill="{LIME}"/><text x="80" y="140" font-size="25" fill="{INK}">PROCESSO / DESIGN / TECNOLOGIA</text><text x="80" y="500" font-size="105" letter-spacing="-5" fill="{INK}"><tspan x="80">O cuidado</tspan><tspan x="80" dy="115">mora no</tspan><tspan x="80" dy="115">detalhe.</tspan></text><svg x="80" y="1140" width="360" height="100" viewBox="0 0 {LOGOW+35} {LOGOH}">{inner}</svg>')
svg_template('capa-apresentacao-1920x1080.svg',1920,1080,f'<rect width="1920" height="1080" fill="{PAPER}"/><svg x="110" y="90" width="320" height="100" viewBox="0 0 {LOGOW+35} {LOGOH}">{inner}</svg><text x="110" y="460" font-size="112" fill="{INK}" letter-spacing="-6">Ideias fortes.</text><text x="110" y="605" font-size="112" fill="{INK}" letter-spacing="-6">Produtos memoráveis.</text><rect x="110" y="860" width="1700" height="2" fill="{INK}"/><text x="110" y="930" font-size="24" fill="{INK}">ROMEIRO / APRESENTAÇÃO DE PROJETO</text>')
svg_template('cartao-frente-90x50mm.svg',900,500,f'<rect width="900" height="500" fill="{LIME}"/><svg x="80" y="150" width="740" height="200" viewBox="0 0 {LOGOW+35} {LOGOH}">{inner}</svg>')
svg_template('cartao-verso-90x50mm.svg',900,500,f'<rect width="900" height="500" fill="{PAPER}"/><text x="65" y="125" font-size="48" fill="{INK}">Vinicius Romeiro</text><text x="65" y="188" font-size="22" fill="{INK}">DESIGN / DESENVOLVIMENTO / IA</text><path d="M65 290H835" stroke="{INK}"/><text x="65" y="360" font-size="29" fill="{INK}">Contato via InovaSys</text><text x="65" y="410" font-size="29" fill="{INK}">+55 19 96000-3434</text>')
(BRAND/'templates/assinatura-email.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Assinatura Romeiro</title><body><table cellpadding="0" cellspacing="0" style="font-family:Arial,sans-serif;color:#242520"><tr><td style="font-size:20px;font-weight:bold;padding-bottom:8px">Vinicius Romeiro</td></tr><tr><td style="font-size:13px;padding-bottom:15px">Design, desenvolvimento &amp; IA</td></tr><tr><td style="border-top:1px solid #c9ccbe;padding-top:15px;font-size:24px;font-weight:bold;letter-spacing:-1px">romeiro</td></tr><tr><td style="padding-top:10px;font-size:12px"><a href="https://wa.me/5519960003434" style="color:#242520">Conversar via InovaSys: +55 19 96000-3434</a></td></tr></table></body></html>',encoding='utf8')

reader=PdfReader(str(pdf));assert len(reader.pages)==30,len(reader.pages)
doc=pdfium.PdfDocument(str(pdf));thumbs=[]
for i in range(len(doc)):
    im=doc[i].render(scale=1.2).to_pil().convert('RGB');im.save(BRAND/'pages'/f'{i+1:02d}.jpg',quality=88)
    thumb=im.copy();thumb.thumbnail((384,240));thumbs.append(thumb)
sheet=Image.new('RGB',(1920,6*268),'#b6b8ae');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%5)*384;y=(i//5)*268;sheet.paste(im,(x,y));draw.text((x+10,y+245),f'{i+1:02d} {titles[i]}',fill='#242520')
sheet.save(TMP/'contact-sheet.jpg',quality=90)
(BRAND/'pages.json').write_text(json.dumps([{'page':i+1,'title':t,'image':f'pages/{i+1:02d}.jpg'} for i,t in enumerate(titles)],ensure_ascii=False,indent=2),encoding='utf8')
(BRAND/'LEIA-ME.txt').write_text('ROMEIRO / KIT DE MARCA 1.0\n\nLogo principal: logos/romeiro-grafite.svg\nVetores em contornos, sem dependência de fontes.\nVersões: grafite, marfim e lima. PNG com fundo transparente.\nÍcone compacto: romeiro-icone.svg.\nFontes e licenças em fonts/.\nTemplates editáveis em templates/. Textos das aplicações usam Space Grotesk.\nTokens digitais em romeiro-tokens.css e romeiro-tokens.json.\nO manual completo está na pasta Manual/.\n\nOs cartões são bases de composição em proporção 90x50mm; a arte final para gráfica deve ser preparada com 3mm de sangria e perfil CMYK da produção. Os SVGs possuem dimensões proporcionais em pixels.\n\nContato utilizado: WhatsApp público da InovaSys.\nVersão 1.0 / Outubro 2026.\n',encoding='utf8')
zip_path=BRAND/'Romeiro-Kit-da-Marca-v1.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for folder in ['logos','fonts','templates']:
        for f in (BRAND/folder).rglob('*'):
            if f.is_file():z.write(f,f.relative_to(BRAND))
    for f in ['LEIA-ME.txt','romeiro-tokens.css','romeiro-tokens.json']:z.write(BRAND/f,f)
    z.write(pdf,'Manual/'+pdf.name)
(TMP/'verification.json').write_text(json.dumps({'pages':len(reader.pages),'titles':titles,'characters':[len(p.extract_text()) for p in reader.pages],'pdfBytes':pdf.stat().st_size,'zipBytes':zip_path.stat().st_size,'contrast':{f'{a}/{b}':round(contrast(a,b),2) for a,b in [(INK,PAPER),(INK,LIME),(MUTED,PAPER)]}},ensure_ascii=False,indent=2),encoding='utf8')
print(f'Created {pdf} ({len(reader.pages)} pages) and {zip_path}')
