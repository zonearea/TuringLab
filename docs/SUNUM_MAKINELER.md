# TuringLab — Video sunum rehberi

**Öğrenci:** Hüseyin Berkay Kayıkçı

Kayıt öncesi:

```powershell
chcp 65001
cd C:\Users\Berkay\Desktop\business\OtomataOdev
```

**Senin akışın (sırayla):** README → `unary_to_binary` YAML → `demo.py` → terminal **TM-1** → `tm_engine.py` → terminal **TM-2** → **TM-3** + tasarım → bonus → kapanış.

El kitabı: en az **2** ödev makinesi şart; bu planda **3** gösteriyorsun: **TM-1 + TM-2 + TM-3**.

---

## 1. README — giriş (~45 sn)

> **[EKRAN]** `README.md` aç.

**Söyle:**

> Merhaba hocam, ben Hüseyin Berkay Kayıkçı. TuringLab final ödevim: tek şeritli deterministik TM motoru.
> Makineler **YAML**’da — el kitabı formatı; motor ayrı, tanım `machines/` içinde; `demo.py` ve pytest aynı dosyayı kullanıyor.
> Ödevde dört makine, repoda el kitabı örnekleri de var.
> Sırada: YAML, üç ödev makinesi terminalde, motorda sonsuz şerit, bonus.

---

## 2. TM-1 YAML — `unary_to_binary` (~30 sn)

> **[EKRAN]** `machines/unary_to_binary.yaml` aç.

**Ne işe yarıyor (özet):** Bu dosya **TM-1’in kural listesi**. Motor çalışırken buradan okur: hangi durumda, hangi sembolü görünce ne yazıp sola/sağa gideceği.

**Söyle:**

> Bu YAML birinci ödev makinesi: sadece `1`’lerden oluşan girdiyi ikili sayıya çeviriyor — `111` gibi üç tane `1`, çıktı `11`, yani 3.
> Dosyada durumlar ve geçişler var; Python’a gömülü değil, buradan yükleniyor.
> Mantık kısaca: soldaki `1`’leri tek tek sil, sağdaki ikili sayacı artır; bitince kabul.

---

## 3. `demo.py` (~30 sn)

> **[EKRAN]** `demo.py` aç — `SingleTapeTM.from_yaml` ve `tm.run` satırları (~168–178).

**Söyle:**

> Terminal demoları `demo.py` ile. YAML yolu veriliyor, motor dosyayı yüklüyor,
> `run` verbose modda her adımı basıyor. Az önce baktığımız makine de böyle çalışıyor.

---

## 4. Terminal — ilk makine TM-1 (~1–1,5 dk)

> **[TERMINAL]**

```powershell
python demo.py tm1
```

veya:

```powershell
python demo.py unary_to_binary
```

**Söyle (çıktı gelirken):**

> Şimdi canlı çalıştırıyorum. Üstte kural satırları, altta adım adım durum ve şerit;
> köşeli parantez kafanın yeri. Sonunda kabul ve ikili sonuç — `111` için `11` gibi.
> Çok `B` görünmesi sayaç alanının boş gezilmesi; hata değil.

Birkaç on adım yeter; sonuç satırını mutlaka göster.

---

## 5. `tm_engine.py` — sonsuz şerit (~1 dk)

> **[EKRAN]** `turinglab/tm_engine.py` → `run` içinde ~247: `tape: dict[int, str]` ve `read_cell` / `tape.get(head, self.blank)`.

**Söyle:**

> Az önceki uzun çıktıda şerit sürekli genişliyor; teoride sonsuz.
> İlk denemede listeyle yaptım — kafa sola gidince indeks hatası alıyordum.
> Çözüm: şeridi sözlük yaptım; indeks negatif de olabiliyor, okunmayan hücre otomatik blank.
> `max_steps` ise sonsuz döngüye karşı emniyet; durma problemi çözümü değil.

İstersen 5 sn `from_yaml` (~99): “YAML buradan yükleniyor.”

---

## 6. İkinci demo — TM-2 `binary_compare` (~30–40 sn)

> **[TERMINAL]** Uzun adım listesi istemiyorsan `--quiet`:

```powershell
python demo.py tm2 --quiet
```

**Söyle:**

> **TM-2:** ikili karşılaştırma — şeritte `sol#sağ` yazıyorsun,
> sol sayı sağdan büyükse kabul. Örnek `1100#1011` — soldaki 12, sağdaki 11, kabul.
> TM-4 mod 3 de repoda; zaman yetmezse sadece `demo.py --only odev` dersin.

---

## 7. Üçüncü demo — TM-3 `string_copy` + tasarım (~1,5 dk)

### 7a. Kısa YAML (isteğe bağlı, ~15 sn)

> **[EKRAN]** `machines/string_copy.yaml` — “TM-3: kelime kopyalama.”

### 7b. Terminal

> **[TERMINAL]**

```powershell
python demo.py string_copy --girdi ab
```

**Söyle:**

> `ab` → `ab#ab`. Sona `#`, başa dönüş, harfleri işaretleyip sağa kopyalama.

### 7c. Tasarım kararı (en zorlandığın)

**Söyle:**

> En çok bu makinede zorlandım: `#` sonrası başa dönmek için sola dönmek,
> `X` işaretini kopyalamadan silmemek, `a` ve `b` için ayrı durumlar.
> Bonus’taki iki şerit kopya daha kolaydı; ödev tek şerit istediği için YAML’de böyle bıraktım.

---

## 8. Bonus + kapanış (~1 dk)

> **[TERMINAL]**

```powershell
python scripts/demo_bonus.py bonus1
python scripts/demo_bonus.py bonus2
```

**Söyle:**

> Bonus 1: iki şerit, `ab` iki şeritte de kopya. Bonus 2: belirsiz TM, BFS ilk kabul yolunu buluyor.

İsteğe bağlı:

```powershell
python -m pytest tests/ -q
```

> 44 test geçti. Özet: README, YAML, motor, **üç ödev makinesi**, bonus. Teşekkürler.

---

## Komutlar (tek bakış)

| Sıra | Ne | Komut / dosya |
|------|-----|----------------|
| 1 | Giriş | `README.md` |
| 2 | TM-1 tanım | `machines/unary_to_binary.yaml` |
| 3 | Demo script | `demo.py` |
| 4 | TM-1 çalıştır | `python demo.py tm1` |
| 5 | Motor / şerit | `turinglab/tm_engine.py` (~247) |
| 6 | TM-2 çalıştır | `python demo.py tm2 --quiet` |
| 7 | TM-3 çalıştır | `python demo.py string_copy --girdi ab` |
| 8 | Bonus | `python scripts/demo_bonus.py bonus1` / `bonus2` |
| 9 | Test (isteğe bağlı) | `python -m pytest tests/ -q` |

---

## Süre özeti

| Bölüm | Süre (örnek) |
|--------|----------------|
| README (giriş) | ~45 sn |
| unary_to_binary YAML | ~1 dk |
| demo.py | ~30 sn |
| Terminal TM-1 | ~1–1,5 dk |
| tm_engine sonsuz şerit | ~1 dk |
| Terminal TM-2 (`--quiet`) | ~30–40 sn |
| string_copy + tasarım | ~1–1,5 dk |
| Bonus + kapanış | ~1 dk |

**Toplam:** ~8–10 dk

**3 makine sırası:** TM-1 (sayı) → TM-2 (karşılaştırma) → TM-3 (kopya + tasarım). TM-4 yerine mod 3 istersen: `python demo.py tm4 --quiet`.
