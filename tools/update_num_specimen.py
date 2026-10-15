# tools/update_num_specimen.py
import re

with open("fonts/font_b64.txt", "r", encoding="ascii") as f:
    b64 = f.read().strip()

with open("tools/num_specimen.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r"src:\s*url\('data:font/truetype;charset=utf-8;base64,[^']+'\)", html)
if m:
    old_src = m.group(0)
    new_src = f"src: url('data:font/truetype;charset=utf-8;base64,{b64}')"
    html = html.replace(old_src, new_src)
    with open("tools/num_specimen.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("tools/num_specimen.html successfully updated!")
else:
    print("Base64 pattern not found in num_specimen.html")
