# Fon Portföyüm: iPhone kurulum rehberi

Bu klasör, uygulamanın iPhone'a kurulacak eksiksiz halidir. Kurulduktan sonra:

- Ana Ekran'da kendi simgesiyle durur ve Safari çubukları olmadan tam ekran açılır.
- İlk açılıştan sonra internet olmadan da çalışır.
- Verileri iPhone'un içinde saklar. Uygulamayı kapatıp açmak veya telefonu yeniden başlatmak verileri silmez.

## Bu sürümde (1.1.0)

Uygulama içindeki bütün geçişler animasyonlu: fona girip çıkarken sayfa kayıyor ve fon simgesi yeni sayfaya uçuyor, sekmeler yönüne göre kayıyor, alt menüde ve seçicilerde vurgu kayarak ilerliyor, sayılar akarak değişiyor, alt paneller yaylı açılıyor ve aşağı çekince kapanıyor, silinen satırlar kapanarak kayboluyor, tema dokunduğun noktadan yayılarak değişiyor. iPhone'da **Ayarlar → Erişilebilirlik → Hareket → Hareketi Azalt** açıksa animasyonlar kapanır, geçişler anında olur.

**1.0.0 kuruluysa:** GitHub'daki deponda **Add file → Upload files** ile yeni `index.html` ve `sw.js` dosyalarını yükleyip **Commit changes**'e bas. iPhone'da uygulamayı uygulama değiştiriciden kapatıp iki kez aç. Verilerin olduğu gibi kalır; simgeyi silip yeniden eklemen gerekmez.

## Klasördeki dosyalar

| Dosya | Görevi |
|---|---|
| `index.html` | Uygulamanın tamamı: arayüz, hesaplar, kayıt |
| `manifest.webmanifest` | Uygulama adı, simgesi, tam ekran ayarı |
| `sw.js` | Çevrimdışı çalışma (dosyaları telefona kaydeder) |
| `icons/` | Ana Ekran simgesi (180, 192, 512 piksel) |

> Önemli: iOS, bir web uygulamasını Ana Ekran'a ancak internette **https** adresiyle yayınlanıyorsa ekler. Dosyayı telefona kopyalayıp açmak çalışmaz. Bu yüzden önce dosyaları ücretsiz bir yere yükleyeceğiz. Aşağıdaki yol tamamen ücretsiz ve Windows bilgisayardan yapılabilir.

---

## 1. Adım: Dosyaları GitHub Pages'e yükle (bilgisayardan, yaklaşık 10 dakika)

1. https://github.com/signup adresinden ücretsiz bir hesap aç (hesabın varsa giriş yap).
2. Sağ üstteki **+** → **New repository** seç.
   - Repository name: `fon-portfoyu`
   - **Public** seçili kalsın. GitHub Pages ücretsiz planda yalnızca herkese açık depolarda çalışıyor. Herkese açık olan yalnızca uygulamanın kodu; **fon verilerin bu depoya hiç gitmez**, sadece senin iPhone'unda durur.
   - **Create repository** düğmesine bas.
3. Açılan sayfada **uploading an existing file** bağlantısına tıkla.
4. Bu klasördeki her şeyi (`index.html`, `manifest.webmanifest`, `sw.js`, `KURULUM.md` ve `icons` klasörü) sürükleyip sayfaya bırak. `icons` klasörünü klasör olarak sürükle, içindekiler yerinde kalsın.
5. Aşağıdaki **Commit changes** düğmesine bas.
6. Deponun üstündeki **Settings** → sol menüde **Pages** bölümüne git.
   - **Source:** `Deploy from a branch`
   - **Branch:** `main`, klasör `/ (root)` → **Save**.
7. 1–2 dakika bekle ve sayfayı yenile. Üstte şu biçimde bir adres çıkacak:
   `https://KULLANICIADIN.github.io/fon-portfoyu/`
   Bu adresi bilgisayarda açıp uygulamanın göründüğünü kontrol et.

## 2. Adım: Eski verilerini al (Claude'daki sürümden)

1. Claude'daki uygulamayı aç → alttaki **Ayarlar** sekmesi.
2. **Yedek kodu** bölümünde **Kopyala**'ya bas.
3. Kodu kendine e-posta, Notlar ya da WhatsApp ile gönder; iPhone'da kopyalayabileceğin bir yere koy.

## 3. Adım: iPhone'a kur

1. iPhone'da **Safari**'yi aç (Chrome değil) ve 1. adımdaki adrese git.
2. Alttaki **Paylaş** düğmesine (yukarı ok olan kare) dokun.
3. Listeyi aşağı kaydır ve **Ana Ekrana Ekle**'ye dokun.
4. **Web Uygulaması Olarak Aç** seçeneği görünüyorsa açık olduğundan emin ol. Ad olarak "Portföy" gelir; istersen değiştir. Sonra **Ekle**'ye dokun.
5. Ana Ekran'daki **Portföy** simgesinden uygulamayı aç. Safari çubukları olmadan tam ekran açılmalı.

## 4. Adım: Verilerini uygulamaya taşı

1. Uygulamada **Ayarlar** → **Yedek kodu** kutusunun içindekileri sil.
2. 2. adımda kopyaladığın kodu yapıştır.
3. **Yapıştırılan yedeği geri yükle** → **Evet, değiştir**.
4. Bundan sonra **Ayarlar → Dışa aktar** → **Dosyalar'a Kaydet** ile iCloud Drive'a bir yedek al.

---

## Bilmen gerekenler

- **Uygulamayı yalnızca Ana Ekran simgesinden aç.** Aynı adresi Safari'de açarsan, iOS orayı ayrı bir uygulama sayar ve verilerini orada göremezsin.
- **Simgeyi silersen veriler de silinir.** Bu yüzden düzenli olarak **Dışa aktar** ile yedek al. Uygulama, 14 gündür yedek alınmadıysa ana ekranda seni uyarır. Yedeği geri getirmek için **Ayarlar → Dosyadan yükle**.
- **Veriler yalnızca bu iPhone'da durur.** Claude'daki sürümün aksine buluta eşitlenmez. Başka bir cihaza geçerken yedek dosyasını kullan.
- **Güncelleme:** `index.html` dosyasını değiştirdiğinde GitHub'a yeniden yükle ve `sw.js` içindeki `VERSION` değerini artır (örneğin `1.0.1`). Uygulamayı iki kez kapatıp açınca yeni sürüm gelir; verilerin kaybolmaz.
- **Fiyatlar elle giriliyor.** Bu sürüm TEFAS'tan otomatik fiyat çekmiyor.

## Sorun giderme

| Belirti | Çözüm |
|---|---|
| "Ana Ekrana Ekle" yok | Safari'de olduğundan emin ol; Paylaş menüsünü aşağı kaydır, en altta **Eylemleri Düzenle**'den ekleyebilirsin. |
| Simge açılınca Safari çubukları görünüyor | Simgeyi sil, 3. adımı tekrarla ve **Web Uygulaması Olarak Aç** seçeneğinin açık olduğundan emin ol. Simgeyi silmeden önce **Dışa aktar** ile yedek al. |
| Adres 404 veriyor | GitHub'da Settings → Pages ayarını kontrol et, 2–3 dakika bekle. Dosyaların klasörün içinde değil, deponun en üstünde olması gerekiyor (`index.html` doğrudan görünmeli). |
| Yeni sürüm gelmiyor | `sw.js` içindeki `VERSION` değerini artırıp yeniden yükle; uygulamayı uygulama değiştiriciden kapatıp iki kez aç. |
