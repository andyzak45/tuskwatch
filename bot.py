import urllib.request
import xml.etree.ElementTree as ET

# Lista słów, na które bot ma reagować
SLOWA_KLUCZOWE = ["tusk", "rząd", "koalicj", "minister", "podat", "obietnic"]

# Przykładowe legalne źródło: Wiadomości z WP (kanał RSS)
URL_ZRODLA = "https://wp.pl"

print("Uruchamiam bota agregującego...")

try:
    # Pobieramy dane ze źródła
    response = urllib.request.urlopen(URL_ZRODLA)
    data = response.read()
    
    # Przetwarzamy format XML/RSS
    root = ET.fromstring(data)
    znalezione_newsy = []
    
    # Przeszukujemy artykuły
    for item in root.findall('.//item'):
        tytul = item.find('title').text
        link = item.find('link').text
        
        # Sprawdzamy, czy w tytule jest któreś z naszych słów
        if any(slowo in tytul.lower() for slowo in SLOWA_KLUCZOWE):
            znalezione_newsy.append(f"<li><a href='{link}' target='_blank'>{tytul}</a></li>")
            
    # Zapisujemy wynik do prostego pliku strony HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>AntyTusk - Agregator</title><meta charset='utf-8'></head><body>")
        f.write("<h1>Najnowsze wiadomości i fakty</h1>")
        f.write("<ul>")
        if znalezione_newsy:
            f.write("\n".join(znalezione_newsy))
        else:
            f.write("<li>Brak nowych wiadomości z ostatnich godzin.</li>")
        f.write("</ul>")
        f.write("</body></html>")
        
    print("Strona została pomyślnie wygenerowana w pliku index.html!")

except Exception as e:
    print(f"Wystąpił błąd: {e}")
