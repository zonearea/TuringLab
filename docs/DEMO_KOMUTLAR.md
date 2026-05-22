# Demo komutları (makine başına)

Proje kökünde:

```powershell
chcp 65001
cd C:\Users\Berkay\Desktop\business\OtomataOdev
```

## Bölüm 1 — Örnek makineler

```powershell
python demo.py binary_increment
python demo.py unary_increment
python demo.py even_a
python demo.py binary_palindrome
```

## Bölüm 2 — Ödev makineleri

```powershell
python demo.py unary_to_binary
python demo.py binary_compare
python demo.py string_copy
python demo.py unary_div3
```

Kısa adlar:

```powershell
python demo.py tm1
python demo.py tm2
python demo.py tm3
python demo.py tm4
```

## Gruplar

```powershell
python demo.py --only ornek
python demo.py --only odev
python demo.py
```

## Özel girdi

```powershell
python demo.py string_copy --girdi ab
python demo.py binary_compare --girdi 11#10
```

## Sessiz (adımsız)

```powershell
python demo.py unary_div3 --quiet
```

## Liste

```powershell
python demo.py --list
```
