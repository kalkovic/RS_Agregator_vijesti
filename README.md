# 📰 Platforma za agregaciju vijesti

Skalabilna platforma za agregaciju vijesti koja prikuplja, obrađuje i prikazuje članke iz više izvora u gotovo stvarnom vremenu.

Sustav agregira vijesti s hrvatskih portala, grupira ih po događajima, provjerava integritet podataka putem blockchaina te omogućuje pretragu, filtriranje i analitiku kroz moderno web sučelje.

---

## 🎯 Pregled projekta

Projekt implementira skalabilnu platformu za agregaciju vijesti, inspiriranu rješenjima poput Ground News, bez klasifikacije političke pristranosti.

Sustav je dizajniran da:

* prikuplja podatke iz više vanjskih RSS izvora
* normalizira heterogene podatke
* grupira povezane članke u događaje pomoću similarity enginea
* bilježi kriptografske hash-eve događaja na blockchain
* izlaže podatke putem REST API-ja kroz mikroservise
* omogućuje autentifikaciju korisnika i administratorski pristup
* pruža statističke uvide kroz analytics servis

---

## 🏗️ Arhitektura sustava

```text
                    FRONTEND
                      React
                        │
                        ▼
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
 │ News Service │ │ Analytics    │ │ Auth Service │
 │   FastAPI    │ │   FastAPI    │ │   FastAPI    │
 └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
        │                │                │
        ▼                ▼                ▼
    DynamoDB         DynamoDB         DynamoDB
        │
        ▼
 Blockchain Service
        │
        ▼
 Solidity Smart Contract
        │
        ▼
 Ethereum Test Network (Ganache)
```

### News Service

Odgovoran za dohvat RSS feedova, normalizaciju podataka, grupiranje sličnih članaka u događaje, pohranu u DynamoDB i interakciju s blockchain slojem.

### Auth Service

Upravlja registracijom, prijavom, JWT autentifikacijom i kontrolom pristupa temeljenom na ulogama (User/Admin).

### Analytics Service

Pruža statističke uvide: najaktivniji izvori, distribucija po kategorijama i metrike događaja.

---

## ⚙️ Ključne funkcionalnosti

### 🔄 Dohvat podataka

* Asinkroni dohvat pomoću `asyncio` i `aiohttp`
* Integracija s RSS feedovima:

  * Index.hr
  * Jutarnji.hr
  * 24sata.hr

### 🧠 Obrada podataka

* Normalizacija podataka iz različitih izvora u jedinstveni format
* Similarity engine za grupiranje članaka po događajima
* Jedan događaj = više izvora koji pokrivaju istu temu

### 🔗 Blockchain integritet

* Hashiranje metapodataka događaja
* Bilježenje hash-a na Ethereum test mreži (Ganache)
* Verifikacija da podaci nisu modificirani nakon obrade

### 🔍 Pretraga i filtriranje

* Pretraga po naslovu vijesti
* Filtriranje po kategoriji i izvoru

### 🔐 Autentifikacija

* Registracija i prijava korisnika
* JWT tokeni
* Uloge: User i Admin

### 📊 Analitika

* Najaktivniji izvori vijesti
* Distribucija članaka po kategorijama
* Metrike događaja

---

## 📦 Tehnologije

### Frontend

* React, React Router, Axios, CSS3

### Backend

* Python 3.10+, FastAPI, asyncio, aiohttp, Pydantic

### Baza podataka

* DynamoDB (boto3)

### Blockchain

* Solidity, Web3.py, Ganache

### Infrastruktura

* Docker, Docker Compose

---

## 📂 Struktura projekta

```text
RS_Agregator_vijesti/
│
├── services/
│   ├── news-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── services/
│   │   │   ├── db/
│   │   │   ├── models/
│   │   │   ├── config.py
│   │   │   └── main.py
│   │   └── requirements.txt
│   ├── auth-service/
│   └── analytics-service/
│
├── frontend/
├── blockchain/
├── docker/
├── .env.example
└── README.md
```

---

## ▶️ Pokretanje projekta

### News Service (Day 1)

```bash
cd services/news-service
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

# Pokretanje cijelog sustava
docker compose up -d --build

# Zaustavljanje sustava
docker compose down

Provjera:

```bash
curl http://localhost:8000/health
```

Očekivani odgovor:

```json
{"status":"ok","service":"news-service"}
```

Kopirajte `.env.example` u `.env` i prilagodite vrijednosti po potrebi.

---

### Blockchain Layer (Ganache & Smart Contract)
Prije pokretanja API-ja, potrebno je podignuti lokalnu Ethereum mrežu i deployati ugovor. 
Detaljne upute nalaze se u [Blockchain dokumentaciji](./blockchain/README.md).

---
## 🔌 API (planirano)

### News Service

| Endpoint | Opis |
|----------|------|
| `GET /health` | Status servisa |
| `GET /api/events` | Popis događaja (q, category, source) |
| `GET /api/events/{id}` | Detalj događaja |
| `GET /api/events/{id}/verify` | Blockchain verifikacija |
| `POST /api/fetch` | Ručno pokretanje dohvata (admin) |

### Auth Service

| Endpoint | Opis |
|----------|------|
| `POST /api/auth/register` | Registracija |
| `POST /api/auth/login` | Prijava |
| `GET /api/auth/me` | Trenutni korisnik |

### Analytics Service

| Endpoint | Opis |
|----------|------|
| `GET /api/analytics/sources` | Aktivnost izvora |
| `GET /api/analytics/categories` | Distribucija kategorija |

---

| Servis | Lokalni port | Opis |
| :--- | :--- | :--- |
| **Frontend** | `http://localhost:3000` | Glavno sučelje aplikacije |
| **News Service** | `http://localhost:8080` | API za vijesti |
| **Auth Service** | `http://localhost:8081` | API za autentifikaciju |
| **Analytics Service** | `http://localhost:8082` | API za statistiku |
| **DynamoDB** | `http://localhost:8001` | Lokalni NoSQL admin panel |
| **Ganache** | `http://localhost:8545` | Lokalna Blockchain mreža |

## 🧪 Plan razvoja (7 dana)

| Dan | Fokus |
|-----|-------|
| 1 | Monorepo, News Service skeleton, modeli, config |
| 2 | RSS dohvat i normalizacija |
| 3 | Similarity engine, agregacija, DynamoDB |
| 4 | API filtri + blockchain integritet |
| 5 | Auth Service (JWT, uloge) |
| 6 | Analytics Service + React frontend |
| 7 | Docker Compose i integracija |

---

## 📌 Napomena

Projekt demonstrira mikroservisnu arhitekturu, asinkrono programiranje, REST API-je, NoSQL pohranu i blockchain verifikaciju integriteta podataka.

---
