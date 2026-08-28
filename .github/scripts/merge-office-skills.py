from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '''            <p><span data-lang="en">Excel · IF / VLOOKUP / PivotTables / Charts</span><span data-lang="ja">Excel · IF / VLOOKUP / ピボットテーブル / グラフ</span><span data-lang="zh">Excel · IF / VLOOKUP / 樞紐分析表 / 圖表</span></p>
            <p><span data-lang="en">Word / PowerPoint · Advanced</span><span data-lang="ja">Word / PowerPoint · 上級</span><span data-lang="zh">Word / PowerPoint · 進階</span></p>'''
new = '''            <p><span data-lang="en">Excel / Word / PowerPoint · Advanced</span><span data-lang="ja">Excel / Word / PowerPoint · 上級</span><span data-lang="zh">Excel / Word / PowerPoint · 進階</span></p>'''
if old not in text:
    raise SystemExit('Target Office skills block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print('Updated Office skills line')
