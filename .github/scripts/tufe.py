"""TCMB 'Tüketici Fiyatları' sayfasındaki TÜFE tablosunu okuyup tufe.json üretir.

Kaynak: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Tuketici+Fiyatlari
Biçim:  {"kaynak": ..., "guncelleme": "YYYY-AA-GG", "son": "YYYY-AA", "m": {"YYYY-AA": [yillik_yuzde, aylik_yuzde], ...}}
Veri değişmediyse dosyaya dokunulmaz (gereksiz kayıt oluşmasın).
Tablo okunamazsa (site değiştiyse) hata koduyla çıkar; GitHub bu durumda depo sahibine e-posta gönderir.
"""
import datetime
import html
import json
import re
import sys
import time
import urllib.request

URL = ("https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/"
       "Istatistikler/Enflasyon+Verileri/Tuketici+Fiyatlari")


def indir():
    son_hata = None
    for deneme in range(4):
        try:
            istek = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (fon-portfoyu TUFE okuyucu)"})
            with urllib.request.urlopen(istek, timeout=60) as yanit:
                return yanit.read().decode("utf-8", "replace")
        except Exception as hata:  # ağ hatasında birkaç kez dene
            son_hata = hata
            time.sleep(5 * (deneme + 1))
    raise SystemExit(f"TCMB sayfası indirilemedi: {son_hata}")


def sayi(metin):
    metin = metin.strip().replace(",", ".")
    return float(metin)


def oku(sayfa):
    aylar = {}
    for satir in re.findall(r"<tr[^>]*>(.*?)</tr>", sayfa, re.S | re.I):
        hucre = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip()
                 for h in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", satir, re.S | re.I)]
        if len(hucre) < 3:
            continue
        m = re.fullmatch(r"(0[1-9]|1[0-2])-(\d{4})", hucre[0])
        if not m:
            continue
        try:
            yillik, aylik = sayi(hucre[1]), sayi(hucre[2])
        except ValueError:
            continue
        if not (-50 < aylik < 100 and -50 < yillik < 1000):
            continue
        aylar[f"{m.group(2)}-{m.group(1)}"] = [yillik, aylik]
    return dict(sorted(aylar.items()))


def main(cikti):
    aylar = oku(indir())
    if len(aylar) < 100:
        raise SystemExit(f"TÜFE tablosu okunamadı (yalnızca {len(aylar)} ay bulundu); TCMB sayfası değişmiş olabilir.")
    try:
        with open(cikti, encoding="utf-8") as f:
            eski = json.load(f)
    except (FileNotFoundError, ValueError):
        eski = {}
    if eski.get("m") == aylar:
        print(f"Değişiklik yok. Son ay: {max(aylar)}")
        return
    veri = {
        "kaynak": "TCMB - Tüketici Fiyatları (TÜİK verisi)",
        "guncelleme": datetime.date.today().isoformat(),
        "son": max(aylar),
        "m": aylar,
    }
    with open(cikti, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print(f"tufe.json yazıldı: {len(aylar)} ay, son ay {veri['son']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tufe.json")
