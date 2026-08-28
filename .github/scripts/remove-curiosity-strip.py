from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

pattern = re.compile(r'\n?<div class="curiosity-strip">.*?</div>\s*(?=<div class="volunteer generated-volunteer">)', re.S)
s2, count = pattern.subn('\n', s, count=1)
if count != 1:
    raise SystemExit('Could not find curiosity strip')

# Remove the now-unused curiosity CSS blocks.
s2 = re.sub(r'\n?\.curiosity-strip\s*\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-title\s*\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-body\s*\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-body p\s*\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-tags\s*\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-tags span\s*\{[^}]*\}', '', s2)

# Remove residual one-line typography overrides that reference curiosity elements.
s2 = re.sub(r'\n?\.curiosity-title\{[^}]*\}', '', s2)
s2 = re.sub(r'\n?\.curiosity-body p\{[^}]*\}', '', s2)

p.write_text(s2, encoding='utf-8')
print('Removed curiosity strip')
