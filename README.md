# CRJ — NeurIPS 2026 project page

**Conceal, Reconstruct, Jailbreak: Exploiting the Reconstruction–Concealment Tradeoff in MLLMs**

This repository contains the **public-facing research website only**. It does **not** include attack-generation source code, harmful query examples, or model-generated unsafe answers. The one worked example in the paper's framework figure is reproduced here with the model response **withheld**.

## What changed in this rebuild

- The page now shows **both halves of the tradeoff** (reconstruction *and* concealment), the **main results tables** (closed- and open-source), the **evaluation protocol**, and a **limitations / responsible-use** section.
- The **poster is not hosted**. The previous poster contained an actionable self-harm example; a redacted web version must be prepared before it is linked (see "Before publishing").
- All plots are the paper's **original figures**, exported to SVG. No research figure was replaced or AI-generated. The hero curve and social card are clearly labelled **conceptual illustrations**.
- The framework overview is the paper's own TikZ figure, recompiled with the example model response replaced by a placeholder. Source: `figure-sources/fig1-overview-redacted-tikz.tex`.
- Fonts (IBM Plex, OFL) are **self-hosted** under `docs/assets/fonts/` — no third-party requests.
- Numbers in the tables and the open-source chart are generated from the manuscript by a build step (see below), so they cannot drift from the paper by hand-editing.

## Preview locally

```bash
python3 -m http.server 8000 -d docs
```

Visit `http://localhost:8000`.

## Rebuild the data-driven HTML (optional)

`docs/index.html` is generated from `template.html` and `tables.json` (parsed from the manuscript) by `build.py`:

```bash
python3 build.py
```

If you only edit copy, editing `docs/index.html` directly is fine. If you change any reported number, edit `tables.json` and re-run the build so the tables and the open-source chart stay consistent.

## Publish with GitHub Pages

1. Create a **public** repository (e.g. `CRJ-Project-Page`) under the `Farhamdur` account.
2. Upload the contents of this package, preserving the `docs/` folder.
3. **Settings → Pages → Build and deployment:** Source = *Deploy from a branch*, Branch = `main`, Folder = `/docs`. Save.
4. Expected URL: `https://farhamdur.github.io/CRJ-Project-Page/`. Update the `canonical`, `og:url`, and `og:image`/`twitter:image` URLs in `docs/index.html` if the final URL differs.
5. `docs/.nojekyll` is included so GitHub Pages serves all files as-is.

## Before publishing

- [ ] **Code link.** The paper abstract points to `github.com/Farhamdur/CRJ`. Either make that repo public or correct the abstract on arXiv and in the proceedings — the page must not imply code is available when it is not.
- [ ] **Poster.** Prepare a redacted web poster (replace the case-study response with a withheld placeholder; correct the "procedural content omitted" footer). If an unredacted poster was ever pushed to any public repo, **rewrite git history or recreate the repo** — deleting the file in a new commit leaves it in history.
- [ ] **arXiv version.** Confirm arXiv `2605.05709` shows the camera-ready text before linking it as the paper of record.
- [ ] **BibTeX.** Replace the provisional entry with the official NeurIPS proceedings citation when available.
- [ ] **Session + recording.** Add the OpenReview/proceedings link, poster-session time and place, and the recording when available.
- [ ] **Authors, affiliations, contact.** Confirm against the final paper; add author homepages and a stable contact email.
- [ ] **Coauthor approval** for hosting figures and the (redacted) poster, and for any applicable publication policy.

## License

- **Content** (text, figures): choose and add a license (e.g. CC BY 4.0) with coauthor agreement.
- **Site code** (HTML/CSS/JS): e.g. MIT.
- **Fonts:** IBM Plex is under the SIL Open Font License; see `docs/assets/fonts/OFL-IBM-Plex.txt`.

A public GitHub repository does not by itself grant a reuse license.

## Source / attribution

Numerical results, titles, author names, and plot images were taken from the authors' manuscript source (`Jailbreak_NeurIPS_arXiv.zip`). The plots are rendered from the original PDF figures. The hero curve and social card are illustrative and not derived from empirical datapoints.

## Final refinement notes (November 11, 2026)

This release is a targeted refinement of the supplied `CRJ_Project_Page_Revised.zip`. The overall design, Fig. 1 framework raster and TikZ source, vector figures, and scientific results data were preserved. Updates include the precise paper title in the hero, a direct (currently private/restricted) code repository link, more accurate content notes, gain-in-percentage-points in the closed-source summary, clear expandable full tables, and a portable `build.py` that runs from this project directory. The recording is left pending its public conference URL. Do not publish the private SlidesLive Recorder share URL.

After editing `template.html` or `tables.json`, regenerate the page with `python build.py` in the repository root. Changes made directly in `docs/index.html` will be overwritten by the build.
