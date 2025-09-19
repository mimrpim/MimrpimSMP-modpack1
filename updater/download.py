import requests
import os

# URL textového souboru se seznamem souborů ke stažení
list_download = "https://example.com/seznam-ke-stazeni.txt"

# Vytvoření složky pro stažené soubory, pokud neexistuje
download_folder = "download"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Vytvořena složka: {download_folder}")

# Stažení seznamu URL
try:
    response = requests.get(list_download)
    response.raise_for_status()  # Vyvolá chybu pro špatné HTTP status kódy
    url_list = response.text.splitlines()
except requests.exceptions.RequestException as e:
    print(f"Chyba při stahování seznamu URL: {e}")
    exit()

print(f"Nalezeno {len(url_list)} URL ke stažení.")

# Procházení každé URL a stahování souboru
for url in url_list:
    url = url.strip()
    if not url:
        continue  # Přeskočí prázdné řádky
    
    try:
        # Získání názvu souboru z URL
        file_name = os.path.basename(url)
        file_path = os.path.join(download_folder, file_name)

        print(f"Stahuji soubor: {url} -> {file_path}")
        
        # Stažení souboru
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Staženo.")
        
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování {url}: {e}")

print("Všechny soubory staženy (nebo přeskočeny kvůli chybě).")