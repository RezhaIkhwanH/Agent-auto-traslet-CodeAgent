# Agent Voice Translate

Repositori ini berisi **kode AI agent/backend saja** untuk proyek voice translate. Kode Discord bot tidak ada di repositori ini. Bot yang menggunakan agent ini tersedia di [agent-Discord-auto-traslet-CodeBot](https://github.com/RezhaIkhwanH/agent-Discord-auto-traslet-CodeBot).

## Gambaran Proyek

Agent ini dibuat dengan LangChain dan model Groq, lalu disajikan sebagai API menggunakan FastAPI dan LangServe. Bot Discord merupakan aplikasi terpisah yang berperan sebagai client untuk berkomunikasi dengan backend agent.

Alur integrasinya secara umum:

1. Bot menerima voice/audio dan menyiapkan konten untuk agent.
2. Bot mengirim input teks/transkrip ke API agent.
3. Agent memproses input dan mengembalikan respons teks.
4. Bot menyampaikan hasilnya kembali kepada pengguna Discord.

## Teknologi

- Python 3.13+
- FastAPI dan LangServe
- LangChain
- Groq (`ChatGroq`)
- MLflow untuk experiment tracking
- `uv` untuk mengelola dependensi

## Persiapan

Pastikan Python 3.13+ dan [`uv`](https://docs.astral.sh/uv/) sudah tersedia. Dari direktori proyek, pasang dependensi:

```bash
uv sync
```

Buat file `.env` di root proyek dan masukkan Groq API key:

```env
GROQ_API_KEY=isi_api_key_groq_anda
```

Dapatkan API key dari [Groq Console](https://console.groq.com/). Jangan membagikan atau meng-commit file `.env`.

## Menjalankan API

Jalankan server dari root proyek:

```bash
uv run uvicorn main:app --reload
```

Alamat lokal dan endpoint:

- Health check: `http://127.0.0.1:8000/health`
- Agent LangServe: `http://127.0.0.1:8000/voice-translate`
- LangServe Playground: `http://127.0.0.1:8000/voice-translate/playground`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Invoke API: `POST http://127.0.0.1:8000/voice-translate/invoke`

LangServe menerima input berupa `messages`, contohnya:

```json
{
  "input": {
    "messages": [{ "role": "user", "content": "Teks transkrip untuk diproses" }]
  }
}
```

## MLflow

Kode agent dikonfigurasi untuk mengirim experiment tracking ke `http://localhost:5000`. Untuk menjalankan server MLflow secara lokal, buka terminal terpisah:

```bash
uv run mlflow server --host 127.0.0.1 --port 5000
```

## Menjalankan Pengujian Lokal

Script lokal di `agent.py` membaca `voice_transcript.txt` dari direktori proyek dan menyimpan terjemahan ke `result/voice_translation.txt`:

```bash
uv run python agent.py
```

Untuk menguji client HTTP, pastikan server sudah berjalan dan siapkan `voice_transcript.txt` di direktori proyek, lalu jalankan:

```bash
uv run python testClient.py
```

## Catatan Implementasi

Endpoint ini menerima teks transkrip, bukan file audio. Bot Discord menangani penerimaan voice dan menyiapkan transkrip, sedangkan agent menerjemahkan teks tersebut ke Bahasa Indonesia.
