# TuringLab — günlük çalışma günlüğü

Proje ilerlemesinin kısa kaydı. Her gün için `## YYYY-MM-DD` başlığı altında **Planlanan**, **Yapılan**, **Test**, **Commit’ler**, **Yarın** ve **Not / blokaj** maddeleri doldurulur.

---
## 2026-05-11

- **Planlanan:** Repo iskeleti; `turinglab` paketi; seyrek şerit + YAML doğrulama; `SingleTapeTM.run` iskeleti; ilk pytest; günlük dosyası.
- **Yapılan:**
  - Kök: [README.md](README.md), [requirements.txt](requirements.txt), [.gitignore](.gitignore), [pytest.ini](pytest.ini), [REPORT.md](REPORT.md) (taslak).
  - Motor: [turinglab/tm_engine.py](turinglab/tm_engine.py) — `SingleTapeTM`, `RunResult`, `TMStep`, YAML yükleme, `run` (accept / no_transition / timeout / reject), `verbose` çıktısı, seyrek `dict[int, str]` şerit ve negatif kafa indeksi.
  - Örnek makine: [machines/binary_increment.yaml](machines/binary_increment.yaml).
  - Testler: [tests/test_tm_engine.py](tests/test_tm_engine.py) (6 senaryo).
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 6 passed.
- **Commit’ler:** `91378ec` … `d3417ae` … arası docs commit’leri — tam liste: `git log --oneline`
- **Yarın:** Geçiş lookup / history ince ayarı; el kitabı örnek YAML’ları ekleme; test sayısını 8+ çıkarma.
- **Not / blokaj:** Yok.

---

## 2026-05-12

- **Planlanan:** El kitabı örnek makine YAML’ları; `test_tm_engine` 8+ test; rubrik kenarları (yinelenen geçiş, geçersiz girdi, `reject`); README ve günlük günceliği.
- **Yapılan:**
  - [machines/unary_increment.yaml](machines/unary_increment.yaml), [machines/even_a.yaml](machines/even_a.yaml), [machines/binary_palindrome.yaml](machines/binary_palindrome.yaml) eklendi (palindrom geçişleri Goldberg FCS örneğine göre, uyuşmazlık için `q_reject`).
  - [tests/test_tm_engine.py](tests/test_tm_engine.py): 12 test (`unary_increment`, `even_a`, `binary_palindrome`, geçersiz girdi `ValueError`, yinelenen δ `ValueError`, `TMStep` alan kontrolü).
  - [README.md](README.md): kurulum, makine tablosu, kaynak notu.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** Tam liste: `git log --oneline`.
- **Yarın:** Bölüm 1 cilası (docstring / rubrik son kontrol); Bölüm 2 için `design_notes.md` taslağı veya TM-1 unary→binary tasarımına başlangıç.
- **Not / blokaj:** Yok.

---

## 2026-05-13

- **Planlanan:** Bölüm 1 motor/docstring cilası; README Bölüm 1 bağımlılık notu; günlük kaydı; pytest yeşil.
- **Yapılan:**
  - [turinglab/tm_engine.py](turinglab/tm_engine.py): modül, ``TMStep``, ``RunResult``, ``SingleTapeTM`` (``__init__``, ``from_yaml``, ``run``) Google tarzı docstring; kullanılmayan ``typing`` importları temizlendi.
  - [turinglab/__init__.py](turinglab/__init__.py): paket docstring ve ``__all__`` açıklaması.
  - [README.md](README.md): Bölüm 1 izinli bağımlılıklar cümlesi.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** `git log --oneline` ile bakılır.
- **Yarın:** TM-1 `unary_to_binary.yaml`, `tests/test_machines.py`, `docs/design_notes.md` (Bölüm 2).
- **Not / blokaj:** Yok.

---

## 2026-05-14

- **Planlanan:** TM-1 `unary_to_binary.yaml` doğrulama; `tests/test_machines.py`; `docs/design_notes.md`; README/günlük; pytest tam paket.
- **Yapılan:**
  - `unary_to_binary`: `q_rw1` ile X’e gelince unary tarafına `L`; `q_lr` sol baştaki `1` için doğrudan silme (`q_er`); `q_lr,X → q_cx` ile ayırıcı sonrası temizlik. Üretici: [scripts/gen_unary_to_binary.py](scripts/gen_unary_to_binary.py).
  - [tests/test_machines.py](tests/test_machines.py): yükleme, kabul (parametre: n∈{1,2,3,4,5,16,255}), boş ret, n=256 ret.
  - [docs/design_notes.md](docs/design_notes.md): TM-1 beş soru cevabı.
  - [README.md](README.md): `unary_to_binary` satırı ve `pytest tests/` komutu.
- **Test:** `python -m pytest tests/ -q` — 22 passed.
- **Commit’ler:** `git log --oneline` ile bakılır.
- **Yarın:** İstenirse `q0,0 → q_reject` ile geçersiz girdi ret; el kitabı son kontrol.
- **Not / blokaj:** Yok.

---

## 2026-05-17

- **Planlanan:** Push/git kontrolü; `q0,0 → q_reject`; geçersiz girdi testi; `REPORT.md` taslak; devam planı; pytest.
- **Yapılan:**
  - [scripts/gen_unary_to_binary.py](scripts/gen_unary_to_binary.py): `q0` + `0` → `q_reject`; YAML yenilendi.
  - [tests/test_machines.py](tests/test_machines.py): `test_unary_to_binary_invalid_zero_reject`.
  - [docs/design_notes.md](docs/design_notes.md): kenar durumu güncellendi.
  - [REPORT.md](REPORT.md): Bölüm 3 mini-rapor taslağı (özet, Bölüm 1–2, sınırlar, teslim checklist).
- **Test:** `python -m pytest tests/ -q` — 23 passed.
- **Commit’ler:** Bu oturum commit’i — mesaj kullanıcıya verildi.
- **Yarın:** El kitabında TM-2/3 zorunlu mu netleştir; `REPORT.md` doldurma; günlük girişi.
- **Not / blokaj:** Remote ile yerel `main` senkron (14 Mayıs son push); bugün yeni commit bekleniyor.

---

## Devam planı (Bölüm 2–3)

| Öncelik | İş | Tahmini |
|--------|-----|---------|
| 1 | El kitabı: Bölüm 2’de ek TM (TM-2, TM-3) var mı — yoksa TM-1 yeter | 30 dk |
| 2 | `REPORT.md` taslağı → teslim metni (son paragraf, öğrenilenler) | 1–2 saat |
| 3 | Rubrik: `DAILY_LOG` eksik günler, README son kontrol | 30 dk |
| 4 | Son `pytest tests/ -q` + `git push origin main` | 10 dk |
