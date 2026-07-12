# Yandex Music Downloader GUI

Графический интерфейс для скачивания музыки с Яндекс.Музыки.

## Структура проекта

```
├── app.py           — запуск (точка входа)
├── api.py           — JS-API мост (Python ↔ JS)
├── ym_client.py     — клиент Яндекс.Музыки (авторизация, треки, превью)
├── downloader.py    — параллельное скачивание
├── config.py        — конфиг (config.json)
├── gui/
│   └── html.py      — весь HTML/CSS/JS интерфейс
├── requirements.txt
└── README.md
```

## Установка

```bash
pip install pywebview yandex-music

# yandex-music-downloader
pip install yandex-music-downloader
# или
pipx install yandex-music-downloader
```

На Linux дополнительно:
```bash
# Ubuntu/Debian
sudo apt install python3-gi gir1.2-webkit2-4.1
```

## Запуск

```bash
python app.py

# С DevTools:
python app.py --debug
```

## Авторизация (автоматически)

1. Нажмите **«Войти»** в шапке приложения
2. На экране появится код (например `ABC-DEF`)
3. Откройте ссылку в браузере и введите код
4. Токен сохраняется автоматически в `config.json`

## Возможности

| Фича | Описание |
|------|----------|
| ⬇ Скачивание | Плейлисты, альбомы, треки, артисты |
| ▶ Превью | Прослушать трек перед скачиванием прямо в приложении |
| ⚡ Параллельность | До 8 треков одновременно (настраивается) |
| 📋 Мои плейлисты | Список плейлистов аккаунта, клик → добавить в очередь |
| 🎵 Скачанные | Просмотр и воспроизведение уже скачанных файлов |
| 📋 Лог | Скрывается/показывается кнопкой |
| 🔑 Device Flow | Авторизация без ручного копирования токена |

## Поддерживаемые URL

| Тип | Пример |
|-----|--------|
| Альбом | `https://music.yandex.ru/album/12345` |
| Трек | `https://music.yandex.ru/album/12345/track/67890` |
| Плейлист | `https://music.yandex.ru/users/username/playlists/3` |
| Поделиться | `https://music.yandex.ru/playlists/lk.UUID` |
| Артист | `https://music.yandex.ru/artist/11111` |

UTM-параметры (`?utm_source=...`) обрезаются автоматически.