# 📰 Platforma za agregaciju vijesti

Skalabilna platforma za agregaciju vijesti koja prikuplja, obrađuje i prikazuje članke iz više izvora u gotovo stvarnom vremenu.

Sustav agregira vijesti s hrvatskih portala, grupira ih po događajima te omogućuje pretragu i filtriranje kroz moderno web sučelje.

---

## 🎯 Pregled projekta

Projekt implementira pojednostavljenu, ali skalabilnu verziju platforme za agregaciju vijesti, inspiriranu rješenjima poput Ground News.

Sustav je dizajniran da:

* prikuplja podatke iz više vanjskih izvora
* normalizira heterogene podatke
* grupira povezane članke u događaje
* izlaže podatke putem REST API-ja
* omogućuje pregled i filtriranje kroz frontend aplikaciju

---

## 🏗️ Arhitektura sustava

```
                ┌────────────────────┐
                │   React frontend   │
                └─────────┬──────────┘
                          │ HTTP
                          ▼
                ┌────────────────────┐
                │   FastAPI backend  │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 ┌────────────┐   ┌──────────────┐   ┌──────────────┐
 │  Fetcher   │   │ Normalizer   │   │ Aggregator   │
 │ (aiohttp)  │   │              │   │              │
 └────────────┘   └──────────────┘   └──────────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     DynamoDB       │
                └────────────────────┘
```

---

## ⚙️ Ključne funkcionalnosti

### 🔄 Dohvat podataka

* Asinkroni dohvat pomoću `asyncio` i `aiohttp`
* Integracija s RSS feedovima:

  * Index.hr
  * Jutarnji.hr
  * 24sata.hr
* Jednostavno proširenje na nove izvore

---

### 🧠 Obrada podataka

* Normalizacija podataka iz različitih izvora u jedinstveni format
* Grupiranje članaka po događajima
* Jedan događaj = više izvora koji pokrivaju istu temu

---

### 🔍 Pretraga i filtriranje

* Pretraga po naslovu vijesti
* Filtriranje po:

  * kategoriji
  * izvoru
* Pripremljeno za daljnje optimizacije (indeksi)

---

### 🗄️ Pohrana podataka

* NoSQL baza podataka (DynamoDB)
* Model temeljen na događajima
* Optimizirano za čitanje podataka

---

### 🌐 Web sučelje

* React SPA aplikacija
* Dinamičko dohvaćanje podataka preko REST API-ja
* Funkcionalnosti:

  * pretraga
  * filtriranje
  * prikaz broja izvora po vijesti

---

## 📦 Tehnologije

### Backend

* FastAPI
* Python (asyncio, aiohttp)
* Pydantic
* DynamoDB (boto3)

### Frontend

* React
* Axios

### Ostalo

* Docker
* Git / GitHub

---

## 📂 Struktura projekta

```
news-aggregator/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── db/
│   │   └── main.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   └── App.js
    └── public/
```

---

## ▶️ Pokretanje projekta

### Backend

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### Frontend

```
cd frontend
npm install
npm start
```

---

## 🔌 API

### Dohvat događaja

```
GET /api/events
```

### Query parametri:

* `q` → pretraga po tekstu
* `category` → filtriranje po kategoriji
* `source` → filtriranje po izvoru

Primjer:

```
/api/events?q=ai&category=News
```

---

## ⚡ Skalabilnost

Sustav je dizajniran s naglaskom na horizontalnu skalabilnost:

* stateless backend
* asinkroni dohvat podataka
* modularna arhitektura (servisi)
* NoSQL baza podataka

Omogućuje:

* pokretanje više instanci aplikacije
* paralelni dohvat podataka
* jednostavno proširenje sustava

---

## 🔄 Tijek obrade podataka

1. Dohvat vijesti iz vanjskih izvora (async)
2. Normalizacija podataka
3. Grupiranje po događajima
4. Pohrana u bazu podataka
5. Dohvat putem API-ja
6. Prikaz u frontend aplikaciji

---

## 🧪 Razvoj projekta

Projekt je razvijan postupno kroz sljedeće faze:

1. Osnovni backend (FastAPI)
2. Definiranje modela podataka
3. Asinkroni dohvat vijesti
4. Normalizacija podataka
5. Grupiranje događaja
6. Integracija baze podataka
7. Pretraga i filtriranje
8. Razvoj frontend aplikacije
9. Dockerizacija

---

## 🚀 Moguća proširenja

* Naprednije grupiranje (NLP)
* Real-time ažuriranje (WebSocket)
* Personalizacija korisnika
* Cache sloj (Redis)
* Paginacija i rangiranje vijesti

---

## 📌 Napomena

Projekt je inspiriran modernim platformama za agregaciju vijesti te demonstrira korištenje asinkronog programiranja, REST arhitekture i skalabilnih sustava.

---
