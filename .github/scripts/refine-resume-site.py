from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')
original = html

# 1) SEO / sharing metadata
seo_marker = '<link rel="canonical" href="https://aling12007-cyber.github.io/Lily/">'
if seo_marker not in html:
    anchor = '<meta name="description" content="LIN YULING — Senior Accounting Specialist in Tokyo with 11+ years in accounting and audit, including IFRS reporting, process improvement and automation.">\n'
    seo = '''<link rel="canonical" href="https://aling12007-cyber.github.io/Lily/">\n<link rel="icon" href="assets/cartoon-profile.webp" type="image/webp">\n<meta property="og:type" content="website">\n<meta property="og:title" content="LIN YULING | Senior Accounting Specialist | Tokyo">\n<meta property="og:description" content="Senior Accounting Specialist in Tokyo with 11+ years in accounting and audit, including IFRS reporting, process improvement and systems experience.">\n<meta property="og:url" content="https://aling12007-cyber.github.io/Lily/">\n<meta property="og:image" content="https://aling12007-cyber.github.io/Lily/assets/cartoon-profile.webp">\n<meta name="twitter:card" content="summary">\n<meta name="twitter:title" content="LIN YULING | Senior Accounting Specialist | Tokyo">\n<meta name="twitter:description" content="Accounting, audit, financial reporting, process improvement and systems experience across Taiwan, China, Hong Kong and Japan.">\n<meta name="twitter:image" content="https://aling12007-cyber.github.io/Lily/assets/cartoon-profile.webp">\n'''
    if anchor not in html:
        raise SystemExit('SEO anchor not found')
    html = html.replace(anchor, anchor + seo, 1)

# 2) Simplify Hero supporting copy
hero_replacements = {
    'PwC audit and operating-company experience across Taiwan, China, Hong Kong and Japan, covering IFRS reporting, internal control and process improvement.':
        'PwC audit and operating-company experience, with a focus on financial reporting, process improvement and systems.',
    'PwCでの監査と事業会社での実務を通じ、台湾・中国・香港・日本でIFRS財務報告、内部統制、業務改善を経験してきました。':
        'PwCでの監査と事業会社での実務を通じ、財務報告、業務改善、システム活用の経験を積んできました。',
    '歷經 PwC 審計與企業端實務，在台灣、中國、香港與日本累積 IFRS 財務報告、內部控制與流程改善經驗。':
        '歷經 PwC 審計與企業端實務，專注於財務報告、流程改善與系統應用。',
}
for old, new in hero_replacements.items():
    if old not in html:
        raise SystemExit(f'Hero text not found: {old[:30]}')
    html = html.replace(old, new, 1)

# 3) Reduce personal trait tags to the five strongest signals
traits_pattern = re.compile(r'<div class="about-trait-tags" aria-label="Personal traits">.*?</div>', re.S)
traits_new = '''<div class="about-trait-tags" aria-label="Personal traits">
        <span class="about-trait"><span data-lang="en">Independent</span><span data-lang="ja">自立</span><span data-lang="zh">獨立</span></span>
        <span class="about-trait"><span data-lang="en">Responsible</span><span data-lang="ja">責任感</span><span data-lang="zh">責任感</span></span>
        <span class="about-trait"><span data-lang="en">Principled</span><span data-lang="ja">原則を大切にする</span><span data-lang="zh">有原則</span></span>
        <span class="about-trait"><span data-lang="en">Observant</span><span data-lang="ja">観察力</span><span data-lang="zh">觀察力</span></span>
        <span class="about-trait"><span data-lang="en">Curious</span><span data-lang="ja">好奇心</span><span data-lang="zh">好奇心</span></span>
      </div>'''
html, traits_count = traits_pattern.subn(traits_new, html, count=1)
if traits_count != 1:
    raise SystemExit(f'Expected one traits block, found {traits_count}')

# 4) Remove duplicated Period / Role / Location grids from every expanded career detail.
def remove_balanced_div_by_class(text, class_name):
    token = f'<div class="{class_name}">'
    removed = 0
    pos = 0
    while True:
        start = text.find(token, pos)
        if start < 0:
            break
        tag_re = re.compile(r'</?div\b[^>]*>', re.I)
        depth = 0
        end = None
        for m in tag_re.finditer(text, start):
            tag = m.group(0)
            if tag.lower().startswith('</div'):
                depth -= 1
                if depth == 0:
                    end = m.end()
                    break
            else:
                depth += 1
        if end is None:
            raise SystemExit(f'Could not balance {class_name} div')
        # Remove a trailing newline as well when present.
        while end < len(text) and text[end] in ' \t':
            end += 1
        if end < len(text) and text[end] == '\n':
            end += 1
        text = text[:start] + text[end:]
        removed += 1
        pos = start
    return text, removed

html, career_grid_count = remove_balanced_div_by_class(html, 'career-detail-grid')
if career_grid_count < 5:
    raise SystemExit(f'Unexpectedly few career detail grids removed: {career_grid_count}')

# 5) English proficiency wording
lang_old = '<p><span data-lang="en">English · TOEIC 585</span><span data-lang="ja">英語 · TOEIC 585</span><span data-lang="zh">英文 · TOEIC 585</span></p>'
lang_new = '<p><span data-lang="en">English · Everyday conversation</span><span data-lang="ja">英語 · 日常会話</span><span data-lang="zh">英文 · 日常口語溝通</span></p>'
if lang_old not in html:
    raise SystemExit('English proficiency line not found')
html = html.replace(lang_old, lang_new, 1)

# 6) Life section: remove work-adjacent cards so this section feels genuinely personal.
def remove_article_containing(text, needle):
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit(f'Life card marker not found: {needle}')
    start = text.rfind('<article class="interest-generated">', 0, idx)
    end = text.find('</article>', idx)
    if start < 0 or end < 0:
        raise SystemExit(f'Could not locate article around: {needle}')
    end += len('</article>')
    if end < len(text) and text[end] == '\n':
        end += 1
    return text[:start] + text[end:]

html = remove_article_containing(html, 'AI Applications')
html = remove_article_containing(html, 'Language Learning')

# 7) Give Now & Next a clearer professional direction.
now_replacements = {
    'Based in Tokyo, I continue to deepen my accounting expertise while learning new tools and languages. I do not need the next step to be perfectly defined; I want to keep the curiosity and initiative to move forward.':
        'Based in Tokyo, I want to keep deepening my accounting expertise and create value in an environment that respects professional judgment, process improvement and cross-border collaboration.',
    '東京を拠点に、会計の専門性を深めながら、新しいツールや言語も学び続けています。次の一歩が完全に決まっていなくても、好奇心と行動力を持って前へ進みたいと考えています。':
        '東京を拠点に会計の専門性をさらに深め、専門的な判断、業務改善、国際的な連携を大切にする環境で価値を生み出していきたいと考えています。',
    '現在以東京為據點，持續累積會計專業，也持續學習新的工具與語言。下一步不必完全確定，但我希望保留對新事物的好奇與行動力。':
        '目前以東京為據點，希望持續深化會計專業，並在尊重專業判斷、重視流程改善與跨國協作的環境中創造價值。',
}
for old, new in now_replacements.items():
    if old not in html:
        raise SystemExit(f'Now & Next text not found: {old[:30]}')
    html = html.replace(old, new, 1)

if html == original:
    raise SystemExit('No changes made')

path.write_text(html, encoding='utf-8')
print(f'Updated index.html; removed {career_grid_count} duplicated career detail grids.')
