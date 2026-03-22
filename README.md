# Rejestrator Temperatur

Aplikacja do automatycznego pobierania i archiwizowania danych o temperaturze z serwisów Airly oraz IMGW. Dane są zapisywane w bazie danych PostgreSQL i mogą być wizualizowane np. za pomocą Grafany.

### Główne Funkcje

- **Pobieranie danych z Airly:** Obsługa wielu stacji na podstawie ich identyfikatorów.
- **Pobieranie danych z IMGW:** Obsługa stacji synoptycznych (np. "poznan").
- **Automatyzacja:** Harmonogram zadań (APScheduler) uruchamia pobieranie co 6 godzin.
- **Niezawodność:** Mechanizm re-try (tenacity) dla zapytań API oraz obsługa błędów dla poszczególnych stacji.
- **Baza Danych:** Wykorzystanie puli połączeń (`psycopg2.pool`) dla zwiększenia wydajności.
- **Konteneryzacja:** Pełne wsparcie dla Docker i Docker Compose.

### Struktura Projektu

- `app/main.py`: Punkt wejścia aplikacji, konfiguracja harmonogramu.
- `app/collector.py`: Logika pobierania danych z zewnętrznych API.
- `app/db.py`: Obsługa połączeń i operacji na bazie danych.
- `app/config.py`: Zarządzanie konfiguracją i zmiennymi środowiskowymi.
- `app/logger.py`: Konfiguracja logowania.
- `docker-compose.yml`: Definicja usług (aplikacja, baza danych, Grafana).
- `docker/postgres/init.sql`: Schemat bazy danych.

### Konfiguracja

Aplikacja konfiguruje się za pomocą zmiennych środowiskowych (można je umieścić w pliku `.env`):

| Zmienna | Opis | Domyślnie |
| --- | --- | --- |
| `AIRLY_API_KEY` | Klucz API do serwisu Airly | (wymagany) |
| `AIRLY_STATION_IDS` | Lista ID stacji Airly (oddzielona przecinkami) | `""` |
| `IMGW_STATION_IDS` | Lista nazw stacji IMGW (oddzielona przecinkami) | `"poznan"` |
| `LOGGING_LEVEL` | Poziom logowania (DEBUG, INFO, etc.) | `INFO` |
| `DB_HOST` | Host bazy danych | `localhost` |
| `DB_USER` | Użytkownik bazy danych | `pgsql` |
| `DB_PASSWORD` | Hasło bazy danych | `""` |
| `DB_NAME` | Nazwa bazy danych | `weather` |
| `AIRLY_API_URL` | URL do API Airly | (wbudowany domyślny) |
| `IMGW_API_URL` | URL do API IMGW | (wbudowany domyślny) |

### Uruchomienie

#### Za pomocą Docker Compose (zalecane)

1. Upewnij się, że masz zainstalowany Docker i Docker Compose.
2. Utwórz plik `.env` z wymaganymi kluczami.
3. Uruchom stos technologiczny:
   ```bash
   docker-compose up -d
   ```
4. Aplikacja zacznie zbierać dane, a Grafana będzie dostępna pod adresem `http://localhost:3000`.

#### Lokalnie

1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Skonfiguruj bazę danych PostgreSQL i ustaw odpowiednie zmienne środowiskowe.
3. Uruchom aplikację:
   ```bash
   python app/main.py
   ```

### Schemat Danych

Dane są zapisywane w tabeli `temperature_readings`:
- `id`: Klucz główny (SERIAL).
- `station`: Identyfikator/nazwa stacji.
- `timestamp`: Czas pomiaru (DEFAULT CURRENT_TIMESTAMP).
- `provider`: Źródło danych (Airly/IMGW).
- `value`: Wartość temperatury (FLOAT).