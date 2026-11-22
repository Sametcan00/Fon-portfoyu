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
  - 1.9.20: `<head>`'de İçerik Güvenliği Politikası (CSP meta): yalnız kendi dosyaları; `connect-src 'self'` (veri başka adrese gönderilemez), `img-src 'self' data: blob:` (mercek simgeleri data: SVG). Harici kaynak eklenirse CSP'ye de eklenmeli. `frame-ancestors` meta ile çalışmaz, eklenmemeli (konsola hata yazar).
- `sw.js`: service worker. Önce cihazdaki kopyayı açar, arka planda internetten günceller. Önbellek adı `fon-portfoyu-` + `VERSION`.
  - 1.9.7: kurulumda dosyalar `cache:'reload'`, arka plan güncellemesi `cache:'no-cache'` ile alınır; kayıt `updateViaCache:'none'`, uygulama öne gelince `reg.update()`. Önceden GitHub Pages'in 10 dk HTTP önbelleği yüzünden yeni sürüm eski `index.html` ile kurulabiliyordu (kullanıcı yayından hemen sonra denediğinde sürüm değişmedi). `tufe.json` için tersi: önce internet, yoksa cihazdaki kopya.
- `tufe.json`: TCMB TÜFE verisi (`{kaynak, guncelleme, son:'YYYY-AA', m:{'YYYY-AA':[yıllık%, aylık%]}}`). Elle düzenlenmez; GitHub Actions üretir.
- `.github/workflows/tufe.yml` + `.github/scripts/tufe.py`: her gün 11:23 (TR) TCMB'nin Tüketici Fiyatları sayfasını okur, yeni ay varsa `tufe.json`'u `main`'e yazar. Tablo okunamazsa iş hata verir (GitHub e-posta atar).
- `manifest.webmanifest`, `icons/` (simgeler yalnızca burada), `KURULUM.md`.

## Sürüm kuralı

- Güncel sürüm: **1.9.21**
- Her güncellemede **iki yerde** sürüm artırılır: `sw.js` içinde `VERSION`, `index.html` içinde `APPV`.
- Ayarlar sayfasının altında "sürüm X.Y.Z" yazar; kullanıcı bununla kontrol eder.

## Veri

- `localStorage` anahtarları: `fon-portfoyum-v2` (veriler), `fon-tema` (tema), `fon-son-yedek` (son yedek tarihi), `fon-gizli` (gizlilik modu), `fon-tufe` (TÜFE verisinin cihazdaki kopyası), `fon-silinenler` (1.9.19, Son silinenler: silinen fon / fiyat kaydı / yedekten önceki portföy; 30 gün, en çok 40 öğe ve 3 portföy; yedek dosyasına girmez).
- 1.9 veri alanları (norm() korur): fonda `chk` (fiyatın son kontrol tarihi). İşlem kayıtlarında `q` (adet), `p` (fiyat), `lot` (alımın sepet kimliği), `used` (satışta kullanılan sepet parçaları), `tax`, `rev`. Geçmişten düzenleme/silme kayıtlarında `ref` + `old` (geri almak için). Eski kayıtlarda bu alanlar yoktur; `buyInfo`/`sellInfo` metinden, `usedOf` satış öncesi/sonrası sepet farkından bulur.
- Fiyat geçmişi fon başına en çok 4000 kayıt (1.8.1'e kadar 400'dü).
- `navigator.storage.persist()` ile kalıcı depolama istenir.
- Yedekleme: "Dışa aktar" paylaşım menüsünü açar (iCloud Drive'a kaydedilebilir). "Dosyadan yükle" ile geri yüklenir. Yedek kodunu kopyalama ve eski yedek formatını içe aktarma da var.
- Yüklenen her veri `norm()` ile aynı şemaya getirilir. Bu davranış bozulmamalı.
  - 1.9.20: `norm()` sonsuz (`1e999`), negatif maliyet ve sayı olmayan değerleri almaz (`fin`/`pos`); fiyatı 0 olan fon fiyat geçmişinin son fiyatını alır; kod kırpılır, boşluk/`|` → `-`; aynı kodlu ikinci fon `KOD-2` olur; fon içinde aynı kimlikli sepet/kayıt yeni kimlik alır; veride ileri tarihli kimlik varsa `lastUid` ona çekilir (yeni kayıt aynı kimliği almasın). Uygulamanın kendi verisinde sonuç eski `norm` ile birebir aynı (test edildi).
  - Eski (Claude/Gemini) yedek biçiminde `5.1.2026` gibi sıfırsız tarihler doğru okunur (`oD`); önceden bugüne dönüyordu.
  - Yedek kodu "Kopyala" her zaman gerçek portföyü (`JSON.stringify(S)`) kopyalar ve kutuyu yeniler; önceden kutuya yapıştırılıp vazgeçilen metni kopyalayıp "yedek alındı" sayıyordu.
  - `fon-tufe` ve indirilen `tufe.json` `tufeClean` ile doğrulanır (`son` = YYYY-AA, aylar dizi); bozuk veri Ayarlar'ı çökertmez, sayfaya kod olarak giremez. `ayAd` yılı `esc` eder.

## Finans mantığı (doğru çalışıyor, korunmalı)

- **Stopaj:** her fon için varsayılan %17,5, fon bazında değiştirilebilir. Hisse fonlarına %0 uygulamak yanlıştı ve geri alındı. Elle değiştirilen oran `taxSet` bayrağıyla korunur.
- **Satış:** FIFO lot mantığıyla hesaplanır. Gerçekleşen kâr/zarar ayrıca tutulur.
  - 1.9.1: satış yalnızca **satış tarihinde portföyde olan** sepetlerden yapılır (`byDate`); sonradan alınan sepet geçmiş tarihli satışta kullanılamaz.
  - Aynı fonda kendisinden sonra satış olan eski bir satış düzenlenemez/silinemez (`laterSell`): FIFO sırası bozulmasın diye önce sonrakiler silinir. Sonraki satışları yeniden hesaplayan bir "tekrar oynatma" bilerek yapılmadı.
  - Satış düzenlenirken satışın kendi stopaj oranı korunur (`rateOf`), fonun güncel oranı değil.
  - 1.9.20 FIFO çelişki denetimi (`lc`, `sellClash`, `buyClash`, `clashMsg`): geçmiş tarihli **yeni satış** ya da tarihi değişen satış, kendisinden sonraki bir satışın kullandığı sepetten daha yeni bir sepete düşecekse; geçmiş tarihli **yeni alım**, alım düzenleme, silinen alımın ya da sepetin geri getirilmesi, kendi tarihinde/sonrasında yapılmış bir satışın kullandığı daha yeni bir sepetten önce gelecekse işlem yapılmaz ve hangi satışın engel olduğu yazılır. Önceden sessizce yanlış sepetten satıyordu (kâr/zarar ve stopaj yanlış satışa yazılıyordu). Tek sepetli ya da çelişmeyen geçmiş tarihli işlemler serbest. Sepet bilgisi olmayan eski satışlar denetlenemez.
- **Getiri (Midas mantığı):** her fonun tarihli fiyat kaydı tutulur (aynı gün tek kayıt).
  - Günlük getiri: bir önceki fiyat gününe göre.
  - Haftalık getiri: son fiyat tarihinden en az 7 gün önceki fiyata göre.
  - Dönem içinde alınan lotlar kendi maliyetiyle hesaplanır.
- **Biçim:** fiyat girişinde Türkçe ondalık virgül desteklenir. Her fonun rengi kendine ait.
  - 1.9.20: `pn` birden çok nokta (`1.234.567`) ya da birden çok virgülü binlik ayırıcı sayar; sonsuz/geçersiz değer `NaN` döner (önceden `Infinity` adet/fiyat girilebiliyordu). Yeni fon kodu boşluk ve `|` içeremez, en çok 12 karakter (`findTx` kimliği `kod|kayıt` biçiminde, `splitId` son `|`'den ayırır).
  - Sayı okuma: `pn` (fiyat/adet girişi; tek nokta ondalık sayılır), `pnM` (tutar kutuları; `10.000` = on bin), `trN` (uygulamanın kendi yazdığı Türkçe metinler, örn. eski kayıtlardaki "10.000 adet"). Eski kayıt metni asla `pn` ile okunmamalı.
  - `isDate` gerçek takvim tarihini doğrular (2025-19-05, 2025-02-30 reddedilir); `norm()` bozuk tarihli fiyat kayıtlarını atar.
- **Fiyatlar elle girilir.** TEFAS'tan otomatik fiyat çekme yok ve yapılmamalı: TEFAS botları F5 korumasıyla bilerek engelliyor, eski `api/DB/BindHistoryInfo` kapatılmış (2026-11 denendi). Bu korumayı atlatmaya çalışılmaz.
- **Toplu fiyat girişi** (`bulkModal`): tüm fonlar tek ekranda. 1.9.15'ten beri düzeni tekli "Fiyat · FON" penceresiyle aynı: üstte tarih, her fon için iki sütun (`.bpr`: solda fon kodu + son fiyat/tarih kutusu `.bpf`, sağda "Birim fiyat (₺)" kutusu `#bp_i`), açıklama, Vazgeç/Kaydet, en altta TEFAS'tan yapıştır (`.bpp`). Kullanıcının TEFAS'tan kendi kopyaladığı metin `parsePaste` ile okunur: fon kodundan sonraki ilk ondalıklı sayı fiyat, kodun hemen önündeki tarih o fiyatın tarihi.
- **Enflasyon (reel getiri):** her sepet kendi alış ayından son açıklanan aya kadar TÜFE ile karşılaştırılır (`inflFrom`, `realOf`). Satılmış sepetler dahil değil.
- **Nakit hesabı (1.9.20):** önerilen adet elde olan adetle sınırlanır ve kesirli adet olduğu gibi aktarılır (`nq`); önceden 0,4 adet varken 1 adet önerip satış ekranında reddediliyordu.
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
    - 1.9.20: ısı haritasında çok küçük kutuda (`xs`: 40×28 birimden küçük) yazı yok (önceden yarısı kesik görünüyordu); her kutuda `aria-label` (kod + getiri).
  - Alt sayfalar `PARENT` ile tanımlı (`tx` ve `year` → Özet, `detail` → Portföy); soldan kaydırınca üst sayfaya dönülür.
  - İşlem geçmişi: alım/satış düzenleme ve silme. Kısmen satılmış alım ya da sepet bilgisi bulunamayan eski satış kilitlidir, nedeni yazılır. Her değişiklik fonun Geçmiş sekmesine düşer ve "Geri al" ile geri alınır.
  - Gizlilik modu (göz düğmesi): tutarlar `••••`. Kayda yazılan metinler her zaman `moneyR`/`sgnR` ile gerçek tutarla yazılır.
    - 1.9.21 (kullanıcı isteği): adetler de gizlenir (`qn`: ekrandaki adet; `dtl` kayıt metnindeki "N adet/adetlik"). Kayda yazılan metinler `num` ile gerçek adetle kalır (buyTxt, sellTxt, commit açıklamaları — bunlarda `qn` kullanılmamalı). Satış panelinde "Tümü" adetsiz yazılır ama gerçek adeti doldurur. Giriş kutularındaki değerler (düzenleme formu) gerçek kalır. Birim fiyatlar (piyasa verisi) görünür.
  - Üst butonlar (1.9.13): Portföy'de göz (tutarları gizle) + tema + fon ekle; Özet'te yalnız göz; Ayarlar'da yok (tema Görünüm'de). Ayarlar'da Gizlilik bölümü yok; tutarları gizleme yalnız göz butonuyla.
  - Face ID kilidi 1.9.13'te kullanıcı isteğiyle tamamen kaldırıldı (kod, CSS, simge, Ayarlar satırı). Açılışta eski `fon-kilit` kaydı silinir.
- **Cam takvim (1.9.14):** iOS'un yerel tarih penceresine animasyon/stil verilemediği için modal içindeki her `input[type=date]` `dpEnhance` ile gizli alana çevrilir (id ve YYYY-AA-GG değeri aynı, hesap kodu `g('p_d')` vb. değişmedi) ve yanına `.dpb` kutusu eklenir. Dokununca `.dp` takvimi (body'de, z-index 40) kutudan yaylanarak büyüyüp açılır, seçince/dışarı dokununca kutuya doğru küçülerek kapanır. Bulanık yarı saydam cam (`--dp-bg` .86), ince kenar parlaması, yumuşak gölge. `max` (bugün) sonrası günler kapalı. Değer değişince `input`/`change` olayı yayılır. Takvim açıkken dışarı dokunmak yalnız takvimi kapatır; panel kapanırken takvim de kapanır.
  - 1.9.16 (kullanıcı daha yumuşak animasyon istedi): açılış `DP_SPRING` sönümlü yay eğrisiyle (`linear()`, ≈%0,5 taşma, 620 ms; desteklenmezse `cubic-bezier(.16,1,.3,1)`), `scale(.6)` + 10 px dikey kaymadan; saydamlık ayrı ve hızlı (220 ms); içerik 90 ms gecikmeyle hafifçe belirir. Kapanış 300 ms `scale(.72)`, saydamlık 60 ms sonra söner. Eski `filter:blur` kaldırıldı (bulanık camla birlikte Safari'de ağırdı) ve eski 1.025 sıçraması yok.
  - 1.9.18 (kullanıcı: 1.9.16 animasyonu "çok yavaş, yavan"): takvim tarih kutusunun kendisinden doğar — `transform-origin:0 0`, kutunun yeri/boyuna eşleyen `translate+scale(x,y)` (`DP.from()`) ile başlar, `dpSpr(.64,17,.52)` (sönümlü yay denkleminden üretilen `linear()`, ≈%7 taşma, 520 ms; ilk varış ≈170 ms) ile açılır, köşe 14→26. Saydamlık 130 ms; içerik (başlık, günler, alt satır) 60 ms + 40 ms aralıkla sırayla belirir. Seçilen gün `DP_POP` yayıyla zıplar, 170 ms sonra takvim kutuya geri çekilerek kapanır (260 ms). Ay değişince günler ve başlık yön yönünde kayarak gelir.
- **Saydam cam (1.9.19, kullanıcı isteği: Apple Music'teki "clear glass"):** sekme çubuğu (`.tabbar::after`), üst dairesel butonlar (`.ib`), geri butonları (`.cap`), bildirim (`#t`) ve segment çubukları yalnız CSS değişkenleriyle (`--cg-*`, `--tb-thumb`, `--segth/--segsh`, `--seg-rim`) güncellendi: çok düşük dolgu (koyu çubuk .26, koyu buton beyaz .07; açık çubuk beyaz .30, buton .42), `blur(10px) saturate(180%)`, üstten parlak alttan zayıf ince kenar + hafif pembe/mavi kenar kırılması + üst parlama gradyanı (`background-image`, `background-color` ayrı: mercek kodu `backgroundColor` okur), dış gölge. `.ib`/`.cap`/`#t`'de `clip-path:none` (dış gölge görünsün; köşeyi border-radius yuvarlar). Okunabilirlik için çubuk yazı/simgelerinde hafif hale (`--cg-ink`, `--cg-ico`). Kullanıcı kuralı: bu tür istekte JS/animasyon/yerleşim koduna dokunulmaz, yalnız malzeme.
- **Silme güvenliği (1.9.19):** her silme onay penceresi açar (fiyat kaydı silmede ve Geçmiş'teki "Geri al"da da). 1.9.20: Son silinenler'den geri getirilen sepet sonradan satılır/silinirse listede yeniden çıkmaz (`lostLot` sonraki kayıtlarda o sepetin eklendiğini arar); önceden ikinci kez geri getirilip bedava pay oluşuyordu. Geri getirme Geçmiş'ten geri alınırsa sepet yeniden listelenir. Eski kayıtta (adedi metinden okunamayan alım) sepet tutarı alım tutarından farklıysa (kısmen satılmış) düzenleme/silme kilitli. Silinen her şey geri getirilebilir: Ayarlar › **Son silinenler** (`trash` sayfası, `PARENT.trash='settings'`). Alım/satış/sepet: fonun geçmişindeki `undone` kayıtlardan bulunur (`trTxList`, süresiz). En son değişiklik bu silmeyse birebir geri alınır (`undoLast`), değilse aynı tarih/adet/fiyatla yeniden uygulanır (`trTx`, geçmişe `restore` türü "Geri getirme" kaydı düşer; satışta `laterSell` ve o tarihteki adet kontrol edilir). Fon, fiyat kaydı (sortLog'un düşürdüğü komşu kayıt dahil, `lost`) ve yedek yüklenmeden önceki portföy `fon-silinenler`'de (`trAdd`/`trRestore`); depolama doluysa kopya saklanamaz ve silme yapılmaz. Silmeden hemen sonra bildirimde "Geri al" düğmesi çıkar (`toast(m,act,id)`, 5,5 sn, yalnız görünürken dokunulur).
- **Satış uyarısı (1.9.18):** elde adet yoksa (`Q(f)=0`) Satış butonu soluk (`.btn.dim`) ve dokununca satış paneli yerine "Satılacak pay yok" uyarısı açılır (Tamam / Alım ekle).
- **Arka plan kaydırma kilidi (1.9.17):** alt panel açıkken (`modal()` → `lockScroll()`) gövde `position:fixed; top:-scrollY` ile dondurulur, `html.mlock` taşmayı/overscroll'u kapatır. Belge düzeyinde (capture) `touchmove` engellenir; yalnız panelin (`.sheet`) ya da takvimin (`.dp`) içindeki gerçekten kaydırılabilir öğede ve odaktaki kutuda serbest (`canScroll`). Kapanış başlarken (`closeM`, aşağı çekerek kapatma, `finishClose`) `unlockScroll()` aynı konuma döner. Panel açıkken `scrollY` 0 okunur; konum gerekiyorsa `curY()` kullanılmalı (`go()` öyle yapar).
- **Fon performansı (1.9.17, Yıllık özet):** eski "En iyi ve en kötü fon" yerine tüm fonların fiyat performansı listesi (`#pfl`). Başlığın sağında tek dokunuşla değişen sıralama butonu (`.sortb`, `data-act="psort"`, açılır menü değil): "En yüksek ↓" (varsayılan) / "En düşük ↑". Durum `view.psort` ('desc'/'asc'); dokununca sayfa yeniden çizilmez, satırlar FLIP ile yer değiştirir (`togglePerfSort`; `nofade` giriş animasyonunun yeniden başlamasını önler).
- **`.wrap` çakışması (1.9.14):** `wrap` ana kabın (`#app`) sınıfı; alt metinlerde satır kaydırma için kullanılan `sub wrap` ana kabın boşluk ve PWA'da ekran boyu yükseklik kurallarını alıp "Fiyatları güncelle" ve "Yıllık özet" kartlarını ekran boyu uzatıyordu. Adı `sub wl` yapıldı. Yeni bir yardımcı sınıfa `wrap` adı verilmemeli.
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
  - 1.9.21'den beri WebKit (Safari'nin motoru, JavaScriptCore) testi de yapılabiliyor: `apt-get install -y webkit2gtk-driver xvfb`, sonra `xvfb-run -a WebKitWebDriver --port=4444` ve WebDriver HTTP API'si ile `MiniBrowser` (`/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser`, `--automation`). Dokunma olayı yok; mantık, CSP, WebGL, service worker ve çizim denenir. `playwright install` çalıştırılmamalı.
  - Ortamın ağ izinlerine `sametcan00.github.io` eklendi (1.9.21): yayından sonra canlı `sw.js`'deki VERSION curl ile kontrol edilebilir.

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
- Gizlilikte Geçmiş sekmesinde tutar sızması (`dtl`); sepet silinince alım kaydının kalması; grafikte "Tümü" getirisinin ilk günün kârını düşmesi; fon grafiğinde çift nokta; toplu girişte yapıştırma kalıntıları; "Ocak–Ocak"; `tufe.json` sunucu hatasında önbelleğe dönülmemesi.
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
- **1.9.9 geri alındı (kullanıcı isteği):** 1.9.9'da kırılma ince kenar şeridine sınırlanmış (B=min(.16h,7), M=.42B), renk ayrışması yumuşatılmış ve uzak sekmeye geçişte jöle esnemesi (`jelly`, iki kenar ayrı yaylarla) eklenmişti. Kullanıcı 1.9.8'e dönmek istedi; kod 1.9.8'in aynısı, sürüm de 1.9.8 olarak yeniden yayınlandı. Yeniden istenirse 3b534fd işlemesine bakılabilir.
- **1.9.10 ince ayarları (temel görünüm 1.9.8; kullanıcı mercek hissini ve kenar kırılmasını korumak istiyor):**
  - Kırılma yalnız kenar şeridinde: B=min(.24h,11). Kaydırma `n·M·sin(π·d/B)`, M=.26B: kenarda (d=0) ve şeridin iç sınırında sıfır, arada eğri; eğim < 1. Böylece görüntü hiçbir yerde kopmaz ya da tekrarlanmaz (çiftlenme/kesilme yok), ortada kaydırma tam 0. 1.9.8'deki `s²` profili dışarıdan içeri çekiyordu: "Tümümü", "Özet" çiftlenmesi, "3A"nın "1Y"ye kayması.
  - Renk ayrışması: kanallar .86/1.14, kenara doğru `mix(düz, ayrık, .85·s)`; kenar koyulaşması .06, parlama koyu .6 / açık .85.
  - Aydınlık mod: gölgelendiricide parlamanın hemen içinde ince gri halka (`uLt`), `::after` kenar çizgisi .17, mercek açıkken `::before` yumuşak gölge (yalnız aydınlık modda).
  - Jöle esnemesi (`jelly`, ilk kez 1.9.9'da yazıldı): iki kenar ayrı yaylarla gider; uzak geçişte belirgin uzama + yaylanma, yakında tok. Ölçülen: uzak 67→141 px, yakın 67→74 px, sekme çubuğu uçtan uca 76→115 px. Sürükleme başlarken iptal edilir; mercek tuvali 16'lık basamakla ayrılır.
- **1.9.11 düzeltmeleri:**
  - **Kopya yok, kayma imkânsız:** WebGL tuvali yalnız kenar şeridini (d < B) çizer; şeridin içinde tamamen saydamdır, altta duran gerçek yazı/simgeler görünür (gösterge `.lqv` iken `::before` zemini kapalı). Şeridin iç yarısında kopyadan gerçeğe yumuşak geçiş (`smoothstep(B,.55B,d)`). Sebep: telefonda sekme çubuğundaki kopya yazı/simge dikeyde kayıyor, gerçekle çift görünüyordu ("1Y 1Y"); muhtemelen Safari'nin yazı tipi ölçüleri farklı. Test: mercek açıkken iç bölge, tuval gizlenmiş haliyle piksel piksel aynı (koyu/açık, sekme çubuğu ve iki seçici). Bu testi bozacak değişiklik yapılmamalı.
  - **Prizma rengi:** kanallar normal yönünde sabit küçük farkla da ayrılır (`n·1.15·s`), kenar parlaması açıya göre hafif gökkuşağı tonuna kayar (%38). Düz beyaz parlama yok.
  - **Esneme çubuğa göre:** `JELLY_K` = {rng:1 (referans, değiştirme), nav:.38, period/hm/theme/txt:.62, tab:.6}; listede olmayan çubukta `67/seçenek genişliği`. Şiddet gecikmeyi (`lag`) ve öndeki kenarın taşmasını ölçekler. Ölçülen: grafik aralığı uzak 67→141 yakın 67→74 (1.9.10 ile aynı), sekme çubuğu uçtan uca 76→90 (1.9.10'da 115), Günlük/Haftalık/Toplam uzak 110→165 yakın 110→122.
- **1.9.12: sekme çubuğundaki rastgele dikey kayma (kök neden bulundu):** tek WebGL tuvali açık olan merceğe taşınıyor, ama göstergeye göre `top`/`left` yalnız boyut değişince yazılıyordu. Segment merceğinden (dikey pay 6) sonra kalıcı sekme çubuğu göstergesine geçince tuval −8'de kalıyordu (doğrusu −12) → kenar şeridi ve kopyası 4 piksel kayık; hangi mercek en son kullanıldıysa ona göre "bir oluyor bir olmuyordu". Eski kodda testle yeniden üretildi (`ybug.js` mantığı).
  - Çözüm: sahip değişince önbellek sıfırlanır, tuval konumu `L.pos` farklıysa her seferinde yazılır.
  - Tüm ölçüler kabın kendi yerleşim koordinatlarında: dikey konum/yükseklik `offsetTop`/`offsetHeight` (CSS, dönüşümden etkilenmez); yatay yalnız o anki `translateX` (`DOMMatrixReadOnly(...).m41`) ve hesaplanan genişlik. Sahne çiziminde ekran ölçüleri kabın ölçeğine bölünür. Sayfa kayması/güvenli alan/kabın animasyonu etkilemez.
  - `.thumb{transform-origin:50% 50%;translate:none;rotate:none}`; esneme yarıda kesilirse yeni hareket o anki gerçek konumdan başlar.
  - Mercek açıkken (`.lqon`) seçeneklerin içindeki animasyon/dönüşüm kapalı (sekme simgesinin zıplaması dahil): gerçek simge kenar şeridine girip kesilmesin.
- **1.9.9 (geri alınmıştı):** kenar şeridi çok inceydi (B=7, M=.42B, `s²`); kullanıcı 1.9.8'e döndü, sonra aynı istekleri yineledi → 1.9.10.
- **Denenip bırakılanlar (tekrar denenmesin):**
  - 1.9.3: yazı kopyası + SVG filtre, içeriden dışarı uzatma. Yanlış yön; bant oluşmuyordu.
  - 1.9.4–1.9.5: opak kopya + SVG `feDisplacementMap`. Safari'de içeriği bütünüyle ~4 nokta kaydırdı, gerçek yazı arkada "damga" gibi kaldı. Sebep doğrulanamadı (feImage ölçüsü ya da 128 nötr değerinin renk uzayı).
  - 1.9.6: düz CSS (iz zemini `scaleY`, renk şeritleri). Yazı bükülmüyordu; kullanıcı gerçek kırılma istedi.
- Yalnız Chromium'da test edildi (ortamda WebKit yok). WebGL gölgelendirici iki tarayıcıda aynı matematikle çalışır, ama gerçek iPhone'da görünüm ve akıcılık kullanıcının kaydıyla doğrulanmalı.

## Açık konular

- 1.9.20–1.9.21'in gerçek iPhone'da doğrulanması: CSP WebKitGTK 2.52'de hiçbir şeyi engellemedi (mercek, TÜFE, service worker, dışa aktarma); gerçek iOS Safari'de ve ana ekran uygulamasında (paylaşım menüsü, simge) kullanıcı denemeli.
- Bilinen sınır: `localStorage` kaynağa (origin) bağlıdır; `sametcan00.github.io` altındaki diğer GitHub Pages projeleri aynı kaynağı paylaşır ve bu veriyi okuyabilir. Yalnız kendi depolarınız bu kaynağa sayfa koyabilir; özel alan adı ayrı kaynak sağlar.

- 1.8.1'in gerçek iPhone'da doğrulanması: hızlı dokunma, parmakla sürükleme, merceğin taşması.
- 1.9.2'nin gerçek iPhone'da doğrulanması: segmentlerde parmakla sürükleme.
- 1.9.12'nin gerçek iPhone'da doğrulanması: sekme çubuğunda rastgele dikey kayma/kesilme bitti mi; jöle esnemesi, aydınlık modda merceğin seçilmesi; WebGL cam mercek (kenarda bükülme, renk ayrışması, parlama) Safari'de sekme çubuğunda ve seçicilerde görünüyor mu, akıcı mı; yeni sürüm hemen yükleniyor mu (1.9.7 önbellek düzeltmesi).
- 1.9.19'un gerçek iPhone'da doğrulanması: saydam cam okunabilir mi (parlak içerik üstünde sekme yazıları), Safari'de `clip-path:none` ile butonların köşesinde kare bulanıklık çıkıyor mu; bildirimdeki "Geri al" dokunuşu.
- 1.9.18'in gerçek iPhone'da doğrulanması: takvim açılışı yeterince canlı/hızlı mı, cam bulanıklığıyla akıcı mı.
- 1.9.17'nin gerçek iPhone'da doğrulanması: alt panel açıkken arka plan kaymıyor mu (klavye açıkken dahil), panel kapanınca konum korunuyor mu.
- 1.9.0'ın gerçek iPhone'da doğrulanması: grafikte parmakla gezinme, TEFAS'tan kopyalanan gerçek metnin okunması.
- TÜFE işinin ilk otomatik güncellemesi (3 Aralık 2026, Kasım verisi) Actions sekmesinden kontrol edilmeli.
- Henüz istenmemiş olası geliştirmeler: hedef dağılım ve dengeleme, düzenli yatırım planı, Mac edinilirse yerel SwiftUI sürümü.
