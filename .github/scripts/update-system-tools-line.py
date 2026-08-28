from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '<p><span data-lang="en">Accounting / ERP systems · Fast learner across different platforms</span><span data-lang="ja">会計 / ERPシステム · 新しい環境への高い適応力</span><span data-lang="zh">會計 / ERP 系統 · 可快速適應不同平台</span></p>'
new = '<p><span data-lang="en">Various accounting / ERP systems (Taiwan / Japan) · Quick to adapt across platforms</span><span data-lang="ja">各種会計 / ERPシステム（台湾 / 日本）· 異なるプラットフォームにも迅速に適応</span><span data-lang="zh">各類會計 / ERP 系統（台灣 / 日本），可快速適應不同平台</span></p>'
if old not in text:
    raise SystemExit('Target systems line not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
