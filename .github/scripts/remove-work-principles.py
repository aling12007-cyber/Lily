from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s2, count = re.subn(r'\s*<div class="work-principles-v66"[^>]*>.*?</div>\s*</div>', '\n', s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('work principles block not found')

p.write_text(s2, encoding='utf-8')
print('Removed work principles block')
