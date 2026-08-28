from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<section class="section" id="profile">'
start = s.find(marker)
if start < 0:
    raise SystemExit('About section not found')
rule = s.find('<div class="rule"></div>', start)
if rule < 0:
    raise SystemExit('About rule not found')
head = s[start:rule]
new_head, count = re.subn(r'\s*<p>.*?</p>\s*', '\n', head, count=1, flags=re.S)
if count != 1:
    raise SystemExit('About subtitle not found')
s = s[:start] + new_head + s[rule:]
p.write_text(s, encoding='utf-8')
print('Removed About subtitle')
