from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

projects = {
    'Quanta Cloud Technology Japan': '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Sole accountant for the Japan entity, independently handling domestic accounting, tax-related coordination and banking operations while serving as the primary accounting contact for external parties.</span><span data-lang="ja">日本法人の唯一の経理担当として、国内会計、税務関連の調整、銀行業務を一貫して担当し、外部関係者との主要な会計窓口も担っています。</span><span data-lang="zh">擔任日本分公司唯一會計，獨立處理日本國內帳務、稅務相關協調及銀行業務，並作為公司與外部單位之間的主要會計窗口。</span></p>
    </div>''',
    'X&T Co., Ltd.': '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Served as the primary and sole accountant for key functions during the company’s early-stage operations, designing customized financial statement formats and building automated reporting workflows.</span><span data-lang="ja">会社の立ち上げ期に主要業務を担う唯一の経理担当として、実務に合わせた財務報告書フォーマットを設計し、レポート作成の自動化フローを構築しました。</span><span data-lang="zh">於公司草創期擔任主要項目的唯一會計，依實務需求訂製財務報表格式，並建立報表自動化流程。</span></p>
    </div>''',
    'Jumbo Technology Co., Ltd.': '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Managed parent-company AP and AR responsibilities, led a fixed-asset management restructuring project, and handled banking operations for a branch office.</span><span data-lang="ja">親会社の売掛金・買掛金業務を担当し、固定資産管理の再構築プロジェクトを主導しました。あわせて支店の銀行関連業務も担当しました。</span><span data-lang="zh">身兼母公司應收、應付業務，主導固定資產管理重整專案，並負責分公司相關銀行業務。</span></p>
    </div>''',
    'Granstar International Co., Ltd.': '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Acted as the sole accountant for the Shenzhen and Hong Kong operations while also covering HR administration such as payroll and social insurance, plus customs and import/export responsibilities.</span><span data-lang="ja">深圳・香港拠点の唯一の経理担当として会計業務を担うと同時に、給与・社会保険などの人事業務、税関・輸出入関連業務まで幅広く担当しました。</span><span data-lang="zh">擔任深圳及香港海外據點的唯一會計，同時兼任人事業務，包括薪資、社會保險等，並負責海關及進出口相關作業，在有限人力下處理多重職能。</span></p>
    </div>''',
    'PwC Taiwan': '''<div class="career-project-highlight">
      <div class="career-project-label"><span data-lang="en">Key contribution</span><span data-lang="ja">代表プロジェクト</span><span data-lang="zh">代表專案</span></div>
      <p><span data-lang="en">Worked as a team member on listed-company audit engagements and later led audit work for a company preparing for public offering and OTC listing, coordinating fieldwork and key audit procedures.</span><span data-lang="ja">上場企業の監査案件にチームメンバーとして参加し、その後、公開・店頭登録を準備する企業の監査業務をリードし、現場進行や主要な監査手続きを調整しました。</span><span data-lang="zh">曾任公開上市公司審計案件組員，並於即將公開發行／上櫃公司的案件中帶領查核工作，協調現場進度與主要查核項目。</span></p>
    </div>''',
}

for needle, highlight in projects.items():
    pattern = re.compile(r'(<article class="career-entry important">)(.*?' + re.escape(needle) + r'.*?)(</article>)', re.S)
    m = pattern.search(s)
    if not m:
        raise SystemExit(f'Career entry not found: {needle}')
    block = m.group(0)
    if 'career-project-highlight' in block:
        continue
    marker = '<div class="career-resp"'
    if marker not in block:
        raise SystemExit(f'Career responsibilities marker not found: {needle}')
    block2 = block.replace(marker, highlight + '\n    ' + marker, 1)
    s = s[:m.start()] + block2 + s[m.end():]

# Ensure the requested university and degree wording appears everywhere it is rendered.
s = s.replace('2007–2011 · Bachelor’s Degree in Accounting</span>', '2007–2011 · Bachelor’s Degree in Accounting Information</span>')
s = s.replace('2007–2011 · 会計学 学士課程</span>', '2007–2011 · 会計情報学 学士</span>')
s = s.replace('2007–2011 · 會計學學士</span>', '2007–2011 · 會計資訊學學士</span>')

css = '''
/* V63 key career project highlights */
.career-project-highlight{
  margin:10px 0 12px;
  padding:12px 14px;
  border-left:3px solid rgba(185,147,97,.66);
  border-radius:0 12px 12px 0;
  background:linear-gradient(90deg,rgba(250,246,238,.88),rgba(250,247,251,.52));
}
.career-project-label{
  margin-bottom:5px;
  color:#a47a43;
  font-size:11.5px;
  font-weight:800;
  letter-spacing:.06em;
  text-transform:uppercase;
}
.career-project-highlight p{
  margin:0!important;
  color:#554b57!important;
  font-size:15px!important;
  line-height:1.72!important;
}
@media(max-width:720px){
  .career-project-highlight{margin:9px 0 10px;padding:11px 12px}
  .career-project-label{font-size:10.5px}
  .career-project-highlight p{font-size:14px!important;line-height:1.68!important}
}
'''
if '/* V63 key career project highlights */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
