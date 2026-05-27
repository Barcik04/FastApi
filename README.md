# FastAPI Crypto System

Prosty backend w **FastAPI** do obsługi użytkowników, portfela, transakcji, wiadomości i trade requestów.

## Wymagania

- Python 3.12+
- Docker + Docker Compose (opcjonalnie, ale polecane)

## 1) Szybki start przez Dockera (najprościej)

1. Utwórz plik `.env` w katalogu projektu:

```env
DATABASE_URL=postgresql+asyncpg://igor:password@db:5432/crypto_system
```

2. Zbuduj i uruchom kontenery:

```bash
docker compose up --build
```

3. API będzie dostępne pod:
- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

4. Zatrzymanie:

```bash
docker compose down
```

---

## Testy

```bash
python -m pytest
```

## Najważniejsze endpointy

Routery są podpięte w `main.py`:

- użytkownicy
- portfolio
- transakcje
- trade requesty
- wiadomości

Najwygodniej podejrzeć pełną listę endpointów w Swaggerze (`/docs`).

## Struktura projektu (skrót)

- `main.py` – start aplikacji i rejestracja routerów
- `src/api/routers/` – endpointy HTTP
- `src/infrastructure/models/` – modele ORM
- `src/infrastructure/repositories/` – repozytoria
- `src/infrastructure/services/` – logika serwisowa
- `tests/` – testy
