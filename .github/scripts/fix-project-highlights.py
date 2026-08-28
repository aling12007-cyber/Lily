from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

projects = [
    ('X&T Co., Ltd.', '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Served as the primary and sole accountant for key functions during the company’s early-stage operations, designing customized financial statement formats and building automated reporting workflows.</span><span data-lang="ja">会社の立ち上げ期に主要業務を担う唯一の経理担当として、実務に合わせた財務報告書フォーマットを設計し、レポート作成の自動化フローを構築しました。</span><span data-lang="zh">於公司草創期擔任主要項目的唯一會計，依實務需求訂製財務報表格式，並建立報表自動化流程。</span></p>
    </div>'''),
    ('Jumbo Technology Co., Ltd.', '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Managed parent-company AP and AR responsibilities, led a fixed-asset management restructuring project, and handled banking operations for a branch office.</span><span data-lang="ja">親会社の売掛金・買掛金業務を担当し、固定資産管理の再構築プロジェクトを主導しました。あわせて支店の銀行関連業務も担当しました。</span><span data-lang="zh">身兼母公司應收、應付業務，主導固定資產管理重整專案，並負責分公司相關銀行業務。</span></p>
    </div>'''),
    ('Granstar International Co., Ltd.', '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Acted as the sole accountant for the Shenzhen and Hong Kong operations while also covering HR administration such as payroll and social insurance, plus customs and import/export responsibilities.</span><span data-lang="ja">深圳・香港拠点の唯一の経理担当として会計業務を担うと同時に、給与・社会保険などの人事業務、税関・輸出入関連業務まで幅広く担当しました。</span><span data-lang="zh">擔任深圳及香港海外據點的唯一會計，同時兼任人事業務，包括薪資、社會保險等，並負責海關及進出口相關作業，在有限人力下處理多重職能。</span></p>
    </div>'''),
    ('PwC Taiwan', '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Worked as a team member on listed-company audit engagements and later led audit work for a company preparing for public offering and OTC listing, coordinating fieldwork and key audit procedures.</span><span data-lang="ja">上場企業の監査案件にチームメンバーとして参加し、その後、公開・店頭登録を準備する企業の監査業務をリードし、現場進行や主要な監査手続きを調整しました。</span><span data-lang="zh">曾任公開上市公司審計案件組員，並於即將公開發行／上櫃公司的案件中帶領查核工作，協調現場進度與主要查核項目。</span></p>
    </div>'''),
]

article_re = re.compile(r'<article class="career-entry important">.*?</article>', re.S)
articles = list(article_re.finditer(s))
if not articles:
    raise SystemExit('No important career entries found')

replacements = []
for m in articles:
    block = m.group(0)
    for needle, highlight in projects:
        if needle not in block:
            continue
        if 'career-project-highlight' in block:
            break
        marker = '<div class="career-resp"'
        if marker not in block:
            raise SystemExit(f'Responsibility marker missing for {needle}')
        block2 = block.replace(marker, highlight + '\n    ' + marker, 1)
        replacements.append((m.start(), m.end(), block2, needle))
        break

for start, end, block2, needle in reversed(replacements):
    s = s[:start] + block2 + s[end:]

expected = ['Quanta Cloud Technology Japan', 'X&T Co., Ltd.', 'Jumbo Technology Co., Ltd.', 'Granstar International Co., Ltd.', 'PwC Taiwan']
for needle in expected:
    matched = False
    for m in article_re.finditer(s):
        block = m.group(0)
        if needle in block:
            matched = True
            if 'career-project-highlight' not in block:
                raise SystemExit(f'Highlight still missing for {needle}')
            break
    if not matched:
        raise SystemExit(f'Career entry missing for {needle}')

p.write_text(s, encoding='utf-8')
