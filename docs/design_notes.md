# Tasarım notları (Bölüm 2)

El kitabındaki dört TM için kısa cevaplar.

## TM-1 — `unary_to_binary.yaml`

1. **Dil / görev:** Girdi `1^n` (n≥1). Çıktı: n’nin ikili yazımı. n=0 veya n>255 ret.
2. **Ayırıcı / sayaç:** Sonuna `X`, sağda K=8 bit ikili sayaç (MSB solda).
3. **Durum grupları:** `q_sc`…`q_wl` ayırıcı; `q_fl`/`q_er` unary silme; `q_msb`…`ca*` +1; `q_rw1`…`q_lr` tur dönüşü; `q_cx`/`q_cz` kabul.
4. **Kenar durumları:** n=1 kısayol; taşma `q_rv`; boş/`0` ret.
5. **Üretim:** `scripts/gen_unary_to_binary.py`.

## TM-2 — `binary_compare.yaml`

1. **Dil / görev:** `w#v` (w,v ∈ {0,1}*). Sol ikili sayı sağdan büyükse kabul (ör. `1100#1011`).
2. **İşaretleme:** Solda 0→`r`, 1→`s`; eşit bitlerde sağda da `r`/`s`. Sonraki turda işaretli hücreler atlanır.
3. **Durum grupları:** `q_scan`/`q_back` sağ uca; `q_next` solda sonraki bit; `q_g0`/`q_g1` + `q_r0`/`q_r1` karşılaştırma; `q_backl`/`q_prevl` dönüş; `q_left_done` sol bittiğinde sağ artığı.
4. **Kenar durumları:** Eşit uzunlukta tam eşitlik ret; sağda fazla 1 kabul; sağda 0 ret.
5. **Üretim:** `scripts/gen_binary_compare.py`.

## TM-3 — `string_copy.yaml`

1. **Dil / görev:** `w` (a,b)* → `w#w` (ör. `abba` → `abba#abba`).
2. **Ayırıcı:** Sona `#` yazılır; kafa başa alınır.
3. **Döngü:** İlk işlenmemiş harf `X` ile işaretlenir; şerit sonuna gidilip karakter kopyalanır; `X` eski harfe çevrilir.
4. **Kenar durumları:** Boş girdi ret; tüm sol işaretlenince `#` üzerinden kabul.
5. **Üretim:** `scripts/gen_string_copy.py` (`q_mka` / `q_mkb` ayrımı).

## TM-4 — `unary_div3.yaml`

1. **Dil / görev:** `1^n`; n, 3’ün katıysa kabul (ör. `111` kabul, `11` ret).
2. **Algoritma:** Üç durumlu sayaç `q0,q1,q2`; her `1` ile mod 3 artar; boş girdi ret.
3. **Dosya:** Elle yazılmış kısa YAML (öğrenci seçimi).
4. **Test:** `tests/test_machines.py` — `111`, `111111`, `11`, `1`, boş.
