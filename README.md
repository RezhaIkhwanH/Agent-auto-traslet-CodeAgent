# Agent Notetaker MOM - Server API 📝

> [!IMPORTANT]
> Repositori ini hanya berisi **kode Backend Agent / API** untuk Agent Notetaker MOM. Kode Discord Bot-nya berada pada repositori terpisah.
>
> - **Bot MOM Repo**: [Bot MoM](https://github.com/RezhaIkhwanH/MOM-agent-bot-discord)

**Agent Notetaker MOM Server** adalah aplikasi backend berbasis AI yang dirancang untuk secara otomatis mengubah transkrip atau catatan rapat mentah menjadi dokumen Notulen Rapat (*Minutes of Meeting* - MOM) yang terstruktur, jelas, dan profesional dalam Bahasa Indonesia.

Proyek ini dibangun menggunakan **FastAPI**, **LangChain**, **LangServe**, dan model dari **Groq** untuk menghasilkan ringkasan dan poin-poin rapat secara instan. Proyek ini juga terintegrasi dengan **MLflow** untuk pelacakan eksperimen (*experiment tracking*).

---

## Fitur Utama ✨

- **Otomatisasi MOM**: Mengonversi transkrip mentah menjadi format MOM standar (Detail Rapat, Poin Diskusi, Keputusan, Action Items, dan Langkah Selanjutnya).
- **Bahasa Indonesia**: System prompt dikonfigurasi secara khusus untuk menghasilkan notulensi formal dalam Bahasa Indonesia.
- **REST API & LangServe**: Menyediakan endpoint API `/agent_MOM` yang dapat diakses dengan mudah oleh client (seperti Discord Bot, Web Application, dll).
- **Interactive Playground & Swagger UI**: Built-in LangServe Playground di `/agent_MOM/playground` serta dokumentasi Swagger di `/docs`.
- **Experiment Tracking**: Terintegrasi dengan **MLflow** untuk melacak setiap eksekusi agent (*runs*), prompt, dan output.
- **Fast Inference**: Menggunakan **Groq API** (`ChatGroq`) untuk eksekusi LLM yang cepat.

---

## Prasyarat 🛠️

Sebelum menjalankan server ini, pastikan Anda telah menyiapkan:
- **Python 3.13+** (atau Python 3.9+)
- Package Manager: [`uv`](https://github.com/astral-sh/uv) (direkomendasikan) atau `pip`
- **Groq API Key** (Dapatkan di [Groq Console](https://console.groq.com/))
- **MLflow Server** (Opsional, untuk tracking eksperimen)

---

## Instalasi 💻

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/Farras-AI/Agent-MOM.git
   cd Agent-MOM
   ```

2. **Buat & Aktifkan Virtual Environment:**
   - **Menggunakan `uv` (Direkomendasikan):**
     ```bash
     uv venv
     # Windows:
     .venv\Scripts\activate
     # Linux/macOS:
     source .venv/bin/activate
     ```
   - **Menggunakan standard `venv`:**
     ```bash
     python -m venv .venv
     # Windows:
     .venv\Scripts\activate
     # Linux/macOS:
     source .venv/bin/activate
     ```

3. **Instal Dependensi:**
   - **Dengan `uv`:**
     ```bash
     uv sync
     ```
   - **Dengan `pip`:**
     ```bash
     pip install fastapi uvicorn langchain langchain-groq langserve pydantic python-dotenv mlflow
     ```

4. **Konfigurasi Environment Variables:**
   Buat file `.env` di root direktori proyek dan tambahkan Groq API Key Anda:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## Cara Penggunaan 🚀

### 1. Menjalankan Server MLflow (Opsional)
Server backend dikonfigurasi untuk mengirim log tracking ke MLflow di `http://localhost:5000`. Buka terminal baru dan jalankan:
```bash
mlflow server --host 127.0.0.1 --port 5000
```

### 2. Menjalankan Server REST API (FastAPI + LangServe)
Jalankan server API menggunakan Uvicorn:
```bash
uvicorn main:app --reload
```
Server akan berjalan di `http://localhost:8000`.

Anda dapat mengakses:
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **LangServe API Endpoint**: `http://localhost:8000/agent_MOM`
- **LangServe Playground (UI)**: [http://localhost:8000/agent_MOM/playground](http://localhost:8000/agent_MOM/playground)
- **Dokumentasi API Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Testing Agent secara Lokal (Script Test)
Jika ingin menguji agent menggunakan file teks transkrip rapat (`mom_test.txt`):
```bash
python agent.py
```
*Hasil notulen rapat akan tersimpan secara otomatis di `result/MOM_result.txt`.*

Atau Anda juga dapat menguji pemanggilan HTTP ke server menggunakan:
```bash
python testClient.py
```

---

## Struktur Proyek 📂

```text
.
├── main.py          # Entry point FastAPI & registrasi rute LangServe
├── agent.py         # Logika utama LangChain agent, system prompt, integrasi Groq & MLflow
├── testClient.py    # Script pengujian pemanggilan HTTP client ke server
├── pyproject.toml   # Konfigurasi dependensi proyek Python
├── uv.lock          # Lockfile dependensi (uv package manager)
├── .env             # File environment variable (GROQ_API_KEY, dll)
├── result/          # Folder output hasil pengujian lokal
└── README.md        # Dokumentasi repositori ini
```

---

## Teknologi yang Digunakan 🔧

- [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for APIs
- [LangChain](https://www.langchain.com/) - Framework for LLM applications
- [LangServe](https://python.langchain.com/docs/langserve) - Deploy LangChain runnables and chains as REST APIs
- [Groq](https://groq.com/) - Ultra-fast LLM Inference Engine
- [MLflow](https://mlflow.org/) - Open source platform for the machine learning lifecycle
