import requests
import pandas as pd
import time
import random
import os

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

t_medias = pd.read_csv("doc/t_medias.csv", sep=";")
urls = t_medias["url"].dropna().astype(str)

CDX_API = "https://web.archive.org/cdx/search/cdx"


session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "HEAD"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

def get_wayback_url(url):
    """Retourne le snapshot Wayback le plus récent pour une URL"""
    try:
        params = {"url": url, "output": "json"}
        r = session.get(CDX_API, params=params, timeout=(5,60))
        if r.status_code != 200:
            print(f"⚠️ Erreur {r.status_code} pour {url}")
            return None

        data = r.json()
        if len(data) <= 1:  # seulement l'entête
            return None

        headers, *rows = data
        snapshots = [dict(zip(headers, row)) for row in rows]

        # prendre le snapshot le plus récent
        latest = snapshots[-1]
        ts = latest["timestamp"]
        return f"https://web.archive.org/web/{ts}/{latest['original']}"
    except Exception as e:
        print(f"⚠️ Exception en traitant {url} : {e}")
    return None

def download_file(archive_url, output_dir="downloads"):
    """Télécharge le fichier archivé (image/pdf/zip/...)"""
    try:
        r = session.get(archive_url, timeout=(5, 60))
        if r.status_code != 200:
            print(f"⚠️ Erreur {r.status_code} en téléchargeant {archive_url}")
            return None

        # Chercher le vrai nom dans les headers
        filename = None
        cd = r.headers.get("Content-Disposition")
        if cd and "filename=" in cd:
            filename = cd.split("filename=")[-1].strip('"')
        if not filename:
            filename = os.path.basename(archive_url.split("?")[0]) or "fichier.jpg"
            if not filename.lower().endswith((".jpg", ".jpeg")):
                filename += ".jpg"

        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(r.content)

        print(f"✅ Fichier téléchargé : {filepath}")
        return filepath
    except Exception as e:
        print(f"⚠️ Impossible de télécharger {archive_url} : {e}")
        return None

def main(output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for url in urls[3338:]:  
        print(f"\n🔎 Recherche d’archive pour {url}")
        archive_url = get_wayback_url(url)

        if archive_url:
            print(f"📂 Archive trouvée : {archive_url}")
            filepath = download_file(archive_url, output_dir=output_dir)
            results.append({
                "url_originale": url,
                "url_wayback": archive_url,
                "fichier_local": filepath if filepath else "Erreur téléchargement"
            })
        else:
            print("❌ Pas d’archive trouvée")
            results.append({
                "url_originale": url,
                "url_wayback": None,
                "fichier_local": None
            })

        # Pause aléatoire 10–15 sec
        pause = random.uniform(10, 15)
        print(f"⏳ Attente {pause:.2f} secondes...")
        time.sleep(pause)

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(output_dir, "wayback_urls.csv"), index=False)
    print(f"\n✅ Résultats enregistrés dans {output_dir}/wayback_urls.csv")

if __name__ == "__main__":
    main()
