# TuringLab — günlük çalışma günlüğü

Her çalışma günü sonunda (push öncesi) aşağıdaki şablonla yeni bir `## YYYY-MM-DD` bölümü ekleyin.

---

## Şablon (kopyala-yapıştır)

```markdown
## YYYY-MM-DD

- **Planlanan:**
- **Yapılan:**
- **Test:**
- **Commit’ler:**
- **Yarın:**
- **Not / blokaj:**
```

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
- **Not / blokaj:** `git push` için henüz `remote` yok. GitHub’da private repo oluşturup: `git remote add origin <URL>` ve `git push -u origin master` (veya `main`).

---

## 2026-05-12

- **Planlanan:** El kitabı örnek makine YAML’ları; `test_tm_engine` 8+ test; rubrik kenarları (yinelenen geçiş, geçersiz girdi, `reject`); README ve günlük günceliği.
- **Yapılan:**
  - [machines/unary_increment.yaml](machines/unary_increment.yaml), [machines/even_a.yaml](machines/even_a.yaml), [machines/binary_palindrome.yaml](machines/binary_palindrome.yaml) eklendi (palindrom geçişleri Goldberg FCS örneğine göre, uyuşmazlık için `q_reject`).
  - [tests/test_tm_engine.py](tests/test_tm_engine.py): 12 test (`unary_increment`, `even_a`, `binary_palindrome`, geçersiz girdi `ValueError`, yinelenen δ `ValueError`, `TMStep` alan kontrolü).
  - [README.md](README.md): kurulum, makine tablosu, kaynak notu.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** (push öncesi yerelde) `feat:` / `test:` / `docs:` ile 1–3 anlamlı commit önerilir — tam liste: `git log --oneline`.
- **Yarın:** Bölüm 1 cilası (docstring / rubrik son kontrol); Bölüm 2 için `design_notes.md` taslağı veya TM-1 unary→binary tasarımına başlangıç.
- **Not / blokaj:** Push kullanıcı makinesinde; remote URL SSH veya HTTPS ile ayarlanmalı.

---

## 2026-05-13 — Parça 1 (push 1)

- **Planlanan:** Bölüm 1 motor/docstring cilası; README Bölüm 1 bağımlılık notu; günlük push 1 kaydı; pytest yeşil.
- **Yapılan:**
  - [turinglab/tm_engine.py](turinglab/tm_engine.py): modül, ``TMStep``, ``RunResult``, ``SingleTapeTM`` (``__init__``, ``from_yaml``, ``run``) Google tarzı docstring; kullanılmayan ``typing`` importları temizlendi.
  - [turinglab/__init__.py](turinglab/__init__.py): paket docstring ve ``__all__`` açıklaması.
  - [README.md](README.md): Bölüm 1 izinli bağımlılıklar cümlesi.
- **Test:** `python -m pytest tests/test_tm_engine.py -q` — 12 passed.
- **Commit’ler:** `docs: motor docstring ve README Bolum 1 notlari` — tam hash: `git log -1 --oneline`.
- **Parça 2 (aynı gün, ikinci push):** TM-1 `unary_to_binary.yaml`, `tests/test_machines.py`, `docs/design_notes.md` (Bölüm 2 başlangıcı).
- **Not / blokaj:** Yok.
