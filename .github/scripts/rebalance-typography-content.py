from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'Missing expected content: {label}')
    s = s.replace(old, new, 1)


def remove_section_description(section_id):
    global s
    marker = f'<section class="section" id="{section_id}">'
    start = s.find(marker)
    if start < 0:
        raise SystemExit(f'Missing section: {section_id}')
    rule = s.find('<div class="rule"></div>', start)
    if rule < 0:
        raise SystemExit(f'Missing rule for section: {section_id}')
    head = s[start:rule]
    new_head, count = re.subn(r'\s*<p>.*?</p>\s*', '\n', head, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'Could not remove section description: {section_id}')
    s = s[:start] + new_head + s[rule:]


def replace_story(number, en, ja, zh):
    global s
    pattern = re.compile(
        rf'(<div class="story-no-v66">{number}</div>.*?<p>).*?(</p>)',
        re.S,
    )
    body = (
        f'<span data-lang="en">{en}</span>'
        f'<span data-lang="ja">{ja}</span>'
        f'<span data-lang="zh">{zh}</span>'
    )
    s, count = pattern.subn(lambda m: m.group(1) + body + m.group(2), s, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace story {number}')


def replace_project(company_marker, en, ja, zh):
    global s
    pos = s.find(company_marker)
    if pos < 0:
        raise SystemExit(f'Missing company marker: {company_marker}')
    article_start = s.rfind('<article class="career-entry', 0, pos)
    article_end = s.find('<article class="career-entry', pos)
    if article_start < 0:
        raise SystemExit(f'Missing article start: {company_marker}')
    if article_end < 0:
        article_end = s.find('</section>', pos)
    segment = s[article_start:article_end]
    pattern = re.compile(r'(<div class="career-project-highlight">.*?<p>).*?(</p>)', re.S)
    body = (
        f'<span data-lang="en">{en}</span>'
        f'<span data-lang="ja">{ja}</span>'
        f'<span data-lang="zh">{zh}</span>'
    )
    segment2, count = pattern.subn(lambda m: m.group(1) + body + m.group(2), segment, count=1)
    if count != 1:
        raise SystemExit(f'Missing project highlight: {company_marker}')
    s = s[:article_start] + segment2 + s[article_end:]


# Hero: shorter secondary copy while preserving positioning.
replace_once(
    '<div class="hero-desc">Experience across PwC audit and operating companies, with IFRS reporting, internal control, system adaptability and cross-border coordination across Taiwan, China, Hong Kong and Japan.</div>',
    '<div class="hero-desc">PwC audit and operating-company experience across Taiwan, China, Hong Kong and Japan, covering IFRS reporting, internal control and process improvement.</div>',
    'hero EN description',
)
replace_once(
    '<div class="hero-desc">PwCでの監査および事業会社での実務を通じ、IFRS財務報告、内部統制、システム対応、台湾・中国・香港・日本にまたがる国際調整を経験してきました。</div>',
    '<div class="hero-desc">PwCでの監査と事業会社での実務を通じ、台湾・中国・香港・日本でIFRS財務報告、内部統制、業務改善を経験してきました。</div>',
    'hero JA description',
)
replace_once(
    '<div class="hero-desc">歷經 PwC 審計與企業端會計實務，涵蓋 IFRS 財務報告、內部控制、系統適應，以及台灣、中國、香港與日本之間的跨國協調。</div>',
    '<div class="hero-desc">歷經 PwC 審計與企業端實務，在台灣、中國、香港與日本累積 IFRS 財務報告、內部控制與流程改善經驗。</div>',
    'hero ZH description',
)

# About: keep the life context, remove repeated explanation.
about_block = '''<div class="about-bridge">
        <p>
          <span data-lang="en">I was born and raised in Dajia, Taichung, and learned independence early after losing my father at five. Curiosity about the world later took me from Taiwan to China, Hong Kong and Japan. Today I live and work in Tokyo, continuing to build my accounting expertise while making my own choices in changing environments.</span>
          <span data-lang="ja">私は台中・大甲で生まれ育ち、5歳で父を亡くした経験から早くから自立を学びました。外の世界への好奇心に導かれ、台湾から中国、香港、日本へと生活と仕事の場を広げてきました。現在は東京で暮らし働きながら、会計の専門性を高め、変化する環境の中でも自分で選択することを大切にしています。</span>
          <span data-lang="zh">我出生、成長於台中大甲，五歲時父親早逝，讓我很早學會獨立。對外面世界的好奇，帶著我從台灣走到中國、香港與日本。現在在東京生活與工作，持續累積會計專業，也持續練習在不同環境裡做出自己的選擇。</span>
        </p>
      </div>'''
s, count = re.subn(r'<div class="about-bridge">\s*<p>.*?</p>\s*</div>', about_block, s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not simplify About copy')

# Work philosophy: one supporting paragraph + three principles. Remove duplicate closing statement.
philosophy_body = '''<div class="work-philosophy-body-v65">
          <p>
            <span data-lang="en">Even in the age of AI, I believe accounting creates value through professional judgment, analysis and improvement. Good accounting should identify issues and offer useful recommendations, and I value organizations that respect that professional role.</span>
            <span data-lang="ja">AIの時代でも、会計の価値は専門的な判断、分析、改善にあると考えています。優れた会計は課題を見つけ、実用的な提案につなげる役割を持ち、私はその専門性を尊重する組織を大切にしています。</span>
            <span data-lang="zh">即使在 AI 時代，我仍相信會計的核心價值在專業判斷、分析與改善。好的會計不只記錄結果，也應該看出問題、提出建議；我也重視願意尊重會計專業的工作環境。</span>
          </p>
        </div>'''
s, count = re.subn(r'<div class="work-philosophy-body-v65">.*?</div>\s*<div class="work-principles-v66"', philosophy_body + '\n        <div class="work-principles-v66"', s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not simplify work philosophy body')
s, count = re.subn(r'\s*<div class="work-philosophy-line-v65">.*?</div>', '', s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not remove duplicate philosophy closing line')

# Stories: shorter, more distinctive, less explanatory.
replace_story('01',
    'In a new environment, I observe first—how people work and what really matters. Being slow to warm up has made me more attentive to details and more deliberate about trust.',
    '新しい環境では、まず人の働き方や本当に大切なことを観察します。ゆっくり打ち解ける性格は、細部を見る力と信頼を丁寧に築く姿勢につながっています。',
    '到新環境時，我習慣先觀察人與做事方式，再慢慢建立信任。慢熟讓我更注意細節，也更懂得先理解再判斷。')
replace_story('02',
    'When I see a recurring report or manual process, I first ask whether it can be simplified or automated. At X&amp;T, that instinct became financial-report formats and automated reporting workflows.',
    '繰り返すレポートや手作業を見ると、まず簡素化や自動化ができないか考えます。X&amp;Tでは、その発想が財務報告書の設計と自動化フローにつながりました。',
    '看到每月重複的報表或人工流程，我會先想能不能簡化或自動化。X&amp;T 的報表格式與自動化流程，就是從這個習慣開始。')
replace_story('03',
    'I have been the sole accounting contact in Shenzhen, Hong Kong and Japan. When banking, tax, payroll and operational questions arrive at the same desk, I break unfamiliar problems down, find the answer and own the result.',
    '深圳、香港、日本で唯一の会計窓口を経験しました。銀行、税務、給与、業務上の問題が同じ窓口に集まる環境で、未知の課題を分解し、答えを見つけ、結果まで責任を持つことを学びました。',
    '我曾在深圳、香港與日本擔任唯一會計窗口。當銀行、稅務、薪資或營運問題都來到同一張桌上，我學會把陌生問題拆開，找到答案並對結果負責。')
replace_story('04',
    'As a child I admired life abroad; today I value the freedom to choose where to live, how to work and what to try next. I care more about that freedom than a perfectly planned life.',
    '子どもの頃は海外生活に憧れていましたが、今大切にしているのは、どこで暮らし、どう働き、次に何を試すかを自分で選べる自由です。完璧な計画より、その自由を大切にしています。',
    '小時候羨慕海外生活，現在更珍惜的是能自己選擇在哪裡生活、怎麼工作，以及下一步想嘗試什麼。比起完美的計畫，我更在意選擇的自由。')

# Remove section-level explanatory copy that repeats what the content already says.
for section in ('experience', 'education', 'expertise', 'life', 'contact'):
    remove_section_description(section)

# Remove duplicate micro-headings / editorial notes.
s, count = re.subn(r'\s*<div class="editorial-note">.*?</div>', '', s, flags=re.S)
if count < 2:
    raise SystemExit('Expected editorial notes were not found')
s, count = re.subn(r'\s*<div class="strengths-heading">.*?</div>', '', s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not remove duplicate strengths heading')
s, count = re.subn(r'\s*<div class="career-education-head">.*?</div>', '', s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not remove duplicate education heading')

# Rename old IT wording in strengths.
replace_once('IT & System Adaptability', 'Systems & Digital Adaptability', 'strength EN title')
replace_once('IT・システムへの高い適応力', 'システム・デジタルツールへの適応力', 'strength JA title')
replace_once('IT 系統與軟體適應力', '系統與數位工具適應力', 'strength ZH title')

# Career key contributions: one clear line each.
replace_project('Quanta Cloud Technology Japan Co., Ltd.',
    'Sole accountant for the Japan entity, covering accounting, tax coordination, banking and the main external accounting contact.',
    '日本法人の唯一の経理担当として、会計、税務調整、銀行業務、主要な対外会計窓口を担当。',
    '日本分公司唯一會計，負責帳務、稅務協調、銀行業務與主要對外會計窗口。')
replace_project('X&T Co., Ltd.',
    'Sole accountant for core operations during the start-up stage; designed financial-report formats and automated reporting workflows.',
    '草創期の主要業務を担う唯一の経理として、財務報告書の形式を設計し、レポート自動化フローを構築。',
    '草創期主要項目唯一會計，設計財務報表格式並建立報表自動化流程。')
replace_project('Jumbo Technology Co., Ltd.',
    'Managed parent-company receivables and payables, led a fixed-asset management overhaul and handled branch banking operations.',
    '親会社の売掛・買掛管理に加え、固定資産管理の再整備を主導し、支店の銀行業務も担当。',
    '負責母公司應收應付，主導固定資產管理重整，並處理分公司銀行業務。')
replace_project('Granstar Technology Enterprise Co., Ltd.',
    'Sole accountant for Shenzhen and Hong Kong, also covering payroll, social insurance, HR administration and customs / import-export work.',
    '深圳・香港の唯一の経理担当として、給与、社会保険、人事、税関・輸出入業務も兼任。',
    '深圳與香港唯一會計，兼任薪資、社會保險、人事及海關進出口業務。')
replace_project('PwC Taiwan',
    'Worked on listed-company audits and led audit work for a company preparing for public listing / OTC registration.',
    '上場企業の監査に携わり、公開・上場準備企業の監査業務をリード。',
    '參與上市公司審計，並帶領準備公開發行／上櫃公司的查核工作。')

# Life: titles are enough for the six interests; remove repetitive descriptors.
s, count = re.subn(
    r'(<article class="interest-generated">.*?<div class="interest-copy">\s*<h4>.*?</h4>)\s*<p>.*?</p>',
    r'\1',
    s,
    flags=re.S,
)
if count != 6:
    raise SystemExit(f'Expected 6 interest descriptions, removed {count}')

curiosity = '''<p>
      <span data-lang="en">I like trying new things to keep life fresh and keep learning.</span>
      <span data-lang="ja">新しいことを試し、日常に新鮮さと学びを取り入れるのが好きです。</span>
      <span data-lang="zh">我喜歡持續嘗試新事物，讓生活保持新鮮，也讓自己持續學習。</span>
    </p>'''
start = s.find('<div class="curiosity-strip">')
if start < 0:
    raise SystemExit('Missing curiosity strip')
p_start = s.find('<p>', start)
p_end = s.find('</p>', p_start)
if p_start < 0 or p_end < 0:
    raise SystemExit('Missing curiosity paragraph')
s = s[:p_start] + curiosity + s[p_end + 4:]

# Volunteer title is self-explanatory.
vol_start = s.find('<div class="volunteer generated-volunteer">')
vol_end = s.find('</div>\n\n\n\n\n', vol_start)
if vol_start < 0:
    raise SystemExit('Missing volunteer block')
segment = s[vol_start:vol_end if vol_end > vol_start else s.find('</section>', vol_start)]
segment2, count = re.subn(r'\s*<p>.*?</p>', '', segment, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not remove volunteer description')
s = s[:vol_start] + segment2 + s[vol_start + len(segment):]

# Now: one concise current-state statement.
now_copy = '''<div class="now-next-copy">
          <p>
            <span data-lang="en">Based in Tokyo, I continue to deepen my accounting expertise while learning new tools and languages. I do not need the next step to be perfectly defined; I want to keep the curiosity and initiative to move forward.</span>
            <span data-lang="ja">東京を拠点に、会計の専門性を深めながら、新しいツールや言語も学び続けています。次の一歩が完全に決まっていなくても、好奇心と行動力を持って前へ進みたいと考えています。</span>
            <span data-lang="zh">現在以東京為據點，持續累積會計專業，也持續學習新的工具與語言。下一步不必完全確定，但我希望保留對新事物的好奇與行動力。</span>
          </p>
        </div>'''
s, count = re.subn(r'<div class="now-next-copy">.*?</div>', now_copy, s, count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not simplify Now copy')

# Final typography hierarchy: fewer extremes, more consistent body text.
css = r'''
/* V67 balanced typography + lower visual noise */
.hero h1{font-size:clamp(46px,6vw,72px)!important;line-height:.9!important;}
.hero-role{font-size:clamp(19px,2.3vw,26px)!important;line-height:1.24!important;}
.hero-desc{font-size:14px!important;line-height:1.7!important;max-width:650px!important;}
.section{padding:26px 0!important;}
.section-no{font-size:46px!important;}
.section-title{margin-bottom:10px!important;}
.section-title h2{font-size:clamp(28px,3.5vw,42px)!important;line-height:1.05!important;}
.section-title p{font-size:13.5px!important;line-height:1.65!important;max-width:560px!important;}
.rule{margin:11px 0 18px!important;}
#profile .about-bridge{padding:18px 20px!important;}
#profile .about-bridge p{font-size:14px!important;line-height:1.75!important;max-width:980px!important;}
.about-trait{font-size:11.5px!important;min-height:28px!important;}
.work-philosophy-v65{padding:18px 20px!important;margin-top:14px!important;}
.work-philosophy-head-v65{grid-template-columns:145px minmax(0,1fr)!important;gap:16px!important;}
.work-philosophy-kicker-v65{font-size:11.5px!important;}
.work-philosophy-head-v65 h3{font-size:18px!important;line-height:1.5!important;}
.work-philosophy-body-v65{grid-template-columns:1fr!important;gap:0!important;margin:12px 0 0 161px!important;}
.work-philosophy-body-v65 p{font-size:13.5px!important;line-height:1.68!important;max-width:780px!important;}
.work-principles-v66{margin:12px 0 0 161px!important;}
.work-principles-v66>div{font-size:12px!important;line-height:1.45!important;padding:9px 10px!important;}
.about-story-details summary{font-size:12.5px!important;}
.story-item-v66{padding:13px 14px!important;}
.story-item-v66 h3{font-size:14.5px!important;line-height:1.4!important;}
.story-item-v66 p{font-size:13.5px!important;line-height:1.65!important;}
.story-final-v66 .about-story-quote{font-size:15px!important;line-height:1.55!important;}
.career-date{font-size:15.5px!important;}
.career-title-row h3{font-size:15.5px!important;line-height:1.3!important;}
.career-meta{font-size:12px!important;}
.career-detail{padding-top:14px!important;padding-bottom:15px!important;}
.career-detail-grid>div{font-size:14px!important;line-height:1.55!important;}
.career-detail-label{font-size:11px!important;}
.milestone-detail{font-size:12.5px!important;line-height:1.5!important;}
.career-detail .career-resp,.career-detail .career-resp li,.career-detail p,.career-detail li{font-size:14px!important;line-height:1.68!important;}
.career-project-highlight p{font-size:14px!important;line-height:1.65!important;}
.career-project-label{font-size:11px!important;}
.strength-card h3{font-size:15.5px!important;line-height:1.35!important;}
.strength-card p{font-size:13.5px!important;line-height:1.55!important;}
.strength-index{font-size:17px!important;}
.credential h3{font-size:18px!important;line-height:1.35!important;}
.credential p{font-size:13px!important;line-height:1.55!important;}
.interest-copy h4{font-size:14px!important;line-height:1.35!important;}
.curiosity-title{font-size:13.5px!important;}
.curiosity-body p{font-size:13px!important;line-height:1.6!important;}
.volunteer-copy h3{font-size:17px!important;line-height:1.4!important;}
.now-next-copy p{font-size:14px!important;line-height:1.72!important;}
.contact-panel h3{font-size:18px!important;line-height:1.35!important;}
.contact-panel p{font-size:13px!important;line-height:1.55!important;}
.editorial-note{display:none!important;}
@media(max-width:820px){
  .work-philosophy-head-v65{grid-template-columns:1fr!important;gap:7px!important;}
  .work-philosophy-body-v65,.work-principles-v66{margin-left:0!important;}
}
@media(max-width:720px){
  .hero h1{font-size:46px!important;}
  .hero-role{font-size:20px!important;}
  .hero-desc{font-size:13.5px!important;line-height:1.65!important;}
  .section{padding:22px 0!important;}
  .section-no{font-size:38px!important;}
  .section-title h2{font-size:30px!important;}
  #profile .about-bridge{padding:15px!important;}
  #profile .about-bridge p{font-size:13.5px!important;line-height:1.7!important;}
  .work-philosophy-head-v65 h3{font-size:16.5px!important;}
  .work-philosophy-body-v65 p{font-size:13px!important;}
  .work-principles-v66>div{font-size:11.5px!important;}
  .story-item-v66 h3{font-size:14px!important;}
  .story-item-v66 p{font-size:13px!important;}
  .career-date,.career-title-row h3{font-size:14.5px!important;}
  .career-meta{font-size:11.5px!important;}
  .career-detail-grid>div,.career-detail .career-resp,.career-detail .career-resp li,.career-detail p,.career-detail li,.career-project-highlight p{font-size:13.5px!important;}
  .strength-card h3{font-size:15px!important;}
  .strength-card p{font-size:13px!important;}
  .credential h3{font-size:17px!important;}
  .credential p,.curiosity-body p,.now-next-copy p{font-size:13px!important;}
}
'''
if '/* V67 balanced typography + lower visual noise */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)
else:
    raise SystemExit('V67 already present')

p.write_text(s, encoding='utf-8')
print('Updated index.html')
