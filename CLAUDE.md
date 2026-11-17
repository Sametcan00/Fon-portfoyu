# Fon Portföyüm — proje notları

Bu dosya yeni Claude sohbetlerinde otomatik okunur. Her sürümden sonra güncel tutulmalı.

## Çalışma tercihleri (önemli)

- **Yanıtlar Türkçe** olmalı.
- Her değişiklikten sonra **test yapılsın ve hata aransın** (Playwright ile iPhone taklidi, dokunma olaylarıyla).
- Yapılamayan bir şey varsa **açıkça söylensin**, yapılmış gibi gösterilmesin.
- Kullanıcı referansı ekran görüntüsü ve videoyla verir (iPhone ekran kaydı .mp4). Videoları `ffmpeg` ile kareye ayırıp incele.
- Görsel referans: **Midas** uygulaması ve **iOS 27 Liquid Glass** görünümü.
- Kullanıcının bilgisayarı Windows; Xcode/Mac yok.

## Proje nedir?

- Kişisel fon portföyü takip uygulaması. İlk sürüm Gemini Canvas'ta yapıldı, Claude ile geliştirildi.
- iPhone 16 Pro (iOS 27) ana ekranına Safari'den "Ana Ekrana Ekle" ile kurulan **PWA**.
- Yerel Swift değil, çünkü Mac yok ve ücretsiz Apple hesabıyla yüklenen uygulama 7 günde siliniyor.
- Barındırma: **GitHub Pages**, `Sametcan00/fon-portfoyu`, `main` dalından yayınlanır.
- Kullanıcı, güncellemeleri doğrudan `main` dalına yüklememi onayladı. Pages kurulumu `main`'e her gönderimde otomatik çalışır.

## Dosyalar

- `index.html`: tüm CSS ve JS tek dosyada, harici kütüphane yok.
- `sw.js`: service worker. Önce cihazdaki kopyayı açar, arka planda internetten günceller. Önbellek adı `fon-portfoyu-` + `VERSION`.
- `manifest.webmanifest`, `icons/` (simgeler yalnızca burada), `KURULUM.md`.

## Sürüm kuralı

- Güncel sürüm: **1.8.1**
- Her güncellemede **iki yerde** sürüm artırılır: `sw.js` içinde `VERSION`, `index.html` içinde `APPV`.
- Ayarlar sayfasının altında "sürüm X.Y.Z" yazar; kullanıcı bununla kontrol eder.

## Veri

- `localStorage` anahtarları: `fon-portfoyum-v2` (veriler), `fon-tema` (tema), `fon-son-yedek` (son yedek tarihi).
- `navigator.storage.persist()` ile kalıcı depolama istenir.
- Yedekleme: "Dışa aktar" paylaşım menüsünü açar (iCloud Drive'a kaydedilebilir). "Dosyadan yükle" ile geri yüklenir. Yedek kodunu kopyalama ve eski yedek formatını içe aktarma da var.
- Yüklenen her veri `norm()` ile aynı şemaya getirilir. Bu davranış bozulmamalı.

## Finans mantığı (doğru çalışıyor, korunmalı)

- **Stopaj:** her fon için varsayılan %17,5, fon bazında değiştirilebilir. Hisse fonlarına %0 uygulamak yanlıştı ve geri alındı. Elle değiştirilen oran `taxSet` bayrağıyla korunur.
- **Satış:** FIFO lot mantığıyla hesaplanır. Gerçekleşen kâr/zarar ayrıca tutulur.
- **Getiri (Midas mantığı):** her fonun tarihli fiyat kaydı tutulur (aynı gün tek kayıt).
  - Günlük getiri: bir önceki fiyat gününe göre.
  - Haftalık getiri: son fiyat tarihinden en az 7 gün önceki fiyata göre.
  - Dönem içinde alınan lotlar kendi maliyetiyle hesaplanır.
- **Biçim:** fiyat girişinde Türkçe ondalık virgül desteklenir. Her fonun rengi kendine ait.
- **Fiyatlar elle girilir.** TEFAS'tan otomatik fiyat çekme yok.

## Arayüz (iOS 27 tarzı)

- **Açık tema:** zemin #F2F2F7, kartlar beyaz, vurgu #007AFF.
- **Koyu tema:** zemin saf siyah, kartlar #1C1C1E, vurgu #0A84FF.
- **Tema seçimi:** Sistem / Açık / Koyu. Tema değişirken daire şeklinde yayılan geçiş (View Transition) var.
- **Kartlar:** düz gruplu hücreler, 26 nokta yuvarlak köşe, kenarlık yok.
- **Butonlar:** üstte dairesel cam butonlar, diğerleri kapsül.
- **Sekme çubuğu** (Portföy / Özet / Ayarlar):
  - Yüzen Liquid Glass kapsül.
  - PWA'da ekran yüksekliğine göre konumlanır, alt kenarı ekranın dibinden 22 nokta yukarıda (`html.pwa .tabbar`).
  - Kısa sayfalar ekrandan 1 piksel uzun yapılır (iOS 27'nin kısa sayfalarda görünür alanı kısaltma hatası).
- **Seçim göstergesi** (`.thumb`, sekme çubuğu ve segment seçicilerde):
  - Yaylanarak kayar.
  - Basılı tutulunca ya da sürüklenince büyüyüp kabın dışına taşan saydam cam **merceğe** dönüşür (`.sw` sınıfı). Kenarlarında pembe/mavi renk kırılması var.
  - Merceğin altındaki simge büyür (`.under` sınıfı).
- **Seçilen sekme simgesi:** zıplama animasyonu (`.pop`).
- **Parmakla sürükleme:** sekme çubuğunda parmakla sürükleyerek sekme seçilebilir.
- **Geçişler:**
  - Sekme ve segment değişimi yerinde yumuşak (kayma yok).
  - Detay sayfasına girişte fon simgesi "uçar".
  - Soldan kaydırarak geri dönülür.
  - Alt paneller aşağı çekerek kapatılır.
- **Sayılar:** değişirken animasyonla güncellenir (`tween`).
- **CSS yapısı:** sürüm sürüm eklenmiş katmanlardan oluşur; sonraki bloklar öncekileri ezer. En sondaki "v1.8.1 — Düzeltmeler" bloğu geçerli olanıdır. Değişiklik yaparken önceki kuralların özgüllüğüne dikkat et (örnek: `:root[data-theme="light"] .tabbar>.thumb.sw`).

## Çözülen sorunlar (tekrar etmesin)

- %0 stopaj hatası, yanlış Günlük/Haftalık getiri, iki fonun aynı renkte görünmesi.
- Alt siyah şerit (iOS 27 hatası, hafifletildi), sekme çubuğu köşesinde kare kutu, taşan alt paneller, ondalık virgül sorunu.
- Sekme geçişinde titreme: animasyon sırasında cam bulanıklığı geçici kapatılır (`#app.moving`).
- Tema değişirken sekme çubuğunun kayması: Ayarlar'daki gizli dosya alanı sayfayı 419 piksele genişletiyordu.
- Sekme çubuğunun sayfadan sayfaya farklı yükseklikte durması; sekme seçerken içeriğin yana kayması; "Dosyadan yükle" yazısının iki satıra düşmesi.
- **1.8.1 düzeltmeleri:**
  - **Hızlı dokunuşlar yutuluyordu.** Sebep: iOS çift dokunma yakınlaştırması. Çözüm: `touch-action: manipulation`; sekme çubuğunda `touch-action: none` ve dokunma `touchend` içinde doğrudan işlenir. Sayfanın küçülüp kaymasının sebebi de bu yakınlaştırmaydı.
  - **iOS sürüklemeyi `touchcancel` ile iptal edince seçim kayboluyordu.** Artık iptalde de parmağın gittiği sekmeye geçilir.
  - **Mercek yamuk görünüyordu.** İki sebep vardı:
    - `scale` ile farklı oranda esnetiliyordu. Çözüm: mercek artık `::before` katmanının gerçek boyutu büyütülerek yapılıyor.
    - `.glass` sınıfının `clip-path` kuralı sekme çubuğunu kırpıyordu. Çözüm: çubuğun cam zemini `.tabbar::after` katmanına taşındı, sadece o katman kırpılıyor.

## Bilinen sınırlar

- Apple'ın gerçek Liquid Glass kırılması (camın arkasını bükme/büyütme) Safari'de yapılamıyor, yakın bir taklit uygulandı.
- Safari'de iç içe `backdrop-filter` bozuk görünür. Merceğe bulanıklık verilmemeli.
- Uygulama silinirse veriler de silinir. Kullanıcı düzenli "Dışa aktar" yapmalı.
- Testler gerçek iOS'ta değil, Chromium'da (Playwright iPhone taklidi). Gerçek cihaz davranışı kullanıcının videolarıyla doğrulanır.

## Güncelleme yayınlama

1. Değişikliği yap, `VERSION` ve `APPV` değerlerini artır, test et.
2. Çalışma dalına commit et, ardından `main` dalına gönder (fast-forward).
3. GitHub Actions'taki "pages build and deployment" işinin başarıyla bittiğini kontrol et.
4. Kullanıcıya şunu söyle: uygulamayı iki kez kapatıp açsın ve Ayarlar'ın altındaki sürüm numarasına baksın.

Kullanıcı isterse dosyaları elle de yükleyebilir: GitHub → Add file → Upload files ile `index.html` ve `sw.js`.

## Açık konular

- 1.8.1'in gerçek iPhone'da doğrulanması: hızlı dokunma, parmakla sürükleme, merceğin taşması.
- Henüz istenmemiş olası geliştirmeler: TEFAS'tan otomatik fiyat çekme, Mac edinilirse yerel SwiftUI sürümü.
