Oto wersja przygotowana bezpośrednio do wklejenia do pliku `README.md` w repozytorium na GitHubie – bez emotikonów, sformatowana w czystym stylu Markdown.

---

# Konwerter listy z ogladajanime.pl na MyAnimeList

Skrypt umożliwia konwersję wyeksportowanego pliku `.csv` z serwisu ogladajanime.pl na format `.xml` zgodny z importerem serwisu MyAnimeList.net. Podczas procesu skrypt automatycznie odpytuje API Jikan w celu dopasowania prawidłowych identyfikatorów serii (MAL ID).

---

## Wersja online (bez instalacji)

Najprostszą metodą konwersji jest użycie aplikacji webowej działającej w przeglądarce, która nie wymaga instalacji żadnego oprogramowania na komputerze:

[Uruchom konwerter online](https://convertanimefileonlinepy-xj6tymukryrrxafuru9ldq.streamlit.app/)

---

## Wersja lokalna (uruchamiana na komputerze lub telefonie)

### 1. Instalacja interpretera Python 3

Do uruchomienia skryptu lokalnie wymagany jest Python w wersji 3. Wybierz odpowiednią metodę instalacji dla swojego systemu operacyjnego:

```bash
# Android (Termux)
pkg install python

# Windows (Wiersz poleceń / PowerShell / Terminal VS Code)
winget install Python.Python.3
# (Alternatywnie można zainstalować aplikację ze sklepu Microsoft Store)

# Linux (Debian / Ubuntu / Mint)
sudo apt update && sudo apt install python3

# Linux (Arch Linux)
sudo pacman -S python
```

### 2. Uruchomienie skryptu

Otwórz terminal i przejdź do folderu, w którym znajduje się pobrany skrypt za pomocą komendy `cd`:

```bash
cd /sciezka/do/folderu/ze/skryptem
```

Następnie uruchom skrypt za pomocą odpowiedniej komendy:

```bash
# Windows
python convert_anime_file.py

# Linux / Android / macOS
python3 convert_anime_file.py
```

Po uruchomieniu skrypt wyświetli w konsoli prośbę o podanie ścieżki do pliku wejściowego:

```text
Wprowadź ścieżkę do pliku .csv (możesz też przeciągnąć i upuścić plik w tym oknie):
```

Wklej ścieżkę do pliku `.csv`, przeciągnij plik do okna terminala lub podaj jego nazwę (jeśli plik znajduje się w tym samym folderze co skrypt) i naciśnij Enter. Przekonwertowany plik `mal_import.xml` zostanie zapisany w folderze roboczym skryptu.
