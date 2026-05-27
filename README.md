# FastAPI Crypto System

Prosty backend w **FastAPI** do obsługi użytkowników, portfela, transakcji, wiadomości i trade requestów. Pozwala na takie czynności jak kupno krypto, wyslanie krypto do innego uzytkownika, 
wyslanie wiadomosci do uzytkownikow innych, obesrowanie wartości krypto w swoim portfolio z generacją grafow pokazujących jak wartość porftolio zmieniała się na przestrzeni czasu, zostało to osiągnięte dzięki komunikacji zewnętrznej z Coingecko API. Jest również autoryzacja JWT.

## Wymagania

- Python 3.12+
- Docker + Docker Compose (opcjonalnie, ale polecane)

## 1) Szybki start przez Dockera (najprościej)

2. Zbuduj i uruchom kontenery:

```bash
docker compose up -d --build
```

3. API będzie dostępne pod:
- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

4. Zatrzymanie:

```bash
docker compose down
```

---

## Testy

```bash
python -m pytest
```

## Coverage 

```bash
python -m pytest --cov=src --cov-report=html
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

## ENpdointy w swagerze: 
<img width="1801" height="158" alt="image" src="https://github.com/user-attachments/assets/26a7aba1-2a15-403e-8727-8219b4b02021" />
- Najpierw trzeba sie zarejestrowac
- potem zalogowac i w respone endpointu user/login dostaniemy Bearer token ktory trzeba skopiować i potem wkleić go tutaj:
  <img width="1858" height="616" alt="image" src="https://github.com/user-attachments/assets/67483dde-ef83-43e9-aa33-b554ab6e8c98" />

## JWT w postmanie:
- tak samo sie rejestrujemy a potem logujemy
- w headerze requestów dajemy - Authorization: Bearer TOKEN 


