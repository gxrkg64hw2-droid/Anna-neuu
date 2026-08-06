"""Rich-based human-readable output renderers for the search command."""
from __future__ import annotations


def render_search_pretty(result: dict) -> None:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    console = Console()
    console.print(
        f"[bold]Query:[/bold] {result['query']}  "
        f"[dim]({result['duration_ms']}ms, {result['total_hits']} hits)[/dim]"
    )
    for hit in result["hits"]:
        src = hit["source"]
        loc = hit["location"]
        header = (
            f"[bold cyan]#{hit['rank']}[/bold cyan]  "
            f"[bold]{src.get('bibkey') or src.get('filename')}[/bold]  "
            f"[dim]p. {loc.get('printed_page_start')}[/dim]  "
            f"[dim]score={hit['score_fused']:.3f}[/dim]"
        )
        body = Text(hit["chunk_text"][:600] + ("..." if len(hit["chunk_text"]) > 600 else ""))
        if hit.get("citation_suggestion"):
            body.append("\n\n")
            body.append(f"-> {hit['citation_suggestion']}", style="green")
        console.print(Panel(body, title=header, title_align="left", border_style="cyan"))
