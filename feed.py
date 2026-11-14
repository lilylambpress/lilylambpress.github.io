"""feed.py do site de pins (só biblioteca padrão; roda no GitHub Actions todo dia).

Lê pins.json e escreve feed.xml com os pins de data <= hoje. O Pinterest lê o RSS e publica os itens novos em até 24 h.
"""
import json
import sys
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape


def feed(agenda: list[dict], hoje: date, titulo: str, base: str) -> str:
    saiu = sorted((p for p in agenda if date.fromisoformat(p["date"]) <= hoje), key=lambda p: p["date"], reverse=True)[:50]
    itens = "".join(
        f"<item><title>{escape(p['title'])}</title><link>{escape(p['link'])}</link><guid>{escape(p['link'])}</guid>"
        f"<description>{escape(p['description'])}</description>"
        f"<pubDate>{format_datetime(datetime.combine(date.fromisoformat(p['date']), datetime.min.time(), timezone.utc))}</pubDate>"
        f"<enclosure url=\"{escape(p['image'])}\" type=\"image/jpeg\" length=\"0\"/></item>"
        for p in saiu)
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{escape(titulo)}</title>'
            f"<link>{escape(base)}</link><description>{escape(titulo)}</description>{itens}</channel></rss>\n")


if __name__ == "__main__":
    pasta = Path(__file__).resolve().parent
    agenda = json.loads((pasta / "pins.json").read_text(encoding="utf-8"))
    titulo = sys.argv[1] if len(sys.argv) > 1 else "Free Printables"
    base = agenda[0]["link"].rsplit("/p/", 1)[0] if agenda else ""
    (pasta / "feed.xml").write_text(feed(agenda, date.today(), titulo, base), encoding="utf-8")
