# Tasarım notları (Bölüm 2)

El kitabındaki her TM için kısa cevaplar (TM-1: `unary_to_binary`).

## TM-1 — `unary_to_binary.yaml`

1. **Dil / görev:** Girdi `1^n` (n≥1, şeritte yalnızca birler ve boşluk). Çıktı: n’nin ikili yazımı (baştaki anlamsız sıfırlar temizlenir). n=0 (boş girdi) ret; n>255 için sabit genişlik taşması ret.

2. **Ayırıcı ve sayaç alanı:** Unary sonuna `X` yazılır; sağda K=8 hücre MSB solda ikili sayaç tutulur. Her turda bir unary `1` silinir; ikili alan +1 (sondan başlayan taşma zinciri, taşma olursa sağa doğru genişleme yolu `q_rv` ile ret).

3. **Durum grupları (özet):** `q_sc`…`q_wl` ayırıcı ve başlangıç konumu; `q_fl`/`q_er` ilk unary silme ve ikili alana giriş; `q_msb`…`q_lsb`/`ca*` ikili +1; `q_rw1`…`q_lr` bir unary silme turu ve tekrar `q_fl` hattına dönüş; `q_cx`/`q_cz` baştaki sıfırları silip kabul.

4. **Kenar durumları:** n=1 doğrudan kabul (`q1l`). n=256: taşma sonrası `q_rv` ile `q_reject`. Başta `0` veya boş girdi: `q0` → `q_reject`.

5. **Üretim:** `scripts/gen_unary_to_binary.py` aynı şemayı yeniden üretir; teslim dosyası `machines/unary_to_binary.yaml`dır.
