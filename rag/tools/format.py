"""Rich-based human-readable output renderers for corpus and extract-citations commands."""
from __future__ import annotations


def render_corpus_pretty(result: dict) -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    t = Table(title=f"Corpus: {result['thesis']} ({result['total_sources']} sources)")
    t.add_column("File", style="cyan", no_wrap=False)
    t.add_column("BibKey", style="green")
    t.add_column("Year")
    t.add_column("PDF Pages", justify="right")
    t.add_column("Print pp", justify="right")
    t.add_column("Offset", justify="right")
    t.add_column("Conf", justify="right")
    t.add_column("Chunks", justify="right")
    t.add_column("Avg Q", justify="right")
    for s in result["sources"]:
        t.add_row(
            s["filename"],
            s.get("bibkey") or "-",
            str(s.get("year") or "-"),
            str(s["page_count_pdf"]),
            str(s.get("page_count_printed") or "-"),
            str(s.get("print_offset", 0)),
            f"{s.get('print_offset_confidence', 1.0):.2f}",
            str(s["chunk_count"]),
            f"{s.get('avg_quality') or 0:.2f}",
        )
    console.print(t)


def render_extract_citations_pretty(result: dict) -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    console.print(
        f"[bold]{result['total_citations']}[/bold] citations across "
        f"[bold]{result['unique_sources']}[/bold] unique sources in "
        f"{result['tex_files_scanned']} .tex file(s)."
    )
    if not result["issues"]:
        console.print("[green]OK no issues.[/green]")
        return
    t = Table(title=f"Issues ({len(result['issues'])})")
    t.add_column("Type", style="red")
    t.add_column("BibKey", style="cyan")
    t.add_column("Where")
    t.add_column("Note")
    for i in result["issues"]:
        where = f"{i.get('file', '')}:{i.get('line', '')}" if i.get("line") else "-"
        note = i.get("note") or i.get("suggestion") or ""
        t.add_row(i["type"], i.get("bibkey", "-"), where, note)
    console.print(t)
    s = result["summary"]
    console.print(
        f"[dim]Summary: missing_bibkeys={s.get('missing_bibkeys', 0)}, "
        f"orphan_bib_entries={s.get('orphan_bib_entries', 0)}[/dim]"
    )
