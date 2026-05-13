# turinglab-HüseyinBerkayKayıkçı

[TuringLab_Ogrenci_ElKitabi.pdf](https://github.com/user-attachments/files/27605487/TuringLab_Ogrenci_ElKitabi.pdf)

Selçuk Üniversitesi Hesaplama Kuramı — **TuringLab** final ödevi: tek şeritli deterministik TM motoru (YAML), örnek makineler ve pytest.

## Gereksinimler

- Python 3.10+
- `pip install -r requirements.txt`

**Bölüm 1 (el kitabı):** Üçüncü parti yalnızca **PyYAML** ve **pytest**; standart kütüphane serbest.

## Test

```bash
python -m pytest tests/test_tm_engine.py -q
```

Tüm testler yeşil olmalı (Bölüm 1 rubriği: en az 8 test).

## Örnek makineler (`machines/`)

| Dosya | Kısa açıklama |
|--------|----------------|
| [machines/binary_increment.yaml](machines/binary_increment.yaml) | İkili sayı +1 (el kitabı örneği) |
| [machines/unary_increment.yaml](machines/unary_increment.yaml) | Unary `1^n` → `1^(n+1)` |
| [machines/even_a.yaml](machines/even_a.yaml) | `{a,b}` üzerinde çift sayıda `a` |
| [machines/binary_palindrome.yaml](machines/binary_palindrome.yaml) | `{0,1}` palindrom (geçişler Paul Goldberg [FCS örneği](http://www.cs.ox.ac.uk/people/paul.goldberg/FCS/tm1.html) tabanı; uyuşmazlıkta `q_reject`) |

Ders sayfasında farklı YAML verilmişse, aynı şema ile `machines/` altına kopyalanıp testlere bağlanabilir.

## Şerit ve sol taşma

Şerit seyrek `dict[int, str]` ile tutulur; kafa indeksi negatif olabilir. Sol uçta okuma yeni `blank` hücreleri oluşturur (davranış [turinglab/tm_engine.py](turinglab/tm_engine.py) + bu README ile sabitlenir).

## GitHub

Remote ekli değilse:

```bash
git remote add origin <repo-URL>
git push -u origin main
```

(Dal adın `master` ise son satırda `master` kullan.)
