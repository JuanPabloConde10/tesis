import re
import time
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

API = "https://es.wikisource.org/w/api.php"

HEADERS = {
    # Poné un contacto real (mail o repo). Wikimedia lo recomienda.
    "User-Agent": "tesis-wikisource-downloader/0.1 (contact: tu_email@algo; purpose: academic research) Python/3.12 requests",
    "Accept": "application/json",
}

OUT_DIR = Path("short-tales")
OUT_DIR.mkdir(exist_ok=True)

def slugify(title: str) -> str:
    # nombre de archivo razonable (mantiene letras/acentos comunes)
    s = title.strip().replace("/", "_")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9A-Za-z_áéíóúÁÉÍÓÚñÑüÜ-]", "", s)
    return s[:180] or "untitled"

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # sacar ruido típico
    for tag in soup(["script", "style", "sup"]):
        tag.decompose()

    # opcional: borrar tablas/infoboxes si molestan
    # for tag in soup(["table"]):
    #     tag.decompose()

    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def fetch_parse_html(title: str, retries: int = 5) -> str:
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "formatversion": 2,
        "redirects": 1,
    }

    last = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(API, params=params, headers=HEADERS, timeout=30)
            if r.status_code in (429, 503):
                time.sleep(1.5 * attempt)
                continue
            r.raise_for_status()

            data = r.json()
            if "error" in data:
                raise RuntimeError(json.dumps(data["error"], ensure_ascii=False))

            return data["parse"]["text"]
        except Exception as e:
            last = e
            time.sleep(1.0 * attempt)

    raise RuntimeError(f"Falló '{title}': {last}")

def download_one(title: str) -> None:
    html = fetch_parse_html(title)
    txt = html_to_text(html)
    fname = slugify(title) + ".txt"
    (OUT_DIR / fname).write_text(txt, encoding="utf-8")

def main():
    titles_path = Path("titulos.txt")
    if not titles_path.exists():
        raise SystemExit("No existe titles.txt (1 título por línea).")

    failed = []
    titles = [line.strip() for line in titles_path.read_text(encoding="utf-8").splitlines()
              if line.strip() and not line.strip().startswith("#")]

    for i, title in enumerate(titles, 1):
        print(f"[{i}/{len(titles)}] {title}")
        try:
            download_one(title)
            time.sleep(0.7)  # sé buen vecino
        except Exception as e:
            print(f"  !! ERROR: {e}")
            failed.append(title)

    if failed:
        Path("failed.txt").write_text("\n".join(failed) + "\n", encoding="utf-8")
        print(f"\nHecho con errores: {len(failed)}. Ver failed.txt")
    else:
        print("\nHecho. Todo OK ✅")

if __name__ == "__main__":
    main()