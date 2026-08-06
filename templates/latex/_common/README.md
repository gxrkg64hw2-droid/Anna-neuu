# `_common/` LaTeX Layer

Shared LaTeX scaffolding used by all five thesis profiles. Each profile's `main.tex` does:

```latex
\input{_common/preamble.tex}
\addbibresource{../bibliography.bib}

\begin{document}
\input{_common/titlepage.tex}
\ifsperrvermerk\input{_common/sperrvermerk.tex}\fi
\tableofcontents
\input{_common/abkuerzungsverzeichnis.tex}

% --- Profile-specific chapters here ---

\printbibliography
\input{_common/eidesstattliche-erklaerung.tex}
\end{document}
```

## Customization

- **Title metadata**: override the `\newcommand{\thesisXxx}{...}` calls from `preamble.tex` in your `main.tex` after the `\input{_common/preamble.tex}` line.
- **Sperrvermerk**: switch on with `\sperrvermerktrue` in `main.tex` before `\begin{document}`.
- **Gendering**: default is `\genderneutral`. To switch: `\renewcommand{\genderstil}{\genderstern}`.

## Compile

```bash
latexmk -lualatex main.tex
make pdf
make watch
make clean
```

Requires MacTeX (`brew install --cask mactex-no-gui`) or equivalent TeX distribution with lualatex + biber.
