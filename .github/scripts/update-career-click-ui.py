from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_marker = '/* V61 clickable career rows + centered controls */'
css = '''
/* V61 clickable career rows + centered controls */
.career-toolbar{justify-content:center!important;text-align:center!important;}
.career-toolbar .career-legend{flex-basis:100%;justify-content:center!important;margin-bottom:2px!important;}
.career-expand-all,.career-secondary-toggle{margin-left:0!important;margin-right:0!important;}
.career-summary{cursor:pointer!important;transition:background .18s ease!important;}
.career-summary:hover{background:rgba(167,127,157,.045)!important;}
.career-summary:focus-visible{outline:2px solid rgba(167,127,157,.45);outline-offset:-2px;border-radius:14px;}
@media(max-width:720px){
  .career-toolbar{justify-content:center!important;gap:8px!important;}
  .career-toolbar .career-legend{width:100%;justify-content:center!important;}
  .career-expand-all,.career-secondary-toggle{flex:0 0 auto!important;}
}
'''
if css_marker not in s:
    if '</style>' not in s:
        raise SystemExit('style closing tag not found')
    s = s.replace('</style>', css + '\n</style>', 1)

js_marker = '// V61 entire career summary is clickable'
js = '''
// V61 entire career summary is clickable
[...document.querySelectorAll('.career-summary')].forEach(summary => {
  summary.setAttribute('role', 'button');
  summary.setAttribute('tabindex', '0');
  const toggleFromSummary = () => {
    const button = summary.querySelector('.career-toggle');
    if(!button) return;
    const next = button.getAttribute('aria-expanded') !== 'true';
    setCareerExpanded(button, next);
    syncExpandAllState();
  };
  summary.addEventListener('click', event => {
    if(event.target.closest('.career-toggle')) return;
    toggleFromSummary();
  });
  summary.addEventListener('keydown', event => {
    if(event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    toggleFromSummary();
  });
});
'''
if js_marker not in s:
    needle = '\nif(expandAllButton){'
    if needle not in s:
        raise SystemExit('expand-all anchor not found')
    s = s.replace(needle, '\n' + js + '\nif(expandAllButton){', 1)

p.write_text(s, encoding='utf-8')
