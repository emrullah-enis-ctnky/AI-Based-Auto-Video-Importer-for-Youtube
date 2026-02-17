# Technical Context

## Tech Stack

- **Language:** Python 3.x
- **AI:** Gemini API (Google Generative AI SDK)
- **YouTube:** YouTube Data API v3 (Google API Client Library)
- **GUI/Dialogs:** Tkinter (Dosya seçimi ve uygulama arayüzü için)
- **Utilities:** `python-dotenv` (ENV), `tqdm` (Progress), `pip` (Dependency management)

## Architecture

- **Modular Structure:** Logic separated into `src/` subdirectories (api, gemini, youtube, etc.).
- **Environment driven:** All sensitive data stored in `.env`.
- **Log-Heavy:** Two-tier logging (Terminal: Concise, File: Extended).
