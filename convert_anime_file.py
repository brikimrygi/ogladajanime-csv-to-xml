import csv
import re
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import os

status_map = {
    "Obejrzane": "Completed",
    "Oglądam": "Watching",
    "Wstrzymane": "On-Hold",
    "Porzucone": "Dropped",
    "Planuje": "Plan to Watch",
    "Nie oglądam": "Dropped"
}

def clean_xml_string(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def get_mal_id(title):
    encoded_title = urllib.parse.quote(title)
    url = f"https://api.jikan.moe/v4/anime?q={encoded_title}&limit=1"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                if res_data.get('data'):
                    return res_data['data'][0]['mal_id']
                return 0
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(4)
            else:
                return 0
        except Exception:
            return 0
    return 0

# --- POBRANIE ŚCIEŻKI OD UŻYTKOWNIKA ---
print("Wprowadź ścieżkę do pliku .csv (możesz też przeciągnąć i upuścić plik w tym oknie):")
input_path = input("> ").strip()

# Usunięcie ewentualnych cudzysłowów, które systemy dodają przy przeciąganiu pliku
input_path = input_path.strip('\'" ')

if not input_path:
    print("Błąd: Nie podano ścieżki pliku.")
    input("\nNaciśnij Enter, aby zamknąć...")
    exit()

if not os.path.exists(input_path):
    print(f"Błąd: Plik pod ścieżką '{input_path}' nie istnieje.")
    input("\nNaciśnij Enter, aby zamknąć...")
    exit()

# Próba otwarcia wskazanego pliku
try:
    with open(input_path, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
except Exception as e:
    print(f"Wystąpił błąd podczas otwierania pliku CSV: {e}")
    input("\nNaciśnij Enter, aby zamknąć...")
    exit()

total_rows = len(rows)
print(f"\nWykryto plik: {os.path.basename(input_path)}")
print(f"Rozpoczęto pobieranie ID dla {total_rows} serii. Szacowany czas: {int(total_rows * 1.6 / 60)} minut...")

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<myanimelist>',
    '  <myinfo>',
    '    <user_id>0</user_id>',
    '    <user_name>Import</user_name>',
    '    <user_export_type>1</user_export_type>',
    '  </myinfo>'
]

for idx, row in enumerate(rows, 1):
    if not row or len(row) < 7:
        continue
        
    raw_title = row[2]
    title = clean_xml_string(raw_title)
    status_pl = row[3]
    status_en = status_map.get(status_pl, "Plan to Watch")
    
    score = row[4]
    if score == "-":
        score = "0"
        
    progress = row[5]
    episodes_match = re.match(r"(\d+)/(\d+)", progress)
    if episodes_match:
        watched_eps = episodes_match.group(1)
        total_eps = episodes_match.group(2)
    else:
        watched_eps = "0"
        total_eps = "0"
        
    anime_type = row[6]
    
    mal_id = get_mal_id(raw_title)
    print(f"[{idx}/{total_rows}] {raw_title} -> MAL ID: {mal_id}")
    
    time.sleep(1.5)
    
    xml_lines.append('  <anime>')
    xml_lines.append(f'    <series_animedb_id>{mal_id}</series_animedb_id>')
    xml_lines.append(f'    <series_title><![CDATA[{title}]]></series_title>')
    xml_lines.append(f'    <series_type>{anime_type}</series_type>')
    xml_lines.append(f'    <series_episodes>{total_eps}</series_episodes>')
    xml_lines.append('    <my_id>0</my_id>')
    xml_lines.append(f'    <my_watched_episodes>{watched_eps}</my_watched_episodes>')
    xml_lines.append('    <my_start_date>0000-00-00</my_start_date>')
    xml_lines.append('    <my_finish_date>0000-00-00</my_finish_date>')
    xml_lines.append(f'    <my_score>{score}</my_score>')
    xml_lines.append(f'    <my_status>{status_en}</my_status>')
    xml_lines.append('    <my_rewatching>0</my_rewatching>')
    xml_lines.append('    <my_rewatching_ep>0</my_rewatching_ep>')
    xml_lines.append('    <my_tags><![CDATA[]]></my_tags>')
    xml_lines.append('    <update_on_import>1</update_on_import>')
    xml_lines.append('  </anime>')

xml_lines.append('</myanimelist>')

# --- ZAPIS PLIKU XML W MIEJSCU URUCHOMIENIA SKRYPTU .PY ---
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "mal_import.xml")

try:
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(xml_lines))
    print(f"\nGotowe! Nowy plik został zapisany jako: {output_path}")
except Exception as e:
    print(f"Błąd podczas zapisu pliku XML: {e}")

input("\nNaciśnij Enter, aby zakończyć działanie programu...")