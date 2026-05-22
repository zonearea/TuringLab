# TuringLab — Bonus modülleri

El kitabı bonus (+20’ye kadar): ayrı modüller, ek bağımlılıklar `requirements-bonus.txt`.

## Kurulum

```bash
pip install -r requirements-bonus.txt
```

Yalnızca PPM (stdlib) için: `pip install -r requirements.txt` yeterli; grafik/GIF için matplotlib ve Pillow gerekir.

## 1. Çok şeritli TM (`turinglab.bonus.MultiTapeTM`)

- İki şerit, YAML: `read` / `write` / `move` iki elemanlı listeler.
- Örnek: [machines/bonus_two_tape_copy.yaml](../machines/bonus_two_tape_copy.yaml)

```python
from turinglab.bonus import MultiTapeTM
tm = MultiTapeTM.from_yaml("machines/bonus_two_tape_copy.yaml")
r = tm.run("ab")
```

## 2. NTM + BFS (`turinglab.bonus.NondeterministicTM`)

- Aynı `(durum, okunan)` için birden fazla geçiş; BFS ile ilk kabul yolu.

```python
from turinglab.bonus import NondeterministicTM
ntm = NondeterministicTM(...)
r = ntm.run_bfs("a", max_steps=10)
```

## 3. Adım karşılaştırma + grafik (`compare_step_counts`)

- Farklı girdilerde adım sayısı; CSV + isteğe bağlı PNG.

```python
from turinglab import SingleTapeTM
from turinglab.bonus import compare_step_counts, save_comparison
tm = SingleTapeTM.from_yaml("machines/unary_increment.yaml")
cmp = compare_step_counts(tm, [("1", "1"), ("3", "111")])
save_comparison(cmp, "out/steps")
```

## 4. Görselleştirici (`export_history_ppm` / `export_history_gif`)

- Her adım bir PPM karesi; Pillow ile GIF animasyonu.

```python
from turinglab import SingleTapeTM
from turinglab.bonus import export_history_gif, export_history_ppm
tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
r = tm.run("1011", max_steps=200)
export_history_ppm(r, "out/frames")
export_history_gif(r, "out/run.gif")
```

## Test

```bash
python -m pytest tests/test_bonus.py -q
```
