# TuringLab — Mini-rapor (Bölüm 3 — taslak)

**Öğrenci:** Hüseyin Berkay Kayıkçı  
**Proje:** `turinglab` — tek şeritli deterministik TM motoru (YAML + pytest)

## Özet

Python paketi `turinglab` ile YAML tanımlı Turing makineleri yüklenip simüle edilir. Bölüm 1’de motor ve el kitabı örnek makineleri; Bölüm 2’de TM-1 (`unary_to_binary`) tamamlandı. Tüm testler `pytest tests/` ile çalıştırılır.

## Bölüm 1 — Motor

- `SingleTapeTM.from_yaml`, `run`: kabul, ret, `no_transition`, `timeout`.
- Seyrek şerit (`dict[int, str]`), negatif kafa indeksi.
- Örnek makineler: `binary_increment`, `unary_increment`, `even_a`, `binary_palindrome`.
- Testler: `tests/test_tm_engine.py` (12 senaryo).

## Bölüm 2 — TM-1

- **Görev:** Unary `1^n` (n≥1) → n’nin ikili yazımı; n≤255 (K=8 bit sayaç alanı).
- **Dosya:** `machines/unary_to_binary.yaml`; tasarım: `docs/design_notes.md`.
- **Algoritma (kısa):** Sonuna ayırıcı `X`, sağda ikili sayaç; her tur bir unary `1` silinir ve sayaç +1; bitince baştaki sıfırlar temizlenir.
- **Testler:** `tests/test_machines.py` — kabul örnekleri, boş/`0` ret, taşma ret.

## Test komutu

```bash
python -m pytest tests/ -q
```

## Sınırlamalar

- TM-1: n>255 ret; girdi yalnızca `1` (başta `0` veya boş ret).
- Palindrom makinesi Goldberg FCS tabanlı; uyuşmazlıkta `q_reject`.
- Bölüm 2 ödev makinesi: yalnızca TM-1 (`unary_to_binary`); ek TM el kitabında açıkça istenmedikçe gerekmez.

## Öğrenilenler

- Deterministik TM’de her `(durum, okunan)` çifti tek geçiş olmalı; YAML yüklerken çakışma reddedilir.
- Seyrek şerit ve negatif kafa indeksi, sol taşma senaryolarını basitleştirir.
- Karmaşık makinelerde ayırıcı sembol (`X`) ve sabit genişlikte sayaç alanı tasarımı okunabilirliği artırır.
- Testler (`pytest`) regresyonu yakalar; TM-1’de `q_lr` / `q_rw1` hataları test olmadan geç fark edilmişti.

## Teslim öncesi yapılacaklar

- [x] Bölüm 2 TM-1: YAML, test, `design_notes`
- [x] `docs/DAILY_LOG.md` 11–19 arası girişler
- [ ] El kitabı Bölüm 3 son rubrik kontrolü
- [ ] `REPORT.md` son okuma (hoca formatı varsa uyarla)
- [ ] Son `pytest` + GitHub `main` push
