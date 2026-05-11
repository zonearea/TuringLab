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
