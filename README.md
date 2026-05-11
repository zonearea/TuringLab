# TuringLab

Selçuk Üniversitesi Hesaplama Kuramı — TuringLab final ödevi. Tek şeritli deterministik Turing makinesi motoru (YAML tanımı) ve ileride eklenecek makine tasarımları.

## Gereksinimler

- Python 3.10+
- Bağımlılıklar: `pip install -r requirements.txt`

## Kurulum ve test

```bash
pip install -r requirements.txt
pytest -q
```

## GitHub

Yerelde `git init` yapıldı. Private repoyu oluşturduktan sonra:

```bash
git remote add origin https://github.com/KULLANICI/turinglab-adsoyad.git
git push -u origin master
```

Dal adın `main` ise `master` yerine `main` kullan.

## Şerit ve sol taşma

Şerit **seyrek sözlük** (`dict[int, str]`) ile tutulur; kafa indeksi negatif olabilir (sol genişleme). Sol uçta okuma yapıldığında yeni hücreler **boşluk sembolü** (`blank`) ile oluşturulur; ekstra `ValueError` fırlatılmaz.

## Kullanım (örnek)

```python
from turinglab import SingleTapeTM, RunResult

tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
result: RunResult = tm.run(input_string="1011", max_steps=1000, verbose=False)
assert result.accepted
```

Demo videosu ve rapor teslim aşamasında `docs/` ve `REPORT.md` ile tamamlanacaktır.
