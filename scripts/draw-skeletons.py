from pathlib import Path
import math
OUT=Path(__file__).resolve().parents[1]/'skeletons'
OUT.mkdir(exist_ok=True)
INK='#76543d';BONE='#fff4dc'
class Drawing:
 def __init__(self):self.parts=[]
 def path(self,d,fill=BONE,sw=4):self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
 def bone(self,a,b,w=15):
  x,y=a;xx,yy=b;dx=xx-x;dy=yy-y;l=math.hypot(dx,dy);ux=dx/l;uy=dy/l
  for stroke,width in [(INK,w+7),(BONE,w)]:self.parts.append(f'<path d="M{x+ux*5:.1f},{y+uy*5:.1f} L{xx-ux*5:.1f},{yy-uy*5:.1f}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"/>')
 def joint(self,x,y,r=10):self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BONE}" stroke="{INK}" stroke-width="4"/>')
 def chain(self,pts,w=14,spines=False):
  for i,(a,b) in enumerate(zip(pts,pts[1:])):
   self.bone(a,b,max(6,w-i*.3));self.joint(*a,max(5,w*.48-i*.13))
   if spines and i%2==0:self.path(f'M{a[0]-4},{a[1]-6} l4,-19 l8,19',sw=3)
 def limb(self,pts,w=18,toes=3,far=False):
  self.chain(pts,w)
  x,y=pts[-1]
  for k in range(toes):self.bone((x,y),(x-25-k*7,y+8+k*5),6)
 def ribs(self,cx,cy,n=9,rx=135,ry=115):
  for i in range(n):
   x=cx-rx+i*rx*2/(n-1);t=(i/(n-1))*math.pi;h=35+math.sin(t)*ry
   curve=f'M{x:.1f},{cy:.1f} C{x+28:.1f},{cy+h*.35:.1f} {x+29:.1f},{cy+h*.88:.1f} {x+9:.1f},{cy+h:.1f} Q{x-2:.1f},{cy+h+4:.1f} {x-8:.1f},{cy+h-6:.1f}'
   for stroke,width in [(INK,10),(BONE,4)]:self.parts.append(f'<path d="{curve}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"/>')
 def pelvis(self,x,y):self.path(f'M{x-40},{y-12} Q{x},{y-36} {x+40},{y-8} L{x+15},{y+55} L{x-5},{y+62} L{x-25},{y+16} Z');self.joint(x,y+8,16)
 def eye(self,x,y,rx=14,ry=18):self.parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK}"/>')
 def save(self,id,name):
  s='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc"><title id="title">'+name+'簡化骨架示意</title><desc id="desc">透明背景的原創教學示意，突出主要骨架與辨識特徵，非逐骨復原或化石照片。</desc>'+''.join(self.parts)+'</svg>'
  (OUT/(id+'.svg')).write_text(s)

def quad(id,name,kind):
 d=Drawing();back=[(340,245),(385,221),(435,205),(490,196),(545,194),(600,198),(650,208),(702,219),(750,232)]
 # Far limbs behind the rib cage.
 for x in [423,688]:d.limb([(x,257),(x+20,333),(x+3,414),(x-8,435)],15)
 d.ribs(548,215,9,132,100);d.chain(back,18,True);d.pelvis(695,247)
 d.chain([(750,232),(805,241),(858,250),(910,262),(961,274),(1010,286),(1060,292),(1115,290)],16)
 for x in [400,660]:d.limb([(x,263),(x-16,338),(x+6,422),(x-10,449)],24)
 if kind=='tri':
  d.path('M360,220 Q310,141 269,134 Q230,147 235,203 Q218,224 185,243 L123,271 L119,292 L181,311 L259,303 L289,279 L345,279 Z')
  d.path('M275,157 Q250,114 220,99 L251,194 Z');d.path('M239,194 L199,135 L222,217 Z');d.path('M162,251 L135,216 L148,269 Z');d.eye(246,234);d.eye(190,277,11,8);d.path('M133,291 Q208,322 267,289',fill='none');d.path('M272,157 L300,177 L317,209 L314,237',fill='none',sw=5)
 elif kind=='stego':
  # Two staggered rows of dermal plates; tail carries two pairs of spikes.
  for x,y,h in [(353,244,48),(405,216,74),(462,198,100),(525,193,111),(593,198,106),(658,210,90),(722,227,66),(786,239,45)]:d.path(f'M{x-17},{y-7} L{x-29},{y-h*.62} L{x-3},{y-h} L{x+24},{y-h*.54} L{x+16},{y-5} Z',sw=4)
  d.chain([(340,245),(302,272),(267,289)],14);d.path('M268,278 Q225,260 190,283 L159,300 L169,320 L223,323 L267,306 Z');d.eye(231,289,9,10);d.path('M169,311 L242,310',fill='none')
  for x,y in [(1010,286),(1058,292)]:d.path(f'M{x-6},{y} L{x+12},{y-64} L{x+5},{y+2} Z');d.path(f'M{x-5},{y+2} L{x+16},{y+45} L{x+7},{y+1} Z')
 elif kind=='anky':
  for row,yy in enumerate([192,222]):
   for i in range(8):x=373+i*49+row*12;d.path(f'M{x-12},{yy} Q{x},{yy-24} {x+17},{yy} L{x+5},{yy+13} Z',sw=3)
  for x in [365,425,490,555,620,685,741]:d.path(f'M{x-12},252 L{x-21},280 L{x+16},259 Z',sw=3)
  d.path('M348,244 L309,226 L265,241 L241,259 L205,266 L198,287 L246,307 L308,297 L346,278 Z');d.eye(280,257);d.path('M246,242 L233,220 L269,240 Z');d.path('M202,287 L279,287',fill='none')
  d.path('M1046,279 Q1071,245 1109,264 Q1155,259 1164,288 Q1154,324 1116,317 Q1074,329 1046,302 Z')
 d.save(id,name)
quad('triceratops','三角龍','tri');quad('stegosaurus','劍龍','stego');quad('ankylosaurus','甲龍','anky')

def sauropod(id,name,tall):
 d=Drawing();cx=640 if tall else 530
 for x in [cx-95,cx+122]:d.limb([(x,272),(x+10,343),(x-3,426),(x-6,449)],19)
 d.ribs(cx,242,10,140,108);d.chain([(cx-151,215 if tall else 245),(cx-100,202 if tall else 222),(cx-50,202 if tall else 210),(cx,210),(cx+50,217),(cx+105,228),(cx+151,245)],20,True);d.pelvis(cx+103,265)
 if tall:
  neck=[(cx-151,215),(466,183),(443,144),(428,104),(417,68),(408,41),(378,38)];tail=[(cx+151,245),(846,253),(900,267),(954,284),(1003,308),(1051,327),(1100,336),(1148,334)]
  d.path('M384,27 L347,19 L304,24 L286,42 L295,62 L344,67 L384,54 Z');d.eye(350,40,13,14);d.path('M295,53 L349,54',fill='none')
 else:
  neck=[(cx-151,245),(338,229),(296,209),(255,187),(216,169),(175,161),(135,161)];tail=[(cx+151,245),(737,245),(794,250),(850,260),(902,271),(953,283),(1002,294),(1051,303),(1100,311),(1159,313)]
  d.path('M139,149 L103,143 L68,150 L51,164 L61,182 L106,185 L139,174 Z');d.eye(112,158,10,12);d.path('M61,174 L110,176',fill='none')
 d.chain(neck,19,True);d.chain(tail,17,True)
 for x in [cx-122,cx+93]:d.limb([(x,230 if tall and x<cx else 272),(x-7,354),(x+1,442),(x-7,466)],27)
 d.save(id,name)
sauropod('brachiosaurus','腕龍',True);sauropod('diplodocus','梁龍',False)

def biped(id,name,kind):
 d=Drawing();para=kind=='para';velo=kind=='velo';headx=263 if para else 240;heady=143 if para else 170
 # Far leg, a rib cage and a long balancing tail.
 d.limb([(644,261),(710,335),(677,402),(705,439)],22)
 d.ribs(533,210,9,111,112);d.chain([(365,228),(405,204),(455,190),(507,188),(557,194),(607,210),(656,232),(706,249)],18,True)
 d.chain([(706,249),(760,251),(816,244),(871,231),(924,214),(975,197),(1024,181),(1076,170),(1131,163)],17,True);d.pelvis(652,253)
 d.limb([(652,265),(600,338),(654,398),(628,452)],30,2 if velo else 3)
 if para:
  d.chain([(365,228),(329,202),(305,169),(280,155)],17)
  d.path('M282,129 Q306,105 359,90 Q398,80 421,85 Q436,92 418,103 L322,143 L300,170 L260,188 L214,195 L180,187 L170,172 L195,154 L231,143 Z');d.eye(266,152,14,17);d.eye(196,174,8,7);d.path('M178,183 L238,182',fill='none')
  d.limb([(417,228),(399,301),(363,368),(356,418)],16)
 elif velo:
  d.chain([(365,228),(329,210),(302,181)],15)
  d.path('M308,158 L279,140 L244,141 L211,154 L161,169 L148,187 L201,197 L250,190 L297,185 Z');d.eye(273,161,15,17);d.eye(181,177,8,6);d.path('M155,186 L247,182',fill='none')
  for j in range(5):x=175+j*15;d.path(f'M{x},189 l4,10 l5,-11 Z',sw=2)
  d.limb([(419,229),(390,273),(345,284)],15,0);d.limb([(345,284),(306,290)],10,0)
  for k in range(3):d.chain([(310,287+k*3),(280-k*4,297+k*10),(265-k*4,308+k*10)],7)
  d.path('M625,448 Q601,403 578,409 Q600,418 609,455 Z');d.path('M600,453 L568,464 L613,465 Z')
 else:
  d.chain([(365,228),(338,191),(310,163)],20)
  d.path('M324,128 Q292,99 242,101 L185,121 L129,135 L103,160 L112,200 L178,219 L254,215 L314,183 Z');d.eye(277,143,22,26);d.eye(209,155,30,22);d.eye(133,163,10,8);d.path('M119,199 L230,188 L288,180',fill='none',sw=6)
  for j in range(9):x=133+j*16;d.path(f'M{x},194 l5,15 l5,-17 Z',sw=2)
  d.limb([(419,230),(401,257),(374,258)],13,0)
  for k in range(2):d.chain([(374,258),(353,266+k*13),(345,279+k*13)],7)
 d.save(id,name)
biped('parasaurolophus','副櫛龍','para');biped('velociraptor','迅猛龍','velo');biped('tyrannosaurus','暴龍','rex')
