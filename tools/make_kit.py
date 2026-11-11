"""Builds a design kit zip (assets + Arabic guide image) for one stage: python3 make_kit.py 2 'بغداد زمن الوالي'"""
import sys, os, shutil, subprocess
from PIL import Image
n, name = sys.argv[1], sys.argv[2]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); A = os.path.join(root, 'app', 'assets')
kit = f'IBRA-World-Tour-Stage{n}-Design-Kit'; out = os.path.join(root, 'dist', 'kit'); K = os.path.join(out, kit)
shutil.rmtree(K, ignore_errors=True); os.makedirs(os.path.join(K, 'hero'))
shutil.copytree(os.path.join(A, f'stage{n}'), os.path.join(K, f'stage{n}')); shutil.copy(os.path.join(A, 'hero', f'stage{n}.png'), os.path.join(K, 'hero'))
S = f'stage{n}/'
rows = [([S+'ground_top.png'], 'سطح الأرضية (الوجه اللي يمشي عليه البطل). لازم يتكرر يمين ويسار بدون ما يبين الفاصل'),
 ([S+'ground_fill.png'], 'حشوة الأرضية جوه السطح. تتكرر بكل الاتجاهات'),
 ([S+'brick.png'], 'الطابوقة اللي تنكسر بالراس'),
 ([S+'box.png', S+'box_used.png'], 'صندوق الجائزة، وشكله بعد ما ينضرب'),
 ([S+'block.png'], 'الحجر الصلب مال الدرج والأعمدة'),
 ([S+'pipe_top.png', S+'pipe_body.png'], 'راس العمود، وجسمه (الجسم يتكرر عمودي)'),
 ([S+'coin.png'], 'العملة: 4 إطارات دوران جنب بعض بنفس العرض'),
 ([S+'enemy1.png'], 'العدو: 3 إطارات جنب بعض (مشي 1، مشي 2، مسحوق)، وجهه لليمين'),
 ([f'hero/stage{n}.png'], 'البطل بلبس المرحلة: 5 إطارات جنب بعض (واقف، ركض 1، ركض 2، ركض 3، قفز)، وجهه لليمين والقدم على أسفل الإطار'),
 ([S+'item_grow.png'], 'جائزة التكبير اللي تطلع من الصندوق وتكبّر البطل'),
 ([S+'item_weapon.png'], 'جائزة السلاح (تطلع من الصندوق إذا البطل كبير) وتظهر بإيده وبأعلى الشاشة'),
 ([S+'shot.png'], 'المقذوف اللي يرميه البطل (يدور وهو طاير)'),
 ([S+'flag.png'], 'عمود العلم بنهاية المرحلة، العمود بالنص'),
 ([S+'goal.png'], 'مبنى النهاية اللي يدخله البطل، الباب بالنص من جوه'),
 ([S+'bg_far.jpg'], 'الخلفية البعيدة، تتحرك ببطء. الحافة اليمنى لازم تكمل اليسرى'),
 ([S+'bg_mid.png'], 'الخلفية الوسطى (المباني) شفافة من فوك. خط الأرض على بعد 936 بكسل من فوك. العرض حر والارتفاع 1080')]
h = '''<!doctype html><html dir="rtl" lang="ar"><meta charset="utf-8"><style>
body{margin:0;background:#14110b;color:#f1e9d6;font-family:"Noto Sans Arabic","Segoe UI",Tahoma,sans-serif;padding:40px;width:1520px}
h1{color:#d4af37;margin:0 0 6px;font-size:44px}p{color:#b9ad92;font-size:20px;margin:4px 0 22px}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #3a3427;padding:12px 14px;text-align:right;font-size:20px;vertical-align:middle}
th{color:#d4af37}td.f{font-family:monospace;direction:ltr;text-align:left;color:#fff}td.s{white-space:nowrap;color:#ffe88c}td.i{background:#2a3a55;text-align:center;width:330px}img{max-height:120px;max-width:300px}li{font-size:20px;margin:6px 0}
</style><h1>دليل تصميم المرحلة @N: @NAME</h1>
<p>كل ملف تصممه بنفس الاسم ونفس القياس بالضبط وترجعه. الخلفية شفافة (PNG) عدا bg_far.</p>
<table><tr><th>الملف</th><th>القياس بالبكسل</th><th>شنو هو</th><th>الحالي</th></tr>'''.replace('@NAME', name).replace('@N', n)
for files, desc in rows:
    w, hh = Image.open(os.path.join(K, files[0])).size
    h += f'<tr><td class="f">{"<br>".join(files)}</td><td class="s">العرض {w} × الارتفاع {hh}</td><td>{desc}</td><td class="i">' + ' '.join(f'<img src="{kit}/{f}">' for f in files) + '</td></tr>'
h += f'''<tr><td class="f">{S}music.mp3</td><td class="s">حوالي 30 ثانية، تتكرر</td><td>موسيقى المرحلة. عدلها أو بدلها بأي طول، بس خلي نهايتها تركب على بدايتها</td><td class="i">♪</td></tr></table>
<ul><li>تريد دقة أعلى؟ تكدر تصمم بضعف القياس بشرط تبقى نفس النسبة.</li><li>داخل اللعبة: F2 يفتح مجلد التصاميم، و F5 يعيد تحميلها فوراً.</li></ul></html>'''
open(os.path.join(out, 'guide.html'), 'w', encoding='utf8').write(h)
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});await p.goto('file://'+process.cwd()+'/guide.html');await p.waitForTimeout(500);await p.screenshot({path:'%s/دليل_التصميم.png',fullPage:true});await b.close()})()" % kit
subprocess.run(['node', '-e', js], cwd=out, check=True); os.remove(os.path.join(out, 'guide.html'))
z = os.path.join(root, 'dist', kit + '.zip')
if os.path.exists(z): os.remove(z)
subprocess.run(['zip', '-qr', z, kit], cwd=out, check=True); print('kit', z)
