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
  - 1.9.7: kurulumda dosyalar `cache:'reload'`, arka plan güncellemesi `cache:'no-cache'` ile alınır; kayıt `updateViaCache:'none'`, uygulama öne gelince `reg.update()`. Önceden GitHub Pages'in 10 dk HTTP önbelleği yüzünden yeni sürüm eski `index.html` ile kurulabiliyordu (kullanıcı yayından hemen sonra denediğinde sürüm değişmedi). `tufe.json` için tersi: önce internet, yoksa cihazdaki kopya.
- `tufe.json`: TCMB TÜFE verisi (`{kaynak, guncelleme, son:'YYYY-AA', m:{'YYYY-AA':[yıllık%, aylık%]}}`). Elle düzenlenmez; GitHub Actions üretir.
- `.github/workflows/tufe.yml` + `.github/scripts/tufe.py`: her gün 11:23 (TR) TCMB'nin Tüketici Fiyatları sayfasını okur, yeni ay varsa `tufe.json`'u `main`'e yazar. Tablo okunamazsa iş hata verir (GitHub e-posta atar).
- `manifest.webmanifest`, `icons/` (simgeler yalnızca burada), `KURULUM.md`.

## Sürüm kuralı

- Güncel sürüm: **1.9.9**
- Her güncellemede **iki yerde** sürüm artırılır: `sw.js` içinde `VERSION`, `index.html` içinde `APPV`.
- Ayarlar sayfasının altında "sürüm X.Y.Z" yazar; kullanıcı bununla kontrol eder.

## Veri

- `localStorage` anahtarları: `fon-portfoyum-v2` (veriler), `fon-tema` (tema), `fon-son-yedek` (son yedek tarihi), `fon-gizli` (gizlilik modu), `fon-kilit` (Face ID geçiş anahtarı kimliği), `fon-tufe` (TÜFE verisinin cihazdaki kopyası).
- 1.9 veri alanları (norm() korur): fonda `chk` (fiyatın son kontrol tarihi). İşlem kayıtlarında `q` (adet), `p` (fiyat), `lot` (alımın sepet kimliği), `used` (satışta kullanılan sepet parçaları), `tax`, `rev`. Geçmişten düzenleme/silme kayıtlarında `ref` + `old` (geri almak için). Eski kayıtlarda bu alanlar yoktur; `buyInfo`/`sellInfo` metinden, `usedOf` satış öncesi/sonrası sepet farkından bulur.
- Fiyat geçmişi fon başına en çok 4000 kayıt (1.8.1'e kadar 400'dü).
- `navigator.storage.persist()` ile kalıcı depolama istenir.
- Yedekleme: "Dışa aktar" paylaşım menüsünü açar (iCloud Drive'a kaydedilebilir). "Dosyadan yükle" ile geri yüklenir. Yedek kodunu kopyalama ve eski yedek formatını içe aktarma da var.
- Yüklenen her veri `norm()` ile aynı şemaya getirilir. Bu davranış bozulmamalı.

## Finans mantığı (doğru çalışıyor, korunmalı)

- **Stopaj:** her fon için varsayılan %17,5, fon bazında değiştirilebilir. Hisse fonlarına %0 uygulamak yanlıştı ve geri alındı. Elle değiştirilen oran `taxSet` bayrağıyla korunur.
- **Satış:** FIFO lot mantığıyla hesaplanır. Gerçekleşen kâr/zarar ayrıca tutulur.
  - 1.9.1: satış yalnızca **satış tarihinde portföyde olan** sepetlerden yapılır (`byDate`); sonradan alınan sepet geçmiş tarihli satışta kullanılamaz.
  - Aynı fonda kendisinden sonra satış olan eski bir satış düzenlenemez/silinemez (`laterSell`): FIFO sırası bozulmasın diye önce sonrakiler silinir. Sonraki satışları yeniden hesaplayan bir "tekrar oynatma" bilerek yapılmadı.
  - Satış düzenlenirken satışın kendi stopaj oranı korunur (`rateOf`), fonun güncel oranı değil.
- **Getiri (Midas mantığı):** her fonun tarihli fiyat kaydı tutulur (aynı gün tek kayıt).
  - Günlük getiri: bir önceki fiyat gününe göre.
  - Haftalık getiri: son fiyat tarihinden en az 7 gün önceki fiyata göre.
  - Dönem içinde alınan lotlar kendi maliyetiyle hesaplanır.
- **Biçim:** fiyat girişinde Türkçe ondalık virgül desteklenir. Her fonun rengi kendine ait.
  - Sayı okuma: `pn` (fiyat/adet girişi; tek nokta ondalık sayılır), `pnM` (tutar kutuları; `10.000` = on bin), `trN` (uygulamanın kendi yazdığı Türkçe metinler, örn. eski kayıtlardaki "10.000 adet"). Eski kayıt metni asla `pn` ile okunmamalı.
  - `isDate` gerçek takvim tarihini doğrular (2025-19-05, 2025-02-30 reddedilir); `norm()` bozuk tarihli fiyat kayıtlarını atar.
- **Fiyatlar elle girilir.** TEFAS'tan otomatik fiyat çekme yok ve yapılmamalı: TEFAS botları F5 korumasıyla bilerek engelliyor, eski `api/DB/BindHistoryInfo` kapatılmış (2026-11 denendi). Bu korumayı atlatmaya çalışılmaz.
- **Toplu fiyat girişi** (`bulkModal`): tüm fonlar tek ekranda. Kullanıcının TEFAS'tan kendi kopyaladığı metin `parsePaste` ile okunur: fon kodundan sonraki ilk ondalıklı sayı fiyat, kodun hemen önündeki tarih o fiyatın tarihi.
- **Enflasyon (reel getiri):** her sepet kendi alış ayından son açıklanan aya kadar TÜFE ile karşılaştırılır (`inflFrom`, `realOf`). Satılmış sepetler dahil değil.
- **Fiyat hatırlatıcısı:** elde tutulan fonun fiyatı en az 2 iş günü girilmediyse (ya da kontrol edilmediyse) uyarı çıkar (`staleDays`). `chk` yalnız ileri gider: geçmiş bir güne fiyat eklemek fonu "güncel" yapmaz.
- **TEFAS yapıştırma:** tarih yalnız fon kodunun hemen önündeki hücreden alınır; mevcut fiyattan %50'den fazla sapan değer (getiri tablosu gibi) kutuya yazılmaz, kullanıcıya gösterilir.

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
- **1.9 ekranları:**
  - Portföy: değer grafiği (1H/1A/3A/1Y/Tümü, parmakla gezinme, kesikli çizgi = yatırılan para). Getiri yüzdesi = dönem kâr/zararı ÷ (dönem başı değer + dönem içi alımlar).
  - Fon detayı: birim fiyat grafiği, alım günü işaretleri, reel getiri satırı.
  - Özet: İşlem geçmişi ve Yıllık özet bağlantıları, enflasyon kartı, ısı haritası.
  - Alt sayfalar `PARENT` ile tanımlı (`tx` ve `year` → Özet, `detail` → Portföy); soldan kaydırınca üst sayfaya dönülür.
  - İşlem geçmişi: alım/satış düzenleme ve silme. Kısmen satılmış alım ya da sepet bilgisi bulunamayan eski satış kilitlidir, nedeni yazılır. Her değişiklik fonun Geçmiş sekmesine düşer ve "Geri al" ile geri alınır.
  - Gizlilik modu (göz düğmesi): tutarlar `••••`. Kayda yazılan metinler her zaman `moneyR`/`sgnR` ile gerçek tutarla yazılır.
  - Face ID kilidi (WebAuthn geçiş anahtarı): açılışta ve 60 sn'den uzun arka planda kalınca. Bir gizlilik perdesidir, veri şifrelenmez. 2 başarısız denemeden sonra "Face ID çalışmıyor mu?" ile kaldırılabilir.
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

- Apple'ın gerçek Liquid Glass kırılması (camın arkasındaki sayfayı bükme) Safari'de yapılamıyor (`backdrop-filter:url()` yok). 1.9.8'den itibaren merceğin altındaki sahne (çubuk zemini + seçenekler) tuvale çizilip WebGL ile bükülüyor; arkadaki gerçek sayfa içeriği (kart, yazı) bükülmüyor, yerine düz renk kullanılıyor.
- Safari'de iç içe `backdrop-filter` bozuk görünür. Merceğe bulanıklık verilmemeli.
- Uygulama silinirse veriler de silinir. Kullanıcı düzenli "Dışa aktar" yapmalı.
- Testler gerçek iOS'ta değil, Chromium'da (Playwright iPhone taklidi). Gerçek cihaz davranışı kullanıcının videolarıyla doğrulanır.

## Güncelleme yayınlama

1. Değişikliği yap, `VERSION` ve `APPV` değerlerini artır, test et.
2. Çalışma dalına commit et, ardından `main` dalına gönder (fast-forward).
3. GitHub Actions'taki "pages build and deployment" işinin başarıyla bittiğini kontrol et.
4. Kullanıcıya şunu söyle: uygulamayı iki kez kapatıp açsın ve Ayarlar'ın altındaki sürüm numarasına baksın.

Kullanıcı isterse dosyaları elle de yükleyebilir: GitHub → Add file → Upload files ile `index.html` ve `sw.js`.

## 1.9.1 düzeltmeleri (Gemini/Antigravity kalite kontrolünden)

- Eski kayıtlarda 1.000+ adetin 1.000 kat küçük okunması (`trN`).
- Geçersiz takvim tarihinin kaydedilmesi (`isDate`).
- Eski satış silme/düzenlemede FIFO sırasının bozulması ve sonradan alınan sepetin satılabilmesi.
- Kapanan alt panelde çift dokunuşla işlemin iki kez yapılması (`#m.closing` dokunmaya kapalı).
- Gizlilikte Geçmiş sekmesinde tutar sızması (`dtl`); sepet silinince alım kaydının kalması; grafikte "Tümü" getirisinin ilk günün kârını düşmesi; fon grafiğinde çift nokta; toplu girişte yapıştırma kalıntıları; Face ID anahtarının kilit kaldırılınca açık görünmesi; "Ocak–Ocak"; `tufe.json` sunucu hatasında önbelleğe dönülmemesi.
- `tufe.yml`: Pages yayın isteği artık hata verirse iş kırmızı biter (sessizce geçilmez); `yayinla` seçeneğiyle elle denenebilir.

## 1.9.2 düzeltmeleri

- **Segment seçicilerde parmakla sürükleme:** Sepetler/Nakit hesabı/Geçmiş, tema, Günlük/Haftalık/Toplam, grafik aralığı, ısı haritası, işlem türü. Sekme çubuğundaki gibi mercek parmağı izler, bırakınca en yakın seçeneğe geçer. `.seg{touch-action:pan-y}`: yatay sürükleme sayfayı kaydırmaz, dikey kaydırma çalışır. Alt sayfada sol kenardan (x<28) başlayan hareket geri kaydırmaya bırakılır. Engelleyen `touchmove`/`touchend` dinleyicileri yalnızca `.seg` öğelerine bağlanır (MutationObserver ile).

## 1.9.3–1.9.8: Cam mercek (kırılma)

- **İstek (kullanıcının kendi tarifi, 1.9.8):** seçili öğe normalde düz yarı saydam gri kapsül; basılı tutup sürükleyince biraz büyüyüp şeffaf, kalın kenarlı cam damlasına dönüşür. Kenarlarına gelen yazılar kalın camın arkasındaymış gibi bükülür (optik kırılma), tam o kenarlarda hafif RGB ayrışması, çevresinde ince ışık parlaması; bırakınca düz gri kapsüle küçülür. Düz CSS bulanıklığıyla değil gerçek kırılmayla. Sekme çubuğunda ve tüm sürüklenebilen seçicilerde.
  - Referans videolar: kullanıcının başka uygulamalarındaki iOS 27 Liquid Glass sekme çubuğu ve hız seçicisi (0.5x…2x). Cam, kenarında dışarıdaki görüntüyü içeri çeker; kenara yakın yerde aynalanma ve gökkuşağı; merkez temiz; mercek izden biraz taşar, izin kenarı içeri kayar.
- **Yöntem (1.9.8): WebGL gölgelendirici.** Tek bir WebGL tuvali (`LQ.cv`, `canvas.lqc`) o an açık olan merceğin göstergesine taşınır.
  - `lqScene`: merceğin altındaki sahne gizli 2D tuvale (`LQ.sc`) kabın koordinatlarında `LQ_SP`=48 payla çizilir. İçeriği: dış zemin, iz/çubuk (yuvarlak köşe, kenar çizgisi), yazılar (`fillText`, gerçek yazı kutusuna ortalı) ve simgeler. Simgeler SVG'den bir kez siyah yüklenir, çizerken o anki renge boyanır (`source-in`). Renk ya da boyut animasyonu yüzünden her karede yeni resim yüklenmemeli. Sahne yalnız düğme sınıfları/ölçü değişince yeniden çizilir (`L.sig`).
  - Gölgelendirici: kapsül uzaklık alanı (SDF) ile kenara uzaklık d; kenar şeridi B=min(.34h,16), en dıştan çekilen mesafe M=min(.3h,13). Örnek noktası `p + n·M·s²` (s=1-d/B; M > B/2 olduğundan kenarda aynalanma). R/G/B .82/1/1.18 oranında ayrı örneklenir (renk ayrışması yalnız kenarda). Çubuğun içinde saydam kalan yer çubuk rengiyle doldurulur. Kenar şeridi hafif koyu; en dışta sol üstten gelen ince parlama.
  - Renkler `lqColors`: segmentte dış zemin kendi kartı. Sekme çubuğunda dış zemin çubuğun hemen üstündeki öğenin rengi, yalnız çubuğun yatay uzunluğunca; uçların dışı saydam, arkadaki gerçek içerik görünür. Çubuk rengi = cam dolgusu + arkasındaki öğe.
  - Mercek açıkken gösterge seçeneklerin üstüne çıkar (`.thumb.lqv{z-index:2}`), alttaki `::before` zemini kapanır, ince koyu kenar `::after` (`--lens-rim`) üstte kalır. `g` (merceğin açıklığı) ile kırılma ve parlama mercek küçülürken söner.
  - WebGL yoksa ya da bağlam kaybolursa mercek eski düz cam olarak çalışır. Hareketi azalt açıksa mercek açılmaz. Gölgelendirici açılıştan 0,4 sn sonra boşta derlenir (ilk basışta takılma olmasın).
  - Gerçek düğme sorguları hep `:scope>button` olmalı.
- **1.9.9 ince ayarları (kullanıcı 1.9.8'i beğendi, temel yapı korunacak):**
  - Kırılma yalnız camın en dıştaki ince şeridinde: B=min(.16h,7), M=.42B (M < B/2 → aynalanma yok). İçerisi birebir (büyütme/kayma yok). 1.9.8'de M=13 dışarıdan komşu yazıyı içeri çekiyor, "Tümümü", "Özet" çiftlenmesi, "3A"nın "1Y"ye kayması görülüyordu.
  - Renk ayrışması sade: kanallar .86/1.14, kenara doğru `mix(düz, ayrık, .75·s)`; kenar koyulaşması .06, parlama koyu .6 / açık .85.
  - Jöle esnemesi (`jelly`): uzak sekmeye geçişte iki kenar ayrı yaylarla gider (öndeki önde, arkadaki `lag` kadar geride) → hıza göre yatay uzama, hedefte öndeki kenar hafif taşıp yaylanır. Ölçek kullanılmaz (yamuk olmasın), `width`+`translateX` Web Animations ile. Ölçülen: uzak (4 seçenek) 67→140 px, yakın 67→74 px, sekme çubuğu uçtan uca 76→117 px. Sürükleme başlarken animasyon iptal edilir (`th._jl`). Mercek tuvali genişliği 16'lık basamakla ayrılır (esnerken her karede yeniden boyutlanmasın).
- **Denenip bırakılanlar (tekrar denenmesin):**
  - 1.9.3: yazı kopyası + SVG filtre, içeriden dışarı uzatma. Yanlış yön; bant oluşmuyordu.
  - 1.9.4–1.9.5: opak kopya + SVG `feDisplacementMap`. Safari'de içeriği bütünüyle ~4 nokta kaydırdı, gerçek yazı arkada "damga" gibi kaldı. Sebep doğrulanamadı (feImage ölçüsü ya da 128 nötr değerinin renk uzayı).
  - 1.9.6: düz CSS (iz zemini `scaleY`, renk şeritleri). Yazı bükülmüyordu; kullanıcı gerçek kırılma istedi.
- Yalnız Chromium'da test edildi (ortamda WebKit yok). WebGL gölgelendirici iki tarayıcıda aynı matematikle çalışır, ama gerçek iPhone'da görünüm ve akıcılık kullanıcının kaydıyla doğrulanmalı.

## Açık konular

- 1.8.1'in gerçek iPhone'da doğrulanması: hızlı dokunma, parmakla sürükleme, merceğin taşması.
- 1.9.2'nin gerçek iPhone'da doğrulanması: segmentlerde parmakla sürükleme.
- 1.9.9'un gerçek iPhone'da doğrulanması: jöle esnemesi; WebGL cam mercek (kenarda bükülme, renk ayrışması, parlama) Safari'de sekme çubuğunda ve seçicilerde görünüyor mu, akıcı mı; yeni sürüm hemen yükleniyor mu (1.9.7 önbellek düzeltmesi).
- 1.9.0'ın gerçek iPhone'da doğrulanması: Face ID kilidi (ana ekran uygulamasında WebAuthn), grafikte parmakla gezinme, TEFAS'tan kopyalanan gerçek metnin okunması.
- TÜFE işinin ilk otomatik güncellemesi (3 Aralık 2026, Kasım verisi) Actions sekmesinden kontrol edilmeli.
- Henüz istenmemiş olası geliştirmeler: hedef dağılım ve dengeleme, düzenli yatırım planı, Mac edinilirse yerel SwiftUI sürümü.
