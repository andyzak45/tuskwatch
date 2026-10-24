import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Słowa kluczowe do filtrowania wiadomości
SLOWA_KLUCZOWE = ["tusk", "rząd", "koalicj", "minister", "podat", "obietnic", "premiera", "premierowi"]

# Słownik z legalnymi i publicznymi źródłami RSS w Polsce
ZRODLA_RSS = {
    "Wirtualna Polska": "https://wp.pl",
    "Rzeczpospolita": "https://rp.pl",
    "Bankier.pl": "https://bankier.pl",
    "Dziennik.pl": "https://dziennik.pl"
}

print("Uruchamiam silnik TuskWatch...")
znalezione_newsy = []
pobrane_linki = set() # Pomaga unikać powtarzania tych samych newsów

for nazwa_zrodla, url in ZRODLA_RSS.items():
    try:
        print(f"Przeszukuję źródło: {nazwa_zrodla}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read()
        
        root = ET.fromstring(data)
        
        for item in root.findall('.//item'):
            tytul = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            
            if not tytul or not link or link in pobrane_linki:
                continue
                
            # Sprawdzamy, czy news dotyczy tematu serwisu
            if any(slowo in tytul.lower() for slowo in SLOWA_KLUCZOWE):
                pobrane_linki.add(link)
                # Tworzymy ładny klocek HTML dla każdego newsa z oznaczeniem źródła
                element_html = f"""
                <li class="news-item">
                    <span class="source-badge">{nazwa_zrodla}</span>
                    <a href="{link}" target="_blank">{tytul}</a>
                    <div class="comment">Kliknij w nagłówek, aby przeczytać pełny artykuł źródłowy.</div>
                </li>
                """
                znalezione_newsy.append(element_html)
                
    except Exception as e:
        print(f"Pominięto źródło {nazwa_zrodla} z powodu błędu: {e}")

# Generowanie finalnej strony TuskWatch
data_aktualizacji = datetime.now().strftime("%Y-%m-%d %H:%M")

szablon_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TuskWatch - Niezależny Agregator Informacyjny</title>
    <link rel="stylesheet" href="https://jsdelivr.net">
    <style>
        body {{ max-width: 800px; margin: 40px auto; padding: 0 20px; font-family: system-ui, sans-serif; background: #f9f9f9; color: #333; }}
        header {{ text-align: center; border-bottom: 3px solid #d9383a; padding-bottom: 20px; margin-bottom: 30px; }}
        h1 {{ color: #d9383a; margin-bottom: 5px; font-size: 2.5rem; letter-spacing: -1px; }}
        .subtitle {{ color: #586069; font-size: 1.1rem; font-style: italic; }}
        .meta-info {{ font-size: 0.85rem; color: #888; margin-top: 10px; }}
        .news-list {{ list-style: none; padding: 0; }}
        .news-item {{ background: #fff; border-left: 5px solid #d9383a; padding: 20px; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .news-item a {{ font-weight: bold; text-decoration: none; color: #0366d6; font-size: 1.15rem; display: block; margin-top: 5px; }}
        .news-item a:hover {{ text-decoration: underline; color: #004494; }}
        .source-badge {{ background: #e1e4e8; color: #444; padding: 3px 8px; font-size: 0.75rem; font-weight: bold; border-radius: 3px; text-transform: uppercase; }}
        .comment {{ margin-top: 10px; color: #666; font-style: italic; font-size: 0.95rem; background: #f6f8fa; padding: 10px; border-radius: 4px; border: 1px solid #eee; }}
        footer {{ text-align: center; margin-top: 60px; font-size: 0.85rem; color: #6a737d; border-top: 1px solid #e1e4e8; padding-top: 20px; }}
    </style>
</head>
<body>

    <header>
        <h1>TuskWatch</h1>
        <div class="subtitle">Agregator prawdziwych wiadomości i faktów o rządzie Donalda Tuska</div>
        <div class="meta-info">Ostatnia automatyczna aktualizacja danych: {data_aktualizacji}</div>
    </header>

    <main>
        <p>Prezentujemy wyłącznie zweryfikowane doniesienia medialne, opatrzone bezpośrednimi odnośnikami do niezależnych źródeł prasowych. Zero fake newsów, czyste fakty.</p>
        
        <ul class="news-list">
            {"".join(znalezione_newsy) if znalezione_newsy else '<li class="news-item">Brak nowych wiadomości z ostatnich godzin spełniających kryteria wyszukiwania.</li>'}
        </ul>
    </main>

    <footer>
        <p>&copy; 2026 TuskWatch. Strona w 100% statyczna i bezpieczna. Dane odświeżane automatycznie.</p>
    </footer>

</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(szablon_html)

print("Strona TuskWatch została pomyślnie zaktualizowana!")
