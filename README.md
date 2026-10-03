# Vestel kumanda

43F9530 için tarayıcıdan çalışan yerel ağ kumandası. Güç, ses, kanal, yön, menü, uygulama kısayolları ve rakamlar tek sayfada.

A local-network remote for the 43F9530, running in the browser. Power, volume, channel, direction, menu, app shortcuts, and digits sit on one page.

![Kumanda / Remote](ekran/ana.png)

## Kurulum / Setup

Televizyon açık olmalı, bilgisayarla aynı ağda olmalı. Medya oynatıcı televizyonda açık kalmalı: Ayarlar → Diğer ayarlar → Medya / Ortam işleyici.

The TV should be on and on the same network as the computer. The media player on the TV stays on: Settings → Other settings → Media player.

```bash
cd vestel-remote
python3 server.py
```

Aç / Open: http://127.0.0.1:8765

Televizyonun adresi `server.py` içindeki `TV_IP` değeridir. Evdeki adres değişirse orası güncellenir.

The TV address is `TV_IP` in `server.py`. If the home address changes, update it there.

## Teknoloji / Stack

**Python** standart kütüphanesi: `ThreadingHTTPServer` sayfayı ve tuş isteklerini verir. Tuşlar Vestel’in ağ kumanda kapısına (`56791`) küçük bir HTTP isteği olarak gider. Keşif kapısı `56792`. Arayüz tek `index.html`. Sunucu yanıt vermezse sayfadaki nokta kırmızı kalır.

The **Python** standard library does the work: `ThreadingHTTPServer` serves the page and key requests. Keys go to Vestel’s network remote port (`56791`) as a small HTTP request. Discovery uses port `56792`. The interface is a single `index.html`. If the server does not answer, the dot on the page stays red.
