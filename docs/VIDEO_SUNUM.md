# TuringLab — Video sunum rehberi

**Öğrenci:** Hüseyin Berkay Kayıkçı  
**Süre:** ~8–10 dakika  
**Örnek:** [Doğukan Sancar — TuringLab demo](https://www.youtube.com/watch?v=FtciwbH_vqg)

**Makine makine anlatım + yaşanan zorluklar:** [SUNUM_MAKINELER.md](SUNUM_MAKINELER.md)

Kayıt öncesi terminalde UTF-8 (Türkçe çıktı için):

```powershell
chcp 65001
cd C:\Users\Berkay\Desktop\business\OtomataOdev
```

Tüm demoları sırayla çalıştırmak için:

```powershell
python scripts/demo_video.py --all
```

Tek bölüm: `python scripts/demo_video.py --section 3` (1–8 arası).

---

## Bölüm 1 — Giriş (30 sn)

**Söylenecek:**

> Merhaba hocam, ben Hüseyin Berkay Kayıkçı. TuringLab final ödevimin sunumunu yapıyorum. Projede Python ile tek şeritli deterministik Turing makinesi motoru yazdım. Makineler YAML dosyalarında tanımlı, testler pytest ile çalışıyor.

**Ekran:** Proje kökü, [README.md](../README.md) kısa gösterim.

**Komut (isteğe bağlı):**

```bash
python scripts/demo_video.py --section 1
```

---

## Bölüm 2 — Motor mimarisi / sonsuz şerit (1,5 dk)

**Söylenecek:**

> En büyük mimari zorluk sonsuz şerit modeliydi. Standart liste kullansaydım, kafa 0. indeksin soluna geçince IndexError alacaktım. Şeridi seyrek sözlük `dict[int, str]` ile tuttum; kafa sola veya sağa gittiğinde yeni hücre otomatik blank alıyor.

**Ekran:** [turinglab/tm_engine.py](../turinglab/tm_engine.py) — `run` içinde `tape: dict[int, str]` (yaklaşık satır 247–261).

**Komut:**

```bash
python scripts/demo_video.py --section 2
```

---

## Bölüm 3 — TM-1: Unary → Binary (2 dk)

**Söylenecek:**

> İlk ödev makinesi: `1^n` girdisini ikili sayıya çeviriyor. Sonuna `X` ayırıcısı, sağda 8 bitlik sayaç; her tur bir `1` silinip sayaç artıyor.

**Komut:**

```bash
python scripts/demo_video.py --section 3
```

**Beklenen çıktı (özet):**

```
Adım 0 | Durum: q0 | Şerit: [1]11 | Hareket: R
...
Sonuç: accept | şerit: '11' | adım: 73
```

**Söylenecek:**

> Girdi `111` (3), çıktı `11` (ikili 3). Tek şeritte sürekli sola-sağa gidildiği için adım sayısı yüksek (~70+); bu normal.

---

## Bölüm 4 — TM-2: Binary Compare (1,5 dk)

**Söylenecek:**

> `sol#sağ` biçiminde iki ikili sayı; sol sağdan büyükse kabul. Solda 0→`r`, 1→`s` işaretleniyor; sağda eşit bitler de işaretleniyor, sonraki turda atlanıyor.

**Komut:**

```bash
python scripts/demo_video.py --section 4
```

**Beklenen (son):**

```
Sonuç: accept | adım: 31
```

**Söylenecek:**

> `1100#1011` → 12 > 11, kabul. Eşit (`11#11`) veya sol küçük (`1011#1100`) ret.

---

## Bölüm 5 — TM-3: String Copy — yaşanan sorun (2 dk)

**Söylenecek:**

> En çok zorlandığım makine. `w` → `w#w` (örnek `abba` → `abba#abba`). İlk sürümde `#` yazıldıktan sonra kafa yanlış yöne gidiyordu; çıktı `abba#` kalıp ret oluyordu.

**Yaşanan hatalar (anlatım için):**

| Sorun | Belirti | Düzeltme |
|--------|---------|----------|
| `#` sonrası yön | `q_whash` sonrası kafa sağda, `q_loop` boşlukta ret | `q_run` sonunda `#` yazıp **L** ile son karaktere dön |
| X erken siliniyor | Kopya `ab#a` gibi yarım kalıyor | `q_wa`/`q_wb` X’i korur; `q_reta`/`q_retb` kopyadan sonra X→a/b |

**Komut:**

```bash
python scripts/demo_video.py --section 5
```

**Beklenen (özet):**

```
Adım 7  | Durum: q_mka | Şerit: X[b]# | …
Sonuç: accept | şerit: ab#ab | adım: 36
```

---

## Bölüm 6 — TM-4: Unary mod 3 (45 sn)

**Söylenecek:**

> Öğrenci seçimi: `1^n`, n 3’ün katıysa kabul. Üç durumlu sayaç; boş girdi `q_start` ile ret.

**Komut:**

```bash
python scripts/demo_video.py --section 6
```

**Beklenen:**

```
111     → accept  (3)
111111  → accept  (6)
11      → reject  (2)
```

---

## Bölüm 7 — Tüm testler (1 dk)

**Söylenecek:**

> Motor 12, ödev makineleri 26, bonus 6 test — toplam 44 test.

**Komut:**

```bash
python scripts/demo_video.py --section 7
```

veya doğrudan:

```bash
python -m pytest tests/ -v
```

**Beklenen:**

```
44 passed in ~20s
```

---

## Bölüm 8 — Kapanış (30 sn)

**Söylenecek:**

> Deterministik TM’de her (durum, okunan) tek geçiş olmalı. TM-3’te işareti erken silmek hataya yol açtı; pytest regresyonu bunu yakaladı. Dinlediğiniz için teşekkürler.

**Komut:**

```bash
python scripts/demo_video.py --section 8
```

---

## Kayıt kontrol listesi

- [ ] `chcp 65001` veya `.\scripts\run_video_demo.ps1` (UTF-8 + `--all`)
- [ ] `python -m pytest tests/ -q` yeşil (44 passed)
- [ ] Ses + ekran kaydı (terminal + isteğe bağlı YAML/dosya)
- [ ] Video yükleme (hoca talimatı)
- [ ] İsteğe bağlı: `git tag final && git push origin final`
