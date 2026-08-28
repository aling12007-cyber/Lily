from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'work-philosophy-v65' in s:
    raise SystemExit('Work philosophy section already exists')

philosophy = r'''
      <section class="work-philosophy-v65" aria-label="Work philosophy">
        <div class="work-philosophy-head-v65">
          <div class="work-philosophy-kicker-v65">
            <span data-lang="en">Work Philosophy</span>
            <span data-lang="ja">仕事の価値観</span>
            <span data-lang="zh">我的工作價值觀</span>
          </div>
          <h3>
            <span data-lang="en">Accounting is not just about bookkeeping. Its value is turning numbers into meaningful information that supports better business decisions.</span>
            <span data-lang="ja">会計の価値は、単に帳簿をつけることではなく、数字を価値ある情報へ変え、会社の判断や意思決定を支えることにあると考えています。</span>
            <span data-lang="zh">我認為，會計的價值不只是作帳，而是把數字轉化成有價值的資訊，提供公司作為判斷與決策的依據。</span>
          </h3>
        </div>
        <div class="work-philosophy-body-v65">
          <p>
            <span data-lang="en">After working across different companies for many years, I still see accounting as a highly specialized and important function—even in the age of AI. Good accounting should not only record what has happened, but also identify issues, provide financial insight and help improve processes.</span>
            <span data-lang="ja">複数の会社で経験を重ねてきた今も、AIの時代だからこそ、会計は高度な専門性を持つ重要な職務だと考えています。優れた会計は、起きたことを記録するだけでなく、数字から課題を見つけ、財務面から提案し、業務プロセスの改善にもつなげる役割を持つべきだと思います。</span>
            <span data-lang="zh">工作多年並經歷不同公司之後，即使進入 AI 快速發展的時代，我依然認為會計是一個高度專業且重要的職位。好的會計不只記錄已經發生的事情，更應該從數字中發現問題、提出財務建議，並協助改善工作流程。</span>
          </p>
          <p>
            <span data-lang="en">I value organizations that respect accounting as a professional function, listen to its recommendations and are willing to improve. Routine bookkeeping will increasingly be automated; the value that remains is professional judgment, analysis and the ability to make the business better.</span>
            <span data-lang="ja">そのため、会計という専門職を尊重し、提案に耳を傾け、改善に取り組む会社で働きたいと考えています。定型的な記帳業務は今後さらに自動化されていきます。だからこそ、判断力、分析力、そして会社をより良くするための提案こそが、会計に残る本当の価値だと思っています。</span>
            <span data-lang="zh">因此，我希望任職的公司能尊重會計專業、願意聽取建議並持續改善。高度重複的作帳工作會愈來愈容易被系統與 AI 自動化；真正難以取代的，是專業判斷、分析，以及讓公司變得更好的能力。</span>
          </p>
        </div>
        <div class="work-philosophy-line-v65">
          <span data-lang="en">Understand what is happening behind the numbers—and use that information to help the company make better decisions.</span>
          <span data-lang="ja">数字の背景で何が起きているのかを理解し、その情報をより良い意思決定につなげる。</span>
          <span data-lang="zh">理解數字背後發生了什麼，並利用這些資訊，讓公司做出更好的決定。</span>
        </div>
      </section>
'''

story_marker = '      <details class="about-story-details">'
pos = s.find(story_marker)
if pos == -1:
    raise SystemExit('Could not find About story insertion point')
s = s[:pos] + philosophy + s[pos:]

css = r'''
/* V65 work philosophy */
.work-philosophy-v65{
  margin:16px 0 8px;
  padding:20px 22px;
  border:1px solid rgba(78,61,82,.10);
  border-radius:20px;
  background:linear-gradient(135deg,rgba(255,255,255,.88),rgba(247,241,248,.70));
  box-shadow:0 10px 28px rgba(78,61,82,.04);
}
.work-philosophy-head-v65{
  display:grid;
  grid-template-columns:150px minmax(0,1fr);
  gap:20px;
  align-items:start;
}
.work-philosophy-kicker-v65{
  padding-top:4px;
  color:var(--mauve);
  font-size:11px;
  font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
}
.work-philosophy-head-v65 h3{
  margin:0;
  max-width:820px;
  color:#4f4351;
  font-family:Georgia,"Times New Roman",serif;
  font-size:20px;
  font-weight:500;
  line-height:1.55;
}
.work-philosophy-body-v65{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:18px;
  margin:17px 0 0 170px;
}
.work-philosophy-body-v65 p{
  margin:0!important;
  color:#665b68!important;
  font-size:13.5px!important;
  line-height:1.78!important;
}
.work-philosophy-line-v65{
  margin:18px 0 0 170px;
  padding:12px 15px;
  border-left:3px solid rgba(185,147,97,.62);
  background:rgba(250,246,238,.62);
  color:#5b4b4e;
  font-size:13.5px;
  font-weight:750;
  line-height:1.65;
}
@media(max-width:820px){
  .work-philosophy-head-v65{grid-template-columns:1fr;gap:8px}
  .work-philosophy-body-v65{margin-left:0}
  .work-philosophy-line-v65{margin-left:0}
}
@media(max-width:720px){
  .work-philosophy-v65{margin-top:13px;padding:16px;border-radius:17px}
  .work-philosophy-kicker-v65{font-size:10.5px}
  .work-philosophy-head-v65 h3{font-size:17px;line-height:1.55}
  .work-philosophy-body-v65{grid-template-columns:1fr;gap:10px;margin-top:13px}
  .work-philosophy-body-v65 p{font-size:12.5px!important;line-height:1.72!important}
  .work-philosophy-line-v65{margin-top:13px;padding:11px 12px;font-size:12.5px;line-height:1.6}
}
'''

style_marker = '</style>'
if style_marker not in s:
    raise SystemExit('Could not find style closing tag')
s = s.replace(style_marker, css + '\n' + style_marker, 1)

p.write_text(s, encoding='utf-8')
