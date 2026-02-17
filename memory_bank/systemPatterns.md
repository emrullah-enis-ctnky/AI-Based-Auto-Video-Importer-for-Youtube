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
3. **Tiered Logging:** A custom logger class that handles dual stream output with varying verbosity.
4. **Commit-Push Flow:** Operational rule to ensure local changes are immediately synced to remote.
