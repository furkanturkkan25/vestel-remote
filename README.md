# Vestel kumanda

43F9530 için tarayıcıdan çalışan yerel ağ kumandası. Güç, ses, kanal, yön, menü, uygulama kısayolları ve rakamlar tek sayfada.

![Kumanda](ekran/ana.png)

## Kurulum

Televizyon açık olmalı, bilgisayarla aynı ağda olmalı. Medya oynatıcı televizyonda açık kalmalı: Ayarlar → Diğer ayarlar → Medya / Ortam işleyici.

```bash
cd vestel-remote
python3 server.py
```

Aç: http://127.0.0.1:8765

Televizyonun adresi `server.py` içindeki `TV_IP` değeridir. Evdeki adres değişirse orası güncellenir.

## Nasıl kuruldu

**Python** standart kütüphanesi: `ThreadingHTTPServer` sayfayı ve tuş isteklerini verir. Tuşlar Vestel’in ağ kumanda kapısına (`56791`) küçük bir HTTP isteği olarak gider. Keşif kapısı `56792`. Arayüz tek `index.html`; ek çerçeve yok. Sunucu yanıt vermezse sayfadaki nokta kırmızı kalır.
