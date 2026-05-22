# TuringLab — Makine makine sunum rehberi

**Öğrenci:** Hüseyin Berkay Kayıkçı  
**Süre önerisi:** ~10–12 dk (8 makine + giriş + test + kapanış)

Kayıt öncesi:

```powershell
chcp 65001
cd C:\Users\Berkay\Desktop\business\OtomataOdev
```

Her makine için tek komut: `python demo.py <ad>` (kurallar üstte, adımlar altta).

---

## Giriş (45 sn)

**Söyle:**

> Merhaba hocam, ben Hüseyin Berkay Kayıkçı. TuringLab final ödevimde tek şeritli deterministik Turing makinesi motoru yazdım. Makineler YAML’da tanımlı; Python motoru okuyup adım adım simüle ediyor. Testler pytest ile.

**Göster:** Kök klasör, `README.md`, `machines/`, `turinglab/tm_engine.py`.

**İsteğe bağlı:** `python demo.py --list`

---

## Motor — ortak zemin (1 dk)

**Söyle:**

> Tüm makineler aynı `SingleTapeTM` sınıfını kullanıyor. En büyük zorluk sonsuz şeritti: liste ile kafa sola gidince indeks hatası alıyordum. Şeridi `dict[int, str]` yaptım; kafa negatif indekse gidebiliyor, okunmayan hücre otomatik blank.

**Göster:** `turinglab/tm_engine.py` içinde `tape: dict[int, str]` ve `read_cell` / `write_cell`.

**Yaşadığım zorluk:** Teoride şerit sonsuz; pratikte bellek sınırlı — `max_steps` ile döngü koruması koydum (Halting problemi çözümü değil, emniyet).

---

## 1. `binary_increment` — ikili +1

**Komut:** `python demo.py binary_increment`

| | |
|--|--|
| **Girdi** | `{0,1}+` örn. `1011` |
| **Görev** | İkili sayıya 1 ekle |
| **Kabul** | Şerit doğru toplama sonucu (`1100`) |
| **YAML** | `machines/binary_increment.yaml` |

**Söyle:**

> El kitabı örneği. Kafa ikili sayı üzerinde taşıma (carry) yaparak son basamağı artırıyor. Verbose çıktıda `[ ]` kafanın yerini gösteriyor.

**Zorluk:** Bu makineyi ben yazmadım; el kitabı / Goldberg hattı üzerinden doğruladım. Asıl öğrenme, verbose formatının şartnameye uygun basılmasıydı (`Adım | Durum | Şerit | Hareket`).

**Beklenen son satır:** `accept`, şerit `1100` civarı.

---

## 2. `unary_increment` — unary +1

**Komut:** `python demo.py unary_increment`

| | |
|--|--|
| **Girdi** | `1+` örn. `111` |
| **Görev** | Bir tane `1` ekle |
| **Kabul** | `111` → `1111` |
| **YAML** | `machines/unary_increment.yaml` |

**Söyle:**

> Sadece birlerden oluşan sayıya sona bir `1` ekliyor. TM-1’den daha basit; Bölüm 1’de motorun doğru çalıştığını göstermek için.

**Zorluk:** Az durumlu makine; asıl zorluk uzun girdide adım sayısının artması — tek şeritte sürekli sağa gidip dönme.

---

## 3. `even_a` — çift sayıda `a`

**Komut:** `python demo.py even_a`

| | |
|--|--|
| **Girdi** | `{a,b}*` örn. `abab` |
| **Görev** | `a` harfi sayısı çift mi? |
| **Kabul** | Çift ise evet; `ab` ret |
| **YAML** | `machines/even_a.yaml` |

**Söyle:**

> Alfabede `a` ve `b` var; makine yalnızca `a`’ları sayıyor (veya eşliyor). `abab` kabul, `ab` ret — tek `a` var.

**Zorluk:** İki harfli alfabe; geçiş tablosunda her `(durum, sembol)` için tek çıkış olmalı — YAML’de çakışan geçiş yükleme hatası veriyor, bunu testlerle yakaladım.

---

## 4. `binary_palindrome` — 0/1 palindrom

**Komut:** `python demo.py binary_palindrome`

| | |
|--|--|
| **Girdi** | `{0,1}*` örn. `0110` |
| **Görev** | Palindrom mu? |
| **Kabul** | Evet; eşleşen bitler silinir, şerit boşalır |
| **YAML** | `machines/binary_palindrome.yaml` (Goldberg FCS tabanı) |

**Söyle:**

> Dıştan içe: soldaki ilk bit silinir, sona gidilir, sağdaki son bit ile karşılaştırılır. Aynıysa o da silinir; değilse ret. `0110` kabul, `01` ret.

**Durum özeti:** `i` → `p0/p1` (sona) → `q0/q1` (son bit) → `r` (başa) → tekrar `i` → bitince `t`.

**Zorluk:** Geçiş tablosunu sıfırdan yazmadım; hazır örneği projeye uyarladım. Uyuşmazlıkta `q_reject` — tek yanlış bitte ret.

**Ek komut:** `python demo.py binary_palindrome --girdi 01` → ret göster.

---

## 5. `unary_to_binary` — TM-1 (ödev)

**Komut:** `python demo.py unary_to_binary` veya `python demo.py tm1`

| | |
|--|--|
| **Girdi** | `1^n`, n≥1, n≤255 |
| **Görev** | Unary → ikili yazım |
| **Kabul** | Şerit = n’nin ikili hali (`111` → `11`) |
| **YAML** | `machines/unary_to_binary.yaml` |
| **Üretim** | `scripts/gen_unary_to_binary.py` |

**Söyle:**

> Sağda 8 bitlik sayaç, solda unary’den her tur bir `1` siliniyor, sayaç +1. Sonunda baştaki gereksiz sıfırlar temizleniyor. `111` için yaklaşık 70+ adım — tek şeritte çok gidip gelme normal.

**Yaşadığım zorluklar (önemli — videoda anlat):**

1. **`q_rw1` / `q_lr`:** Unary silme turunda kafa yanlış yönde kalınca `no_transition` — `q_rw1`’de X’e gelince `L`, `q_lr`’de sol baştaki `1` doğrudan silme yolu düzeltildi.
2. **`q0, 0`:** Başta `0` girdisi ret olmalı — ayrı geçiş eklendi.
3. **Taşma:** 256 bir → `q_rv` ile ret; test `test_unary_to_binary_overflow_reject`.

**Beklenen:** `accept`, şerit `'11'`, adım sayısı yüksek.

---

## 6. `binary_compare` — TM-2 (ödev)

**Komut:** `python demo.py binary_compare` veya `python demo.py tm2`

| | |
|--|--|
| **Girdi** | `w#v`, ikili örn. `1100#1011` |
| **Görev** | Sol ikili > sağ ikili? |
| **Kabul** | Büyükse evet; eşit/küçük ret |
| **YAML** | `machines/binary_compare.yaml` |
| **Üretim** | `scripts/gen_binary_compare.py` |

**Söyle:**

> MSB’den başlayarak bit bit karşılaştırma. Solda 0→`r`, 1→`s` işareti; eşit bitte sağda da işaret konur. Sonraki turda işaretli hücreler atlanır. `1100#1011` → 12 > 11 → kabul.

**Yaşadığım zorluklar:**

1. **Sağ şerit işaretlenmiyordu:** Her turda sağın en başındaki bit ile karşılaştırılıyordu; ikinci bit hep yanlış eşleşiyordu. Çözüm: `q_r0` / `q_r1` ile sağda da `r`/`s` yazmak.
2. **`q_prevl` boşlukta ret:** Eşit bitten sonra sola dönünce blank’te ret — blank’te `q_next`’e `R` ile devam.
3. **Eşitlik:** `11#11` ret olmalı — `q_left_done` sağda fazla 0/1 kontrolü.

**Ek:** `python demo.py binary_compare --girdi 11#11` → ret.

---

## 7. `string_copy` — TM-3 (ödev)

**Komut:** `python demo.py string_copy` veya `python demo.py tm3`

| | |
|--|--|
| **Girdi** | `{a,b}+` örn. `abba` |
| **Görev** | `w` → `w#w` |
| **Kabul** | `abba#abba` |
| **YAML** | `machines/string_copy.yaml` |
| **Üretim** | `scripts/gen_string_copy.py` |

**Söyle:**

> Sona `#` konur. Her turda soldan bir harf `X` ile işaretlenir, şerit sonundaki boşluğa kopyalanır, `X` tekrar `a` veya `b` yapılır. Kısa demo: `python demo.py string_copy --girdi ab` (~36 adım).

**Yaşadığım zorluklar (en uzun kısım — videoda vurgula):**

1. **`#` sonrası yön:** `#` yazıldıktan sonra kafa sağa gidiyordu → `q_loop` boşlukta ret, çıktı `abba#` kalıyordu. Düzeltme: `q_run` sonunda `#` + **L** ile kelimenin son harfine dön.
2. **X erken siliniyordu:** `q_wa` X’i hemen `a` yapınca makine hangi harfi kopyalayacağını unutuyordu → `ab#a`. Düzeltme: `q_puta`/`q_putb` bitene kadar X korunur; `q_reta`/`q_retb` sonra geri yazar.
3. **a/b ayrımı:** Tek `X` yetmiyor; `q_mka` / `q_mkb` ile hangi harf kopyalanacağı ayrıldı.

**Beklenen:** `accept`, şerit `'abba#abba'`.

---

## 8. `unary_div3` — TM-4 (öğrenci seçimi)

**Komut:** `python demo.py unary_div3` veya `python demo.py tm4`

| | |
|--|--|
| **Girdi** | `1^n` |
| **Görev** | n mod 3 = 0 mı? |
| **Kabul** | `111`, `111111` evet; `11` ret |
| **YAML** | `machines/unary_div3.yaml` (elle yazıldı) |

**Söyle:**

> Üç durumlu sayaç: `q_start` → `q1` → `q2` → `q0` … Her `1` mod 3’ü artırır. Şerit bitince `q0`’da boşluk → kabul; değilse ret.

**Zorluk:**

- Boş girdi: Başta `q0` + blank doğrudan kabul veriyordu (0 mod 3). **`q_start`** eklendi — boş ret, en az bir `1` şart.
- En kısa ödev makinesi; tasarım notlarında “elle YAML” diye belirttim.

**Hızlı gösterim:** `python demo.py unary_div3 --quiet` (üç satır accept/reject).

---

## Testler (1 dk)

**Komut:** `python -m pytest tests/ -v`

**Söyle:**

> Her makine için otomatik test var. Motor 12, ödev makineleri 26, bonus 6 — toplam 44 test. Regresyon: TM-1’deki `q_lr` hatası test olmadan geç fark edilmişti.

**Kısa:** `python -m pytest tests/ -q` → `44 passed`.

---

## Kapanış (30 sn)

**Söyle:**

> Özet: YAML ile makine tanımı, dict ile şerit, pytest ile doğrulama. En zor makineler TM-1 (uzun algoritma + tur dönüşü), TM-2 (sağ şerit senkronu), TM-3 (kopya + işaret yönetimi). Dinlediğiniz için teşekkürler.

**Rapor:** `REPORT.md`, tasarım: `docs/design_notes.md`.

---

## Hızlı komut tablosu (ekran paylaşımı)

| # | Makine | Komut |
|---|--------|--------|
| 1 | binary_increment | `python demo.py binary_increment` |
| 2 | unary_increment | `python demo.py unary_increment` |
| 3 | even_a | `python demo.py even_a` |
| 4 | binary_palindrome | `python demo.py binary_palindrome` |
| 5 | TM-1 | `python demo.py tm1` |
| 6 | TM-2 | `python demo.py tm2` |
| 7 | TM-3 | `python demo.py string_copy` |
| 8 | TM-4 | `python demo.py tm4` |
| — | Tüm ödev | `python demo.py --only odev` |
| — | Test | `python -m pytest tests/ -q` |

---

## Video sırası önerisi

1. Giriş + motor (dict şerit)  
2. Kısa örnek: `binary_increment` veya `binary_palindrome`  
3. TM-1 → TM-2 → TM-3 (**zorluklar burada**) → TM-4  
4. pytest + kapanış  

TM-1 verbose uzun; videoda `111` ile göster, “tam liste YAML’de” de.
