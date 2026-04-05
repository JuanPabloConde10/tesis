#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests

API_URL = "https://es.wikisource.org/w/api.php"
USER_AGENT = "tesis-wikisource-titles/0.1 (contact: tu_email@algo) python-requests"


def category_to_txt(category_title: str, out_path: str = "titulos.txt", sleep_s: float = 0.2):
    titles = []
    cont = None

    while True:
        params = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "list": "categorymembers",
            "cmtitle": category_title,   # e.g. "Categoría:Cuentos"
            "cmlimit": "500",
        }
        if cont:
            params["cmcontinue"] = cont

        r = requests.get(API_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
        r.raise_for_status()
        data = r.json()

        members = data.get("query", {}).get("categorymembers", [])
        titles.extend(m["title"] for m in members)

        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break

        time.sleep(sleep_s)

    # Dejarlo limpio: únicos + ordenados (si querés preservar orden “API”, sacá el sorted)
    titles = sorted(set(titles))

    with open(out_path, "w", encoding="utf-8") as f:
        for t in titles:
            f.write(t + "\n")

    print(f"OK: {len(titles)} títulos guardados en {out_path}")


if __name__ == "__main__":
    category_to_txt("Categoría:Cuentos", "titulos.txt")
