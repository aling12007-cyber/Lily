from pathlib import Path
import base64
import hashlib
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Positioning consistency.
s = s.replace('ACCOUNTING · AUDIT · IT · GLOBAL', 'ACCOUNTING · AUDIT · SYSTEMS · GLOBAL', 1)
s = s.replace(
    '<span><span data-lang="en">11+ years</span><span data-lang="ja">実務経験11年以上</span><span data-lang="zh">11+ 年經驗</span></span>',
    '<span><span data-lang="en">11+ years in accounting &amp; audit</span><span data-lang="ja">会計・監査11年以上</span><span data-lang="zh">會計・審計 11+ 年</span></span>',
    1,
)
s = s.replace(
    'LIN YULING — Senior Accounting Specialist in Tokyo with 11+ years across accounting, audit, financial reporting and process improvement.',
    'LIN YULING — Senior Accounting Specialist in Tokyo with 11+ years in accounting and audit, including IFRS reporting, process improvement and automation.',
    1,
)

# 2) Downloadable resume CTA.
linkedin = '<a class="btn" href="https://www.linkedin.com/in/yu-ling-l-0a185a166" target="_blank" rel="noopener">LinkedIn</a>'
resume = '<a class="btn" href="assets/LIN_YULING_Resume.pdf" download><span data-lang="en">Download Resume</span><span data-lang="ja">履歴書 PDF</span><span data-lang="zh">下載履歷 PDF</span></a>'
if resume not in s:
    if linkedin not in s:
        raise SystemExit('LinkedIn CTA not found')
    s = s.replace(linkedin, linkedin + '\n        ' + resume, 1)

# 3) Make the work philosophy more concise and memorable.
philosophy_body = '''<div class="work-philosophy-body-v65">
          <p>
            <span data-lang="en">Even in the age of AI, I see accounting as a highly specialized and important function. Good accounting should not only record what happened, but also identify issues, provide financial insight and improve the way work is done.</span>
            <span data-lang="ja">AIの時代であっても、会計は高度な専門性を持つ重要な職務だと考えています。優れた会計は、起きたことを記録するだけでなく、課題を見つけ、財務面から提案し、仕事の進め方そのものを改善する役割を持つべきだと思います。</span>
            <span data-lang="zh">即使在 AI 時代，我仍認為會計是一個高度專業且重要的職位。好的會計不只記錄已經發生的事情，更應該從數字中發現問題、提出財務建議，並改善工作的方式。</span>
          </p>
          <p>
            <span data-lang="en">I value organizations that respect accounting expertise, listen to recommendations and are willing to improve. Routine bookkeeping will increasingly be automated; professional judgment, analysis and the ability to make the business better are much harder to replace.</span>
            <span data-lang="ja">私は、会計の専門性を尊重し、提案に耳を傾け、改善に取り組む会社で働きたいと考えています。定型的な記帳業務は今後さらに自動化されても、専門的な判断、分析、そして会社をより良くする力は簡単には置き換えられません。</span>
            <span data-lang="zh">我希望任職的公司能尊重會計專業、願意聽取建議並持續改善。高度重複的作帳工作會愈來愈容易被自動化；真正難以取代的，是專業判斷、分析，以及讓公司變得更好的能力。</span>
          </p>
        </div>
        <div class="work-principles-v66" aria-label="Work principles">
          <div><strong><span data-lang="en">Numbers should explain reality.</span><span data-lang="ja">数字は現実を説明できること。</span><span data-lang="zh">數字要能說明真實狀況。</span></strong></div>
          <div><strong><span data-lang="en">Improve what can be improved.</span><span data-lang="ja">改善できることは、繰り返さない。</span><span data-lang="zh">能改善的流程，就不要一直重複。</span></strong></div>
          <div><strong><span data-lang="en">Judgment over routine.</span><span data-lang="ja">定型作業より、専門的な判断。</span><span data-lang="zh">專業判斷，比重複作業更有價值。</span></strong></div>
        </div>
        <div class="work-philosophy-line-v65">'''
pat = re.compile(r'<div class="work-philosophy-body-v65">.*?<div class="work-philosophy-line-v65">', re.S)
if not pat.search(s):
    raise SystemExit('Work philosophy body not found')
s = pat.sub(philosophy_body, s, count=1)

# 4) Replace the generic overseas story with four short, distinctive stories.
story_html = '''<div class="about-story-content">
          <div class="story-grid-v66">
            <article class="story-item-v66">
              <div class="story-no-v66">01</div>
              <div>
                <h3><span data-lang="en">I am rarely the first to speak.</span><span data-lang="ja">私は、最初に話し始めるタイプではありません。</span><span data-lang="zh">我通常不是第一個說話的人。</span></h3>
                <p><span data-lang="en">In a new environment, I usually observe first: how people work, what matters to them and where the real problem is. I used to think being slow to warm up was a weakness. Over time, I realized it also made me more attentive to details and better at building trust.</span><span data-lang="ja">新しい環境では、まず人の働き方、何を大切にしているのか、問題がどこにあるのかを観察します。以前は、打ち解けるまで時間がかかることを弱みだと思っていましたが、今では細部を見る力や信頼関係を築く力につながっていると感じています。</span><span data-lang="zh">到一個新的環境，我通常會先觀察大家怎麼工作、在意什麼，以及真正的問題在哪裡。以前我曾覺得慢熟是一種缺點，後來才發現，它也讓我更容易注意細節，並慢慢建立真正的信任。</span></p>
              </div>
            </article>
            <article class="story-item-v66">
              <div class="story-no-v66">02</div>
              <div>
                <h3><span data-lang="en">I dislike doing the same thing again every month.</span><span data-lang="ja">「毎月また同じことをする」が苦手です。</span><span data-lang="zh">我最受不了「每個月都要再做一次」。</span></h3>
                <p><span data-lang="en">When I see a recurring report or manual process, I naturally ask whether it can be made simpler or automated. At X&amp;T, that instinct led me to design financial statement formats and build automated reporting workflows. Systems and automation became an extension of how I think about accounting.</span><span data-lang="ja">毎月繰り返すレポートや手作業を見ると、もっと簡単にできないか、自動化できないかを考えます。X&amp;Tでは、その発想から財務報告書の形式を設計し、レポート作成の自動化フローを構築しました。システムや自動化は、私にとって会計の考え方の延長にあります。</span><span data-lang="zh">看到重複性的報表或人工流程，我很自然會想：能不能再簡單一點？能不能讓系統自己完成？在 X&amp;T，這個習慣讓我開始設計財務報表格式並建立報表自動化流程。對我而言，系統與自動化其實是會計思考方式的延伸。</span></p>
              </div>
            </article>
            <article class="story-item-v66">
              <div class="story-no-v66">03</div>
              <div>
                <h3><span data-lang="en">Being the “only accountant” means more than one job.</span><span data-lang="ja">「唯一の経理担当」は、一つの仕事だけではありません。</span><span data-lang="zh">「唯一會計」這四個字，比看起來忙很多。</span></h3>
                <p><span data-lang="en">I have been the sole accounting contact in Shenzhen, Hong Kong and Japan. When there is no second accountant beside you, questions about banking, tax, payroll, customs or operations often arrive at the same desk. Those roles taught me to break unfamiliar problems down, find the right information and take ownership of the result.</span><span data-lang="ja">深圳、香港、日本で、唯一の会計担当として働いた経験があります。隣にもう一人の経理がいない環境では、銀行、税務、給与、税関、業務上のさまざまな問題が同じ窓口に集まります。その経験から、知らない問題を分解し、必要な情報を探し、結果まで責任を持つ習慣が身につきました。</span><span data-lang="zh">我曾在深圳、香港與日本擔任唯一的會計窗口。當身邊沒有第二個會計可以先確認答案時，銀行、稅務、薪資、海關甚至營運上的問題，最後常常都會來到同一張桌上。這些經驗讓我習慣把陌生的問題拆開、找到需要的資訊，並對最後的結果負責。</span></p>
              </div>
            </article>
            <article class="story-item-v66 story-final-v66">
              <div class="story-no-v66">04</div>
              <div>
                <h3><span data-lang="en">What I wanted was not only life abroad.</span><span data-lang="ja">憧れていたのは、海外生活だけではありませんでした。</span><span data-lang="zh">小時候羨慕的是海外，長大後更在意的是選擇的自由。</span></h3>
                <p><span data-lang="en">As a child, the world outside Taiwan felt very far away. Looking back now, I think what I truly admired was not simply living overseas, but having the freedom to choose where to live, how to work and what to try next. I am still figuring out what comes next, but that freedom is something I value more than a perfectly planned life.</span><span data-lang="ja">子どもの頃、台湾の外の世界はとても遠く感じていました。今振り返ると、憧れていたのは海外に住むことだけではなく、どこで暮らすか、どう働くか、次に何を試すかを自分で選べることだったのだと思います。これから先も答えは一つではありませんが、完璧な計画より、その選択の自由を大切にしています。</span><span data-lang="zh">小時候，台灣以外的世界對我來說很遙遠。現在回頭看，我真正羨慕的或許不只是「住在國外」，而是可以自己決定在哪裡生活、怎麼工作，以及下一步想嘗試什麼。我仍然不知道人生最後會走到哪裡，但比起一張完美的計畫，我更珍惜可以自己選擇的自由。</span></p>
                <blockquote class="about-story-quote"><span data-lang="en">“I am living the overseas life that my younger self once admired.”</span><span data-lang="ja">「今の私は、子どもの頃の自分が憧れていた海外生活を送っています。」</span><span data-lang="zh">「我正在過著小時候的我所羨慕的海外生活。」</span></blockquote>
              </div>
            </article>
          </div>
        </div>'''
story_pat = re.compile(r'<div class="about-story-content">.*?</div>\s*</details>', re.S)
if not story_pat.search(s):
    raise SystemExit('About story content not found')
s = story_pat.sub(story_html + '\n      </details>', s, count=1)

# 5) Reduce routine duty lists for the five key roles so project impact comes first.
replacements = {
'<div class="career-resp" data-lang="en"><ul><li>Monthly, quarterly and annual closing.</li><li>Prepared IFRS financial statements and reporting materials.</li><li>Journal entries, expense reimbursement and budget management.</li><li>Petty cash and internal administrative management.</li><li>Coordination with tax accountants, banks and government authorities.</li></ul></div>': '<div class="career-resp" data-lang="en"><ul><li>Monthly, quarterly and annual closing, including IFRS reporting.</li><li>Journal entries, expense reimbursement, budgets and cash administration.</li><li>Coordination with tax accountants, banks and government authorities.</li></ul></div>',
'<div class="career-resp" data-lang="ja"><ul><li>月次・四半期・年次決算業務。</li><li>IFRSに基づく財務諸表および報告資料の作成。</li><li>仕訳、経費精算、予算管理。</li><li>小口現金管理および社内管理業務。</li><li>税理士、銀行、官公庁との連絡・書類対応。</li></ul></div>': '<div class="career-resp" data-lang="ja"><ul><li>月次・四半期・年次決算およびIFRS報告。</li><li>仕訳、経費精算、予算、小口現金管理。</li><li>税理士、銀行、官公庁との連絡・書類対応。</li></ul></div>',
'<div class="career-resp" data-lang="zh"><ul><li>月／季／年度結算。</li><li>依 IFRS 編製財務報表與報告資料。</li><li>會計傳票、費用報銷與預算管理。</li><li>零用金及公司內部管理作業。</li><li>與稅理士、銀行及政府機關聯繫與文件處理。</li></ul></div>': '<div class="career-resp" data-lang="zh"><ul><li>月／季／年度結算及 IFRS 財務報表與報告資料編製。</li><li>會計傳票、費用報銷、預算與零用金管理。</li><li>與稅理士、銀行及政府機關聯繫與文件處理。</li></ul></div>',
'<div class="career-resp" data-lang="en"><ul><li>Financial statement preparation and review.</li><li>Reporting of business performance.</li><li>Guidance for new employees.</li></ul></div>': '<div class="career-resp" data-lang="en"><ul><li>Financial statement preparation, review and management performance reporting.</li><li>New-employee guidance and improvement of recurring reporting processes.</li></ul></div>',
'<div class="career-resp" data-lang="ja"><ul><li>財務諸表作成・確認。</li><li>経営成績の報告。</li><li>新入社員への業務指導。</li></ul></div>': '<div class="career-resp" data-lang="ja"><ul><li>財務諸表の作成・確認および経営成績の報告。</li><li>新入社員への業務指導と定型レポート業務の改善。</li></ul></div>',
'<div class="career-resp" data-lang="zh"><ul><li>財務報表編製與確認。</li><li>經營成果報告。</li><li>新進員工工作指導。</li></ul></div>': '<div class="career-resp" data-lang="zh"><ul><li>財務報表編製、確認與經營成果報告。</li><li>新進員工工作指導及重複性報表流程改善。</li></ul></div>',
'<div class="career-resp" data-lang="en"><ul><li>AP / AR and invoicing.</li><li>Cash flow, banking and payments.</li><li>Closing and variance analysis.</li><li>Business tax and withholding tax filings.</li></ul></div>': '<div class="career-resp" data-lang="en"><ul><li>AP / AR and invoicing.</li><li>Cash flow, banking and payments.</li><li>Closing, variance analysis, business tax and withholding tax filings.</li></ul></div>',
'<div class="career-resp" data-lang="ja"><ul><li>売掛金・買掛金・請求書管理。</li><li>資金繰り・銀行取引・支払。</li><li>決算および差異分析。</li><li>事業税・源泉徴収税申告。</li></ul></div>': '<div class="career-resp" data-lang="ja"><ul><li>売掛金・買掛金・請求書管理。</li><li>資金繰り・銀行取引・支払。</li><li>決算、差異分析、事業税・源泉徴収税申告。</li></ul></div>',
'<div class="career-resp" data-lang="zh"><ul><li>應收帳款、應付帳款與發票管理。</li><li>資金調度、銀行交易與付款管理。</li><li>結算與差異分析。</li><li>營業稅與扣繳申報。</li></ul></div>': '<div class="career-resp" data-lang="zh"><ul><li>應收帳款、應付帳款與發票管理。</li><li>資金調度、銀行交易與付款管理。</li><li>結算、差異分析、營業稅與扣繳申報。</li></ul></div>',
'<div class="career-resp" data-lang="en"><ul><li>Daily accounting and supplier / manufacturer payments.</li><li>Checked purchasing and shipment records.</li><li>Payroll and social insurance calculations.</li><li>Prepared customs declaration documents.</li><li>Coordinated with accounting firms, banks, tax authorities and other government offices.</li></ul></div>': '<div class="career-resp" data-lang="en"><ul><li>Daily accounting, supplier / manufacturer payments, purchasing and shipment checks.</li><li>Payroll and social insurance calculations.</li><li>Customs / import-export documentation and coordination with accounting firms, banks and tax authorities.</li></ul></div>',
'<div class="career-resp" data-lang="ja"><ul><li>日常業務、製造者の支払い。</li><li>仕入れと出荷を確認。</li><li>給与、社会保険計算。</li><li>税関申告書類を作成。</li><li>会計事務所、銀行、税務署、その他官庁との対応。</li></ul></div>': '<div class="career-resp" data-lang="ja"><ul><li>日常会計、仕入先・製造者への支払い、仕入れ・出荷確認。</li><li>給与・社会保険計算。</li><li>税関・輸出入書類および会計事務所、銀行、税務署との調整。</li></ul></div>',
'<div class="career-resp" data-lang="zh"><ul><li>日常會計作業及供應商／製造商付款。</li><li>確認採購與出貨資料。</li><li>薪資與社會保險計算。</li><li>製作海關申報文件。</li><li>與會計師事務所、銀行、稅務機關及其他政府單位聯繫。</li></ul></div>': '<div class="career-resp" data-lang="zh"><ul><li>日常會計、供應商／製造商付款及採購出貨資料確認。</li><li>薪資與社會保險計算。</li><li>海關／進出口文件及與會計師事務所、銀行、稅務機關等對外協調。</li></ul></div>',
'<div class="career-resp" data-lang="en"><ul><li>Financial statement audits.</li><li>Internal control audits.</li><li>Tax return preparation.</li><li>Client coordination.</li></ul></div>': '<div class="career-resp" data-lang="en"><ul><li>Financial statement and internal control audits.</li><li>Tax return preparation.</li><li>Client communication, audit progress and issue follow-up.</li></ul></div>',
'<div class="career-resp" data-lang="ja"><ul><li>財務諸表監査。</li><li>内部統制監査。</li><li>税務申告書作成。</li><li>顧客対応。</li></ul></div>': '<div class="career-resp" data-lang="ja"><ul><li>財務諸表監査および内部統制監査。</li><li>税務申告書作成。</li><li>顧客対応、監査進捗および課題フォロー。</li></ul></div>',
'<div class="career-resp" data-lang="zh"><ul><li>財務報表審計。</li><li>內部控制審計。</li><li>稅務申報書編製。</li><li>客戶聯繫與協調。</li></ul></div>': '<div class="career-resp" data-lang="zh"><ul><li>財務報表與內部控制審計。</li><li>稅務申報書編製。</li><li>客戶溝通、查核進度與問題追蹤。</li></ul></div>',
}
for old, new in replacements.items():
    if old in s:
        s = s.replace(old, new, 1)

# 6) Remove CSS for retired story/curiosity components that are no longer in the HTML.
for ver in (46, 47, 49, 50):
    s = re.sub(r'\n/\* V' + str(ver) + r'\b.*?(?=\n/\* V\d+)', '\n', s, count=1, flags=re.S)

# 7) Add the new compact story + principle styling.
css = r'''
/* V66 portfolio refinement */
.work-principles-v66{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin:11px 0 12px}
.work-principles-v66>div{padding:9px 11px;border:1px solid rgba(167,127,157,.13);border-radius:12px;background:rgba(255,255,255,.62);color:#6e5c6b;font-size:11px;line-height:1.45}
.story-grid-v66{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
.story-item-v66{display:grid;grid-template-columns:34px minmax(0,1fr);gap:9px;padding:14px 15px;border:1px solid rgba(78,61,82,.09);border-radius:15px;background:linear-gradient(145deg,rgba(255,255,255,.76),rgba(247,241,248,.62))}
.story-no-v66{font-family:Georgia,"Times New Roman",serif;color:#b38a50;font-size:16px;line-height:1.2;padding-top:2px}
.story-item-v66 h3{margin:0 0 6px;font-size:15px;line-height:1.38;color:var(--ink)}
.story-item-v66 p{margin:0!important;font-size:13px!important;line-height:1.72!important;color:#675c69!important}
.story-final-v66{grid-column:1 / -1}
.story-final-v66 .about-story-quote{margin:11px 0 0!important;font-size:16px!important}
@media(max-width:720px){.work-principles-v66{grid-template-columns:1fr}.story-grid-v66{grid-template-columns:1fr}.story-final-v66{grid-column:auto}.story-item-v66{grid-template-columns:30px minmax(0,1fr);padding:12px}.story-item-v66 h3{font-size:14px}.story-item-v66 p{font-size:12.5px!important;line-height:1.68!important}.story-final-v66 .about-story-quote{font-size:14.5px!important}}
'''
if '/* V66 portfolio refinement */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

# 8) Extract embedded base64 images into assets to reduce index.html weight.
assets = Path('assets')
assets.mkdir(exist_ok=True)
img_pat = re.compile(r'data:image/(?P<fmt>png|jpe?g|webp);base64,(?P<data>[A-Za-z0-9+/=\r\n]+)')
created = []
def extract_image(m):
    fmt = m.group('fmt').lower()
    ext = 'jpg' if fmt in ('jpeg', 'jpg') else fmt
    raw = base64.b64decode(re.sub(r'\s+', '', m.group('data')))
    digest = hashlib.sha1(raw).hexdigest()[:12]
    out = assets / f'embedded-{digest}.{ext}'
    if not out.exists():
        out.write_bytes(raw)
        created.append(str(out))
    return str(out).replace('\\', '/')
s, extracted = img_pat.subn(extract_image, s)

p.write_text(s, encoding='utf-8')
print(f'Updated index.html; extracted {extracted} embedded images; created {len(created)} files.')
