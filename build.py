"""Build docs/index.html from template.html and tables.json (numbers parsed from main.tex)."""
import json, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent

D = json.load(open(ROOT / 'tables.json', encoding='utf-8'))
M = D['methods']
BASE = M[:5]
PROP = M[5:]

def f2(x):
    return f"{x:.2f}"

def best(vals, names):
    m = max(vals)
    return m, [n for v, n in zip(vals, names) if v == m]

def worst(vals, names):
    m = min(vals)
    return m, [n for v, n in zip(vals, names) if v == m]

# ---------- closed-source summary ----------
rows = []
for model, mets in D['closed'].items():
    for i, (key, label) in enumerate([('ASR_GPT', 'GPT-5.4-mini'), ('ASR_HB', 'HarmBench')]):
        v = mets[key]
        bv, bn = best(v[:5], BASE)
        pv, pn = best(v[5:], PROP)
        wv, wn = worst(v[5:], PROP)
        first = (f'<th scope="rowgroup" rowspan="2">{html.escape(model)}</th>' if i == 0 else '')
        rows.append(
            f'<tr{" class=\"group-start\"" if i == 0 else ""}>{first}<td>{label}</td>'
            f'<td class="num">{f2(bv)}<span class="who">{" / ".join(bn)}</span></td>'
            f'<td class="num strong">{f2(pv)}<span class="who">{" / ".join(pn)}</span></td>'
            f'<td class="num gain">+{f2(pv-bv)}</td></tr>')
CLOSED_SUMMARY = (
    '<div class="table-scroll"><table class="data">'
    '<caption>Closed-source victims: attack success rate (%) by judge. Strongest baseline, best proposed strategy are picked per row from paper Table&nbsp;1.</caption>'
    '<thead><tr><th scope="col">Victim model</th><th scope="col">Judge</th><th scope="col" class="num">Strongest baseline</th>'
    '<th scope="col" class="num">Best proposed</th><th scope="col" class="num">Gain (pp)</th></tr></thead><tbody>'
    + ''.join(rows) + '</tbody></table></div>')

# ---------- full Table 1 ----------
hdr = ''.join(f'<th scope="col" class="num">{m}</th>' for m in M)
body = []
for model, mets in D['closed'].items():
    for i, (key, label) in enumerate([('Toxicity', 'Toxicity (1–5)'), ('Detailedness', 'Detailedness (0–10)'), ('ASR_GPT', 'ASR, GPT judge (%)'), ('ASR_HB', 'ASR, HarmBench (%)')]):
        first = f'<th scope="rowgroup" rowspan="4">{html.escape(model)}</th>' if i == 0 else ''
        body.append(f'<tr{" class=\"group-start\"" if i == 0 else ""}>{first}<td>{label}</td>' + ''.join(f'<td class="num{" sep" if j == 5 else ""}">{f2(x)}</td>' for j, x in enumerate(mets[key])) + '</tr>')
FULL_T1 = ('<div class="table-scroll"><table class="data dense"><caption>Paper Table&nbsp;1, all metrics. Baselines: FigStep to SI. Proposed: TxtV to TTV-GDI.</caption>'
           f'<thead><tr><th scope="col">Victim</th><th scope="col">Metric</th>{hdr}</tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>')

# ---------- full Table 2 ----------
body = []
for model, v in D['open'].items():
    body.append(f'<tr><th scope="row">{html.escape(model)}</th>' + ''.join(f'<td class="num{" sep" if j == 5 else ""}">{f2(x)}</td>' for j, x in enumerate(v)) + '</tr>')
FULL_T2 = ('<div class="table-scroll"><table class="data dense"><caption>Paper Table&nbsp;2: HarmBench ASR (%) on open-source victims.</caption>'
           f'<thead><tr><th scope="col">Victim</th>{hdr}</tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>')

# ---------- open-source dumbbell chart (inline SVG) ----------
fam_breaks = {'Llama-4-Maverick', 'InternVL3-8B', 'Qwen3-VL-8B'}
items = list(D['open'].items())
W, L, R = 760, 222, 96          # width, left label column, right annotation column
rowh, top = 30, 34
gap = 12
ys, y = [], top
for name, _ in items:
    if name in fam_breaks:
        y += gap
    ys.append(y)
    y += rowh
H = y + 28
x0, x1 = L, W - R
def X(v): return x0 + (x1 - x0) * v / 100
svg = [f'<svg class="dumbbell" viewBox="0 0 {W} {H}" role="img" aria-labelledby="db-title db-desc" xmlns="http://www.w3.org/2000/svg">',
       '<title id="db-title">Open-source victims: strongest baseline versus best proposed strategy</title>',
       '<desc id="db-desc">HarmBench attack success rate for 14 open-source models. For every model the best proposed strategy is above the strongest evaluated baseline. The full values are in the table below the chart.</desc>']
for t in (0, 25, 50, 75, 100):
    svg.append(f'<line class="grid" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{top-14}" y2="{H-24}"/>')
    svg.append(f'<text class="tick" x="{X(t):.1f}" y="{H-8}" text-anchor="middle">{t}</text>')
svg.append(f'<text class="axis-label" x="{x1:.1f}" y="{top-20}" text-anchor="end">HarmBench ASR (%)</text>')
svg.append(f'<text class="gain-head" x="{W-4}" y="{top-20}" text-anchor="end">Gain (pts)</text>')
for (name, v), yy in zip(items, ys):
    bv, bn = best(v[:5], BASE)
    pv, pn = best(v[5:], PROP)
    cy = yy + rowh / 2
    svg.append(f'<g><title>{html.escape(name)}: strongest baseline {f2(bv)} ({", ".join(bn)}), best proposed {f2(pv)} ({", ".join(pn)})</title>')
    svg.append(f'<text class="model" x="{L-14}" y="{cy+4.5:.1f}" text-anchor="end">{html.escape(name)}</text>')
    svg.append(f'<line class="link" x1="{X(bv):.1f}" x2="{X(pv):.1f}" y1="{cy:.1f}" y2="{cy:.1f}"/>')
    svg.append(f'<circle class="base" cx="{X(bv):.1f}" cy="{cy:.1f}" r="5.5"/>')
    svg.append(f'<circle class="prop" cx="{X(pv):.1f}" cy="{cy:.1f}" r="6"/>')
    svg.append(f'<text class="gain" x="{W-4}" y="{cy+4.5:.1f}" text-anchor="end">+{pv-bv:.2f}</text></g>')
svg.append('</svg>')
DUMBBELL = '\n'.join(svg)

# ---------- GDI vs DI ----------
g = D['gdi']; gm = D['gdi_models']
body = []
for i, m in enumerate(gm):
    a, b, c, d = g['TxtV-DI'][i], g['TxtV-GDI'][i], g['TTV-DI'][i], g['TTV-GDI'][i]
    body.append(f'<tr><th scope="row">{html.escape(m)}</th><td class="num">{f2(a)}</td><td class="num">{f2(b)}</td><td class="num gain">+{b-a:.2f}</td>'
                f'<td class="num sep">{f2(c)}</td><td class="num">{f2(d)}</td><td class="num gain">+{d-c:.2f}</td></tr>')
GDI_TABLE = ('<div class="table-scroll"><table class="data"><caption>HarmBench ASR (%) with generic distractors (DI, 100 random LLaVA-CC3M images, the CS-DJ image source) versus generated keyword/phrase-related distractors (GDI). Paper Table&nbsp;4; gains computed from it.</caption>'
             '<thead><tr><th scope="col" rowspan="2">Victim model</th><th scope="colgroup" colspan="3" class="num">TxtV</th><th scope="colgroup" colspan="3" class="num sep">TTV</th></tr>'
             '<tr><th scope="col" class="num">DI</th><th scope="col" class="num">GDI</th><th scope="col" class="num">Gain</th><th scope="col" class="num sep">DI</th><th scope="col" class="num">GDI</th><th scope="col" class="num">Gain</th></tr></thead><tbody>'
             + ''.join(body) + '</tbody></table></div>')

# sanity facts used in prose
assert all(best(v[5:], PROP)[0] > best(v[:5], BASE)[0] for v in D['open'].values())
for mets in D['closed'].values():
    for k in ('ASR_GPT', 'ASR_HB'):
        assert worst(mets[k][5:], PROP)[0] > best(mets[k][:5], BASE)[0]
gains = [g['TxtV-GDI'][i]-g['TxtV-DI'][i] for i in range(7)] + [g['TTV-GDI'][i]-g['TTV-DI'][i] for i in range(7)]
print('GDI gain range', round(min(gains), 2), round(max(gains), 2))

t = open(ROOT / 'template.html', encoding='utf-8').read()
for k, v in dict(CLOSED_SUMMARY=CLOSED_SUMMARY, FULL_T1=FULL_T1, FULL_T2=FULL_T2, DUMBBELL=DUMBBELL, GDI_TABLE=GDI_TABLE).items():
    assert '{{%s}}' % k in t, k
    t = t.replace('{{%s}}' % k, v)
assert '{{' not in t
open(ROOT / 'docs' / 'index.html', 'w', encoding='utf-8').write(t)
print('ok', len(t))
