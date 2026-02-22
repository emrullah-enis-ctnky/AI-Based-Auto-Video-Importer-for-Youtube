# 🎬 AI-Powered Auto Video Importer for YouTube

*(Bilingual Documentation: English | Türkçe)*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, open-source automation tool that acts as your AI social media manager. It uses Google's Gemini Vision AI to analyze your videos and automatically generate high-CTR titles, SEO-optimized descriptions, and relevant tags, before seamlessly uploading them to YouTube.

Available as a sleek Desktop GUI Application and a fast Terminal CLI.

---

## 🇹🇷 Türkçe Eğitim & Dokümantasyon

### 🌟 Özellikler

* 🤖 **AI Analizi:** Videonuzun ve küçük resminizin (thumbnail) içeriğini Gemini Vision modeliyle inceleyerek genel bağlamı anlar.
* ✍️ **Otomatik SEO:** YouTube algoritmasına uygun, tıklama oranı (CTR) yüksek başlıklar, SEO odaklı açıklamalar ve hedefli etiketler (tags) üretir.
* 🚀 **Otomatik Yükleme:** YouTube Data API v3 kullanarak videoyu ve küçük resmi belirlediğiniz ayarlarla (Gizli/Açık vb.) otomatik yükler.
* 🎨 **Modern Masaüstü Arayüzü (GUI):** Karanlık/Aydınlık mod destekli, CustomTkinter ile hazırlanmış şık bir arayüze sahiptir. Dosya seçici, anlık ilerleme çubuğu ve uygulama içi log takibi ile süreci anlık izleyin.
* 💻 **Terminal (CLI) Desteği:** İsterseniz doğrudan komut satırından çalıştırıp arka plan otomasyon zincirlerine dahil edebilirsiniz.
* 🌍 **Çoklu Dil Desteği:** Arayüz tamamen İngilizce ve Türkçe olarak iki dilde kullanılabilir.

### ⚙️ Kurulum ve Gereksinimler

**1. Sistem Gereksinimleri:**

* Python 3.10 veya üzeri.
* [FFmpeg](https://ffmpeg.org/download.html) (Videonun analiz edilebilmesi, ses ve görüntü verilerinin işlenmesi için bilgisayarınızda mutlaka kurulu ve Sistem Yoluna (PATH) eklenmiş olmalıdır).

**2. Repoyu İndirin ve Bağımlılıkları Yükleyin:**
Terminal veya komut satırını açıp aşağıdaki adımları izleyin:

```bash
git clone https://github.com/emrullah-enis-ctnky/AI-Based-Auto-Video-Importer-for-Youtube.git
cd AI-Based-Auto-Video-Importer-for-Youtube

# Sanal ortam (virtual environment) oluşturun ve aktif edin
python -m venv venv
source venv/bin/activate  # Windows kullanıyorsanız: venv\Scripts\activate

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

**3. API Anahtarlarının Ayarlanması (.env):**
Proje dizininde bir `.env` dosyası oluşturun (veya var olan `.env.example` dosyasının adını `.env` olarak değiştirin) ve içini doldurun:

```env
# Google Gemini API Anahtarınız (AI analizi için zorunludur)
GEMINI_API_KEY="AIzaSy..."

# YouTube API Projesi (Boş bırakabilirsiniz ancak client_secret zorunlu)
YOUTUBE_API_KEY="..." 
CLIENT_SECRET_FILE="client_secret.json"
```

*Önemli Not: YouTube'a video yükleyebilmek için Google Cloud Console üzerinden bir proje oluşturmalı, "YouTube Data API v3" servisini aktif etmeli ve bir OAuth 2.0 Web Client ID oluşturmalısınız. İndirdiğiniz JSON dosyasını proje ana dizinine `client_secret.json` adıyla koymalısınız.*

### 🚀 Kullanım

**▶ Seçenek 1: Modern Arayüz (GUI) ile Başlatma**
En iyi kullanıcı deneyimi için arayüzü başlatın:

```bash
python src/gui/app.py
```

Açılan pencereden "Home" (Ana Sayfa) sekmesini seçin; videonuzu, küçük resminizi seçin, yapay zekaya iletmek istediğiniz isteğe bağlı özel notları ekleyin ve işlemi başlatın. Sistem loglarını sayfa üzerinden canlı olarak izleyebilirsiniz!

**▶ Seçenek 2: Terminal (CLI) ile Başlatma**
Eğer saf hız istiyorsanız veya arayüz sevmiyorsanız Terminal modunu kullanabilirsiniz:

```bash
python main.py
```

### 🔨 Nasıl Derlenir? (Stand-alone EXE / Binary Üretme)

Eğer uygulamayı Python kurulu olmayan başka bilgisayarlarda çalıştırmak üzere bağımsız bir `.exe` (Windows) veya çalıştırılabilir dosya (Linux) haline getirmek istiyorsanız bu adımları kullanabilirsiniz:

* **Windows:** Komut satırında kök dizindeyken `build_windows.bat` dosyasına çift tıklayın veya CLI üzerinden çalıştırın. Script, kendi sanal ortamını kurup PyInstaller'ı çalıştıracak ve `dist/` klasörü içerisinde `youtube_importer.exe` dosyasını oluşturacaktır.
* **Linux:** Terminalden `./build_linux.sh` komutunu çalıştırın. `dist/` klasörü içerisinde `youtube_importer` adında çalıştırılabilir binary dosyası oluşacaktır.

---

## 🇬🇧 English Documentation

### 🌟 Features

* 🤖 **AI Video Analysis:** Deeply analyzes your video content and thumbnail using Google's Gemini Vision capabilities to understand the context and mood.
* ✍️ **Automated SEO Generator:** Automatically generates high-CTR (Click-Through Rate) titles, SEO-friendly descriptions, and highly targeted tags tailored to the current YouTube algorithm.
* 🚀 **Auto YouTube Upload:** Utilizes the official YouTube Data API v3 to completely automate the uploading process, including the application of custom thumbnails and video privacy configurations.
* 🎨 **Modern Desktop Interface (GUI):** A sleek, CustomTkinter-based interface featuring Dark/Light modes, robust file explorers, and real-time aesthetic progress bars.
* 💻 **Terminal (CLI) Support:** Can be easily executed via CLI for pure terminal enthusiasts or for headless server automation workflows.
* 🌍 **Bilingual Native UI:** The application interface is natively integrated and available in both English and Turkish.

### ⚙️ Setup and Prerequisites

**1. System Requirements:**

* Python 3.10 or higher.
* [FFmpeg](https://ffmpeg.org/download.html) (Must be installed and added to your system PATH for video and audio chunk extraction to work properly).

**2. Clone and Install Dependencies:**

```bash
git clone https://github.com/emrullah-enis-ctnky/AI-Based-Auto-Video-Importer-for-Youtube.git
cd AI-Based-Auto-Video-Importer-for-Youtube

# Create and activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all required Python packages
pip install -r requirements.txt
```

**3. Configure API Keys (.env):**
Create a `.env` file in the root directory (or rename `.env.example`) and define the following crucial variables:

```env
# Google Gemini API Key (Required for AI Content Generation)
GEMINI_API_KEY="AIzaSy..."

# YouTube API Variables
YOUTUBE_API_KEY="..." 
CLIENT_SECRET_FILE="client_secret.json"
```

*Crucial Note: To upload videos to your own channel, you must create a project in the Google Cloud Console, enable the "YouTube Data API v3", generate an OAuth 2.0 Client ID, and place the downloaded JSON file in the root directory as `client_secret.json`.*

### 🚀 Usage

**▶ Option 1: Modern GUI Application**
For the best graphical and user-friendly experience, launch the graphical interface:

```bash
python src/gui/app.py
```

Select the "Home" tab on the sidebar. Pick your `.mp4` video and `.jpg/.png` thumbnail files, type out any optional context notes for the AI, and click start. You can watch the detailed progress and terminal logs directly from the active UI window!

**▶ Option 2: Terminal (CLI) Mode**
For developers who prefer the command-line interface:

```bash
python main.py
```

### 🔨 How to Build (Stand-alone Executable)

You can compile this project into a standalone executable that doesn't require a Python or PIP locally installed on the target machine.

* **Windows:** Simply execute the `build_windows.bat` script in your command prompt. This script automates virtual environment creation, runs PyInstaller, and magically outputs `youtube_importer.exe` into the `dist/` directory.
* **Linux:** Run the `build_linux.sh` bash script. Navigate to `dist/youtube_importer` to find your generated, portable binary executable.
