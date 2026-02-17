# System Patterns

## Folder Structure

```text
project_root/
│── src/
│   ├── api/            # Client initialization
│   ├── gemini/         # AI Prompting & Analysis
│   ├── youtube/        # API Interactions & Uploads
│   ├── video_analiz/   # Metadata Preparation
│   ├── video_yukleme/  # Progress & Chunk management
│   └── utils/          # Helpers (Logging, Auto-PIP, File Checks)
│── logs/               # App logs
│── main.py             # Entry point
```

## Core Patterns

1. **Dependency Guard:** A startup check that verifies `requirements.txt` against installed packages.
2. **Hybrid Input Pattern:**
    - Try reading CLI arguments.
    - If absent, invoke File Dialogs.
3. **Tiered Logging:** A custom logger class that handles dual stream output (Terminal: Rich, File: Standard).
4. **Stylish UI Pattern:** Use of `rich` panels, banners, and banners to provide a premium CLI experience.
5. **Commit-Push Flow (STRICT):** Operational rule to ensure local changes are immediately synced to remote. *Every commit MUST be followed by a push.*
