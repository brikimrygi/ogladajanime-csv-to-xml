import streamlit as st
import csv
import re
import time
import json
import urllib.request
import urllib.parse
import urllib.error

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
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
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

st.title("Konwerter listy Anime do formatu MyAnimeList XML")
st.write("Prześlij swój plik CSV, aby automatycznie wyszukać ID serii i wygenerować plik XML do importu.")

uploaded_file = st.file_uploader("Wybierz plik .csv", type=["csv"])

if uploaded_file is not None:
    # Odczyt przesłanego pliku
    file_contents = uploaded_file.read().decode("utf-8").splitlines()
    reader = csv.reader(file_contents)
    header = next(reader)
    rows = list(reader)
    
    total_rows = len(rows)
    st.info(f"Wykryto {total_rows} serii. Proces może zająć trochę czasu ze względu na limity zapytań API.")
    
    if st.button("Rozpocznij konwersję"):
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<myanimelist>',
            '  <myinfo>',
            '    <user_id>0</user_id>',
            '    <user_name>Import</user_name>',
            '    <user_export_type>1</user_export_type>',
            '  </myinfo>'
        ]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
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
            status_text.text(f"Przetwarzanie [{idx}/{total_rows}]: {raw_title} -> MAL ID: {mal_id}")
            progress_bar.progress(idx / total_rows)
            
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
        xml_data = "\n".join(xml_lines)
        
        st.success("Konwersja zakończona pomyślnie!")
        
        # Przycisk do pobrania gotowego pliku XML
        st.download_button(
            label="Pobierz plik mal_import.xml",
            data=xml_data,
            file_name="mal_import.xml",
            mime="application/xml"
        )