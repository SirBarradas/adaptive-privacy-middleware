# adaptive-privacy-middleware
O projeto consiste no desenvolvimento de um middleware/proxy de segurança em Python destinado a proteger a privacidade dos dados que circulam entre diferentes sistemas de informação.

## Compilar o template LaTeX

Com TeX Live instalada em `C:\texlive\2026`, compile a partir da pasta `report` do repositório:

```powershell
Set-Location report
& "C:\texlive\2026\bin\windows\latexmk.exe" -pdf -interaction=nonstopmode -halt-on-error report.tex
```

O diagrama da arquitetura (`report/images/arquitetura.png`) é gerado por `report/images/gerar_arquitetura.py` (requer `matplotlib`).

O `latexmk` executa automaticamente o BibTeX e as passagens necessárias para atualizar as citações e o índice. As imagens podem ser guardadas em `report/images/` e inseridas com `\includegraphics{nome-do-ficheiro}`. As referências são mantidas em `report/references.bib` e citadas no texto com `\cite{chave}`. Se o TeX Live estiver instalado noutra pasta, atualize o caminho do executável neste comando e em `.vscode/settings.json`.
