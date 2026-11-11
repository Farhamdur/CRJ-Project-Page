# Figure sources

- `fig1-overview-redacted-tikz.tex` — the paper's Fig. 1 TikZ body, with the
  example model-response node replaced by a withheld placeholder.
- `fig1-standalone-wrapper.tex` — standalone wrapper to compile it:

  ```bash
  pdflatex fig1-standalone-wrapper.tex
  pdftocairo -png -r 220 -singlefile fig1-standalone-wrapper.pdf fig1
  ```

The plot SVGs in `docs/assets/figures/` were produced from the manuscript's
original PDF figures with `pdftocairo -svg`. No research figure was redrawn or
AI-generated.
