
# Proje: AI-Powered YouTube Automation Tool (Terminal & GUI)

## 1. Proje Özeti

Bu araç, yerel bir video dosyasını Gemini AI kullanarak analiz eden, içeriğe uygun ilgi çekici başlık, açıklama ve etiketler oluşturan ve ardından YouTube API aracılığıyla videoyu (thumbnail ile birlikte) otomatik olarak yükleyen bir otomasyon sistemidir.

## 2. Teknik Gereksinimler & Kurallar

### A. Geliştirme ve Versiyon Kontrolü

* **Commit Kuralı:** Her anlamlı işlemden (bir modülün bitişi, bir fonksiyonun yazımı vb.) sonra mutlaka ilgili bir `git commit` atılmalıdır. Commit atıldıktan hemen sonra push yapılacaktır.
* **Dil:** Commit mesajları tamamen **Türkçe** olmalıdır.
* **Ortam Değişkenleri:** Hassas bilgiler (API Keyler) asla kodun içine yazılmamalıdır. Kök dizinde bir `.env` dosyası bulunmalı ve şu değişkenleri içermelidir:
* `YOUTUBE_API_KEY` / `CLIENT_SECRET_FILE`
* `GEMINI_API_KEY`

### B. Mimari ve Klasör Yapısı (Modüler Yapı)

Proje `src/` klasörü altında mantıksal katmanlara ayrılmalıdır:

```text
project_root/
│── src/
│   ├── api/            # API istemcilerinin yapılandırılması (Client initialization)
│   ├── gemini/         # AI analiz istemleri ve içerik üretimi
│   ├── youtube/        # YouTube Data API etkileşimleri
│   ├── video_analiz/   # Video işleme ve metadata hazırlığı
│   ├── video_yukleme/  # Upload işlemleri ve chunk yönetimi
│   └── utils/          # Yardımcı araçlar (Loglama, dosya kontrolleri)
│── logs/               # Log dosyalarının tutulduğu dizin
│── main.py             # Terminal giriş noktası
│── .env                # API anahtarları
└── requirements.txt    # Bağımlılıklar

```

### C. Fonksiyonel Gereksinimler

1. **Video Analizi:** Gemini API (Vision yetenekleri olan model) kullanılarak video dosyası analiz edilmelidir. Video içeriğine göre:

* Tıklanma oranı (CTR) yüksek bir **Başlık**.
* SEO uyumlu, linkler içeren bir **Açıklama**.
* Videonun keşfedilmesini sağlayacak **Etiketler** oluşturulmalıdır.

1. **YouTube Entegrasyonu:**

* Oauth2 veya API Key (yükleme için Oauth2 gereklidir) ile yetkilendirme yapılmalıdır.
* Video; başlık, açıklama ve etiketlerle birlikte yüklenmelidir.
* Belirtilen **Thumbnail (küçük resim)** dosyası videoya set edilmelidir.

### C. Kullanım ve Dosya Seçimi

1. **Terminal Parametreleri:** Program şu şekilde parametreli çalışmayı desteklemelidir:
`python main.py --video "yol/video.mp4" --thumbnail "yol/resim.jpg"`

2. **Hibrit Giriş Sistemi (File Dialog):** Eğer program herhangi bir parametre verilmeden doğrudan çalıştırılırsa:

* Önce bir dosya seçme penceresi açılmalı ve kullanıcıdan **Video** dosyasını seçmesi istenmelidir.
* Ardından ikinci bir pencere açılarak **Thumbnail (küçük resim)** dosyasını seçmesi istenmelidir.

### D. Loglama Sistemi

* Programın attığı her adım (API bağlantısı kuruldu, analiz başladı, yükleme %50 tamamlandı vb.) loglanmalıdır.
* Loglar hem **terminale** yazılmalı (kısa ve anlaşılır mesajlar) hem de `logs/app.log` gibi bir **dosyaya** detaylı olarak kaydedilmelidir.
* Hata mesajları (Örn: API limit aşımı, dosya bulunamadı) detaylı traceback içermelidir.

## 3. Eklenen Kritik Detaylar (Eksik Noktalar)

* **Otomatik Bağımlılık Yönetimi:** Program başlamadan önce `requirements.txt` dosyasındaki paketlerin yüklü olup olmadığını kontrol edecek ayrı bir ana script (veya başlangıç modülü) olmalıdır. Eksik paketler otomatik olarak `pip` ile yüklenmelidir.
* **Video Kontrolü:** Yükleme başlamadan önce dosya formatı (mp4, mov vb.) ve boyutu kontrol edilmelidir.
* **Hata Yönetimi (Retry):** İnternet kesilmesi veya API hatası durumunda yükleme işlemi kaldığı yerden devam edebilmeli veya belirli sayıda tekrar denenmelidir.
* **Gizlilik Durumu:** Videonun varsayılan olarak "Private" (Gizli) mi yoksa "Public" (Açık) mı yükleneceği parametre olarak eklenmelidir.
* **İlerleme Çubuğu:** Terminalde yükleme yüzdesini gösteren bir `tqdm` benzeri ilerleme çubuğu eklenmelidir.

## 4. Gelecek Planı (GUI Fazı)

* Terminal yapısı stabil çalıştıktan sonra, bu modüler yapı bozulmadan üzerine bir **PyQt** veya **Tkinter** arayüzü inşa edilecektir.
* Arayüzde "Dosya Seç" butonları, analiz sonucunu önizleme ekranı ve "Yükle" butonu bulunacaktır.

---
