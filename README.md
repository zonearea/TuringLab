# TuringLab — Hüseyin Berkay Kayıkçı

Selçuk Üniversitesi, Hesaplama Kuramı dersi için **TuringLab** final ödevi.  
El kitabı: [TuringLab Öğrenci El Kitabı (PDF)](https://github.com/user-attachments/files/27605487/TuringLab_Ogrenci_ElKitabi.pdf)

## Video sunum

Ödevin canlı anlatımı ve terminal demoları:

**[YouTube — TuringLab sunum](https://www.youtube.com/watch?v=_4cI3NZbW9U)**

Kayıt sırasında gösterilenler kısaca: README ve proje yapısı, YAML makine tanımları, `demo.py` ile adım adım çalıştırma, motorda sonsuz şerit sorunu ve çözümü, üç ödev makinesi (unary→ikili, ikili karşılaştırma, dize kopyalama), bonus modüller. Sunum metni: [docs/SUNUM_MAKINELER.md](docs/SUNUM_MAKINELER.md).

---

## Bu repo ne yapıyor?

Tek şeritli **deterministik Turing makinesi** simülatörü. Her makine bir **YAML dosyasında** tanımlı; Python motoru (`turinglab`) dosyayı okuyup şerit üzerinde adım adım ilerliyor. Terminalde her adımda durum, şerit ve hareket görünüyor (`Adım | Durum | Şerit | Hareket`); köşeli parantez kafanın yerini gösteriyor.

Makine kurallarını koda gömmek yerine YAML kullandım çünkü el kitabı da bu formatta ve yeni makine eklemek ya da geçiş düzeltmek dosyayı açmak kadar kolay. `demo.py` ve `pytest` aynı YAML dosyalarını kullanıyor.

**Bölüm 1:** Motor + el kitabı örnekleri (ikili +1, unary artırma, palindrom vb.).  
**Bölüm 2:** Dört ödev makinesi (aşağıdaki tablo).  
**Bonus:** Çok şerit, belirsiz TM + BFS, görselleştirme — [docs/BONUS.md](docs/BONUS.md).

---

## Ödev makineleri (Bölüm 2)

| | Dosya | Ne yapıyor? |
|---|--------|-------------|
| TM-1 | [unary_to_binary.yaml](machines/unary_to_binary.yaml) | `111…` gibi unary girdi → aynı sayının ikili yazımı (`111` → `11`, yani 3) |
| TM-2 | [binary_compare.yaml](machines/binary_compare.yaml) | `sol#sağ` — sol ikili sayı sağdan büyükse kabul |
| TM-3 | [string_copy.yaml](machines/string_copy.yaml) | `abba` → `abba#abba` (tek şeritte kopya) |
| TM-4 | [unary_div3.yaml](machines/unary_div3.yaml) | `1^n` yalnızca n, 3’ün katıysa kabul (`111` evet, `11` hayır) |

Tasarım notları ve kenar durumlar: [docs/design_notes.md](docs/design_notes.md).  
Mini-rapor (Bölüm 3): [REPORT.md](REPORT.md).

En çok uğraştığım kısım **TM-3 (dize kopyalama)**: ayırıcı `#` sonrası yön, işaret sembolü `X`’in zamanlaması, `a`/`b` için ayrı durumlar. Motor tarafında şeridi başta liste ile denedim; kafa sola gidince indeks hatası alınca **seyrek sözlük** (`dict[int, str]`) kullandım — detay [turinglab/tm_engine.py](turinglab/tm_engine.py).

---

## El kitabı örnekleri (`machines/`)

| Dosya | Kısa açıklama |
|--------|----------------|
| [binary_increment.yaml](machines/binary_increment.yaml) | İkili +1 (`1011` → `1100`) |
| [unary_increment.yaml](machines/unary_increment.yaml) | Unary’ye bir `1` ekleme |
| [even_a.yaml](machines/even_a.yaml) | Çift sayıda `a` |
| [binary_palindrome.yaml](machines/binary_palindrome.yaml) | `{0,1}` palindrom |

---

## Kurulum ve çalıştırma

**Gereksinimler:** Python 3.10+, `pip install -r requirements.txt` (Bölüm 1’de esasen PyYAML + pytest).

Windows’ta Türkçe terminal çıktısı için:

```powershell
chcp 65001
cd <proje-klasörü>
```

Tüm testler:

```bash
python -m pytest tests/ -q
```

Makine listesi ve demolar:

```powershell
python demo.py --list
python demo.py tm1                    # TM-1 unary → ikili
python demo.py tm2 --quiet            # TM-2 karşılaştırma (kısa çıktı)
python demo.py string_copy --girdi ab # TM-3 kopya
python demo.py tm4 --quiet            # TM-4 mod 3
python demo.py --only odev            # dört ödev makinesi sırayla
```

Bonus:

```powershell
python scripts/demo_bonus.py bonus1
python scripts/demo_bonus.py bonus2
```

Daha fazla komut: [docs/DEMO_KOMUTLAR.md](docs/DEMO_KOMUTLAR.md).

---

## Proje yapısı (kısa)

| Yol | İçerik |
|-----|--------|
| `turinglab/tm_engine.py` | Ana motor: YAML yükleme, `run`, seyrek şerit |
| `machines/*.yaml` | Makine tanımları |
| `demo.py` | Terminal demosu |
| `tests/` | Motor + makine testleri |
| `scripts/` | Üretim betikleri, bonus demo, video yardımcıları |

Şerit `dict` ile tutulur; kafa negatif indekse gidebilir, okunmayan hücre `blank` sayılır. `max_steps` sonsuz döngüye karşı emniyet sınırıdır (durma problemi çözümü değil).

---

## Diğer belgeler

- [docs/DAILY_LOG.md](docs/DAILY_LOG.md) — geliştirme günlüğü  
- [docs/VIDEO_SUNUM.md](docs/VIDEO_SUNUM.md) — uzun video senaryosu (Bölüm 1–8)  
- [docs/BONUS.md](docs/BONUS.md) — bonus kurulum (`requirements-bonus.txt`)

## GitHub

Depoyu uzaktan bağlamak için:

```bash
git remote add origin <repo-URL>
git push -u origin main
```

(Dal adın `master` ise son satırda `master` kullan.)
