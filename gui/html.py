"""
HTML-интерфейс приложения.
Импортируется из app.py как строка HTML.
"""

HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>YM Downloader</title>
<style>
:root {
  --bg:#0f0f11; --surface:#1a1a1f; --surface2:#22222a; --surface3:#2a2a35;
  --border:#2e2e3a; --border2:#3e3e50;
  --text:#e8e8f0; --muted:#888899; --hint:#55556a;
  --accent:#ffcc00; --accent-dim:rgba(255,204,0,.12);
  --green:#4ade80; --green-dim:rgba(74,222,128,.1);
  --red:#f87171; --red-dim:rgba(248,113,113,.1);
  --blue:#60a5fa; --blue-dim:rgba(96,165,250,.1);
  --r:10px; --rsm:6px;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;}
body{font-family:-apple-system,'Segoe UI',system-ui,sans-serif;font-size:13px;
  background:var(--bg);color:var(--text);display:flex;flex-direction:column;
  height:100vh;user-select:none;-webkit-user-select:none;}

/* ── Titlebar ── */
.titlebar{display:flex;align-items:center;gap:10px;padding:10px 16px;
  background:var(--surface);border-bottom:1px solid var(--border);
  -webkit-app-region:drag;flex-shrink:0;}
.titlebar h1{font-size:13px;font-weight:600;letter-spacing:.02em;}
.tb-badge{font-size:10px;padding:2px 7px;border-radius:20px;
  background:var(--accent-dim);color:var(--accent);font-weight:600;}

/* ── Layout ── */
.layout{display:flex;flex:1;overflow:hidden;}

/* ── Sidebar ── */
.sidebar{width:190px;background:var(--surface);border-right:1px solid var(--border);
  display:flex;flex-direction:column;padding:10px 8px;gap:2px;flex-shrink:0;}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 10px;
  border-radius:var(--rsm);cursor:pointer;font-size:13px;color:var(--muted);
  transition:background .15s,color .15s;border:none;background:none;
  width:100%;text-align:left;}
.nav-item:hover{background:var(--surface2);color:var(--text);}
.nav-item.active{background:var(--accent-dim);color:var(--accent);}
.nav-icon{font-size:15px;flex-shrink:0;width:18px;text-align:center;}
.sidebar-footer{margin-top:auto;padding-top:10px;border-top:1px solid var(--border);
  font-size:10px;color:var(--hint);padding-left:10px;line-height:1.7;}

/* ── Main / Pages ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.page{display:none;flex-direction:column;flex:1;overflow:hidden;padding:16px 18px;gap:12px;}
.page.active{display:flex;}
#page-settings,#page-downloaded{overflow-y:auto;}

/* ── Controls ── */
input[type=text],input[type=password],input[type=number],select,textarea{
  width:100%;padding:0 10px;height:34px;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:var(--rsm);color:var(--text);font-size:13px;outline:none;
  transition:border-color .15s;}
input:focus,select:focus{border-color:var(--border2);}
input[type=number]{-moz-appearance:textfield;}
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button{-webkit-appearance:none;}
select option{background:var(--surface2);}
.input-row{display:flex;gap:8px;}
.input-row input{flex:1;}

/* ── Buttons ── */
.btn{height:32px;padding:0 12px;border-radius:var(--rsm);border:1px solid var(--border);
  background:var(--surface2);color:var(--text);font-size:13px;font-weight:500;
  cursor:pointer;display:inline-flex;align-items:center;gap:6px;
  transition:background .15s,transform .1s,color .15s;white-space:nowrap;flex-shrink:0;}
.btn:hover{background:var(--border);}
.btn:active{transform:scale(.97);}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none;}
.btn.accent{background:var(--accent);color:#000;border-color:transparent;font-weight:700;}
.btn.accent:hover{opacity:.88;}
.btn.danger{color:var(--red);border-color:rgba(248,113,113,.3);}
.btn.danger:hover{background:var(--red-dim);}
.btn.sm{height:28px;padding:0 9px;font-size:12px;}
.btn.ghost{background:none;border-color:transparent;color:var(--muted);}
.btn.ghost:hover{background:var(--surface2);color:var(--text);}
.btn.active-mode{color:var(--accent);border-color:rgba(255,204,0,.3);background:none;}

/* ── URL Tags ── */
.url-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.url-tag{display:inline-flex;align-items:center;gap:5px;background:var(--surface2);
  border:1px solid var(--border);border-radius:20px;padding:3px 8px 3px 7px;
  font-size:11px;color:var(--muted);max-width:340px;}
.url-tag-txt{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px;}
.url-tag-type{font-size:9px;background:var(--accent-dim);color:var(--accent);
  padding:1px 5px;border-radius:20px;font-weight:600;letter-spacing:.04em;flex-shrink:0;}
.rm{cursor:pointer;color:var(--hint);font-size:15px;transition:color .15s;flex-shrink:0;line-height:1;}
.rm:hover{color:var(--red);}

/* ── Toolbar ── */
.toolbar{display:flex;align-items:center;gap:8px;flex-shrink:0;flex-wrap:wrap;}
.toolbar-right{margin-left:auto;display:flex;gap:6px;}

/* ── Track List ── */
.tl-wrap{flex:1;overflow:hidden;display:flex;flex-direction:column;
  border:1px solid var(--border);border-radius:var(--r);}
.tl-head{display:grid;grid-template-columns:20px 24px 1fr 150px 64px 72px 28px 28px;
  gap:6px;padding:7px 10px;background:var(--surface);
  border-bottom:1px solid var(--border);font-size:10px;color:var(--hint);
  font-weight:600;letter-spacing:.06em;flex-shrink:0;align-items:center;}
.tl-body{flex:1;overflow-y:auto;}
.tl-row{display:grid;grid-template-columns:20px 24px 1fr 150px 64px 72px 28px 28px;
  gap:6px;padding:8px 10px;align-items:center;
  border-bottom:1px solid var(--border);transition:background .1s;cursor:default;}
.tl-row:last-child{border-bottom:none;}
.tl-row:hover{background:var(--surface2);}
.tl-row.downloading{background:var(--blue-dim);}
.tl-row.done{background:var(--green-dim);}
.tl-row.error{background:var(--red-dim);}
.tl-row.playing-row{outline:1px solid var(--accent);outline-offset:-1px;}
.tl-num{font-size:11px;color:var(--hint);text-align:right;}
.tl-title{font-weight:500;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tl-sub{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;}
.tl-album{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tl-dur{font-size:11px;color:var(--hint);text-align:right;}
.tl-status{font-size:11px;text-align:right;}
.s-idle{color:var(--hint);} .s-queued,.s-downloading{color:var(--blue);}
.s-done{color:var(--green);} .s-error{color:var(--red);}
.cb{width:14px;height:14px;cursor:pointer;accent-color:var(--accent);}

/* ── Icon Buttons ── */
.iBtn{width:26px;height:26px;border-radius:var(--rsm);border:1px solid var(--border);
  background:var(--surface2);color:var(--muted);font-size:13px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background .15s,color .15s,transform .1s;flex-shrink:0;}
.iBtn:hover{background:var(--accent);color:#000;border-color:transparent;}
.iBtn:active{transform:scale(.92);}
.iBtn:disabled{opacity:.3;cursor:not-allowed;transform:none;}
.iBtn.playing{background:var(--blue-dim);color:var(--blue);border-color:var(--blue);}
.iBtn.done{color:var(--green);border-color:rgba(74,222,128,.4);background:var(--green-dim);}
.iBtn.error{color:var(--red);border-color:rgba(248,113,113,.4);background:var(--red-dim);}

/* ── Empty State ── */
.empty{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:var(--hint);gap:10px;}
.empty-icon{font-size:36px;} .empty p{font-size:13px;}

/* ── Progress ── */
.prog-wrap{flex-shrink:0;}
.prog-bar{height:3px;background:var(--border);border-radius:2px;overflow:hidden;}
.prog-fill{height:100%;background:var(--accent);border-radius:2px;transition:width .3s;}
.prog-info{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);margin-top:4px;}

/* ── Log ── */
.log-wrap{flex-shrink:0;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);overflow-y:auto;padding:8px 10px;
  font-family:'Cascadia Code','Fira Code','SF Mono',monospace;font-size:11px;line-height:1.8;
  transition:max-height .25s ease, padding .25s ease, border-width .25s;}
.log-wrap.collapsed{max-height:0;padding:0;border-width:0;overflow:hidden;}
.log-wrap.expanded{max-height:150px;}
.log-line{display:flex;gap:8px;}
.log-time{color:var(--hint);flex-shrink:0;}
.ok .log-msg{color:var(--green);} .err .log-msg{color:var(--red);} .info .log-msg{color:var(--muted);}

/* ── Mini Player ── */
.player{display:flex;align-items:center;gap:10px;padding:8px 14px;
  background:var(--surface);border-top:1px solid var(--border);flex-shrink:0;}
.player.hidden{display:none;}
.player-cover{width:36px;height:36px;border-radius:4px;object-fit:cover;
  background:var(--surface2);flex-shrink:0;}
.player-info{min-width:0;width:180px;flex-shrink:0;}
.player-title{font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px;}
.player-artist{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.player-controls{display:flex;align-items:center;gap:4px;flex-shrink:0;}
.player-time{font-size:11px;color:var(--muted);min-width:90px;text-align:center;flex-shrink:0;}
.player-seek{flex:1;accent-color:var(--accent);cursor:pointer;height:4px;min-width:60px;}
.player-mode{display:flex;align-items:center;gap:4px;flex-shrink:0;}
audio{display:none;}

/* ── Auth Modal ── */
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.75);
  display:flex;align-items:center;justify-content:center;z-index:100;}
.modal-bg.hidden{display:none;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:24px;width:400px;display:flex;flex-direction:column;gap:14px;}
.modal h2{font-size:15px;font-weight:600;}
.modal p{font-size:13px;color:var(--muted);line-height:1.6;}
.code-box{background:var(--surface2);border:1px solid var(--border);border-radius:var(--rsm);
  padding:12px 14px;text-align:center;display:flex;flex-direction:column;gap:8px;}
.code-box .code{font-size:32px;font-weight:700;letter-spacing:.2em;color:var(--accent);
  font-family:'Cascadia Code','Fira Code',monospace;cursor:pointer;
  transition:opacity .15s;line-height:1.2;}
.code-box .code:hover{opacity:.75;}
.code-copy-btn{height:28px;padding:0 12px;
  border-radius:var(--rsm);border:1px solid var(--border);background:var(--surface3);
  color:var(--muted);font-size:11px;cursor:pointer;display:inline-flex;align-items:center;
  gap:4px;transition:background .15s,color .15s;align-self:center;}
.code-copy-btn:hover{background:var(--accent);color:#000;border-color:transparent;}
.code-copy-btn.copied{background:var(--green-dim);color:var(--green);border-color:var(--green);}
.code-url{font-size:11px;color:var(--muted);}
.code-url a{color:var(--accent);}
.auth-timer{font-size:11px;color:var(--hint);}

/* ── Settings ── */
.s-grid{display:grid;gap:12px;}
.s-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;}
.s-card-title{padding:8px 12px;font-size:10px;font-weight:600;letter-spacing:.06em;
  color:var(--muted);border-bottom:1px solid var(--border);}
.s-row{display:flex;align-items:flex-start;gap:12px;padding:10px 12px;
  border-bottom:1px solid var(--border);}
.s-row:last-child{border-bottom:none;}
.s-label{flex:1;min-width:0;}
.s-name{font-size:13px;font-weight:500;}
.s-desc{font-size:11px;color:var(--muted);margin-top:2px;line-height:1.5;}
.s-ctrl{flex-shrink:0;min-width:0;display:flex;align-items:center;}
.s-ctrl select{width:200px;}
.s-ctrl input[type=text]:not([style]){width:200px;}
.s-ctrl input[type=number]{width:80px;text-align:right;padding:0 8px;}
.toggle{position:relative;width:38px;height:22px;cursor:pointer;}
.toggle input{opacity:0;width:0;height:0;position:absolute;}
.toggle-track{position:absolute;inset:0;background:var(--border2);border-radius:22px;transition:background .2s;}
.toggle input:checked+.toggle-track{background:var(--accent);}
.toggle-thumb{position:absolute;top:3px;left:3px;width:16px;height:16px;
  background:var(--bg);border-radius:50%;transition:transform .2s;pointer-events:none;}
.toggle input:checked~.toggle-thumb{transform:translateX(16px);}

/* ── Playlists ── */
.pl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;padding:2px;}
.pl-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  overflow:hidden;cursor:pointer;transition:border-color .15s,transform .15s;}
.pl-card:hover{border-color:var(--border2);transform:translateY(-2px);}
.pl-cover{width:100%;aspect-ratio:1;object-fit:cover;background:var(--surface2);display:block;}
.pl-cover-ph{width:100%;aspect-ratio:1;background:var(--surface2);
  display:flex;align-items:center;justify-content:center;font-size:28px;}
.pl-info{padding:8px;}
.pl-name{font-weight:500;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pl-count{font-size:11px;color:var(--muted);margin-top:2px;}

/* ── Downloaded ── */
.dl-row{display:flex;align-items:center;gap:10px;padding:8px 12px;
  border-bottom:1px solid var(--border);transition:background .1s;}
.dl-row:hover{background:var(--surface2);}
.dl-row.dl-playing{background:var(--blue-dim);}
.dl-ext{font-size:10px;font-weight:700;color:var(--accent);min-width:36px;text-align:center;
  background:var(--accent-dim);padding:2px 5px;border-radius:4px;flex-shrink:0;}
.dl-name{flex:1;min-width:0;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.dl-size{font-size:11px;color:var(--muted);flex-shrink:0;}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
</style>
</head>
<body>

<!-- ══ Auth Modal ══ -->
<div class="modal-bg hidden" id="authModal">
  <div class="modal">
    <h2>🔑 Вход в Яндекс.Музыку</h2>
    <p>Откройте ссылку и введите код подтверждения.</p>

    <div class="code-box" id="codeBox" style="display:none">
      <div class="code" id="codeText" onclick="copyCode()" title="Нажмите чтобы скопировать">—</div>
      <button class="code-copy-btn" id="copyCodeBtn" onclick="copyCode()" title="Скопировать код">⎘ Копировать</button>
      <div class="code-url"><a id="codeUrl" href="#" onclick="openAuthUrl();return false">Открыть страницу авторизации</a></div>
    </div>

    <p id="authStatus" style="color:var(--muted)">Запрашиваем код...</p>
    <div class="auth-timer" id="authTimer"></div>

    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn accent" id="authOpenBtn" style="display:none" onclick="openAuthUrl()">🌐 Открыть в браузере</button>
      <button class="btn danger" onclick="cancelAuth()">Отмена</button>
    </div>
  </div>
</div>

<!-- ══ Titlebar ══ -->
<div class="titlebar">
  <span style="font-size:18px;-webkit-app-region:no-drag">🎵</span>
  <h1>Yandex Music Downloader</h1>
  <span class="tb-badge">GUI</span>
  <div style="margin-left:auto;display:flex;gap:6px;-webkit-app-region:no-drag;align-items:center">
    <span id="authInfo" style="font-size:11px;color:var(--muted)"></span>
    <button class="btn sm ghost" id="btnLogin" onclick="showAuthModal()">Войти</button>
  </div>
</div>

<!-- ══ Layout ══ -->
<div class="layout">
  <nav class="sidebar">
    <button class="nav-item active" onclick="showPage('download',this)"><span class="nav-icon">⬇</span>Скачивание</button>
    <button class="nav-item" onclick="showPage('playlists',this);loadMyPlaylists()"><span class="nav-icon">📋</span>Плейлисты</button>
    <button class="nav-item" onclick="showPage('downloaded',this);scanDownloaded()"><span class="nav-icon">🎵</span>Скачанные</button>
    <button class="nav-item" onclick="showPage('settings',this)"><span class="nav-icon">⚙</span>Настройки</button>
    <div class="sidebar-footer">yandex-music-downloader</div>
  </nav>

  <div class="main">

    <!-- ══ СКАЧИВАНИЕ ══ -->
    <div class="page active" id="page-download">
      <div>
        <label style="font-size:10px;color:var(--muted);font-weight:600;letter-spacing:.04em;display:block;margin-bottom:5px">URL ПЛЕЙЛИСТА / АЛЬБОМА / ТРЕКА</label>
        <div class="input-row">
          <input type="text" id="urlInput"
            placeholder="https://music.yandex.ru/album/... или /users/.../playlists/..."
            onkeydown="if(event.key==='Enter')addUrl()">
          <button class="btn" onclick="addUrl()">+ Добавить</button>
        </div>
        <div class="url-tags" id="urlTags"></div>
      </div>

      <div class="toolbar">
        <button class="btn accent" id="btnFetch" onclick="fetchTracks()">⬇ Получить треки</button>
        <button class="btn" id="btnSelAll" onclick="selAll(true)" style="display:none">☑ Все</button>
        <button class="btn" id="btnDeselAll" onclick="selAll(false)" style="display:none">☐ Снять</button>
        <span id="selInfo" style="font-size:12px;color:var(--muted)"></span>
        <div class="toolbar-right">
          <button class="btn accent" id="btnDownload" onclick="startDownload()" style="display:none">▶ Скачать</button>
          <button class="btn danger" id="btnStop" onclick="cancelDownloads()" style="display:none">⏹ Стоп</button>
          <button class="btn ghost sm" id="btnLog" onclick="toggleLog()" title="Показать/скрыть лог">📋 Лог</button>
        </div>
      </div>

      <div class="tl-wrap">
        <div class="tl-head">
          <input type="checkbox" class="cb" id="checkAll" onchange="selAll(this.checked)" style="margin:auto">
          <span>#</span><span>ТРЕК</span><span>АЛЬБОМ</span>
          <span style="text-align:right">ДЛИТ.</span>
          <span style="text-align:right">СТАТУС</span>
          <span></span><span></span>
        </div>
        <div class="tl-body" id="tlBody">
          <div class="empty"><span class="empty-icon">🎵</span><p>Добавьте URL и нажмите «Получить треки»</p></div>
        </div>
      </div>

      <div class="prog-wrap" id="progWrap" style="display:none">
        <div class="prog-bar"><div class="prog-fill" id="progFill" style="width:0%"></div></div>
        <div class="prog-info"><span id="progText">0/0</span><span id="progPct">0%</span></div>
      </div>

      <div class="log-wrap collapsed" id="logBox"></div>
    </div>

    <!-- ══ МОИ ПЛЕЙЛИСТЫ ══ -->
    <div class="page" id="page-playlists">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Мои плейлисты</span>
        <button class="btn sm" onclick="loadMyPlaylists()">↻ Обновить</button>
      </div>
      <div id="plGrid" style="flex:1;overflow-y:auto">
        <div class="empty"><span class="empty-icon">📋</span><p>Войдите в аккаунт и нажмите «Обновить»</p></div>
      </div>
    </div>

    <!-- ══ СКАЧАННЫЕ ══ -->
    <div class="page" id="page-downloaded">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Скачанные треки</span>
        <button class="btn sm" onclick="scanDownloaded()">↻ Обновить</button>
        <span id="dlCount" style="font-size:12px;color:var(--muted)"></span>
        <button class="btn sm" onclick="window.pywebview.api.open_download_folder()">📂 Открыть папку</button>
        <span id="dlCount" style="font-size:12px;color:var(--muted)"></span>
      </div>
      <div id="dlList" style="flex:1;overflow-y:auto;border:1px solid var(--border);border-radius:var(--r)">
        <div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов</p></div>
      </div>
    </div>

    <!-- ══ НАСТРОЙКИ ══ -->
    <div class="page" id="page-settings">
      <div class="s-grid">

        <div class="s-card">
          <div class="s-card-title">АВТОРИЗАЦИЯ</div>
          <div class="s-row">
            <div class="s-label">
              <div class="s-name">Токен Яндекс.Музыки</div>
              <div class="s-desc">Или нажмите «Войти» в шапке для автоматического получения</div>
            </div>
            <div class="s-ctrl" style="flex:1"><input type="password" id="cfgToken" placeholder="Вставьте токен вручную..."></div>
          </div>
        </div>

        <div class="s-card">
          <div class="s-card-title">АУДИО</div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Качество</div><div class="s-desc">--quality · 0=AAC 64, 1=AAC 192, 2=FLAC</div></div>
            <div class="s-ctrl"><select id="cfgQuality">
              <option value="0">0 — AAC 64 kbps</option>
              <option value="1">1 — AAC 192 kbps</option>
              <option value="2" selected>2 — FLAC (лучшее)</option>
            </select></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Встраивать обложку</div><div class="s-desc">--embed-cover</div></div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgEmbedCover" checked><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Разрешение обложки</div><div class="s-desc">--cover-resolution</div></div>
            <div class="s-ctrl"><select id="cfgCoverRes">
              <option value="original" selected>original</option>
              <option value="400">400 px</option>
              <option value="200">200 px</option>
            </select></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Текст песни</div><div class="s-desc">--lyrics-format</div></div>
            <div class="s-ctrl"><select id="cfgLyrics">
              <option value="none" selected>none</option>
              <option value="text">text</option>
              <option value="lrc">lrc</option>
            </select></div>
          </div>
        </div>

        <div class="s-card">
          <div class="s-card-title">ФАЙЛЫ</div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Шаблон пути</div><div class="s-desc">--path-pattern · #number-padded, #track-artist, #album-artist, #title, #album, #year, #track-id</div></div>
            <div class="s-ctrl" style="flex:1"><input type="text" id="cfgPathPattern"></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Папка загрузки</div><div class="s-desc">--dir</div></div>
            <div class="s-ctrl" style="flex:1;display:flex;gap:6px">
              <input type="text" id="cfgDownloadDir" placeholder="Текущая папка" style="flex:1">
              <button class="btn sm" onclick="chooseFolder()">📂</button>
            </div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Пропускать существующие</div><div class="s-desc">--skip-existing</div></div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgSkipExisting" checked><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
          </div>
        </div>

        <div class="s-card">
          <div class="s-card-title">ФИЛЬТРЫ</div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Только треки артиста</div><div class="s-desc">--stick-to-artist</div></div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgStickToArtist"><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Только музыка</div><div class="s-desc">--only-music · пропускать подкасты/аудиокниги</div></div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgOnlyMusic"><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Уровень совместимости</div><div class="s-desc">--compatibility-level</div></div>
            <div class="s-ctrl"><select id="cfgCompatLevel"><option value="0">0</option><option value="1" selected>1</option></select></div>
          </div>
        </div>

        <div class="s-card">
          <div class="s-card-title">СЕТЬ</div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Параллельных загрузок</div><div class="s-desc">Сколько треков скачивать одновременно</div></div>
            <div class="s-ctrl"><select id="cfgParallel">
              <option value="1">1</option><option value="2">2</option>
              <option value="3">3</option><option value="4" selected>4</option>
              <option value="6">6</option><option value="8">8</option>
            </select></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Задержка между треками, сек</div><div class="s-desc">--delay</div></div>
            <div class="s-ctrl"><input type="number" id="cfgDelay" value="0" min="0"></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Таймаут ответа, сек</div><div class="s-desc">--timeout</div></div>
            <div class="s-ctrl"><input type="number" id="cfgTimeout" value="20" min="1"></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Попыток при ошибке</div><div class="s-desc">--tries · 0=∞</div></div>
            <div class="s-ctrl"><input type="number" id="cfgTries" value="20" min="0"></div>
          </div>
          <div class="s-row">
            <div class="s-label"><div class="s-name">Задержка между попытками, сек</div><div class="s-desc">--retry-delay</div></div>
            <div class="s-ctrl"><input type="number" id="cfgRetryDelay" value="5" min="0"></div>
          </div>
        </div>

      </div>
      <div style="display:flex;gap:8px;padding-bottom:4px;flex-shrink:0">
        <button class="btn accent" onclick="saveSettings()">💾 Сохранить</button>
        <span id="saveStatus" style="font-size:12px;color:var(--green);align-self:center;opacity:0;transition:opacity .4s"></span>
      </div>
    </div>

  </div><!-- .main -->
</div><!-- .layout -->

<!-- ══ Mini Player ══ -->
<div class="player hidden" id="player">
  <img class="player-cover" id="plCover" src="" alt="" style="display:none">
  <div class="player-info">
    <div class="player-title" id="plTitle">—</div>
    <div class="player-artist" id="plArtist">—</div>
  </div>
  <div class="player-controls">
    <button class="btn sm ghost" onclick="playerPrev()" title="Предыдущий трек">⏮</button>
    <button class="btn sm ghost" onclick="playerSkip(-10)" title="-10 сек">«10</button>
    <button class="btn sm accent" id="plPlayBtn" onclick="playerToggle()">▶</button>
    <button class="btn sm ghost" onclick="playerSkip(10)" title="+10 сек">10»</button>
    <button class="btn sm ghost" onclick="playerNext()" title="Следующий трек">⏭</button>
  </div>
  <span class="player-time" id="plTime">0:00 / 0:00</span>
  <input type="range" class="player-seek" id="plSeek" value="0" min="0" max="100" step="0.1"
    oninput="playerSeek(this.value)">
  <div class="player-mode">
    <button class="btn sm ghost" id="btnShuffle" onclick="toggleShuffle()" title="Перемешать">⇄</button>
    <button class="btn sm ghost" id="btnRepeat" onclick="cycleRepeat()" title="Повтор">↻</button>
  </div>
  <button class="btn sm ghost" onclick="playerClose()" title="Закрыть плеер">✕</button>
  <audio id="audioEl"
    onplay="_updatePlayBtn()"
    onpause="_updatePlayBtn()"
    onended="playerEnded()"
    ontimeupdate="playerTimeUpdate()"
    oncanplay="playerCanPlay()"
    onerror="playerError()"></audio>
</div>

<script>
/* ═══════════════════════════════════════════════════════════════════
   LOCAL STORAGE
═══════════════════════════════════════════════════════════════════ */
const STORE = {
  set(key, val) {
    localStorage.setItem(key, JSON.stringify(val));
  },

  get(key, def = null) {
    try {
      const v = localStorage.getItem(key);
      return v ? JSON.parse(v) : def;
    } catch {
      return def;
    }
  },

  del(key) {
    localStorage.removeItem(key);
  }
};

/* ═══════════════════════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════════════════════ */
const S = {
  urls:      STORE.get('ym_urls', []),
  tracks:    [],
  selected:  new Set(),
  downloading: false,
  // player
  playerTrackId: null,
  playerSource: 'tracks',   // 'tracks' | 'downloaded'
  dlFiles: [],              // список скачанных для навигации
  // player modes (persist in cookies)
  shuffle: STORE.get('ym_shuffle', false),
  // repeat: 'none' | 'one' | 'all'
  repeat:  (['none','one'].includes(STORE.get('ym_repeat','none')) ? STORE.get('ym_repeat','none') : 'none'),
  // shuffled play order
  shuffleOrder: [],
  shufflePos: -1,
  logVisible: STORE.get('ym_log', false),
  authUrl: '',
  authTimerInterval: null,
  currentCode: '',
};

/* ═══════════════════════════════════════════════════════════════════
   UTILS
═══════════════════════════════════════════════════════════════════ */
function esc(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function fmtBytes(b){ return b>1e6?(b/1e6).toFixed(1)+' MB':(b/1e3).toFixed(0)+' KB'; }
function fmtTime(s){ s=Math.floor(s||0); return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`; }

/* ═══════════════════════════════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════════════════════════════ */
function showPage(id,btn){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
  document.getElementById('page-'+id).classList.add('active');
  btn.classList.add('active');
}

/* ═══════════════════════════════════════════════════════════════════
   LOG
═══════════════════════════════════════════════════════════════════ */
function addLog(msg,kind='info'){
  const box=document.getElementById('logBox');
  const now=new Date().toLocaleTimeString('ru',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  const d=document.createElement('div');
  d.className=`log-line ${kind}`;
  d.innerHTML=`<span class="log-time">${now}</span><span class="log-msg">${esc(msg)}</span>`;
  box.appendChild(d);
  if(box.children.length>400) box.removeChild(box.children[0]);
  box.scrollTop=box.scrollHeight;
}
function toggleLog(){
  S.logVisible=!S.logVisible;
  STORE.set('ym_log',S.logVisible);
  const box=document.getElementById('logBox');
  box.classList.toggle('expanded',S.logVisible);
  box.classList.toggle('collapsed',!S.logVisible);
  document.getElementById('btnLog').classList.toggle('active-mode',S.logVisible);
}

/* ═══════════════════════════════════════════════════════════════════
   PY EVENTS
═══════════════════════════════════════════════════════════════════ */
window.addEventListener('py:log', e=>addLog(e.detail.msg,e.detail.kind));

window.addEventListener('py:tracks_ready', e=>{
  const tracks=e.detail||[];
  S.tracks=tracks;
  S.selected=new Set(tracks.map(t=>t.id));
  renderTracks();
  addLog(tracks.length?`Итого: ${tracks.length} треков.`:'Треков не найдено.',tracks.length?'ok':'err');
  const btn=document.getElementById('btnFetch');
  btn.disabled=false; btn.textContent='⬇ Получить треки';
});

window.addEventListener('py:track_status', e=>{
  const{id,status}=e.detail;
  const t=S.tracks.find(x=>x.id===id);
  if(t) t.status=status;
  updateProgress();
  const row=document.getElementById('row-'+id);
  if(row && t) updateRow(row,t);
});

window.addEventListener('py:preview_url', e=>{
  const{track_id,url}=e.detail;
  const t=S.tracks.find(x=>x.id===track_id);
  if(t) _loadAndPlay(t,url,'tracks');
});

window.addEventListener('py:preview_error', e=>{
  addLog('Превью: '+e.detail.msg,'err');
  _clearPlayingUI();
});

window.addEventListener('py:my_playlists', e=>renderMyPlaylists(e.detail||[]));
window.addEventListener('py:downloaded_files', e=>{ S.dlFiles=e.detail||[]; renderDownloaded(S.dlFiles); });

window.addEventListener('py:auth_code', e=>{
  const{user_code,url,expires_in}=e.detail;
  S.authUrl=url; S.currentCode=user_code;
  document.getElementById('codeText').textContent=user_code;
  const a=document.getElementById('codeUrl'); a.textContent=url; a.href=url;
  document.getElementById('codeBox').style.display='';
  document.getElementById('authStatus').textContent='Введите код на сайте Яндекса:';
  document.getElementById('authOpenBtn').style.display='';
  document.getElementById('copyCodeBtn').classList.remove('copied');
  document.getElementById('copyCodeBtn').textContent='📋 Копировать';
  // Timer
  const end=Date.now()+expires_in*1000;
  if(S.authTimerInterval) clearInterval(S.authTimerInterval);
  S.authTimerInterval=setInterval(()=>{
    const left=Math.max(0,Math.ceil((end-Date.now())/1000));
    document.getElementById('authTimer').textContent=`Действует ещё: ${left} сек.`;
    if(left===0) clearInterval(S.authTimerInterval);
  },1000);
});

window.addEventListener('py:auth_done', e=>{
  hideAuthModal();
  document.getElementById('cfgToken').value=e.detail.token;
  document.getElementById('authInfo').textContent='✓ Авторизован';
  document.getElementById('btnLogin').textContent='⚙ Аккаунт';
});

window.addEventListener('py:auth_error', e=>{
  document.getElementById('authStatus').textContent='Ошибка: '+e.detail.msg;
});

/* ═══════════════════════════════════════════════════════════════════
   AUTH MODAL
═══════════════════════════════════════════════════════════════════ */
function showAuthModal(){
  document.getElementById('authModal').classList.remove('hidden');
  document.getElementById('codeBox').style.display='none';
  document.getElementById('authOpenBtn').style.display='none';
  document.getElementById('authStatus').textContent='Запрашиваем код...';
  document.getElementById('authTimer').textContent='';
  window.pywebview.api.start_device_auth();
}
function hideAuthModal(){
  document.getElementById('authModal').classList.add('hidden');
  if(S.authTimerInterval) clearInterval(S.authTimerInterval);
}
function cancelAuth(){ window.pywebview.api.cancel_device_auth(); hideAuthModal(); }
function openAuthUrl(){ window.pywebview.api.open_link(S.authUrl); }

function copyCode(){
  if(!S.currentCode) return;
  // Используем textarea-трюк для копирования в буфер (работает в webview)
  const ta=document.createElement('textarea');
  ta.value=S.currentCode;
  ta.style.cssText='position:fixed;opacity:0;top:0;left:0';
  document.body.appendChild(ta);
  ta.select(); ta.setSelectionRange(0,99);
  document.execCommand('copy');
  document.body.removeChild(ta);
  // Визуальная обратная связь
  const btn=document.getElementById('copyCodeBtn');
  btn.textContent='✓ Скопировано';
  btn.classList.add('copied');
  setTimeout(()=>{ btn.textContent='📋 Копировать'; btn.classList.remove('copied'); },2000);
}

/* ═══════════════════════════════════════════════════════════════════
   URL TAGS
═══════════════════════════════════════════════════════════════════ */
function guessType(url){
  if(/\/album\/\d+\/track\//.test(url)) return 'ТРЕК';
  if(/\/album\//.test(url)) return 'АЛЬБОМ';
  if(/\/playlists?\//.test(url)) return 'ПЛЕЙЛИСТ';
  if(/\/artist\//.test(url)) return 'АРТИСТ';
  return 'URL';
}
function addUrl(){
  const inp=document.getElementById('urlInput');
  const url=inp.value.trim();
  if(!url.startsWith('https://')){addLog('URL должен начинаться с https://','err');return;}
  if(S.urls.includes(url)){addLog('URL уже добавлен','err');return;}
  S.urls.push(url); inp.value='';
  STORE.set('ym_urls',S.urls);
  renderUrlTags();
  addLog('Добавлен: '+url.slice(0,70),'ok');
}
function removeUrl(url){
  S.urls=S.urls.filter(u=>u!==url);
  STORE.set('ym_urls',S.urls);
  renderUrlTags();
}
function renderUrlTags(){
  document.getElementById('urlTags').innerHTML=S.urls.map(u=>`
    <div class="url-tag">
      <span class="url-tag-type">${guessType(u)}</span>
      <span class="url-tag-txt" title="${esc(u)}">${esc(u)}</span>
      <span class="rm" onclick="removeUrl('${esc(u)}')" title="Удалить">×</span>
    </div>`).join('');
}

/* ═══════════════════════════════════════════════════════════════════
   TRACK LIST
═══════════════════════════════════════════════════════════════════ */
function renderTracks(){
  const body=document.getElementById('tlBody');
  if(!S.tracks.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🎵</span><p>Добавьте URL и нажмите «Получить треки»</p></div>`;
    ['btnSelAll','btnDeselAll','btnDownload'].forEach(id=>{const el=document.getElementById(id);if(el)el.style.display='none';});
    document.getElementById('selInfo').textContent='';
    return;
  }
  body.innerHTML=S.tracks.map(t=>trackRowHTML(t)).join('');
  updateSelUI();
}

function trackRowHTML(t){
  const checked=S.selected.has(t.id)?'checked':'';
  const statusLabel={idle:'—',queued:'В очереди',downloading:'↓',done:'✓ Готово',error:'✗ Ошибка'}[t.status]||'—';
  const dlIcon={idle:'⬇',queued:'⏳',downloading:'⏳',done:'✓',error:'↺'}[t.status]||'⬇';
  const dlCls={done:'done',error:'error'}[t.status]||'';
  const dlDis=t.status==='downloading'||t.status==='queued'?'disabled':'';

  const isPlaying=S.playerTrackId===t.id&&S.playerSource==='tracks';
  const prvCls=isPlaying?'playing':'';
  const playingRow=isPlaying?'playing-row':'';

  // Определяем актуальную иконку
  let playIcon = '▶';
  if (isPlaying) {
    const audio = document.getElementById('audioEl');
    if (audio && !audio.paused) playIcon = '⏸';
  }

  return `<div class="tl-row ${t.status} ${playingRow}" id="row-${t.id}">
    <input type="checkbox" class="cb" ${checked} onchange="toggleTrack('${t.id}',this.checked)">
    <span class="tl-num">${t.num}</span>
    <div style="min-width:0">
      <div class="tl-title" title="${esc(t.title)}">${esc(t.title)}</div>
      <div class="tl-sub" title="${esc(t.artist)}">${esc(t.artist)}</div>
    </div>
    <div class="tl-album" title="${esc(t.album)}">${esc(t.album)}</div>
    <span class="tl-dur">${t.duration}</span>
    <span class="tl-status s-${t.status}">${statusLabel}</span>
    <button class="iBtn ${prvCls}" title="Прослушать" onclick="previewTrack('${t.id}')">${playIcon}</button>
    <button class="iBtn ${dlCls}" ${dlDis} title="Скачать" onclick="downloadOne('${t.id}')">${dlIcon}</button>
  </div>`;
}

function updateRow(row,t){
  const tmp=document.createElement('div');
  tmp.innerHTML=trackRowHTML(t);
  row.replaceWith(tmp.firstElementChild);
}

function toggleTrack(id,checked){
  if(checked) S.selected.add(id); else S.selected.delete(id);
  updateSelUI();
}
function selAll(v){
  S.selected=v?new Set(S.tracks.map(t=>t.id)):new Set();
  renderTracks();
}
function updateSelUI(){
  const n=S.selected.size,total=S.tracks.length;
  document.getElementById('selInfo').textContent=`Выбрано: ${n} из ${total}`;
  document.getElementById('checkAll').indeterminate=n>0&&n<total;
  document.getElementById('checkAll').checked=n===total;
  ['btnSelAll','btnDeselAll'].forEach(id=>document.getElementById(id).style.display='');
  document.getElementById('btnDownload').style.display=S.downloading?'none':'';
}
function updateProgress(){
  const active=S.tracks.some(t=>t.status==='downloading'||t.status==='queued');
  const done=S.tracks.filter(t=>t.status==='done'||t.status==='error').length;
  const total=S.tracks.length;
  const pct=total?Math.round(done/total*100):0;
  document.getElementById('progWrap').style.display=(active||done)?'':'none';
  document.getElementById('progFill').style.width=pct+'%';
  document.getElementById('progText').textContent=`${done}/${total}`;
  document.getElementById('progPct').textContent=pct+'%';
  S.downloading=active;
  document.getElementById('btnStop').style.display=active?'':'none';
  document.getElementById('btnDownload').style.display=active?'none':'';
}

/* ═══════════════════════════════════════════════════════════════════
   DOWNLOAD API
═══════════════════════════════════════════════════════════════════ */
function fetchTracks(){
  if(!S.urls.length){addLog('Добавьте хотя бы один URL','err');return;}
  const btn=document.getElementById('btnFetch');
  btn.disabled=true; btn.textContent='⏳ Загружаем...';
  S.tracks=[]; S.selected=new Set();
  renderTracks();
  addLog('Подключаемся к Яндекс.Музыке...','info');
  window.pywebview.api.fetch_tracks(S.urls);
}
function startDownload(){
  const sel=S.tracks.filter(t=>S.selected.has(t.id));
  if(!sel.length){addLog('Выберите хотя бы один трек','err');return;}
  sel.forEach(t=>{if(t.status!=='done')t.status='queued';});
  S.downloading=true;
  document.getElementById('btnDownload').style.display='none';
  document.getElementById('btnStop').style.display='';
  renderTracks();
  window.pywebview.api.start_download(sel);
  addLog(`Поставлено в очередь: ${sel.length} треков`,'info');
}
function downloadOne(id){
  const t=S.tracks.find(x=>x.id===id);
  if(!t||t.status==='downloading'||t.status==='queued') return;
  if(t.status==='error') t.status='idle';
  window.pywebview.api.start_download([t]);
  t.status='queued';
  const row=document.getElementById('row-'+id);
  if(row) updateRow(row,t);
  updateProgress();
}
function cancelDownloads(){
  window.pywebview.api.cancel_downloads();
  S.tracks.forEach(t=>{if(t.status==='queued')t.status='idle';});
  S.downloading=false;
  renderTracks();
  addLog('Отменено','info');
}

/* ═══════════════════════════════════════════════════════════════════
   PLAYER — ядро
═══════════════════════════════════════════════════════════════════ */
function _loadAndPlay(trackInfo, url, source){
  S.playerTrackId=trackInfo.id;
  S.playerSource=source;
  document.getElementById('plTitle').textContent=trackInfo.title||trackInfo.name||'—';
  document.getElementById('plArtist').textContent=trackInfo.artist||'';
  const cover=document.getElementById('plCover');
  if(trackInfo.cover_uri){ cover.src=trackInfo.cover_uri; cover.style.display=''; }
  else cover.style.display='none';
  document.getElementById('player').classList.remove('hidden');
  const audio=document.getElementById('audioEl');
  audio.src=url;
  audio.play().catch(()=>{});
  // Подсветка строки
  renderTracks();
  if(source==='downloaded') renderDownloaded(S.dlFiles);
}

function _clearPlayingUI(){
  document.querySelectorAll('.iBtn.playing').forEach(b=>{b.classList.remove('playing');b.textContent='▶';});
}

/* ── Текущий индекс и получение следующего трека ── */
function _currentIdx(){
  if(S.playerSource==='tracks'){
    return S.tracks.findIndex(t=>t.id===S.playerTrackId);
  } else {
    return S.dlFiles.findIndex(f=>f.rel_path===S.playerTrackId);
  }
}
function _listLen(){
  return S.playerSource==='tracks'?S.tracks.length:S.dlFiles.length;
}
function _shuffleIdx(curIdx){
  // Случайный, но не текущий
  const len=_listLen();
  if(len<=1) return 0;
  let r;
  do{ r=Math.floor(Math.random()*len); }while(r===curIdx);
  return r;
}
function _goToIndex(idx){
  if(S.playerSource==='tracks'){
    const t=S.tracks[idx];
    if(!t) return;
    S.playerTrackId=t.id;
    document.getElementById('plPlayBtn').textContent='⏳';
    window.pywebview.api.get_preview_url(t.id);
  } else {
    const f=S.dlFiles[idx];
    if(!f) return;
    playLocalFile(f);
  }
}

/* ── Публичные кнопки ── */
function previewTrack(id){
  const t=S.tracks.find(x=>x.id===id);
  if(!t) return;
  const audio=document.getElementById('audioEl');
  if(S.playerTrackId===id && S.playerSource==='tracks'){
    if(audio.paused) audio.play(); else audio.pause();
    _updatePlayBtn();
    return;
  }
  S.playerSource='tracks';
  S.playerTrackId=id;
  document.getElementById('plTitle').textContent=t.title;
  document.getElementById('plArtist').textContent=t.artist;
  const cov=document.getElementById('plCover');
  if(t.cover_uri){cov.src=t.cover_uri;cov.style.display='';}else cov.style.display='none';
  document.getElementById('player').classList.remove('hidden');
  document.getElementById('plPlayBtn').textContent='⏳';
  renderTracks();
  window.pywebview.api.get_preview_url(id);
}
function playerToggle(){
  const a=document.getElementById('audioEl');
  if(a.paused) a.play(); else a.pause();
  _updatePlayBtn();
}
function playerSkip(sec){
  const a=document.getElementById('audioEl');
  a.currentTime=Math.max(0,Math.min(a.duration||0,a.currentTime+sec));
}
function playerSeek(v){
  const a=document.getElementById('audioEl');
  if(a.duration) a.currentTime=a.duration*v/100;
}
function playerPrev(){
  const cur=_currentIdx();
  if(cur<0) return;
  const idx=S.shuffle?_shuffleIdx(cur):Math.max(0,cur-1);
  _goToIndex(idx);
}
function playerNext(){
  // Кнопки Prev/Next всегда переключают трек — повтор влияет только на авто-переход
  const cur=_currentIdx();
  const len=_listLen();
  if(cur<0||!len) return;
  const idx=S.shuffle?_shuffleIdx(cur):(cur+1)%len;
  _goToIndex(idx);
}
function playerEnded(){
  const cur=_currentIdx();
  const len=_listLen();
  if(cur<0||!len){ _updatePlayBtn(); return; }
  if(S.repeat==='one'){ document.getElementById('audioEl').play(); return; }
  const next=S.shuffle?_shuffleIdx(cur):(cur+1)%len;
  _goToIndex(next);
}
function playerClose(){
  const a=document.getElementById('audioEl');
  a.pause(); a.src='';
  document.getElementById('player').classList.add('hidden');
  S.playerTrackId=null;
  renderTracks();
  renderDownloaded(S.dlFiles);
}
function playerCanPlay(){ document.getElementById('plPlayBtn').textContent='⏸'; }
function playerError(){ addLog('Ошибка воспроизведения','err'); _updatePlayBtn(); }
function playerTimeUpdate(){
  const a=document.getElementById('audioEl');
  document.getElementById('plTime').textContent=`${fmtTime(a.currentTime)} / ${fmtTime(a.duration)}`;
  if(a.duration) document.getElementById('plSeek').value=(a.currentTime/a.duration*100).toFixed(1);
}
function _updatePlayBtn(){
  const audio = document.getElementById('audioEl');
  const paused = audio ? audio.paused : true;
  document.getElementById('plPlayBtn').textContent = paused ? '▶' : '⏸';

  // Обновляем иконку в основном списке треков
  if (S.playerSource === 'tracks' && S.playerTrackId) {
    const row = document.getElementById('row-' + S.playerTrackId);
    if (row) {
      // Ищем именно активную кнопку прослушивания по классу playing
      const btn = row.querySelector('.iBtn.playing');
      if (btn) btn.textContent = paused ? '▶' : '⏸';
    }
  }
  // Обновляем иконку в скачанных треках
  else if (S.playerSource === 'downloaded' && S.playerTrackId) {
    const idx = S.dlFiles.findIndex(f => f.rel_path === S.playerTrackId);
    if (idx !== -1) {
      const row = document.getElementById('dlrow-' + idx);
      if (row) {
        // Находим кнопку Play
        const btn = row.querySelectorAll('.btn')[0];
        if (btn) {
          btn.textContent = paused ? '▶' : '⏸';
          btn.title = paused ? 'Воспроизвести' : 'Играет';
        }
      }
    }
  }
}

/* ── Режимы ── */
function toggleShuffle(){
  S.shuffle=!S.shuffle;
  STORE.set('ym_shuffle',S.shuffle);
  document.getElementById('btnShuffle').classList.toggle('active-mode',S.shuffle);
}
function cycleRepeat(){
  S.repeat = S.repeat==='one' ? 'none' : 'one';
  STORE.set('ym_repeat',S.repeat);
  _applyModeUI();
}
function _applyModeUI(){
  document.getElementById('btnShuffle').classList.toggle('active-mode',S.shuffle);
  const btn=document.getElementById('btnRepeat');
  const isOne=S.repeat==='one';
  btn.textContent=isOne?'↻':'↻';
  btn.title=isOne?'Повтор трека':'Повтор трека (выкл)';
  btn.classList.toggle('active-mode',isOne);
}

/* ═══════════════════════════════════════════════════════════════════
   MY PLAYLISTS
═══════════════════════════════════════════════════════════════════ */
function loadMyPlaylists(){
  document.getElementById('plGrid').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем...</p></div>`;
  window.pywebview.api.get_my_playlists();
}
function renderMyPlaylists(pls){
  if(!pls.length){
    document.getElementById('plGrid').innerHTML=`<div class="empty"><span class="empty-icon">📋</span><p>Плейлистов нет или нет авторизации</p></div>`;
    return;
  }

  // Заранее подготовленные категории
  const groups = {
    'system': { title: '❤️ Моя музыка', items: [] },
    'smart':  { title: '✨ Умные плейлисты', items: [] },
    'created':{ title: '👤 Созданные мной', items: [] },
    'liked':  { title: '📌 Понравившиеся плейлисты', items: [] }
  };

  // Распределяем плейлисты по группам
  pls.forEach(pl => {
    const g = pl.group && groups[pl.group] ? pl.group : 'created';
    groups[g].items.push(pl);
  });

  let html = '';

  // Проходимся по каждой категории и генерируем HTML
  for (const key in groups) {
    if (groups[key].items.length > 0) {
      // Заголовок категории (растягивается на всю ширину сетки благодаря grid-column: 1 / -1)
      html += `
        <div style="grid-column: 1 / -1; padding: 12px 6px 4px; font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); margin-bottom: 4px; margin-top: 4px;">
          ${groups[key].title}
        </div>
      `;
      // Карточки плейлистов этой категории
      html += groups[key].items.map(pl=>`
        <div class="pl-card" onclick="addPlaylistUrl('${esc(pl.url)}')" title="Добавить в очередь">
          ${pl.cover
            ?`<img class="pl-cover" src="${esc(pl.cover)}" alt="" onerror="this.style.display='none'">`
            :`<div class="pl-cover-ph">🎵</div>`}
          <div class="pl-info">
            <div class="pl-name">${esc(pl.title)}</div>
            <div class="pl-count">${pl.count} треков</div>
          </div>
        </div>`).join('');
    }
  }

  // Оборачиваем всё в сетку
  document.getElementById('plGrid').innerHTML = `<div class="pl-grid" style="padding-bottom: 20px;">${html}</div>`;
}
function addPlaylistUrl(url){
  if(!url) return;
  showPage('download',document.querySelector('.nav-item'));
  if(!S.urls.includes(url)){ S.urls.push(url); STORE.set('ym_urls',S.urls); renderUrlTags(); }
  addLog('Добавлен плейлист: '+url.slice(0,60),'ok');
}

/* ═══════════════════════════════════════════════════════════════════
   DOWNLOADED FILES
═══════════════════════════════════════════════════════════════════ */
function scanDownloaded(){
  window.pywebview.api.scan_downloaded();
}
function renderDownloaded(files){
  document.getElementById('dlCount').textContent=files.length?`${files.length} файлов`:'';
  const el=document.getElementById('dlList');
  if(!files.length){
    el.innerHTML=`<div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов в папке загрузки</p></div>`;
    return;
  }
  el.innerHTML=files.map((f,i)=>{
    const isPlaying=S.playerSource==='downloaded'&&S.playerTrackId===f.rel_path;

    // Определяем актуальную иконку
    let playIcon = '▶';
    if (isPlaying) {
      const audio = document.getElementById('audioEl');
      if (audio && !audio.paused) playIcon = '⏸';
    }

    return `<div class="dl-row${isPlaying?' dl-playing':''}" id="dlrow-${i}">
      <span class="dl-ext">${esc(f.ext)}</span>
      <span class="dl-name" title="${esc(f.path)}">${esc(f.name)}</span>
      <span class="dl-size">${fmtBytes(f.size)}</span>
      <button class="btn sm ghost" onclick="playLocalFile(S.dlFiles[${i}])"
        title="${isPlaying?'Играет':'Воспроизвести'}">${playIcon}</button>
    </div>`;
  }).join('');
}
async function playLocalFile(f){
  const audio=document.getElementById('audioEl');
  if(S.playerSource==='downloaded'&&S.playerTrackId===f.rel_path){
    if(audio.paused) audio.play(); else audio.pause();
    _updatePlayBtn(); return;
  }
  const url=await window.pywebview.api.get_file_url(f.rel_path);
  _loadAndPlay({id:f.rel_path,title:f.name,artist:'Скачанный файл',cover_uri:''}, url,'downloaded');
}

/* ═══════════════════════════════════════════════════════════════════
   SETTINGS
═══════════════════════════════════════════════════════════════════ */
async function loadSettings(){
  const c=await window.pywebview.api.get_config();
  document.getElementById('cfgToken').value=c.token||'';
  document.getElementById('cfgQuality').value=c.quality||'2';
  document.getElementById('cfgEmbedCover').checked=!!c.embed_cover;
  document.getElementById('cfgCoverRes').value=c.cover_resolution||'original';
  document.getElementById('cfgLyrics').value=c.lyrics_format||'none';
  document.getElementById('cfgPathPattern').value=c.path_pattern||String.raw`#album-artist\#album\#number-padded - #title`;
  document.getElementById('cfgDownloadDir').value=c.download_dir||'';
  document.getElementById('cfgSkipExisting').checked=!!c.skip_existing;
  document.getElementById('cfgStickToArtist').checked=!!c.stick_to_artist;
  document.getElementById('cfgOnlyMusic').checked=!!c.only_music;
  document.getElementById('cfgCompatLevel').value=c.compatibility_level||'1';
  document.getElementById('cfgParallel').value=c.parallel||'4';
  document.getElementById('cfgDelay').value=c.delay||'0';
  document.getElementById('cfgTimeout').value=c.timeout||'20';
  document.getElementById('cfgTries').value=c.tries||'20';
  document.getElementById('cfgRetryDelay').value=c.retry_delay||'5';
  if(c.token){ document.getElementById('authInfo').textContent='✓ Токен сохранён'; }
}
async function saveSettings(){
  await window.pywebview.api.save_config({
    token:document.getElementById('cfgToken').value.trim(),
    quality:document.getElementById('cfgQuality').value,
    embed_cover:document.getElementById('cfgEmbedCover').checked,
    cover_resolution:document.getElementById('cfgCoverRes').value,
    lyrics_format:document.getElementById('cfgLyrics').value,
    path_pattern:document.getElementById('cfgPathPattern').value,
    download_dir:document.getElementById('cfgDownloadDir').value.trim(),
    skip_existing:document.getElementById('cfgSkipExisting').checked,
    stick_to_artist:document.getElementById('cfgStickToArtist').checked,
    only_music:document.getElementById('cfgOnlyMusic').checked,
    compatibility_level:document.getElementById('cfgCompatLevel').value,
    parallel:document.getElementById('cfgParallel').value,
    delay:document.getElementById('cfgDelay').value,
    timeout:document.getElementById('cfgTimeout').value,
    tries:document.getElementById('cfgTries').value,
    retry_delay:document.getElementById('cfgRetryDelay').value,
  });
  const st=document.getElementById('saveStatus');
  st.textContent='✓ Сохранено'; st.style.opacity='1';
  setTimeout(()=>st.style.opacity='0',2000);
  addLog('Настройки сохранены','ok');
}
async function chooseFolder(){
  const f=await window.pywebview.api.choose_folder();
  if(f) document.getElementById('cfgDownloadDir').value=f;
}

/* ═══════════════════════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════════════════════ */
window.addEventListener('pywebviewready',()=>{
  // Восстановить сохранённые URL
  renderUrlTags();
  // Восстановить состояние лога
  const box=document.getElementById('logBox');
  box.classList.add(S.logVisible?'expanded':'collapsed');
  document.getElementById('btnLog').classList.toggle('active-mode',S.logVisible);
  // Восстановить режимы плеера
  _applyModeUI();
  // Загрузить настройки
  loadSettings();
  addLog('Приложение готово к работе','info');
});
</script>
</body>
</html>
"""
