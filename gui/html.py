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
  /* Единая «мягкая» кривая для всех переходов интерфейса */
  --ease:cubic-bezier(.22,1,.36,1);
  --ease-soft:cubic-bezier(.4,0,.2,1);
  --spring:cubic-bezier(.34,1.4,.64,1);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;}
body{font-family:-apple-system,'Segoe UI',system-ui,sans-serif;font-size:13px;
  background:var(--bg);color:var(--text);display:flex;flex-direction:column;
  height:100vh;user-select:none;-webkit-user-select:none;}

/* ── Общие анимации ── */
@keyframes fadeInUp{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
@keyframes popIn{0%{transform:scale(1);}40%{transform:scale(1.35);}100%{transform:scale(1);}}
@keyframes rowIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
@keyframes rowOut{
  0%{opacity:1;transform:translateX(0);}
  45%{opacity:0;transform:translateX(-30px);}
  100%{opacity:0;transform:translateX(-30px);height:0;
       padding-top:0;padding-bottom:0;border-bottom-width:0;}
}
@keyframes modalIn{from{opacity:0;transform:translateY(14px) scale(.96);}to{opacity:1;transform:none;}}
@keyframes bvCoverIn{from{opacity:0;transform:scale(.9) translateY(14px);}to{opacity:1;transform:none;}}
@keyframes bvInfoIn{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:none;}}
.fade-in{animation:fadeInUp .28s var(--ease);}
.pop{animation:popIn .32s var(--spring);}

/* Плавное «выезжание» строки при удалении — высоту проставляет JS перед стартом */
.row-removing{animation:rowOut .3s var(--ease-soft) forwards;pointer-events:none;overflow:hidden;}

/* Каскадное появление списков: первые строки въезжают со сдвигом по времени */
.list-enter>*{animation:rowIn .3s var(--ease) backwards;}
.list-enter>*:nth-child(1){animation-delay:0ms;}
.list-enter>*:nth-child(2){animation-delay:22ms;}
.list-enter>*:nth-child(3){animation-delay:44ms;}
.list-enter>*:nth-child(4){animation-delay:66ms;}
.list-enter>*:nth-child(5){animation-delay:88ms;}
.list-enter>*:nth-child(6){animation-delay:110ms;}
.list-enter>*:nth-child(7){animation-delay:132ms;}
.list-enter>*:nth-child(8){animation-delay:154ms;}
.list-enter>*:nth-child(9){animation-delay:176ms;}
.list-enter>*:nth-child(n+10){animation-delay:198ms;}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-delay:0ms!important;
    transition-duration:.01ms!important;}
}

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
  transition:background .2s var(--ease),color .2s var(--ease),transform .15s var(--ease);
  border:none;background:none;width:100%;text-align:left;}
.nav-item:hover{background:var(--surface2);color:var(--text);}
.nav-item:active{transform:scale(.98);}
.nav-item.active{background:var(--accent-dim);color:var(--accent);}
.nav-icon{font-size:15px;flex-shrink:0;width:18px;text-align:center;}
.sidebar-footer{margin-top:auto;padding-top:10px;border-top:1px solid var(--border);
  font-size:10px;color:var(--hint);padding-left:10px;line-height:1.7;}

/* ── Main / Pages ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.page{display:none;flex-direction:column;flex:1;overflow:hidden;padding:16px 18px;gap:12px;}
.page.active{display:flex;animation:fadeInUp .3s var(--ease);}
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
.btn{height:32px;padding:0 14px;border-radius:10px;border:1px solid transparent;
  background:var(--surface3);color:var(--text);font-size:13px;font-weight:500;
  cursor:pointer;display:inline-flex;align-items:center;gap:6px;
  transition:background .2s var(--ease),transform .14s var(--ease),
    color .2s var(--ease),border-color .2s var(--ease),opacity .2s var(--ease),
    box-shadow .2s var(--ease);
  white-space:nowrap;flex-shrink:0;}
.btn:hover{background:#353544;}
.btn:active{transform:scale(.97);}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none;}
.btn.accent{background:var(--accent);color:#1a1400;border-color:transparent;font-weight:700;
  box-shadow:0 4px 14px rgba(255,204,0,.22);}
.btn.accent:hover{opacity:.92;box-shadow:0 6px 18px rgba(255,204,0,.3);}
.btn.danger{color:var(--red);background:var(--red-dim);border-color:transparent;}
.btn.danger:hover{background:rgba(248,113,113,.22);}
.btn.sm{height:28px;padding:0 11px;font-size:12px;border-radius:8px;}
.btn.ghost{background:transparent;border-color:transparent;color:var(--muted);
  box-shadow:none;}
.btn.ghost:hover{background:var(--surface2);color:var(--text);}
.btn.active-mode{color:var(--accent);background:var(--accent-dim);box-shadow:none;}

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
  border-bottom:1px solid var(--border);cursor:pointer;
  transition:background .2s var(--ease);}
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
.cb{appearance:none;-webkit-appearance:none;width:15px;height:15px;margin:0;
  border:1.5px solid #4a4a5c;border-radius:4px;background:transparent;
  cursor:pointer;flex-shrink:0;position:relative;
  transition:background .15s var(--ease),border-color .15s var(--ease),box-shadow .15s var(--ease);}
.cb:hover{border-color:var(--accent);}
.cb:checked{background:var(--accent);border-color:var(--accent);}
.cb:checked::after{content:'';position:absolute;left:4px;top:1px;width:4px;height:8px;
  border:solid #1a1400;border-width:0 1.8px 1.8px 0;transform:rotate(45deg);}
.cb:indeterminate{background:var(--accent-dim);border-color:var(--accent);}
.cb:indeterminate::after{content:'';position:absolute;left:3px;right:3px;top:6px;height:1.8px;
  background:var(--accent);border:none;transform:none;}

/* ── Icon Buttons ── */
.iBtn{width:28px;height:28px;border-radius:8px;border:none;
  background:transparent;color:var(--muted);font-size:14px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background .2s var(--ease),color .2s var(--ease),
    transform .14s var(--ease);flex-shrink:0;}
.iBtn:hover{background:var(--surface3);color:var(--text);}
.iBtn:active{transform:scale(.9);}
.iBtn:disabled{opacity:.3;cursor:not-allowed;transform:none;}
.iBtn.playing{background:var(--blue-dim);color:var(--blue);}
.iBtn.done{color:var(--green);background:var(--green-dim);}
.iBtn.error{color:var(--red);background:var(--red-dim);}
.like-btn.liked{color:var(--red);background:var(--red-dim);}
.like-btn.liked:hover{background:rgba(248,113,113,.28);color:var(--red);}
.btn.like-btn.liked{color:var(--red);background:var(--red-dim);border-color:transparent;}
.btn.like-btn.liked:hover{background:rgba(248,113,113,.22);color:var(--red);}
.del-btn:hover{background:var(--red-dim);color:var(--red);}

/* ── Empty State ── */
.empty{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:var(--hint);gap:10px;}
.empty-icon{font-size:36px;} .empty p{font-size:13px;}

/* ── Progress ── */
.prog-wrap{flex-shrink:0;}
.prog-bar{height:3px;background:var(--border);border-radius:2px;overflow:hidden;}
.prog-fill{height:100%;background:var(--accent);border-radius:2px;transition:width .4s var(--ease);}
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
  background:var(--surface2);flex-shrink:0;cursor:pointer;transition:transform .15s;}
.player-cover:hover{transform:scale(1.08);}
.player-info{min-width:0;width:180px;flex-shrink:0;cursor:pointer;}
.player-title{font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px;}
.player-artist{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.player-controls{display:flex;align-items:center;gap:4px;flex-shrink:0;}
.player-time{font-size:11px;color:var(--muted);min-width:90px;text-align:center;flex-shrink:0;}
.player-seek{flex:1;accent-color:var(--accent);cursor:pointer;height:4px;min-width:60px;}
.player-mode{display:flex;align-items:center;gap:4px;flex-shrink:0;}
audio{display:none;}

/* ── Полноэкранный просмотр трека ── */
.bigview{position:fixed;inset:0;z-index:400;display:flex;flex-direction:column;
  background:var(--bg);opacity:0;pointer-events:none;transform:scale(1.015);
  transition:opacity .3s var(--ease),transform .3s var(--ease);}
.bigview.show{opacity:1;pointer-events:auto;transform:none;}
.bigview.hidden{display:none;}
.bigview-bg{position:absolute;inset:0;overflow:hidden;cursor:pointer;background:#0a0a10;}
.bv-wash{position:absolute;inset:-28%;background-size:cover;background-position:center;
  filter:blur(72px) saturate(1.5) brightness(.38);transform:scale(1.22);
  transition:opacity .9s var(--ease);animation:bvWash 22s ease-in-out infinite alternate;
  will-change:transform,filter;}
@keyframes bvWash{
  from{filter:blur(72px) saturate(1.35) brightness(.34) hue-rotate(-12deg);
    transform:scale(1.22) translate3d(-2%,0,0);}
  to{filter:blur(86px) saturate(1.75) brightness(.5) hue-rotate(16deg);
    transform:scale(1.34) translate3d(2.4%,1.6%,0);}
}
.bv-aurora{position:absolute;inset:-42%;opacity:0;pointer-events:none;
  background:
    radial-gradient(ellipse 52% 42% at 18% 28%, var(--c1) 0%, transparent 58%),
    radial-gradient(ellipse 46% 50% at 82% 22%, var(--c2) 0%, transparent 55%),
    radial-gradient(ellipse 58% 44% at 48% 86%, var(--c3) 0%, transparent 58%);
  filter:blur(48px) saturate(1.25);mix-blend-mode:screen;
  transition:opacity 1.5s var(--ease);
  animation:bvFlow 18s ease-in-out infinite;
  will-change:transform,opacity;
  --c1:rgba(80,60,120,.7); --c2:rgba(40,90,140,.6); --c3:rgba(160,70,90,.55);}
.bv-aurora.on{opacity:.85;}
.bv-aurora.alt{animation-duration:26s;animation-direction:reverse;filter:blur(64px) saturate(1.1);}
@keyframes bvFlow{
  0%{transform:translate3d(-2%,0,0) scale(1) rotate(0deg);}
  40%{transform:translate3d(3.5%,-4%,0) scale(1.12) rotate(12deg);}
  70%{transform:translate3d(-4.5%,3%,0) scale(1.07) rotate(-9deg);}
  100%{transform:translate3d(-2%,0,0) scale(1) rotate(0deg);}
}
.bv-vignette{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at 50% 42%, transparent 28%, rgba(0,0,0,.42) 100%);}
@media (prefers-reduced-motion:reduce){
  .bv-wash,.bv-aurora{animation:none!important;}
}
.bigview-top{position:relative;display:flex;align-items:center;gap:10px;
  padding:14px 18px;flex-shrink:0;}
.bigview-src{font-size:11px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;}
.bigview-body{position:relative;flex:1;display:flex;gap:36px;padding:0 48px 28px;overflow:hidden;
  align-items:stretch;}
.bigview-cover{width:min(340px,32vw);height:min(340px,32vw);flex-shrink:0;border-radius:14px;
  object-fit:cover;background:var(--surface2);box-shadow:0 20px 60px rgba(0,0,0,.5);
  align-self:center;cursor:pointer;transition:transform .3s var(--ease),box-shadow .3s var(--ease);}
.bigview-cover:hover{transform:scale(1.02);box-shadow:0 26px 70px rgba(0,0,0,.6);}
.bigview-cover.swap{animation:coverSwap .35s var(--ease);}
@keyframes coverSwap{from{opacity:.35;transform:scale(.97);}to{opacity:1;transform:none;}}
.bigview.show .bigview-cover{animation:bvCoverIn .45s var(--ease) both;}
.bigview.show .bigview-info{animation:bvInfoIn .45s .05s var(--ease) both;}
.bigview-info{flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden;}
.bigview-title{font-size:26px;font-weight:700;margin-bottom:6px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.bigview-artist{font-size:15px;color:var(--muted);margin-bottom:2px;}
.bigview-album{font-size:13px;color:var(--hint);margin-bottom:14px;}

/* Прогресс и управление внутри полноэкранного режима */
.bigview-seek{display:flex;align-items:center;gap:10px;margin-bottom:12px;max-width:640px;}
.bigview-seek .player-seek{flex:1;}
.bv-time{font-size:11px;color:var(--muted);min-width:38px;flex-shrink:0;
  font-variant-numeric:tabular-nums;}
.bv-time.right{text-align:right;}
.bigview-actions{display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;}
.bigview-tools{display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap;}
.bigview-next{font-size:11px;color:var(--hint);margin-bottom:14px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:640px;}
.bigview-next b{color:var(--muted);font-weight:600;}
.bigview-lyrics-wrap{flex:1;overflow-y:auto;border-top:1px solid var(--border);padding-top:16px;}
.bigview-lyrics{white-space:pre-wrap;line-height:1.9;font-size:14px;color:var(--text);
  max-width:640px;}
.bigview-lyrics.muted{color:var(--hint);font-style:italic;white-space:normal;}
.bigview-lyrics.fade-swap{animation:lyricsIn .3s var(--ease);}
@keyframes lyricsIn{from{opacity:0;transform:translateY(5px);}to{opacity:1;transform:none;}}

/* ── Кликабельные исполнитель / альбом ── */
.lnk{cursor:pointer;transition:color .15s var(--ease);}
.lnk:hover{color:var(--accent);text-decoration:underline;}
.search-hint{font-size:11px;color:var(--hint);min-height:14px;margin-top:6px;}
.search-sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--muted);padding:12px 10px 6px;}
.search-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));
  gap:8px;padding:2px 10px 12px;}

/* ── Страницы исполнителя и альбома ── */
.br-crumb{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:6px;
  min-width:0;overflow:hidden;white-space:nowrap;}
.br-crumb b{color:var(--text);font-weight:600;}
.br-sep{color:var(--hint);}
.browse-body{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:14px;padding-right:4px;}
.br-hero{display:flex;gap:18px;align-items:center;flex-shrink:0;}
.br-hero-cover{width:150px;height:150px;border-radius:12px;object-fit:cover;flex-shrink:0;
  background:var(--surface2);box-shadow:0 14px 34px rgba(0,0,0,.45);}
.br-hero-ph{display:flex;align-items:center;justify-content:center;font-size:48px;}
.br-hero-info{min-width:0;display:flex;flex-direction:column;gap:5px;}
.br-hero-kind{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.br-hero-title{font-size:26px;font-weight:700;line-height:1.15;}
.br-hero-sub{font-size:12px;color:var(--muted);}
.br-hero-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;}
.br-sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid var(--border);padding-bottom:5px;flex-shrink:0;}
.br-list{border:1px solid var(--border);border-radius:var(--r);overflow:hidden;flex-shrink:0;}

/* ── Modals ── */
.modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.75);
  display:flex;align-items:center;justify-content:center;z-index:100;
  animation:fadeInUp .2s var(--ease);backdrop-filter:blur(2px);}
.modal-bg.hidden{display:none;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:24px;width:400px;display:flex;flex-direction:column;gap:14px;
  animation:modalIn .3s var(--ease);}
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
.pl-card{position:relative;background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  overflow:hidden;cursor:pointer;
  transition:border-color .25s var(--ease),transform .25s var(--ease),box-shadow .25s var(--ease);}
.pl-card:hover{border-color:var(--border2);transform:translateY(-3px);
  box-shadow:0 10px 24px rgba(0,0,0,.35);}
.pl-card:active{transform:translateY(-1px) scale(.99);}
.pl-cover{width:100%;aspect-ratio:1;object-fit:cover;background:var(--surface2);display:block;
  transition:transform .3s var(--ease);}
.pl-card:hover .pl-cover{transform:scale(1.04);}
.pl-cover-ph{width:100%;aspect-ratio:1;background:var(--surface2);
  display:flex;align-items:center;justify-content:center;font-size:28px;}
.pl-info{padding:8px;}
.pl-name{font-weight:500;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pl-count{font-size:11px;color:var(--muted);margin-top:2px;}
.pl-card.artist-card .pl-cover,.pl-card.artist-card .pl-cover-ph{border-radius:50%;
  width:calc(100% - 16px);margin:8px auto 0;aspect-ratio:1;}
.card-like{position:absolute;top:6px;right:6px;z-index:2;opacity:0;
  background:rgba(15,15,17,.72);backdrop-filter:blur(6px);}
.pl-card:hover .card-like,.card-like.liked,.pl-card:hover .card-del{opacity:1;}
.card-del{position:absolute;top:6px;right:6px;z-index:2;opacity:0;
  background:rgba(15,15,17,.72);backdrop-filter:blur(6px);}
.card-play{position:absolute;left:8px;top:8px;z-index:2;opacity:0;width:34px;height:34px;
  border-radius:50%;background:rgba(15,15,17,.75);font-size:15px;}
.pl-card:hover .card-play,.card-play.on{opacity:1;}
.card-play.on{background:var(--accent);color:#1a1400;}
input.pl-search{width:min(220px,36vw);height:28px;padding:0 10px;font-size:12px;flex:0 1 220px;}

/* ── Extra track rows (search / wave / playlist detail) ── */
.ex-row{display:grid;grid-template-columns:24px 1fr 150px 64px 28px 28px 28px 28px 28px;
  gap:6px;padding:8px 10px;align-items:center;cursor:pointer;
  border-bottom:1px solid var(--border);transition:background .2s var(--ease);}
.br-more{display:flex;justify-content:center;padding:12px 10px;}
.ex-row.selectable{grid-template-columns:18px 24px 1fr 150px 64px 28px 28px 28px 28px 28px;}
.ex-row.removable{grid-template-columns:24px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;}
.ex-row.selectable.removable{grid-template-columns:18px 24px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;}
.ex-row:last-child{border-bottom:none;}
.ex-row:hover{background:var(--surface2);}
.ex-row.downloading{background:var(--blue-dim);}
.ex-row.done{background:var(--green-dim);}
.ex-row.error{background:var(--red-dim);}
.add-menu-item:hover{background:var(--surface2);}
.wave-card{display:flex;align-items:center;gap:10px;padding:10px;cursor:pointer;
  max-width:280px;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);
  transition:border-color .25s var(--ease),transform .25s var(--ease),box-shadow .25s var(--ease);}
.wave-card:hover{border-color:var(--border2);transform:translateY(-3px);
  box-shadow:0 10px 24px rgba(0,0,0,.35);}

/* ── Toasts ── */
.toast-container{position:fixed;bottom:16px;right:16px;display:flex;flex-direction:column;
  gap:8px;z-index:500;pointer-events:none;}
.toast{pointer-events:auto;background:var(--surface3);border:1px solid var(--border2);
  border-radius:var(--r);padding:10px 12px;display:flex;align-items:center;gap:10px;
  min-width:230px;max-width:340px;box-shadow:0 6px 24px rgba(0,0,0,.45);
  opacity:0;transform:translateX(24px) scale(.98);
  transition:opacity .3s var(--ease),transform .3s var(--ease);font-size:12px;color:var(--text);}
.toast.show{opacity:1;transform:translateX(0) scale(1);}
.toast.hide{opacity:0;transform:translateX(24px) scale(.98);}
.toast-ok{border-color:rgba(74,222,128,.45);}
.toast-err{border-color:rgba(248,113,113,.45);}
.toast-icon{font-size:15px;flex-shrink:0;}
.toast-msg{flex:1;line-height:1.4;min-width:0;}
.toast-action{flex-shrink:0;background:var(--accent);color:#000;border:none;border-radius:6px;
  padding:5px 9px;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap;
  transition:opacity .15s;}
.toast-action:hover{opacity:.85;}
.toast-close{flex-shrink:0;cursor:pointer;color:var(--hint);font-size:14px;line-height:1;
  transition:color .15s;}
.toast-close:hover{color:var(--text);}

/* ── Downloaded ── */
.dl-row{display:flex;align-items:center;gap:10px;padding:8px 12px;overflow:hidden;cursor:pointer;
  border-bottom:1px solid var(--border);transition:background .2s var(--ease);}
.dl-row:hover{background:var(--surface2);}
.dl-row.dl-playing{background:var(--blue-dim);}
.dl-cover,.dl-cover-ph{width:40px;height:40px;border-radius:6px;flex-shrink:0;
  background:var(--surface2);object-fit:cover;}
.dl-cover{cursor:pointer;}
.dl-cover-ph{display:flex;align-items:center;justify-content:center;font-size:16px;color:var(--hint);cursor:pointer;}
.dl-meta{flex:1;min-width:0;}
.dl-ext{font-size:10px;font-weight:700;color:var(--accent);min-width:36px;text-align:center;
  background:var(--accent-dim);padding:2px 5px;border-radius:4px;flex-shrink:0;}
.dl-name{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.dl-sub{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;}
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

<!-- ══ Confirm Modal ══ -->
<div class="modal-bg hidden" id="confirmModal" onclick="if(event.target===this)closeConfirm()">
  <div class="modal" style="width:360px">
    <h2 id="confirmTitle">Подтверждение</h2>
    <p id="confirmText"></p>
    <div style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn" onclick="closeConfirm()">Отмена</button>
      <button class="btn danger" id="confirmOk" onclick="acceptConfirm()">Удалить</button>
    </div>
  </div>
</div>

<!-- ══ Prompt Modal (название плейлиста) ══ -->
<div class="modal-bg hidden" id="promptModal" onclick="if(event.target===this)closePrompt()">
  <div class="modal" style="width:360px">
    <h2 id="promptTitle">Новый плейлист</h2>
    <p id="promptText" style="display:none"></p>
    <input type="text" id="promptInput" placeholder="Название плейлиста"
      onkeydown="if(event.key==='Enter'){event.preventDefault();acceptPrompt();}">
    <div style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn" onclick="closePrompt()">Отмена</button>
      <button class="btn accent" id="promptOk" onclick="acceptPrompt()">Создать</button>
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
    <button class="nav-item active" onclick="showPage('search',this)"><span class="nav-icon">🔍</span>Поиск</button>
    <button class="nav-item" onclick="showPage('playlists',this);openPlaylistsList()"><span class="nav-icon">📋</span>Плейлисты</button>
    <button class="nav-item" onclick="showPage('artists',this);openArtistsPage()"><span class="nav-icon">🎤</span>Исполнители</button>
    <button class="nav-item" onclick="showPage('albums',this);openAlbumsPage()"><span class="nav-icon">💿</span>Альбомы</button>
    <button class="nav-item" onclick="showPage('downloaded',this);scanDownloaded()"><span class="nav-icon">🎵</span>Скачанные</button>
    <button class="nav-item" onclick="showPage('settings',this)"><span class="nav-icon">⚙</span>Настройки</button>
    <div style="height:1px;background:var(--border);margin:8px 6px"></div>
    <button class="nav-item" onclick="showPage('download',this)" style="opacity:.65" title="Дополнительно: скачивание по прямой ссылке">
      <span class="nav-icon">🔗</span>По ссылке
      <span style="font-size:9px;color:var(--hint);margin-left:auto;flex-shrink:0">доп.</span>
    </button>
    <div class="sidebar-footer">yandex-music-downloader</div>
  </nav>

  <div class="main">

    <!-- ══ СКАЧИВАНИЕ ПО ССЫЛКЕ (доп.) ══ -->
    <div class="page" id="page-download">
      <div>
        <div style="font-size:11px;color:var(--hint);margin-bottom:2px">Дополнительная функция — прямое скачивание по ссылке, в обход поиска и плейлистов</div>
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

    <!-- ══ ПОИСК ══ -->
    <div class="page active" id="page-search">
      <div>
        <label style="font-size:10px;color:var(--muted);font-weight:600;letter-spacing:.04em;display:block;margin-bottom:5px">ПОИСК В ЯНДЕКС.МУЗЫКЕ</label>
        <div class="input-row">
          <input type="text" id="searchInput" placeholder="Трек, исполнитель или альбом..."
            oninput="onSearchInput()"
            onkeydown="if(event.key==='Enter')doSearch()">
          <button class="btn accent" onclick="doSearch()">🔍 Найти</button>
        </div>
        <div class="search-hint" id="searchHint">Начните вводить — результаты появятся сами</div>
      </div>
      <div class="tl-wrap">
        <div class="tl-body" id="searchBody">
          <div class="empty"><span class="empty-icon">🔍</span><p>Начните вводить — найдутся треки, исполнители и альбомы</p></div>
        </div>
      </div>
    </div>

    <!-- ══ ЛЮБИМЫЕ ИСПОЛНИТЕЛИ ══ -->
    <div class="page" id="page-artists">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Любимые исполнители</span>
        <button class="btn sm" onclick="loadLikedLibrary(true)">↻ Обновить</button>
        <span id="artistsCount" style="font-size:12px;color:var(--muted)"></span>
      </div>
      <div id="artistsGrid" style="flex:1;overflow-y:auto">
        <div class="empty"><span class="empty-icon">🎤</span><p>Войдите в аккаунт — здесь появятся любимые исполнители</p></div>
      </div>
    </div>

    <!-- ══ ПОНРАВИВШИЕСЯ АЛЬБОМЫ ══ -->
    <div class="page" id="page-albums">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Понравившиеся альбомы</span>
        <button class="btn sm" onclick="loadLikedLibrary(true)">↻ Обновить</button>
        <span id="albumsCount" style="font-size:12px;color:var(--muted)"></span>
      </div>
      <div id="albumsGrid" style="flex:1;overflow-y:auto">
        <div class="empty"><span class="empty-icon">💿</span><p>Войдите в аккаунт — здесь появятся понравившиеся альбомы</p></div>
      </div>
    </div>

    <!-- ══ МОИ ПЛЕЙЛИСТЫ / ВОЛНА ══ -->
    <div class="page" id="page-playlists">

      <!-- Сетка плейлистов -->
      <div id="plGridWrap" style="display:flex;flex-direction:column;flex:1;overflow:hidden;gap:10px">
        <div class="toolbar">
          <span style="font-size:13px;font-weight:600">Мои плейлисты</span>
          <button class="btn sm accent" onclick="promptCreatePlaylist()">＋ Создать</button>
          <button class="btn sm" onclick="loadMyPlaylists(true)">↻ Обновить</button>
          <span id="plRefreshHint" style="font-size:11px;color:var(--hint)"></span>
        </div>
        <div style="flex-shrink:0">
          <div class="wave-card" onclick="openWave()" title="Открыть «Мою волну»">
            <div class="pl-cover-ph" style="width:44px;height:44px;border-radius:8px;font-size:20px;flex-shrink:0">🌊</div>
            <div>
              <div class="pl-name" style="font-size:13px">Моя волна</div>
              <div class="pl-count">Бесконечный поток треков</div>
            </div>
          </div>
        </div>
        <div id="plGrid" style="flex:1;overflow-y:auto">
          <div class="empty"><span class="empty-icon">📋</span><p>Войдите в аккаунт и нажмите «Обновить»</p></div>
        </div>
      </div>

      <!-- Детали открытого плейлиста -->
      <div id="plDetailWrap" style="display:none;flex-direction:column;flex:1;overflow:hidden;gap:10px">
        <div class="toolbar">
          <button class="btn sm" onclick="closePlaylistDetail()">← Назад</button>
          <span id="plDetailTitle" style="font-size:13px;font-weight:600"></span>
          <span id="plDetailCount" style="font-size:12px;color:var(--muted)"></span>
          <input type="text" id="plTrackSearch" class="pl-search" placeholder="Поиск по плейлисту…"
            oninput="onPlTrackSearch()">
          <div class="toolbar-right">
            <button class="btn sm" onclick="selectAllIn('playlist_detail',true)">☑ Все</button>
            <button class="btn sm" onclick="selectAllIn('playlist_detail',false)">☐ Снять</button>
            <button class="btn sm accent" id="btnPlDownloadSel" onclick="downloadSelected('playlist_detail')" style="display:none">⬇ Скачать выбранные</button>
            <button class="btn ghost sm" onclick="addPlaylistUrl(S.plDetail.url)" title="Скачать всё как в старом режиме, по ссылке">🔗 По ссылке</button>
            <button class="btn accent sm" onclick="downloadAllPlaylistDetail()">⬇ Скачать все</button>
            <button class="btn sm danger" id="btnPlDelete" onclick="confirmDeleteCurrentPlaylist()" style="display:none">🗑 Удалить</button>
          </div>
        </div>
        <div class="tl-wrap">
          <div class="tl-body" id="plDetailBody"></div>
        </div>
      </div>

      <!-- Моя волна -->
      <div id="plWaveWrap" style="display:none;flex-direction:column;flex:1;overflow:hidden;gap:10px">
        <div class="toolbar">
          <button class="btn sm" onclick="closeWave()">← Назад</button>
          <span style="font-size:13px;font-weight:600" id="waveTitle">🌊 Моя волна</span>
          <span id="waveCount" style="font-size:12px;color:var(--muted)"></span>
          <div class="toolbar-right">
            <button class="btn sm" onclick="resetWave()" title="Начать волну заново">↻ Заново</button>
            <button class="btn sm" onclick="selectAllIn('wave',true)">☑ Все</button>
            <button class="btn sm" onclick="selectAllIn('wave',false)">☐ Снять</button>
            <button class="btn sm" id="btnWaveMore" onclick="loadMoreWave()">▶ Ещё треки</button>
            <button class="btn sm accent" id="btnWaveDownloadSel" onclick="downloadSelected('wave')" style="display:none">⬇ Скачать выбранные</button>
            <button class="btn accent sm" onclick="downloadAllWave()">⬇ Скачать все</button>
          </div>
        </div>
        <div class="tl-wrap">
          <div class="tl-body" id="waveBody"></div>
        </div>
      </div>

    </div>

    <!-- ══ СКАЧАННЫЕ ══ -->
    <div class="page" id="page-downloaded">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Скачанные треки</span>
        <button class="btn sm" onclick="scanDownloaded()">↻ Обновить</button>
        <span id="dlCount" style="font-size:12px;color:var(--muted)"></span>
        <button class="btn sm" onclick="dlSelectAll(true)">☑ Все</button>
        <button class="btn sm" onclick="dlSelectAll(false)">☐ Снять</button>
        <span id="dlSelInfo" style="font-size:12px;color:var(--accent)"></span>
        <div class="toolbar-right">
          <button class="btn sm danger" id="btnDlDeleteSel" onclick="deleteSelectedDownloaded()" style="display:none">🗑 Удалить выбранные</button>
          <button class="btn sm" onclick="window.pywebview.api.open_download_folder()">📂 Открыть папку</button>
        </div>
      </div>
      <div id="dlList" style="flex:1;overflow-y:auto;border:1px solid var(--border);border-radius:var(--r)">
        <div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов</p></div>
      </div>
    </div>

    <!-- ══ ИСПОЛНИТЕЛЬ / АЛЬБОМ ══ -->
    <div class="page" id="page-browse">
      <div class="toolbar">
        <button class="btn sm" id="browseBack" onclick="browseBack()">← Назад</button>
        <div class="br-crumb" id="browseCrumb"></div>
        <div class="toolbar-right">
          <button class="btn sm" onclick="selectAllIn('browse',true)">☑ Все</button>
          <button class="btn sm" onclick="selectAllIn('browse',false)">☐ Снять</button>
          <button class="btn sm accent" id="btnBrowseDownloadSel" onclick="downloadSelected('browse')" style="display:none">⬇ Скачать выбранные</button>
          <button class="btn ghost sm" onclick="closeBrowse()" title="Закрыть (Esc)">✕</button>
        </div>
      </div>
      <div class="browse-body" id="browseBody"></div>
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
  <img class="player-cover" id="plCover" src="" alt="" style="display:none" onclick="openBigView()" title="Развернуть">
  <div class="player-info" onclick="openBigView()" title="Развернуть">
    <div class="player-title" id="plTitle">—</div>
    <div class="player-artist" id="plArtist">—</div>
  </div>
  <button class="iBtn like-btn" id="plLikeBtn" onclick="toggleLikeCurrent()" title="Мне нравится">♡</button>
  <button class="iBtn" id="plAddBtn" onclick="miniPlayerAdd(event)" title="Добавить в плейлист">➕</button>
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

<!-- ══ Полноэкранный просмотр трека ══ -->
<div class="bigview hidden" id="bigView">
  <div class="bigview-bg" id="bigViewBg" onclick="closeBigView()" title="Свернуть">
    <div class="bv-wash" id="bvWash"></div>
    <div class="bv-aurora" id="bvAuroraA"></div>
    <div class="bv-aurora alt" id="bvAuroraB"></div>
    <div class="bv-vignette"></div>
  </div>
  <div class="bigview-top">
    <span class="bigview-src" id="bigViewSrc"></span>
    <button class="btn sm ghost" style="margin-left:auto" onclick="closeBigView()" title="Свернуть (Esc)">✕ Свернуть</button>
  </div>
  <div class="bigview-body">
    <img class="bigview-cover" id="bigViewCover" src="" alt=""
      onclick="playerToggle()" title="Плей / пауза">
    <div class="bigview-info">
      <div class="bigview-title" id="bigViewTitle">—</div>
      <div class="bigview-artist" id="bigViewArtist">—</div>
      <div class="bigview-album" id="bigViewAlbum"></div>

      <div class="bigview-seek">
        <span class="bv-time" id="bvCur">0:00</span>
        <input type="range" class="player-seek" id="bvSeek" value="0" min="0" max="100" step="0.1"
          oninput="playerSeek(this.value)">
        <span class="bv-time right" id="bvDur">0:00</span>
      </div>

      <div class="bigview-actions">
        <button class="btn sm ghost" id="bvShuffle" onclick="toggleShuffle()" title="Перемешать">⇄</button>
        <button class="btn sm ghost" onclick="playerPrev()" title="Предыдущий трек">⏮</button>
        <button class="btn sm ghost" onclick="playerSkip(-10)" title="-10 сек">«10</button>
        <button class="btn accent" id="bigViewPlayBtn" onclick="playerToggle()" title="Плей / пауза (Пробел)">▶</button>
        <button class="btn sm ghost" onclick="playerSkip(10)" title="+10 сек">10»</button>
        <button class="btn sm ghost" onclick="playerNext()" title="Следующий трек">⏭</button>
        <button class="btn sm ghost" id="bvRepeat" onclick="cycleRepeat()" title="Повтор трека">↻</button>
      </div>

      <div class="bigview-tools">
        <button class="iBtn like-btn" id="bigViewLikeBtn" onclick="toggleLikeCurrent()" title="Мне нравится">♡</button>
        <button class="iBtn" id="bvAddBtn" onclick="bigViewAdd(event)" title="Добавить в плейлист">➕</button>
        <button class="iBtn" id="bvWaveBtn" onclick="startTrackWaveCurrent()" title="Волна по треку">🌊</button>
        <button class="iBtn" id="bvDlBtn" onclick="bigViewDownload()" title="Скачать трек">⬇</button>
        <button class="iBtn del-btn" id="bvDelBtn" onclick="bigViewRemove()" title="Удалить из плейлиста" style="display:none">🗑</button>
        <button class="btn sm ghost" id="bvOpenBtn" onclick="bigViewOpenExternal()" title="Открыть в Яндекс.Музыке">🔗 В Яндекс.Музыке</button>
      </div>

      <div class="bigview-next" id="bvNext"></div>

      <div class="bigview-lyrics-wrap">
        <div class="bigview-lyrics muted" id="bigViewLyrics">Текст песни не загружен</div>
      </div>
    </div>
  </div>
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

/* Кэш с меткой времени: показываем сразу, в Яндекс ходим только если устарело */
const CACHE = {
  TTL: 30*60*1000,
  read(key){
    const v=STORE.get(key, null);
    if(v==null) return {data:null, missing:true, stale:true};
    if(v && typeof v==='object' && 'ts' in v && 'data' in v){
      return {data:v.data, missing:false, stale:(Date.now()-v.ts)>CACHE.TTL};
    }
    return {data:v, missing:false, stale:true};
  },
  write(key, data){
    try{ STORE.set(key, {ts:Date.now(), data}); }
    catch(e){
      try{
        STORE.del('ym_browse_cache');
        STORE.del('ym_pl_tracks');
        STORE.set(key, {ts:Date.now(), data});
      }catch(e2){}
    }
  },
  fresh(key){ const r=CACHE.read(key); return !r.missing && !r.stale; },
  age(key){
    const v=STORE.get(key, null);
    return (v && v.ts) ? Date.now()-v.ts : null;
  },
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
  playerSource: 'tracks',   // 'tracks' | 'downloaded' | 'search' | 'wave' | 'playlist_detail' | 'browse'
  // очередь воспроизведения — снимок списка, из которого запустили трек:
  // уход на страницу исполнителя или новый поиск не должны менять «что дальше»
  playerQueue: null,
  dlFiles: [],              // список скачанных для навигации
  dlSelected: new Set(),    // выбранные скачанные файлы (rel_path)
  dlIds: new Set(),         // yandex id скачанных треков
  dlKeys: new Set(),        // artist+title — запасное совпадение без id
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
  // поиск / плейлисты / волна
  searchResults: [],
  myPlaylistsFlat: [],
  plView: 'grid',           // 'grid' | 'detail' | 'wave'
  plRendered: false,        // в сетке уже показаны карточки (а не «Загружаем…»)
  plTracksCache: {},        // url плейлиста → загруженные треки
  plTracksTs: {},
  browseCacheTs: {},
  pendingPlaylistCreate: null,
  pendingPlaylistDeletes: {},
  // id/group нужны, чтобы понимать, можно ли удалять треки из открытого плейлиста
  plDetail: { url: '', title: '', tracks: [], id: null, group: '', editable: false },
  waveTracks: [],
  waveSeenIds: [],
  waveLoading: false,
  waveStation: 'user:onyourwave',
  waveSeedTitle: '',
  pendingWavePlay: false,
  pendingPlaylistPlay: null,
  pendingAlbumPlay: '',
  pendingArtistPlay: '',
  playingPlaylistUrl: '',
  playingCardKey: '',
  // выбранные треки для скачивания, отдельно по каждому списку
  sel: { wave: new Set(), playlist_detail: new Set(), browse: new Set() },
  // страницы исполнителя/альбома: стек переходов + кэш загруженного
  browseStack: [],
  browseCache: {},
  browseOpen: false,
  browseReturn: null,       // id страницы, на которую вернёт «Назад»
  pendingAdds: {},
  // снимки удалённых строк — чтобы вернуть их назад, если сервер отказал
  pendingRemovals: {},
  likedRemovals: {},
  pendingFileDeletes: {},
  searchDone: false,
  searchArtists: [],
  searchAlbums: [],
  searchSeq: 0,             // отсекает ответы на уже устаревший запрос
  searchTimer: null,
  previewUrls: {},          // track_id → прямая ссылка (живёт, пока не истечёт)
  // лайки / полноэкранный просмотр
  likedIds: new Set(),
  likedPending: new Set(),
  likedArtistIds: new Set(),
  likedAlbumIds: new Set(),
  likedArtists: [],
  likedAlbums: [],
  likedArtistPending: new Set(),
  likedAlbumPending: new Set(),
  plTrackQuery: '',
  lyricsCache: {},
  lyricsPending: new Set(),
  coverToken: 0,            // отсекает загрузку обложки уже неактуального трека
  coverColors: {},          // url обложки → 3 цвета для фона
  auroraOn: 'A',            // какой слой aurora сейчас виден
  // заранее подготовленный следующий трек: ссылка + прогретое аудио
  prefetch: { id: null, url: null, audio: null },
  usedPrefetchUrl: false,
  prefetchTimer: null,
  bigViewOpen: false,
  bigViewTrackId: null,
  bigViewHideTimer: null,
  // снимок играющего трека — переживает смену плейлиста/поиска
  playerTrack: null,
  likeUiTrackId: null,
  likeUiLiked: false,
  confirmAction: null,
  promptAction: null,
};

function hydrateCaches(){
  const dl=STORE.get('ym_dl_marks', null);
  if(dl && typeof dl==='object'){
    S.dlIds=new Set((dl.ids||[]).map(String));
    S.dlKeys=new Set(dl.keys||[]);
  }
  const pl=CACHE.read('ym_pl_cache');
  if(Array.isArray(pl.data) && pl.data.length) S.myPlaylistsFlat=pl.data;
  const lib=CACHE.read('ym_liked_library');
  if(lib.data && typeof lib.data==='object'){
    S.likedArtists=lib.data.artists||[];
    S.likedAlbums=lib.data.albums||[];
    S.likedArtistIds=new Set(S.likedArtists.map(a=>String(a.id)).filter(Boolean));
    S.likedAlbumIds=new Set(S.likedAlbums.map(a=>String(a.id)).filter(Boolean));
  }
  const ids=CACHE.read('ym_liked_ids');
  if(Array.isArray(ids.data)) S.likedIds=new Set(ids.data.map(String));
  const tracks=CACHE.read('ym_pl_tracks');
  if(tracks.data && typeof tracks.data==='object'){
    S.plTracksCache=tracks.data.list||tracks.data;
    S.plTracksTs=tracks.data.ts||{};
  }
  const browse=CACHE.read('ym_browse_cache');
  if(browse.data && typeof browse.data==='object'){
    const map=browse.data.list||browse.data;
    const ts=browse.data.ts||{};
    Object.keys(map).forEach(k=>{
      if(k.startsWith('artist_tracks:')) return;
      S.browseCache[k]=map[k];
      if(ts[k]) S.browseCacheTs[k]=ts[k];
    });
  }
}
function _persistPlTracks(){
  CACHE.write('ym_pl_tracks', {list:S.plTracksCache, ts:S.plTracksTs});
}
function _persistBrowseCache(){
  const list={}, ts={};
  Object.keys(S.browseCache).forEach(k=>{
    if(k.startsWith('artist_tracks:')) return;
    list[k]=S.browseCache[k];
    if(S.browseCacheTs[k]) ts[k]=S.browseCacheTs[k];
  });
  CACHE.write('ym_browse_cache', {list, ts});
}
function _persistLikedIds(){
  CACHE.write('ym_liked_ids', [...S.likedIds]);
}
function _persistLibrary(){
  CACHE.write('ym_liked_library', {artists:S.likedArtists, albums:S.likedAlbums});
}
function _normDl(s){
  return String(s||'').toLowerCase().replace(/ё/g,'е').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
}
function _dlKey(artist, title){
  const t=_normDl(title);
  return t ? (_normDl(artist)+'\t'+t) : '';
}
function _isDownloaded(t){
  if(!t) return false;
  if(t.id && S.dlIds.has(String(t.id))) return true;
  const k=_dlKey(t.artist, t.title);
  return !!(k && S.dlKeys.has(k));
}
function _applyDlStatus(t){
  if(!t || !t.id) return t;
  if(t.status==='downloading' || t.status==='queued') return t;
  if(_isDownloaded(t)) t.status='done';
  else if(t.status==='done') t.status='idle';
  return t;
}
function _applyDlList(list){
  (list||[]).forEach(_applyDlStatus);
  return list;
}
function _persistDlMarks(){
  STORE.set('ym_dl_marks', {ids:[...S.dlIds], keys:[...S.dlKeys]});
}
function _rebuildDlMarks(files){
  S.dlIds=new Set();
  S.dlKeys=new Set();
  (files||[]).forEach(f=>{
    if(f.track_id) S.dlIds.add(String(f.track_id));
    const k=_dlKey(f.artist, f.title);
    if(k) S.dlKeys.add(k);
  });
  _persistDlMarks();
  _syncDlMarks();
}
function _rememberDlTrack(t){
  if(!t || !t.id) return;
  S.dlIds.add(String(t.id));
  const k=_dlKey(t.artist, t.title);
  if(k) S.dlKeys.add(k);
  _persistDlMarks();
  try{ window.pywebview.api.remember_download(String(t.id), t.title||'', t.artist||''); }catch(_e){}
}
function _dropDlFileMark(f){
  if(!f) return;
  if(f.track_id) S.dlIds.delete(String(f.track_id));
  const k=_dlKey(f.artist, f.title);
  if(k) S.dlKeys.delete(k);
}
function _restoreDlFileMark(f){
  if(!f) return;
  if(f.track_id) S.dlIds.add(String(f.track_id));
  const k=_dlKey(f.artist, f.title);
  if(k) S.dlKeys.add(k);
}
function _forgetDlFile(f){
  _dropDlFileMark(f);
  _persistDlMarks();
  _syncDlMarks();
}
function _syncDlMarks(){
  _applyDlList(S.tracks);
  _applyDlList(S.searchResults);
  _applyDlList(S.waveTracks);
  _applyDlList(S.plDetail && S.plDetail.tracks);
  Object.values(S.plTracksCache||{}).forEach(list=>{ if(Array.isArray(list)) _applyDlList(list); });
  Object.values(S.browseCache||{}).forEach(d=>{ if(d && Array.isArray(d.tracks)) _applyDlList(d.tracks); });
  (S.browseStack||[]).forEach(en=>{ if(en && en.tracks) _applyDlList(en.tracks); });
  const active=document.querySelector('.page.active');
  const page=active?active.id:'';
  if(page==='page-download') renderTracks();
  else S.tracks.forEach(t=>{ const row=document.getElementById('row-'+t.id); if(row) updateRow(row,t); });
  if(S.plView==='detail') renderPlaylistDetail();
  if(S.plView==='wave') renderWave();
  if(S.browseOpen) renderBrowse();
  if(page==='page-search' && S.searchDone) renderSearchResults(false);
  if(S.bigViewOpen) _fillBigView();
}

function refreshStaleCaches(force){
  if(force || !CACHE.fresh('ym_pl_cache')) window.pywebview.api.get_my_playlists();
  if(force || !CACHE.fresh('ym_liked_ids')) window.pywebview.api.get_liked_ids();
  if(force || !CACHE.fresh('ym_liked_library')) window.pywebview.api.get_liked_library();
}
hydrateCaches();

/* ═══════════════════════════════════════════════════════════════════
   UTILS
═══════════════════════════════════════════════════════════════════ */
function esc(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function fmtBytes(b){ return b>1e6?(b/1e6).toFixed(1)+' MB':(b/1e3).toFixed(0)+' KB'; }
function fmtTime(s){ s=Math.floor(s||0); if(!isFinite(s)||s<0) s=0; return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`; }

/* Имена исполнителей и альбома как ссылки на их страницы */
function _artistLinks(t){
  const list=(t.artists||[]).filter(a=>a&&a.name);
  if(!list.length) return esc(t.artist||'');
  return list.map(a=>a.id
    ?`<span class="lnk" onclick="event.stopPropagation();openArtist('${esc(a.id)}')">${esc(a.name)}</span>`
    :esc(a.name)).join(', ');
}
function _albumLink(t){
  if(!t.album) return '';
  if(!t.album_id) return esc(t.album);
  return `<span class="lnk" onclick="event.stopPropagation();openAlbum('${esc(t.album_id)}')">${esc(t.album)}</span>`;
}

/* Каскадное появление только что отрисованного списка */
function _playListEnter(el){
  if(!el) return;
  el.classList.remove('list-enter');
  void el.offsetWidth; // форсируем reflow, иначе анимация не перезапустится
  el.classList.add('list-enter');
}

/* Плавно «схлопывает» строку и удаляет её из DOM, затем зовёт after() */
function _animateElOut(el, after){
  if(!el){ if(after) after(); return; }
  el.style.height=el.offsetHeight+'px';
  el.classList.add('row-removing');
  let finished=false;
  const finish=()=>{
    if(finished) return;
    finished=true;
    el.remove();
    if(after) after();
  };
  el.addEventListener('animationend', finish, {once:true});
  setTimeout(finish, 420); // страховка, если animationend не придёт
}
function _animateRowOut(source, id, after){
  _animateElOut(document.getElementById('exrow-'+source+'-'+id), after);
}

/* Перенумеровывает оставшиеся строки на месте, без перерисовки всего списка */
function _renumberList(source){
  _listFor(source).forEach((t,i)=>{
    t.num=i+1;
    const el=document.getElementById('exrow-'+source+'-'+t.id);
    if(el){
      const n=el.querySelector('.tl-num');
      if(n) n.textContent=t.num;
    }
  });
}

/* ═══════════════════════════════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════════════════════════════ */
function showPage(id,btn){
  if(S.browseOpen){ _resetBrowse(); S.browseReturn=null; }
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
  S.tracks=_applyDlList(tracks);
  S.selected=new Set(tracks.map(t=>t.id));
  renderTracks();
  addLog(tracks.length?`Итого: ${tracks.length} треков.`:'Треков не найдено.',tracks.length?'ok':'err');
  const btn=document.getElementById('btnFetch');
  btn.disabled=false; btn.textContent='⬇ Получить треки';
});

window.addEventListener('py:track_status', e=>{
  const{id,status}=e.detail;
  ['tracks','search','wave','playlist_detail','browse'].forEach(src=>{
    const t=_listFor(src).find(x=>x.id===id);
    if(t) t.status=status;
  });
  if(status==='done'){
    const t=['tracks','search','wave','playlist_detail','browse']
      .map(src=>_listFor(src).find(x=>x.id===id)).find(Boolean);
    _rememberDlTrack(t||{id, title:'', artist:''});
    _syncDlMarks();
    updateProgress();
    return;
  }
  updateProgress();
  const row=document.getElementById('row-'+id);
  const tMain=S.tracks.find(x=>x.id===id);
  if(row && tMain) updateRow(row,tMain);
  ['search','wave','playlist_detail','browse'].forEach(src=>_updateExRow(src,id));
  if(S.bigViewOpen && S.playerTrackId===id) _fillBigView();
});

window.addEventListener('py:preview_url', e=>{
  const{track_id,url}=e.detail;
  if(url) S.previewUrls[track_id]=url;
  // Ответ мог прийти уже после следующего переключения — чужой трек не трогаем
  if(S.playerTrackId!==track_id) return;
  const t=_trackFor(S.playerSource, track_id);
  if(t) _loadAndPlay(t,url,S.playerSource);
});
window.addEventListener('py:track_prefetched', e=>{
  const{track_id,url}=e.detail;
  if(!url) return;
  S.previewUrls[track_id]=url;
  if(S.prefetch.id===track_id){
    S.prefetch.url=url;
    _warmAudio(url);
  }
});

window.addEventListener('py:preview_error', e=>{
  addLog('Превью: '+e.detail.msg,'err');
  _clearPlayingUI();
});

window.addEventListener('py:my_playlists', e=>applyMyPlaylists(e.detail||[]));
window.addEventListener('py:downloaded_files', e=>{
  // uid переживает удаление строк, в отличие от индекса в массиве
  S.dlFiles=(e.detail||[]).map((f,i)=>Object.assign({}, f, {uid:'f'+i}));
  // из выбора убираем то, чего на диске уже нет
  const present=new Set(S.dlFiles.map(f=>f.rel_path));
  S.dlSelected=new Set([...S.dlSelected].filter(p=>present.has(p)));
  renderDownloaded(S.dlFiles);
  _rebuildDlMarks(S.dlFiles);
});
window.addEventListener('py:downloaded_ids', e=>{
  const ids=(e.detail||[]).map(String);
  S.dlIds=new Set(ids);
  (S.dlFiles||[]).forEach(f=>{ if(f.track_id) S.dlIds.add(String(f.track_id)); });
  _persistDlMarks();
  _syncDlMarks();
});

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
  refreshStaleCaches(true);
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

  return `<div class="tl-row ${t.status} ${playingRow}" id="row-${t.id}"
    onclick="rowPlay(event,'tracks','${t.id}')">
    <input type="checkbox" class="cb" ${checked} onchange="toggleTrack('${t.id}',this.checked)">
    <span class="tl-num">${t.num}</span>
    <div style="min-width:0">
      <div class="tl-title" title="${esc(t.title)}">${esc(t.title)}</div>
      <div class="tl-sub" title="${esc(t.artist)}">${_artistLinks(t)}</div>
    </div>
    <div class="tl-album" title="${esc(t.album)}">${_albumLink(t)}</div>
    <span class="tl-dur">${t.duration}</span>
    <span class="tl-status s-${t.status}">${statusLabel}</span>
    <button class="iBtn play-btn ${prvCls}" title="Прослушать" onclick="previewTrack('${t.id}')">${playIcon}</button>
    <button class="iBtn ${dlCls}" ${dlDis} title="${t.status==='done'?'Скачан':'Скачать'}" onclick="downloadOne('${t.id}')">${dlIcon}</button>
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
  if(url) S.previewUrls[trackInfo.id]=url;
  _setPlaying(source, trackInfo.id);
  _paintMiniPlayer(trackInfo);
  _warmNowPlaying(trackInfo);
  document.getElementById('player').classList.remove('hidden');
  const audio=document.getElementById('audioEl');
  audio.src=url;
  audio.play().catch(()=>{});
  _schedulePrefetch();
}

/* Если ссылка уже есть — играем сразу, без секундной паузы на API */
function _playTrack(t, source, queue){
  if(!t) return;
  if(source==='wave'){
    S.playingPlaylistUrl='';
    S.playingCardKey='';
    S.pendingAlbumPlay='';
    S.pendingArtistPlay='';
    _paintCardPlayBtns();
  }
  if(queue!==undefined) S.playerQueue=queue;
  document.getElementById('player').classList.remove('hidden');
  document.getElementById('plPlayBtn').textContent='⏳';
  const cached=S.previewUrls[t.id] || (S.prefetch.id===t.id && S.prefetch.url);
  if(cached){
    _loadAndPlay(t, cached, source);
    return;
  }
  _setPlaying(source, t.id);
  _paintMiniPlayer(t);
  _warmNowPlaying(t);
  window.pywebview.api.get_preview_url(t.id);
}

function _peekNext(){
  if(S.playerSource==='downloaded') return null;
  const cur=_currentIdx(), len=_listLen();
  if(cur<0 || len<=1) return null;
  const idx=S.shuffle ? _shuffleIdx(cur) : (cur+1)%len;
  return _queue()[idx] || null;
}
function _schedulePrefetch(){
  if(S.prefetchTimer) clearTimeout(S.prefetchTimer);
  // Даём текущему треку первым занять сеть, потом готовим следующий
  S.prefetchTimer=setTimeout(_prefetchNext, 500);
}
function _prefetchNext(){
  S.prefetchTimer=null;
  const next=_peekNext();
  if(!next || next.id===S.playerTrackId) return;
  if(S.prefetch.id!==next.id){
    _disposePrefetchAudio();
    S.prefetch={id:next.id, url:S.previewUrls[next.id]||null, audio:null};
  }
  _requestLyrics(next.id);
  _prefetchCover(next, false);
  if(S.prefetch.url){ _warmAudio(S.prefetch.url); return; }
  window.pywebview.api.prefetch_track(next.id);
}
function _warmAudio(url){
  if(!url) return;
  try{
    if(S.prefetch.audio && S.prefetch.audio.src===url) return;
    _disposePrefetchAudio();
    const a=new Audio();
    a.preload='auto';
    a.src=url;
    S.prefetch.audio=a;
  }catch(_e){}
}
function _disposePrefetchAudio(){
  if(!S.prefetch.audio) return;
  try{ S.prefetch.audio.removeAttribute('src'); S.prefetch.audio.load(); }catch(_e){}
  S.prefetch.audio=null;
}

/* Текст и большая обложка — сразу с началом трека, не дожидаясь открытия экрана */
function _warmNowPlaying(t){
  if(!t) return;
  if(S.playerSource!=='downloaded') _requestLyrics(t.id);
  _prefetchCover(t, true);
}
function _requestLyrics(trackId){
  if(!trackId) return;
  if(Object.prototype.hasOwnProperty.call(S.lyricsCache, trackId)) return;
  if(S.lyricsPending.has(trackId)) return;
  S.lyricsPending.add(trackId);
  window.pywebview.api.get_lyrics(trackId);
}
function _prefetchCover(t, apply){
  const url=_bigCoverUrl(t,'600x600');
  if(!url) return;
  const pre=new Image();
  pre.crossOrigin='anonymous';
  pre.onload=()=>{
    if(!S.coverColors[url]) _sampleCoverColors(pre, S.coverToken, url, false);
    if(!apply || S.playerTrackId!==t.id) return;
    // Кладём картинку в скрытый img, чтобы при открытии не ждать декодирования
    if(!S.bigViewOpen){
      const img=document.getElementById('bigViewCover');
      const wash=document.getElementById('bvWash');
      if(img && img.getAttribute('src')!==url){
        img.src=url;
        if(wash) wash.style.backgroundImage=`url('${url}')`;
      }
    }
  };
  pre.onerror=()=>{
    const plain=new Image();
    plain.onload=()=>{
      if(!apply || S.playerTrackId!==t.id || S.bigViewOpen) return;
      const img=document.getElementById('bigViewCover');
      if(img && img.getAttribute('src')!==url) img.src=url;
    };
    plain.src=url;
  };
  pre.src=url;
}

/* Название/исполнитель/обложка в мини-плеере; исполнитель кликабелен */
function _paintMiniPlayer(t){
  document.getElementById('plTitle').textContent=t.title||t.name||'—';
  const art=document.getElementById('plArtist');
  if(t.artists && t.artists.length) art.innerHTML=_artistLinks(t);
  else art.textContent=t.artist||'';
  const cover=document.getElementById('plCover');
  if(t.cover_uri){ cover.src=t.cover_uri; cover.style.display=''; }
  else cover.style.display='none';
}

/* Пересобирает строку целиком — только когда изменились её данные (статус, лайк) */
function _refreshRow(source,id){
  if(!source||!id) return;
  if(source==='tracks'){
    const t=S.tracks.find(x=>x.id===id);
    const row=document.getElementById('row-'+id);
    if(t&&row) updateRow(row,t);
  } else if(source==='downloaded'){
    _updateDlRow(id);
  } else {
    _updateExRow(source,id);
  }
}

/*
  Состояние воспроизведения меняется постоянно (плей, пауза, переход), поэтому
  строку здесь не пересобираем, а правим ровно то, что видно: иконку кнопки и
  подсветку строки.
*/
function _rowElement(source,id){
  if(source==='downloaded'){
    const f=S.dlFiles.find(x=>x.rel_path===id);
    return f ? document.getElementById('dlrow-'+f.uid) : null;
  }
  if(source==='tracks') return document.getElementById('row-'+id);
  return document.getElementById('exrow-'+source+'-'+id);
}
function _paintPlaying(source,id){
  const row=_rowElement(source,id);
  if(!row) return;
  const isCur=S.playerSource===source && S.playerTrackId===id;
  const audio=document.getElementById('audioEl');
  const playing=isCur && audio && !audio.paused;
  if(source==='downloaded') row.classList.toggle('dl-playing',isCur);
  else if(source==='tracks') row.classList.toggle('playing-row',isCur);
  const btn=row.querySelector('.play-btn');
  if(!btn) return;
  btn.textContent=playing?'⏸':'▶';
  if(source==='downloaded') btn.title=playing?'Играет':'Воспроизвести';
  else btn.classList.toggle('playing',isCur);
}

/*
  Смена играющего трека: подсветку снимаем со старой строки, ставим на новую.
  queue передают только те, кто начинает воспроизведение нового списка —
  переключение внутри очереди её не трогает.
*/
function _setPlaying(source,id,queue){
  const prevSource=S.playerSource, prevId=S.playerTrackId;
  S.playerSource=source;
  S.playerTrackId=id;
  if(queue!==undefined) S.playerQueue=queue;
  const found=source==='downloaded'
    ? _listFor(source).find(x=>x.rel_path===id || x.id===id)
    : (_listFor(source).find(x=>x.id===id) || (S.playerQueue||[]).find(x=>x.id===id));
  S.playerTrack = found
    ? (source==='downloaded' ? _dlAsTrack(found) : found)
    : (S.playerTrack && S.playerTrack.id===id ? S.playerTrack : null);
  const changed = prevSource!==source || prevId!==id;
  if(changed){
    _paintPlaying(prevSource,prevId);
    // Старый трек нужно остановить сразу же, иначе он продолжает двигать
    // полосу перемотки, пока в шапке уже показан следующий
    _resetPlaybackUI(found || S.playerTrack);
  }
  _paintPlaying(source,id);
  _updateLikeButtons();
  if(S.bigViewOpen) _fillBigView();
}

/* Обнуляет прогресс и показывает длительность нового трека до его загрузки */
function _resetPlaybackUI(t){
  const a=document.getElementById('audioEl');
  a.pause();
  if(a.getAttribute('src')){ a.removeAttribute('src'); a.load(); }
  const dur=(t && t.duration) ? t.duration : fmtTime(t && t.duration_ms ? t.duration_ms/1000 : 0);
  ['plSeek','bvSeek'].forEach(id=>{ const el=document.getElementById(id); if(el) el.value=0; });
  document.getElementById('plTime').textContent=`0:00 / ${dur}`;
  const cur=document.getElementById('bvCur'), tot=document.getElementById('bvDur');
  if(cur) cur.textContent='0:00';
  if(tot) tot.textContent=dur;
}

/* Полная перерисовка — нужна только когда меняется сразу весь набор данных */
function _rerenderActive(){
  renderTracks();
  renderDownloaded(S.dlFiles);
  renderSearchResults();
  if(S.plView==='detail') renderPlaylistDetail();
  if(S.plView==='wave') renderWave();
  if(S.browseOpen) renderBrowse();
  _updateLikeButtons();
  if(S.bigViewOpen) _fillBigView();
}

/* ── Лайки ("Мне нравится") ── */
/*
  Ищем трек в его списке, а если списка уже нет — берём снимок, сделанный при
  запуске воспроизведения. Иначе после перехода в другой плейлист или нового
  поиска играющий трек «терялся», и обложка переставала разворачиваться.
*/
function _dlAsTrack(f){
  if(!f) return null;
  return {
    id:f.rel_path||f.id,
    title:f.title||f.name||'—',
    artist:f.artist||'',
    artists:[],
    album:f.album||'',
    album_id:null,
    cover_uri:f.cover_uri||'',
    cover_uri_tmpl:'',
    duration:f.duration||'',
    duration_ms:f.duration_ms||0,
    local:true,
  };
}
function _trackFor(source,id){
  if(!source||!id) return null;
  if(source==='downloaded'){
    const f=_listFor('downloaded').find(x=>x.rel_path===id || x.id===id);
    return f ? _dlAsTrack(f)
      : (S.playerTrack && S.playerTrack.id===id ? S.playerTrack : null);
  }
  return _listFor(source).find(x=>x.id===id)
    || (S.playerQueue||[]).find(x=>x.id===id)
    || (S.playerTrack && S.playerTrack.id===id ? S.playerTrack : null);
}
function _currentPlayingTrack(){
  return _trackFor(S.playerSource, S.playerTrackId);
}
function _updateLikeButtons(){
  const t=_currentPlayingTrack();
  const liked=!!(t && S.likedIds.has(t.id));
  const id=t?t.id:null;
  // «Пшик» сердечка только когда лайк поставили у того же трека, а не при его смене
  const pop = liked && id===S.likeUiTrackId && !S.likeUiLiked;
  S.likeUiTrackId=id;
  S.likeUiLiked=liked;
  [document.getElementById('plLikeBtn'), document.getElementById('bigViewLikeBtn')].forEach(btn=>{
    if(!btn) return;
    btn.classList.toggle('liked', liked);
    btn.textContent=liked?'♥':'♡';
    btn.style.visibility=(t && S.playerSource!=='downloaded')?'':'hidden';
    if(pop){
      btn.classList.remove('pop');
      void btn.offsetWidth;
      btn.classList.add('pop');
    }
  });
  const add=document.getElementById('plAddBtn');
  if(add) add.style.visibility=(t && S.playerSource!=='downloaded')?'':'hidden';
}
function toggleLike(source,id){
  const t=_listFor(source).find(x=>x.id===id) || _trackFor(source,id);
  if(!t || S.likedPending.has(id)) return;
  const nextLiked=!S.likedIds.has(id);
  S.likedPending.add(id);
  if(nextLiked) S.likedIds.add(id); else S.likedIds.delete(id);

  // Снятый лайк = трека больше нет в «Мне нравится»: убираем строку сразу,
  // не дожидаясь ответа сервера и не перерисовывая весь список
  const dropped = !nextLiked && _dropFromLikedPlaylist(id);
  if(!dropped) _updateExRow(source,id,true);

  _updateLikeButtons();
  window.pywebview.api.toggle_like(id, nextLiked);
}
function toggleLikeCurrent(){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleLike(S.playerSource, t.id);
}

/* Убирает трек из открытого «Мне нравится» с анимацией. true — если убрали. */
function _dropFromLikedPlaylist(id){
  if(S.plDetail.group!=='system') return false;
  const idx=S.plDetail.tracks.findIndex(x=>x.id===id);
  if(idx<0) return false;
  S.likedRemovals[id]={track:S.plDetail.tracks[idx], index:idx, url:S.plDetail.url};
  S.plDetail.tracks.splice(idx,1);
  _finishPlaylistRowRemoval(id);
  return true;
}
function _restoreToLikedPlaylist(id){
  const info=S.likedRemovals[id];
  delete S.likedRemovals[id];
  if(!info || S.plDetail.url!==info.url) return;
  S.plDetail.tracks.splice(Math.min(info.index,S.plDetail.tracks.length),0,info.track);
  _updatePlDetailCount();
  if(S.plView==='detail') renderPlaylistDetail();
}

/* Общий финал удаления строки плейлиста: анимация → перенумерация → счётчик */
function _finishPlaylistRowRemoval(id){
  const after=()=>{
    _renumberList('playlist_detail');
    if(!S.plDetail.tracks.length && S.plView==='detail') renderPlaylistDetail();
  };
  if(document.getElementById('exrow-playlist_detail-'+id)) _animateRowOut('playlist_detail',id,after);
  else after();
  _updatePlDetailCount();
}
function _plDetailVisibleTracks(){
  const q=(S.plTrackQuery||'').trim().toLowerCase();
  const list=S.plDetail.tracks||[];
  if(!q) return list;
  return list.filter(t=>{
    const hay=[t.title,t.artist,t.album,(t.artists||[]).map(a=>a&&a.name).filter(Boolean).join(' ')].join(' ').toLowerCase();
    return hay.includes(q);
  });
}
function onPlTrackSearch(){
  const el=document.getElementById('plTrackSearch');
  S.plTrackQuery=el?el.value:'';
  renderPlaylistDetail();
  _updatePlDetailCount();
}
function _updatePlDetailCount(){
  const el=document.getElementById('plDetailCount');
  if(!el) return;
  const tot=(S.plDetail.tracks||[]).length;
  const q=(S.plTrackQuery||'').trim();
  if(q){
    const vis=_plDetailVisibleTracks().length;
    el.textContent=`${vis} из ${tot}`;
  } else {
    el.textContent=`${tot} треков`;
  }
}

window.addEventListener('py:liked_ids', e=>{
  S.likedIds = new Set(e.detail || []);
  _persistLikedIds();
  _rerenderActive();
});
window.addEventListener('py:like_result', e=>{
  const{track_id,liked,ok,msg}=e.detail;
  S.likedPending.delete(track_id);
  if(liked) S.likedIds.add(track_id); else S.likedIds.delete(track_id);
  if(ok){
    delete S.likedRemovals[track_id];
  } else {
    _restoreToLikedPlaylist(track_id);
    addLog(`✗ Не удалось изменить лайк: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось изменить лайк${msg?': '+esc(msg):''}`});
  }
  if(ok) _persistLikedIds();
  ['search','wave','playlist_detail','browse'].forEach(src=>_updateExRow(src,track_id));
  _updateLikeButtons();
});

/* ── Лайки исполнителей и альбомов (коллекция Яндекса) ── */
function _artistById(id){
  id=String(id||'');
  const top=_browseTop();
  if(top && (top.type==='artist'||top.type==='artist_tracks') && top.id===id && top.info) return top.info;
  return (S.likedArtists||[]).find(a=>String(a.id)===id)
    || (S.searchArtists||[]).find(a=>String(a.id)===id)
    || null;
}
function _albumById(id){
  id=String(id||'');
  const top=_browseTop();
  if(top && top.type==='album' && top.id===id && top.info) return top.info;
  const from=(top && top.albums)||[];
  return from.find(a=>String(a.id)===id)
    || (S.likedAlbums||[]).find(a=>String(a.id)===id)
    || (S.searchAlbums||[]).find(a=>String(a.id)===id)
    || null;
}
function _entityLikeBtn(kind,id,labeled){
  id=String(id||'');
  const liked=kind==='artist'?S.likedArtistIds.has(id):S.likedAlbumIds.has(id);
  const attr=kind==='artist'?'data-like-artist':'data-like-album';
  const fn=kind==='artist'?'toggleArtistLike':'toggleAlbumLike';
  const label=labeled?(liked?'♥ Нравится':'♡ Нравится'):(liked?'♥':'♡');
  const cls=labeled?'btn sm like-btn':'iBtn card-like like-btn';
  return `<button class="${cls}${liked?' liked':''}" ${attr}="${esc(id)}"${labeled?' data-like-label="1"':''}
    title="${liked?'Убрать из любимых':'Нравится'}"
    onclick="event.stopPropagation();${fn}('${esc(id)}')">${label}</button>`;
}
function _paintEntityLikes(){
  document.querySelectorAll('[data-like-artist]').forEach(el=>{
    const liked=S.likedArtistIds.has(el.dataset.likeArtist);
    el.classList.toggle('liked', liked);
    el.textContent=el.dataset.likeLabel?(liked?'♥ Нравится':'♡ Нравится'):(liked?'♥':'♡');
    el.title=liked?'Убрать из любимых':'Нравится';
  });
  document.querySelectorAll('[data-like-album]').forEach(el=>{
    const liked=S.likedAlbumIds.has(el.dataset.likeAlbum);
    el.classList.toggle('liked', liked);
    el.textContent=el.dataset.likeLabel?(liked?'♥ Нравится':'♡ Нравится'):(liked?'♥':'♡');
    el.title=liked?'Убрать из понравившихся':'Нравится';
  });
}
function toggleArtistLike(id){
  id=String(id||'');
  if(!id || S.likedArtistPending.has(id)) return;
  const next=!S.likedArtistIds.has(id);
  S.likedArtistPending.add(id);
  if(next){
    S.likedArtistIds.add(id);
    const a=_artistById(id);
    if(a && !S.likedArtists.some(x=>String(x.id)===id)) S.likedArtists=[a, ...S.likedArtists];
  } else {
    S.likedArtistIds.delete(id);
    S.likedArtists=S.likedArtists.filter(x=>String(x.id)!==id);
  }
  _paintEntityLikes();
  renderLikedArtists();
  _persistLibrary();
  window.pywebview.api.toggle_artist_like(id, next);
}
function toggleAlbumLike(id){
  id=String(id||'');
  if(!id || S.likedAlbumPending.has(id)) return;
  const next=!S.likedAlbumIds.has(id);
  S.likedAlbumPending.add(id);
  if(next){
    S.likedAlbumIds.add(id);
    const al=_albumById(id);
    if(al && !S.likedAlbums.some(x=>String(x.id)===id)) S.likedAlbums=[al, ...S.likedAlbums];
  } else {
    S.likedAlbumIds.delete(id);
    S.likedAlbums=S.likedAlbums.filter(x=>String(x.id)!==id);
  }
  _paintEntityLikes();
  renderLikedAlbums();
  _persistLibrary();
  window.pywebview.api.toggle_album_like(id, next);
}
function _applyLikedLibrary(d){
  const artists=d&&d.artists||[];
  const albums=d&&d.albums||[];
  S.likedArtists=artists;
  S.likedAlbums=albums;
  S.likedArtistIds=new Set(artists.map(a=>String(a.id)).filter(Boolean));
  S.likedAlbumIds=new Set(albums.map(a=>String(a.id)).filter(Boolean));
  _persistLibrary();
  _paintEntityLikes();
  renderLikedArtists();
  renderLikedAlbums();
}
window.addEventListener('py:liked_library', e=>_applyLikedLibrary(e.detail||{}));
window.addEventListener('py:artist_like_result', e=>{
  const{id,liked,ok,msg}=e.detail||{};
  const key=String(id||'');
  S.likedArtistPending.delete(key);
  if(liked) S.likedArtistIds.add(key); else S.likedArtistIds.delete(key);
  if(!liked) S.likedArtists=S.likedArtists.filter(x=>String(x.id)!==key);
  if(!ok){
    addLog(`✗ Не удалось изменить лайк исполнителя: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось сохранить исполнителя${msg?': '+esc(msg):''}`});
  }
  if(ok) _persistLibrary();
  _paintEntityLikes();
  renderLikedArtists();
});
window.addEventListener('py:album_like_result', e=>{
  const{id,liked,ok,msg}=e.detail||{};
  const key=String(id||'');
  S.likedAlbumPending.delete(key);
  if(liked) S.likedAlbumIds.add(key); else S.likedAlbumIds.delete(key);
  if(!liked) S.likedAlbums=S.likedAlbums.filter(x=>String(x.id)!==key);
  if(!ok){
    addLog(`✗ Не удалось изменить лайк альбома: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось сохранить альбом${msg?': '+esc(msg):''}`});
  }
  if(ok) _persistLibrary();
  _paintEntityLikes();
  renderLikedAlbums();
});

/* ── Удаление трека из плейлиста ── */
function removeFromPlaylist(trackId){
  const t=S.plDetail.tracks.find(x=>x.id===trackId);
  if(!t || S.pendingRemovals[trackId]) return;
  showConfirm({
    title:'Удалить трек из плейлиста?',
    text:`«${t.artist} — ${t.title}» будет удалён из плейлиста «${S.plDetail.title}».`,
    okLabel:'Удалить',
    onOk:()=>_doRemoveFromPlaylist(trackId),
  });
}
function _doRemoveFromPlaylist(trackId){
  const idx=S.plDetail.tracks.findIndex(x=>x.id===trackId);
  if(idx<0) return;
  const track=S.plDetail.tracks[idx];
  S.pendingRemovals[trackId]={track, index:idx, url:S.plDetail.url, title:S.plDetail.title};
  S.plDetail.tracks.splice(idx,1);
  _finishPlaylistRowRemoval(trackId);
  window.pywebview.api.remove_from_playlist(S.plDetail.id, trackId);
}
window.addEventListener('py:remove_from_playlist_result', e=>{
  const{ok,track_id,msg}=e.detail;
  const info=S.pendingRemovals[track_id];
  delete S.pendingRemovals[track_id];
  const title=info?info.track.title:'Трек';
  if(ok){
    showToast({kind:'ok', icon:'🗑', message:`«${esc(title)}» удалён из «${esc(info?info.title:'плейлиста')}»`});
    return;
  }
  // Не получилось — возвращаем трек на прежнее место
  if(info && S.plDetail.url===info.url){
    S.plDetail.tracks.splice(Math.min(info.index,S.plDetail.tracks.length),0,info.track);
    _updatePlDetailCount();
    if(S.plView==='detail') renderPlaylistDetail();
  }
  showToast({kind:'err', icon:'✗', message:`Не удалось удалить «${esc(title)}»${msg?': '+esc(msg):''}`});
});

/* ── Полноэкранный просмотр обложки / текста песни ── */
function _bigCoverUrl(t,size){
  if(t.cover_uri_tmpl) return t.cover_uri_tmpl.replace('%%', size);
  return t.cover_uri || '';
}
/*
  Обложку подменяем только когда новая уже раскодирована: если присвоить src
  сразу, картинка на секунду пропадает, и смена трека выглядит рвано.
*/
function _setBigCover(t){
  const img=document.getElementById('bigViewCover');
  const wash=document.getElementById('bvWash');
  const hq=_bigCoverUrl(t,'600x600')||'';
  const lo=t.cover_uri||'';
  const token=++S.coverToken;
  if(!hq && !lo){
    img.removeAttribute('src');
    if(wash) wash.style.backgroundImage='none';
    _paintAurora(null, token);
    return;
  }
  const url=hq||lo;
  if(img.getAttribute('src')===url){
    if(S.coverColors[url]) _paintAurora(S.coverColors[url], token);
    return;
  }
  // Сразу мелкая обложка из мини-плеера — она уже в кэше, без пустого кадра
  if(lo && img.getAttribute('src')!==lo){
    img.src=lo;
    if(wash) wash.style.backgroundImage=`url('${lo}')`;
  }
  const swap=(decoded)=>{
    if(token!==S.coverToken) return;
    img.src=url;
    if(wash) wash.style.backgroundImage=`url('${url}')`;
    img.classList.remove('swap');
    void img.offsetWidth;
    img.classList.add('swap');
    if(S.coverColors[url]) _paintAurora(S.coverColors[url], token);
    else if(decoded) _sampleCoverColors(decoded, token, url);
  };
  if(!hq || hq===lo){
    if(S.coverColors[url]) _paintAurora(S.coverColors[url], token);
    return;
  }
  const pre=new Image();
  pre.crossOrigin='anonymous';
  pre.onload=()=>swap(pre);
  pre.onerror=()=>{
    // CDN без CORS — обложку всё равно покажем, фон перельётся из самой картинки
    const plain=new Image();
    plain.onload=()=>swap(null);
    plain.onerror=()=>swap(null);
    plain.src=url;
  };
  pre.src=url;
}

/* 2–3 самых заметных цвета обложки: по ним рисуются мягкие пятна фона */
function _sampleCoverColors(img, token, url, paint=true){
  try{
    const w=32,h=32;
    const c=document.createElement('canvas');
    c.width=w; c.height=h;
    const ctx=c.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(img,0,0,w,h);
    const {data}=ctx.getImageData(0,0,w,h);
    const buckets=new Map();
    for(let i=0;i<data.length;i+=4){
      const r=data[i],g=data[i+1],b=data[i+2],a=data[i+3];
      if(a<180) continue;
      const mx=Math.max(r,g,b), mn=Math.min(r,g,b);
      if(mx<22 || mn>238) continue;
      const sat=mx?(mx-mn)/mx:0;
      if(sat<0.07 && mx<170) continue;
      const key=((r>>4)<<8)|((g>>4)<<4)|(b>>4);
      let rec=buckets.get(key);
      if(!rec){ rec={r:0,g:0,b:0,n:0,w:0}; buckets.set(key,rec); }
      rec.r+=r; rec.g+=g; rec.b+=b; rec.n++;
      rec.w += 0.35 + sat*1.7 + mx/255*0.25;
    }
    const ranked=[...buckets.values()].map(x=>({
      r:Math.round(x.r/x.n), g:Math.round(x.g/x.n), b:Math.round(x.b/x.n), w:x.w
    })).sort((a,b)=>b.w-a.w);
    const picked=[];
    for(const col of ranked){
      if(picked.every(p=>((p.r-col.r)**2+(p.g-col.g)**2+(p.b-col.b)**2)>4800))
        picked.push(col);
      if(picked.length>=3) break;
    }
    while(picked.length<3) picked.push(picked[picked.length-1]||{r:48,g:42,b:78});
    const colors=picked.map(col=>({
      r:Math.min(255, Math.round(col.r*1.18)),
      g:Math.min(255, Math.round(col.g*1.18)),
      b:Math.min(255, Math.round(col.b*1.18)),
    }));
    S.coverColors[url]=colors;
    if(paint) _paintAurora(colors, token);
  }catch(_e){
    if(paint) _paintAurora(null, token);
  }
}
function _paintAurora(colors, token){
  if(token!=null && token!==S.coverToken) return;
  const cols=colors||[
    {r:72,g:56,b:120},{r:36,g:82,b:140},{r:150,g:64,b:86}
  ];
  const next=S.auroraOn==='A'?'B':'A';
  const el=document.getElementById('bvAurora'+next);
  const prev=document.getElementById('bvAurora'+S.auroraOn);
  if(!el) return;
  el.style.setProperty('--c1',`rgba(${cols[0].r},${cols[0].g},${cols[0].b},.78)`);
  el.style.setProperty('--c2',`rgba(${cols[1].r},${cols[1].g},${cols[1].b},.62)`);
  el.style.setProperty('--c3',`rgba(${cols[2].r},${cols[2].g},${cols[2].b},.55)`);
  if(prev && prev!==el) prev.classList.remove('on');
  el.classList.add('on');
  S.auroraOn=next;
}
function openBigView(){
  const t=_currentPlayingTrack();
  if(!t) return;
  S.bigViewOpen=true;
  const el=document.getElementById('bigView');
  // Отменяем отложенное скрытие: без этого повторное открытие сразу после
  // закрытия получало display:none от «догоняющего» таймера
  if(S.bigViewHideTimer){ clearTimeout(S.bigViewHideTimer); S.bigViewHideTimer=null; }
  el.classList.remove('hidden');
  // Показываем синхронно, через принудительный reflow: с requestAnimationFrame
  // класс мог прийти уже после закрытия и оставить окно в подвешенном виде
  void el.offsetWidth;
  el.classList.add('show');
  _fillBigView();
  playerTimeUpdate();
}
function closeBigView(){
  if(!S.bigViewOpen) return;
  S.bigViewOpen=false;
  const el=document.getElementById('bigView');
  el.classList.remove('show');
  if(S.bigViewHideTimer) clearTimeout(S.bigViewHideTimer);
  S.bigViewHideTimer=setTimeout(()=>{
    S.bigViewHideTimer=null;
    el.classList.add('hidden');
  },300);
}
function _bigViewSourceLabel(){
  switch(S.playerSource){
    case 'playlist_detail': return S.plDetail.title||'Плейлист';
    case 'wave':   return _waveTitle();
    case 'search': return 'Поиск';
    case 'tracks': return 'По ссылке';
    case 'browse': return (_browseTop() && _browseTop().title) || 'Исполнитель';
    case 'downloaded': return 'Скачанные';
    default: return '';
  }
}
function _fillBigView(){
  const t=_currentPlayingTrack();
  if(!t){ closeBigView(); return; }

  // Обложку, текст и заголовки трогаем только при смене трека — иначе картинка
  // моргает на каждом обновлении статуса
  const changed = S.bigViewTrackId!==t.id;
  S.bigViewTrackId=t.id;
  const local=S.playerSource==='downloaded';
  if(changed){
    _setBigCover(t);
    document.getElementById('bigViewTitle').textContent=t.title||'—';
    if(local){
      document.getElementById('bigViewArtist').textContent=t.artist||'';
      document.getElementById('bigViewAlbum').textContent=t.album||'';
    } else {
      document.getElementById('bigViewArtist').innerHTML=_artistLinks(t);
      document.getElementById('bigViewAlbum').innerHTML=_albumLink(t);
      _loadLyricsFor(t.id);
    }
  }

  document.getElementById('bigViewSrc').textContent=_bigViewSourceLabel();

  // В скачанных лайк / плейлист / скачать / Яндекс не имеют смысла
  const tools=document.getElementById('bvDlBtn');
  const st=t.status||'idle';
  if(tools){
    tools.textContent={idle:'⬇',queued:'⏳',downloading:'⏳',done:'✓',error:'↺'}[st]||'⬇';
    tools.className='iBtn '+({done:'done',error:'error'}[st]||'');
    tools.disabled=(st==='downloading'||st==='queued');
  }
  const canRemove = !local && S.playerSource==='playlist_detail' && S.plDetail.editable
    && S.plDetail.tracks.some(x=>x.id===t.id);
  document.getElementById('bvDelBtn').style.display=canRemove?'':'none';
  document.getElementById('bvOpenBtn').style.display=(!local && t.album_id)?'':'none';
  ['bigViewLikeBtn','bvAddBtn','bvDlBtn','bvWaveBtn'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.style.display=local?'none':'';
  });
  const toolsRow=document.querySelector('.bigview-tools');
  if(toolsRow) toolsRow.style.display=local?'none':'';
  const lyricsWrap=document.querySelector('.bigview-lyrics-wrap');
  if(lyricsWrap) lyricsWrap.style.display=local?'none':'';

  // Подсказка «что дальше» по текущей очереди воспроизведения
  const list=_queue();
  const field=_idField(S.playerSource);
  const cur=list.findIndex(x=>x[field]===t.id || x.id===t.id);
  const atEnd=!S.shuffle && cur>=0 && cur===list.length-1 && S.playerSource!=='wave' && S.repeat!=='one';
  const nextT=(!atEnd && cur>=0&&list.length>1)?list[(cur+1)%list.length]:null;
  const nextTitle=nextT?(nextT.title||nextT.name||''):'';
  const nextArtist=nextT?(nextT.artist||''):'';
  document.getElementById('bvNext').innerHTML=
    atEnd?'<b>Далее:</b> 🌊 Моя волна'
    :(nextT?`<b>Далее:</b> ${esc(nextArtist)}${nextArtist?' — ':''}${esc(nextTitle)}`:'');

  _applyModeUI();
  _updatePlayBtn();
}
function bigViewDownload(){
  const t=_currentPlayingTrack();
  if(!t || t.status==='downloading' || t.status==='queued') return;
  if(t.status==='error') t.status='idle';
  window.pywebview.api.start_download([t]);
  t.status='queued';
  _refreshRow(S.playerSource,t.id);
  _fillBigView();
  addLog('В очереди на скачивание: '+t.title,'info');
}
function bigViewAdd(evt){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleAddMenu(evt, S.playerSource, t.id);
}
function bigViewRemove(){
  const t=_currentPlayingTrack();
  if(!t) return;
  removeFromPlaylist(t.id);
}
function bigViewOpenExternal(){
  const t=_currentPlayingTrack();
  if(!t) return;
  const url=t.album_id
    ? `https://music.yandex.ru/album/${t.album_id}/track/${t.id}`
    : `https://music.yandex.ru/track/${t.id}`;
  window.pywebview.api.open_link(url);
}
function _loadLyricsFor(trackId){
  const box=document.getElementById('bigViewLyrics');
  if(!box) return;
  if(Object.prototype.hasOwnProperty.call(S.lyricsCache,trackId)){
    _renderLyrics(trackId);
    return;
  }
  // Не пишем «Загружаем...» — это как раз и давало рывок: пусто → загрузка → текст.
  // Место очищаем, а текст появится сам, часто уже из предзагрузки с началом трека.
  _paintLyrics('muted','', false);
  _requestLyrics(trackId);
}
function _renderLyrics(trackId){
  const box=document.getElementById('bigViewLyrics');
  if(!box || !S.bigViewOpen) return;
  const t=_currentPlayingTrack();
  if(!t || t.id!==trackId) return; // трек уже сменился — не показываем чужой текст
  const text=S.lyricsCache[trackId];
  if(text) _paintLyrics('', text, true);
  else _paintLyrics('muted','Текст песни недоступен для этого трека', false);
}
/* animate — только когда пришёл настоящий текст, не на очистке */
function _paintLyrics(cls,text,animate){
  const box=document.getElementById('bigViewLyrics');
  if(!box) return;
  box.className=('bigview-lyrics '+cls).trim();
  box.textContent=text;
  const wrap=box.parentElement;
  if(wrap) wrap.scrollTop=0;
  if(animate){
    void box.offsetWidth;
    box.classList.add('fade-swap');
  }
}
window.addEventListener('py:lyrics_result', e=>{
  const{track_id,text}=e.detail;
  S.lyricsPending.delete(track_id);
  S.lyricsCache[track_id]=text||null;
  _renderLyrics(track_id);
});

/* ── Универсальные превью / скачивание для поиска / волны / плейлиста ── */
/* Клик по строке — плей/пауза; кнопки, галочки и ссылки не перехватываем */
function rowPlay(evt,source,id){
  if(evt.target.closest('button, input, .lnk, a')) return;
  previewGeneric(source,id);
}
function rowPlayDownloaded(evt,uid){
  if(evt.target.closest('button, input, .lnk, a, .dl-cover, .dl-cover-ph')) return;
  playDownloaded(uid);
}
function miniPlayerAdd(evt){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleAddMenu(evt, S.playerSource, t.id);
}
function previewGeneric(source,id){
  const list=_listFor(source);
  const t=list.find(x=>x.id===id);
  if(!t) return;
  const audio=document.getElementById('audioEl');
  if(S.playerTrackId===id && S.playerSource===source){
    if(audio.paused) audio.play(); else audio.pause();
    _updatePlayBtn();
    return;
  }
  if(source==='playlist_detail'){
    S.playingPlaylistUrl=S.plDetail.url||'';
    _setPlayingCard('pl', S.plDetail.url||'');
  } else if(source==='browse'){
    S.playingPlaylistUrl='';
    const top=_browseTop();
    if(top && top.type==='album') _setPlayingCard('album', top.id);
    else if(top && (top.type==='artist'||top.type==='artist_tracks')) _setPlayingCard('artist', top.id);
    else _setPlayingCard('', '');
  } else if(source!=='wave'){
    S.playingPlaylistUrl='';
    _setPlayingCard('', '');
  }
  _playTrack(t, source, list);
}
function downloadGeneric(source,id){
  const list=_listFor(source);
  const t=list.find(x=>x.id===id);
  if(!t||t.status==='downloading'||t.status==='queued') return;
  if(t.status==='error') t.status='idle';
  window.pywebview.api.start_download([t]);
  t.status='queued';
  _updateExRow(source,id);
  addLog('В очереди на скачивание: '+t.title,'info');
}
function exRowHTML(t,source){
  const isPlaying=S.playerTrackId===t.id && S.playerSource===source;
  let playIcon='▶';
  if(isPlaying){
    const audio=document.getElementById('audioEl');
    if(audio && !audio.paused) playIcon='⏸';
  }
  const prvCls=isPlaying?'playing':'';
  const st=t.status||'idle';
  const dlIcon={idle:'⬇',queued:'⏳',downloading:'⏳',done:'✓',error:'↺'}[st]||'⬇';
  const dlCls={done:'done',error:'error'}[st]||'';
  const dlDis=(st==='downloading'||st==='queued')?'disabled':'';
  const liked=S.likedIds.has(t.id);
  const likeCls=liked?'liked':'';
  const selectable=_selectable(source);
  const removable=source==='playlist_detail' && S.plDetail.editable;
  const cbHtml=selectable
    ?`<input type="checkbox" class="cb" ${_selSet(source).has(t.id)?'checked':''} onchange="toggleSel('${source}','${t.id}',this.checked)">`
    :'';
  const rmHtml=removable
    ?`<button class="iBtn del-btn" title="Удалить из плейлиста" onclick="removeFromPlaylist('${t.id}')">🗑</button>`
    :'';
  return `<div class="ex-row ${selectable?'selectable':''} ${removable?'removable':''} ${st}" id="exrow-${source}-${t.id}"
    onclick="rowPlay(event,'${source}','${t.id}')">
    ${cbHtml}
    <span class="tl-num">${t.num||''}</span>
    <div style="min-width:0">
      <div class="tl-title" title="${esc(t.title)}">${esc(t.title)}</div>
      <div class="tl-sub" title="${esc(t.artist)}">${_artistLinks(t)}</div>
    </div>
    <div class="tl-album" title="${esc(t.album)}">${_albumLink(t)}</div>
    <span class="tl-dur">${t.duration||''}</span>
    <button class="iBtn play-btn ${prvCls}" title="Прослушать" onclick="previewGeneric('${source}','${t.id}')">${playIcon}</button>
    <button class="iBtn" title="Волна по треку" onclick="startTrackWave(event,'${source}','${t.id}')">🌊</button>
    <button class="iBtn like-btn ${likeCls}" title="Мне нравится" onclick="toggleLike('${source}','${t.id}')">${liked?'♥':'♡'}</button>
    <button class="iBtn" title="Добавить в плейлист" onclick="toggleAddMenu(event,'${source}','${t.id}')">➕</button>
    <button class="iBtn ${dlCls}" ${dlDis} title="${st==='done'?'Скачан':'Скачать'}" onclick="downloadGeneric('${source}','${t.id}')">${dlIcon}</button>
    ${rmHtml}
  </div>`;
}
function _updateExRow(source,id,popLike){
  const list=_listFor(source);
  const t=list.find(x=>x.id===id);
  const el=document.getElementById('exrow-'+source+'-'+id);
  if(t && el){
    const tmp=document.createElement('div');
    tmp.innerHTML=exRowHTML(t,source);
    const fresh=tmp.firstElementChild;
    el.replaceWith(fresh);
    if(popLike){
      const btn=fresh.querySelector('.like-btn');
      if(btn) btn.classList.add('pop');
    }
  }
}

/* ── Добавление трека в плейлист (выпадающее меню) ── */
function toggleAddMenu(evt,source,id){
  evt.stopPropagation();
  closeAddMenu();
  // В плейлист можно добавить трек только если он создан самим пользователем —
  // системные (Мне нравится), умные (Плейлист дня и т.п.) и чужие понравившиеся не редактируются
  const own = S.myPlaylistsFlat.filter(pl=>pl.group==='created');
  const rect=evt.currentTarget.getBoundingClientRect();
  const menu=document.createElement('div');
  menu.id='addMenu';
  menu.style.cssText=`position:fixed;top:${rect.bottom+4}px;left:${Math.max(4,rect.left-170)}px;
    background:var(--surface3);border:1px solid var(--border2);border-radius:var(--rsm);
    box-shadow:0 4px 16px rgba(0,0,0,.4);z-index:600;min-width:200px;max-height:280px;
    overflow-y:auto;padding:4px;animation:modalIn .18s var(--ease);`;
  const create=`<div class="add-menu-item" style="padding:7px 10px;font-size:12px;cursor:pointer;border-radius:4px;
      white-space:nowrap;color:var(--accent);font-weight:600"
      onclick="promptCreatePlaylist('${esc(source)}','${esc(id)}')">＋ Новый плейлист</div>`;
  const list=own.map(pl=>`
    <div class="add-menu-item" style="padding:7px 10px;font-size:12px;cursor:pointer;border-radius:4px;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
      onclick="addToPlaylist('${pl.id}','${source}','${id}')">${esc(pl.title)}</div>
  `).join('');
  menu.innerHTML=create+(own.length?`<div style="height:1px;background:var(--border);margin:4px 2px"></div>${list}`:'');
  document.body.appendChild(menu);
  setTimeout(()=>document.addEventListener('click',closeAddMenu,{once:true}),0);
}
function closeAddMenu(){
  const m=document.getElementById('addMenu');
  if(m) m.remove();
}
function addToPlaylist(playlistId,source,trackId){
  closeAddMenu();
  const list=_listFor(source);
  const t=list.find(x=>x.id===trackId);
  if(!t) return;
  const pl=S.myPlaylistsFlat.find(p=>String(p.id)===String(playlistId));
  const key=trackId+'|'+playlistId;
  S.pendingAdds[key]={playlist:pl, trackTitle:t.title};
  window.pywebview.api.add_to_playlist(playlistId, t.id, t.album_id||null);
  addLog(`Добавляем «${t.title}» в плейлист «${pl?pl.title:''}»...`,'info');
}
window.addEventListener('py:add_to_playlist_result', e=>{
  const{ok,track_id,playlist_id,msg}=e.detail;
  const key=track_id+'|'+playlist_id;
  const info=S.pendingAdds[key]||{};
  delete S.pendingAdds[key];
  const plTitle=info.playlist?info.playlist.title:'плейлист';
  const trackTitle=info.trackTitle||'Трек';
  if(ok){
    if(info.playlist){
      info.playlist.count=(info.playlist.count||0)+1;
      const pl=S.myPlaylistsFlat.find(p=>String(p.id)===String(playlist_id) && p.group==='created');
      if(pl) pl.count=(pl.count||0)+1;
      CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
      if(info.playlist.url) delete S.plTracksTs[info.playlist.url];
      if(S.plView==='grid') _drawLibraryGrid(true);
    }
    addLog(`✓ «${trackTitle}» добавлен в «${plTitle}»`,'ok');
    showToast({
      kind:'ok',
      icon:'✓',
      message:`«${esc(trackTitle)}» добавлен в плейлист «${esc(plTitle)}»`,
      actionLabel: info.playlist ? 'Открыть плейлист' : null,
      onAction: info.playlist ? ()=>{
        const navBtns=document.querySelectorAll('.nav-item');
        showPage('playlists', navBtns[1]);
        openPlaylist(info.playlist);
      } : null,
    });
  } else {
    addLog(`✗ Не удалось добавить «${trackTitle}»: ${msg||''}`,'err');
    showToast({
      kind:'err',
      icon:'✗',
      message:`Не удалось добавить «${esc(trackTitle)}»${msg?': '+esc(msg):''}`,
    });
  }
});

/* ── Всплывающие уведомления (тосты) ── */
function _getToastContainer(){
  let c=document.getElementById('toastContainer');
  if(!c){
    c=document.createElement('div');
    c.id='toastContainer';
    c.className='toast-container';
    document.body.appendChild(c);
  }
  return c;
}
function showToast({kind='info', icon='', message='', actionLabel=null, onAction=null, duration=5000}){
  const container=_getToastContainer();
  const el=document.createElement('div');
  el.className=`toast toast-${kind}`;
  el.innerHTML=`
    <span class="toast-icon">${icon}</span>
    <span class="toast-msg">${message}</span>
    ${actionLabel?`<button class="toast-action">${esc(actionLabel)}</button>`:''}
    <span class="toast-close" title="Закрыть">✕</span>
  `;
  if(actionLabel && onAction){
    el.querySelector('.toast-action').onclick=()=>{ onAction(); _removeToast(el); };
  }
  el.querySelector('.toast-close').onclick=()=>_removeToast(el);
  container.appendChild(el);
  requestAnimationFrame(()=>el.classList.add('show'));
  let timer=setTimeout(()=>_removeToast(el),duration);
  el.addEventListener('mouseenter',()=>clearTimeout(timer));
  el.addEventListener('mouseleave',()=>{ timer=setTimeout(()=>_removeToast(el),duration); });
  return el;
}
function _removeToast(el){
  if(!el||!el.parentNode) return;
  el.classList.remove('show');
  el.classList.add('hide');
  setTimeout(()=>el.remove(),300);
}

/* ── Диалог подтверждения (для необратимых действий) ── */
function showConfirm({title='Подтверждение', text='', okLabel='Удалить', danger=true, onOk=null}){
  S.confirmAction=onOk;
  document.getElementById('confirmTitle').textContent=title;
  document.getElementById('confirmText').textContent=text;
  const ok=document.getElementById('confirmOk');
  ok.textContent=okLabel;
  ok.className='btn '+(danger?'danger':'accent');
  document.getElementById('confirmModal').classList.remove('hidden');
  setTimeout(()=>ok.focus(),0);
}
function closeConfirm(){
  document.getElementById('confirmModal').classList.add('hidden');
  S.confirmAction=null;
}
function showPrompt({title='Новый плейлист', text='', placeholder='Название', okLabel='Создать', onOk=null}){
  S.promptAction=onOk;
  document.getElementById('promptTitle').textContent=title;
  const p=document.getElementById('promptText');
  if(text){ p.style.display=''; p.textContent=text; } else p.style.display='none';
  const inp=document.getElementById('promptInput');
  inp.placeholder=placeholder;
  inp.value='';
  document.getElementById('promptOk').textContent=okLabel;
  document.getElementById('promptModal').classList.remove('hidden');
  setTimeout(()=>inp.focus(),0);
}
function closePrompt(){
  document.getElementById('promptModal').classList.add('hidden');
  S.promptAction=null;
}
function acceptPrompt(){
  const name=(document.getElementById('promptInput').value||'').trim();
  const cb=S.promptAction;
  if(!name){ document.getElementById('promptInput').focus(); return; }
  closePrompt();
  if(cb) cb(name);
}
function _promptOpen(){
  return !document.getElementById('promptModal').classList.contains('hidden');
}
function promptCreatePlaylist(source, trackId){
  closeAddMenu();
  showPrompt({
    title:'Новый плейлист',
    text: trackId ? 'Плейлист появится в Яндекс.Музыке, трек добавится сразу.' : 'Плейлист появится в Яндекс.Музыке и в списке «Созданные мной».',
    placeholder:'Название плейлиста',
    okLabel: trackId ? 'Создать и добавить' : 'Создать',
    onOk:(name)=>{
      S.pendingPlaylistCreate={title:name, source:source||'', trackId:trackId||''};
      window.pywebview.api.create_playlist(name);
    },
  });
}
function _rememberPlaylist(pl){
  if(!pl || !pl.id) return;
  S.myPlaylistsFlat=S.myPlaylistsFlat.filter(p=>!(p.group==='created' && String(p.id)===String(pl.id)));
  S.myPlaylistsFlat=[pl, ...S.myPlaylistsFlat];
  CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  if(S.plView==='grid') _drawLibraryGrid(true);
}
window.addEventListener('py:playlist_created', e=>{
  const{ok,playlist,msg}=e.detail||{};
  const pending=S.pendingPlaylistCreate;
  S.pendingPlaylistCreate=null;
  if(!ok || !playlist){
    showToast({kind:'err', icon:'✗', message:`Не удалось создать плейлист${msg?': '+esc(msg):''}`});
    return;
  }
  _rememberPlaylist(playlist);
  addLog(`✓ Создан плейлист «${playlist.title}»`,'ok');
  if(pending && pending.trackId){
    addToPlaylist(playlist.id, pending.source, pending.trackId);
    return;
  }
  showToast({kind:'ok', icon:'✓', message:`Плейлист «${esc(playlist.title)}» создан`});
});
function confirmDeletePlaylist(key){
  const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===key);
  if(!pl || pl.group!=='created') return;
  showConfirm({
    title:'Удалить плейлист?',
    text:`«${pl.title}» будет удалён из Яндекс.Музыки. Это нельзя отменить.`,
    okLabel:'Удалить',
    onOk:()=>_deletePlaylist(pl),
  });
}
function confirmDeleteCurrentPlaylist(){
  if(!S.plDetail.editable || !S.plDetail.id) return;
  confirmDeletePlaylist(_plKey({group:S.plDetail.group, id:S.plDetail.id}));
}
function _deletePlaylist(pl){
  if(!pl) return;
  const key=String(pl.id);
  if(S.pendingPlaylistDeletes[key]) return;
  S.pendingPlaylistDeletes[key]=pl;
  S.myPlaylistsFlat=S.myPlaylistsFlat.filter(p=>!(p.group==='created' && String(p.id)===key));
  CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  if(pl.url){
    delete S.plTracksCache[pl.url];
    delete S.plTracksTs[pl.url];
    _persistPlTracks();
  }
  if(S.plView==='detail' && String(S.plDetail.id)===key) closePlaylistDetail();
  if(S.plView==='grid') _drawLibraryGrid(true);
  window.pywebview.api.delete_playlist(pl.id);
}
window.addEventListener('py:playlist_deleted', e=>{
  const{ok,playlist_id,msg}=e.detail||{};
  const key=String(playlist_id||'');
  const pl=S.pendingPlaylistDeletes[key];
  delete S.pendingPlaylistDeletes[key];
  if(ok){
    const title=pl?pl.title:'Плейлист';
    showToast({kind:'ok', icon:'🗑', message:`Плейлист «${esc(title)}» удалён`});
    return;
  }
  if(pl) _rememberPlaylist(pl);
  showToast({kind:'err', icon:'✗', message:`Не удалось удалить плейлист${msg?': '+esc(msg):''}`});
});
function acceptConfirm(){
  const cb=S.confirmAction;
  closeConfirm();
  if(cb) cb();
}
function _confirmOpen(){
  return !document.getElementById('confirmModal').classList.contains('hidden');
}

function _clearPlayingUI(){
  document.querySelectorAll('.iBtn.playing').forEach(b=>{b.classList.remove('playing');b.textContent='▶';});
}

/* ── Список треков по источнику (для унификации плеера) ── */
function _listFor(source){
  switch(source){
    case 'tracks': return S.tracks;
    case 'downloaded': return S.dlFiles;
    case 'search': return S.searchResults;
    case 'wave': return S.waveTracks;
    case 'playlist_detail': return S.plDetail.tracks;
    case 'browse': return (_browseTop() || {}).tracks || [];
    default: return [];
  }
}
function _idField(source){ return source==='downloaded' ? 'rel_path' : 'id'; }

/*
  Очередь — это список, из которого запустили трек. Держим её отдельно: иначе
  новый поиск или переход на страницу альбома подменяли бы «следующий трек».
*/
function _queue(){
  if(S.playerSource==='downloaded') return S.dlFiles;
  return S.playerQueue || _listFor(S.playerSource);
}

/* ── Текущий индекс и получение следующего трека ── */
function _currentIdx(){
  const field=_idField(S.playerSource);
  return _queue().findIndex(x=>x[field]===S.playerTrackId);
}
function _listLen(){
  return _queue().length;
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
  if(S.playerSource==='downloaded'){
    const f=S.dlFiles[idx];
    if(!f) return;
    playLocalFile(f);
    return;
  }
  const t=_queue()[idx];
  if(!t) return;
  _playTrack(t, S.playerSource);
}

/* ── Публичные кнопки ── */
function previewTrack(id){
  previewGeneric('tracks', id);
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
  _advanceQueue(false);
}
function playerEnded(){
  if(S.repeat==='one'){ document.getElementById('audioEl').play(); return; }
  _advanceQueue(true);
}
function _advanceQueue(fromEnd){
  const cur=_currentIdx();
  const len=_listLen();
  if(cur<0||!len){
    if(fromEnd && S.playerSource!=='wave') _startMyWaveAuto();
    else _updatePlayBtn();
    return;
  }
  if(S.playerSource==='wave'){
    if(!S.waveLoading && cur>=len-3) loadMoreWave();
    if(S.shuffle){ _goToIndex(_shuffleIdx(cur)); return; }
    if(cur<len-1){ _goToIndex(cur+1); return; }
    S.pendingWavePlay='next';
    loadMoreWave();
    return;
  }
  if(!S.shuffle && cur>=len-1){
    _startMyWaveAuto();
    return;
  }
  const idx=S.shuffle?_shuffleIdx(cur):(cur+1)%len;
  _goToIndex(idx);
}
function playerClose(){
  const a=document.getElementById('audioEl');
  a.pause();
  // removeAttribute + load(), а не src='': иначе поток к файлу остаётся открытым
  a.removeAttribute('src');
  a.load();
  document.getElementById('player').classList.add('hidden');
  const prevSource=S.playerSource, prevId=S.playerTrackId;
  S.playerTrackId=null;
  S.playerTrack=null;
  S.playerQueue=null;
  if(S.prefetchTimer){ clearTimeout(S.prefetchTimer); S.prefetchTimer=null; }
  _disposePrefetchAudio();
  S.prefetch={id:null,url:null,audio:null};
  closeBigView();
  S.playingPlaylistUrl='';
  S.playingCardKey='';
  S.pendingAlbumPlay='';
  S.pendingArtistPlay='';
  _paintPlaying(prevSource,prevId);
  _paintCardPlayBtns();
  _updateLikeButtons();
}
function playerCanPlay(){
  const a=document.getElementById('audioEl');
  if(!a || !a.getAttribute('src')) return;
  document.getElementById('plPlayBtn').textContent='⏸';
  _schedulePrefetch();
}
function playerError(){
  const a=document.getElementById('audioEl');
  if(!a || !a.getAttribute('src')) return;  // сброс src при переключении — не ошибка
  addLog('Ошибка воспроизведения','err');
  _updatePlayBtn();
}
function playerTimeUpdate(){
  const a=document.getElementById('audioEl');
  // После сброса src браузер ещё шлёт timeupdate со старыми числами — их игнорируем.
  // Пока метаданные нового файла не приехали, оставляем длительность из карточки трека.
  if(!a || !a.getAttribute('src') || !a.duration) return;
  const pct=a.currentTime/a.duration*100;
  document.getElementById('plTime').textContent=`${fmtTime(a.currentTime)} / ${fmtTime(a.duration)}`;
  document.getElementById('plSeek').value=pct.toFixed(1);
  if(!S.bigViewOpen) return;
  document.getElementById('bvCur').textContent=fmtTime(a.currentTime);
  document.getElementById('bvDur').textContent=fmtTime(a.duration);
  const seek=document.getElementById('bvSeek');
  // не дёргаем ползунок, пока пользователь его тащит
  if(document.activeElement!==seek) seek.value=pct.toFixed(1);
}
function _updatePlayBtn(){
  const audio=document.getElementById('audioEl');
  const paused=audio?audio.paused:true;
  document.getElementById('plPlayBtn').textContent=paused?'▶':'⏸';
  const bigBtn=document.getElementById('bigViewPlayBtn');
  if(bigBtn) bigBtn.textContent=paused?'▶':'⏸';
  _paintPlaying(S.playerSource,S.playerTrackId);
  _paintPlaylistPlayBtns();
}

/* ── Режимы ── */
function toggleShuffle(){
  S.shuffle=!S.shuffle;
  STORE.set('ym_shuffle',S.shuffle);
  _applyModeUI();
}
function cycleRepeat(){
  S.repeat = S.repeat==='one' ? 'none' : 'one';
  STORE.set('ym_repeat',S.repeat);
  _applyModeUI();
}
function _applyModeUI(){
  const isOne=S.repeat==='one';
  ['btnShuffle','bvShuffle'].forEach(id=>{
    const b=document.getElementById(id);
    if(!b) return;
    b.classList.toggle('active-mode',S.shuffle);
    b.title=S.shuffle?'Перемешать (вкл)':'Перемешать';
  });
  ['btnRepeat','bvRepeat'].forEach(id=>{
    const b=document.getElementById(id);
    if(!b) return;
    b.classList.toggle('active-mode',isOne);
    b.title=isOne?'Повтор трека (вкл)':'Повтор трека';
  });
}

/* ═══════════════════════════════════════════════════════════════════
   MY PLAYLISTS
═══════════════════════════════════════════════════════════════════ */
/* Переключение между сеткой плейлистов / деталями / волной с плавным появлением */
function _showPlSubView(which){
  const map={grid:'plGridWrap', detail:'plDetailWrap', wave:'plWaveWrap'};
  Object.entries(map).forEach(([key,id])=>{
    const el=document.getElementById(id);
    if(!el) return;
    if(key===which){
      el.style.display='flex';
      el.classList.remove('fade-in');
      void el.offsetWidth; // форсируем reflow, чтобы анимация перезапустилась
      el.classList.add('fade-in');
    } else {
      el.style.display='none';
    }
  });
}
function openPlaylistsList(){
  S.plView='grid';
  _showPlSubView('grid');
  loadMyPlaylists();
}
/*
  Плейлисты тянутся из сети несколько секунд, поэтому сразу показываем то, что
  было в прошлый раз, а свежий ответ дописываем поверх — без перерисовки сетки,
  если ничего не изменилось.
*/
function loadMyPlaylists(force){
  if(!S.plRendered){
    if(S.myPlaylistsFlat.length) renderMyPlaylists(S.myPlaylistsFlat);
    else document.getElementById('plGrid').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем...</p></div>`;
  }
  if(!force && CACHE.fresh('ym_pl_cache')){
    const hint=document.getElementById('plRefreshHint');
    if(hint) hint.textContent='';
    return;
  }
  const hint=document.getElementById('plRefreshHint');
  if(hint) hint.textContent='обновляем…';
  window.pywebview.api.get_my_playlists();
}
function applyMyPlaylists(pls){
  const hint=document.getElementById('plRefreshHint');
  if(hint) hint.textContent='';
  if(pls.length) CACHE.write('ym_pl_cache', pls);
  if(S.plRendered && _patchPlaylists(pls)) return;
  renderMyPlaylists(pls);
}

const PL_GROUPS=[
  ['system', '❤️ Моя музыка'],
  ['smart',  '✨ Умные плейлисты'],
  ['created','👤 Созданные мной'],
  ['liked',  '📌 Понравившиеся плейлисты'],
];
/* Плейлисты по категориям, в том же порядке, в котором лягут карточки */
function _groupPlaylists(pls){
  const buckets=new Map(PL_GROUPS.map(([key])=>[key,[]]));
  (pls||[]).forEach(pl=>{
    const g=(pl.group && buckets.has(pl.group)) ? pl.group : 'created';
    buckets.get(g).push(pl);
  });
  return PL_GROUPS
    .map(([key,title])=>({key, title, items:buckets.get(key)}))
    .filter(sec=>sec.items.length);
}
function _plKey(pl){ return pl.group+':'+pl.id; }

/* Точечно правит существующие карточки. false — состав изменился, нужна перерисовка */
function _libSectionTitle(title){
  return `<div class="lib-sec" style="grid-column:1/-1;padding:12px 6px 4px;font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--border);margin:4px 0;">
    ${title}</div>`;
}
function _artistCardHTML(a){
  return `
    <div class="pl-card artist-card" data-kind="artist" onclick="openArtist('${esc(a.id)}')" title="${esc(a.name)}">
      ${a.cover
        ?`<img class="pl-cover" src="${esc(a.cover)}" alt="" onerror="this.style.display='none'">`
        :`<div class="pl-cover-ph">🎤</div>`}
      <button class="iBtn card-play" data-play-key="artist:${esc(a.id)}" title="Играть все треки"
        onclick="event.stopPropagation();playArtistCard('${esc(a.id)}')">▶</button>
      ${_entityLikeBtn('artist', a.id, false)}
      <div class="pl-info">
        <div class="pl-name">${esc(a.name)}</div>
        <div class="pl-count">${a.tracks_count?`${a.tracks_count} треков`:'исполнитель'}</div>
      </div>
    </div>`;
}
function openArtistsPage(){
  renderLikedArtists();
  loadLikedLibrary(false);
}
function openAlbumsPage(){
  renderLikedAlbums();
  loadLikedLibrary(false);
}
function loadLikedLibrary(force){
  if(!force && CACHE.fresh('ym_liked_library')) return;
  window.pywebview.api.get_liked_library();
}
function renderLikedArtists(){
  const grid=document.getElementById('artistsGrid');
  const count=document.getElementById('artistsCount');
  if(count) count.textContent=S.likedArtists.length?`${S.likedArtists.length}`:'';
  if(!grid) return;
  if(!S.likedArtists.length){
    grid.innerHTML=`<div class="empty"><span class="empty-icon">🎤</span><p>Нет любимых исполнителей — нажмите «Нравится» на странице артиста</p></div>`;
    return;
  }
  const keep=grid.scrollTop;
  grid.innerHTML=`<div class="pl-grid" style="padding-bottom:20px;">${S.likedArtists.map(a=>_artistCardHTML(a)).join('')}</div>`;
  grid.scrollTop=keep;
  _paintCardPlayBtns();
}
function renderLikedAlbums(){
  const grid=document.getElementById('albumsGrid');
  const count=document.getElementById('albumsCount');
  if(count) count.textContent=S.likedAlbums.length?`${S.likedAlbums.length}`:'';
  if(!grid) return;
  if(!S.likedAlbums.length){
    grid.innerHTML=`<div class="empty"><span class="empty-icon">💿</span><p>Нет понравившихся альбомов — нажмите «Нравится» на странице альбома</p></div>`;
    return;
  }
  const keep=grid.scrollTop;
  grid.innerHTML=`<div class="pl-grid" style="padding-bottom:20px;">${S.likedAlbums.map(al=>_albumCardHTML(al)).join('')}</div>`;
  grid.scrollTop=keep;
  _paintCardPlayBtns();
}
function _drawLibraryGrid(keepPlaylists){
  const grid=document.getElementById('plGrid');
  if(!grid) return;
  const keep=grid.scrollTop;
  const pls=S.myPlaylistsFlat||[];
  const groups=_groupPlaylists(pls);
  if(!groups.length){
    S.plRendered=false;
    grid.innerHTML=`<div class="empty"><span class="empty-icon">📋</span><p>Плейлистов нет — создайте свой или войдите в аккаунт</p></div>`;
    return;
  }
  const plsHtml=groups.map(sec=>`
    ${_libSectionTitle(sec.title)}
    ${sec.items.map(pl=>`
      <div class="pl-card" data-kind="pl" data-key="${esc(_plKey(pl))}" onclick="openPlaylistByKey('${esc(_plKey(pl))}')" title="Открыть плейлист">
        ${pl.cover
          ?`<img class="pl-cover" src="${esc(pl.cover)}" alt="" onerror="this.style.display='none'">`
          :`<div class="pl-cover-ph">🎵</div>`}
        <button class="iBtn card-play" data-play-key="pl:${esc(pl.url)}" title="Играть"
          onclick="event.stopPropagation();playPlaylistCard('${esc(_plKey(pl))}')">▶</button>
        ${pl.group==='created'
          ?`<button class="iBtn card-del del-btn" title="Удалить плейлист"
              onclick="event.stopPropagation();confirmDeletePlaylist('${esc(_plKey(pl))}')">🗑</button>`
          :''}
        <div class="pl-info">
          <div class="pl-name">${esc(pl.title)}</div>
          <div class="pl-count">${pl.count} треков</div>
        </div>
      </div>`).join('')}
  `).join('');
  grid.innerHTML=`<div class="pl-grid" style="padding-bottom:20px;">${plsHtml}</div>`;
  S.plRendered=true;
  if(!keepPlaylists) _playListEnter(grid.firstElementChild);
  grid.scrollTop=keep;
  _paintPlaylistPlayBtns();
}
function _patchPlaylists(pls){
  const cards=document.querySelectorAll('#plGrid .pl-card[data-kind="pl"]');
  const flat=_groupPlaylists(pls).flatMap(sec=>sec.items);
  if(cards.length!==flat.length) return false;
  for(let i=0;i<flat.length;i++){
    if(cards[i].dataset.key!==_plKey(flat[i])) return false;
  }
  S.myPlaylistsFlat=pls;
  flat.forEach((pl,i)=>{
    const card=cards[i];
    const name=card.querySelector('.pl-name');
    const count=card.querySelector('.pl-count');
    const img=card.querySelector('.pl-cover');
    const countText=`${pl.count} треков`;
    if(name && name.textContent!==pl.title) name.textContent=pl.title;
    if(count && count.textContent!==countText) count.textContent=countText;
    if(img && pl.cover && img.getAttribute('src')!==pl.cover) img.src=pl.cover;
  });
  return true;
}

function renderMyPlaylists(pls){
  S.myPlaylistsFlat = pls || [];
  _drawLibraryGrid(false);
}
function openPlaylistByKey(key){
  const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===key);
  if(pl) openPlaylist(pl);
}
function playPlaylistCard(key){
  const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===key);
  if(!pl) return;
  if(S.playingCardKey==='pl:'+pl.url){
    playerToggle();
    return;
  }
  const cached=S.plTracksCache[pl.url];
  if(cached && cached.length){
    _startPlaylistPlayback(pl, cached);
    return;
  }
  S.pendingPlaylistPlay=pl;
  _paintCardPlayBtns();
  window.pywebview.api.open_playlist(pl.url);
}
function _startPlaylistPlayback(pl, tracks){
  if(!pl || !tracks || !tracks.length) return;
  S.playingPlaylistUrl=pl.url;
  _setPlayingCard('pl', pl.url);
  _playTrack(tracks[0], 'playlist_detail', tracks);
}
function _setPlayingCard(kind, id){
  S.playingCardKey=(kind && id) ? kind+':'+id : '';
  if(kind!=='pl') S.playingPlaylistUrl='';
  if(kind!=='album') S.pendingAlbumPlay='';
  if(kind!=='artist') S.pendingArtistPlay='';
  _paintCardPlayBtns();
}
function _paintCardPlayBtns(){
  const audio=document.getElementById('audioEl');
  const paused=!audio || audio.paused;
  document.querySelectorAll('.card-play[data-play-key]').forEach(btn=>{
    const key=btn.dataset.playKey;
    const pending=(S.pendingAlbumPlay && key==='album:'+S.pendingAlbumPlay)
      || (S.pendingArtistPlay && key==='artist:'+S.pendingArtistPlay)
      || (S.pendingPlaylistPlay && key==='pl:'+S.pendingPlaylistPlay.url);
    const on=S.playingCardKey===key;
    btn.classList.toggle('on', !!(pending || (on && !paused)));
    btn.textContent=pending?'⏳':((on && !paused)?'⏸':'▶');
  });
}
function _paintPlaylistPlayBtns(){ _paintCardPlayBtns(); }

function playAlbumCard(id){
  id=String(id||'');
  if(!id) return;
  if(S.playingCardKey==='album:'+id){ playerToggle(); return; }
  const cached=S.browseCache['album:'+id];
  if(cached && cached.tracks && cached.tracks.length){
    _startAlbumPlayback(id, cached.tracks);
    return;
  }
  S.pendingAlbumPlay=id;
  _paintCardPlayBtns();
  window.pywebview.api.open_album(id);
}
function _startAlbumPlayback(id, tracks){
  const list=_applyDlList((tracks||[]).slice());
  if(!list.length) return;
  S.pendingAlbumPlay='';
  S.playingPlaylistUrl='';
  _setPlayingCard('album', id);
  _playTrack(list[0], 'browse', list);
}

function playArtistCard(id){
  id=String(id||'');
  if(!id) return;
  if(S.playingCardKey==='artist:'+id){ playerToggle(); return; }
  const cached=S.browseCache['artist_tracks:'+id];
  if(cached && cached.tracks && cached.tracks.length){
    _startArtistPlayback(id, cached.tracks, !!cached.has_more, cached.page||0);
    return;
  }
  S.pendingArtistPlay=id;
  _paintCardPlayBtns();
  window.pywebview.api.open_artist_tracks(id, 0);
}
function _startArtistPlayback(id, tracks, hasMore, page){
  const list=_applyDlList((tracks||[]).slice());
  if(!list.length) return;
  S.pendingArtistPlay='';
  S.playingPlaylistUrl='';
  _setPlayingCard('artist', id);
  _playTrack(list[0], 'browse', list);
  if(hasMore) window.pywebview.api.open_artist_tracks(id, (page||0)+1);
}
function _appendArtistPlayback(id, tracks, hasMore, page){
  if(S.playingCardKey!=='artist:'+id) return;
  const extra=_applyDlList(tracks||[]);
  if(!extra.length){
    if(hasMore) window.pywebview.api.open_artist_tracks(id, (page||0)+1);
    return;
  }
  const q=S.playerQueue || [];
  const have=new Set(q.map(t=>t.id));
  extra.forEach(t=>{ if(!have.has(t.id)) q.push(t); });
  q.forEach((t,i)=>t.num=i+1);
  S.playerQueue=q;
  if(S.playerSource==='browse') S.playerQueue=q;
  if(hasMore) window.pywebview.api.open_artist_tracks(id, (page||0)+1);
}

/* Открытие плейлиста внутри приложения (вместо передачи ссылки в поле URL) */
function openPlaylist(pl){
  if(!pl) return;
  S.plView='detail';
  // Отдельная кнопка удаления — только для своих плейлистов. В «Мне нравится»
  // роль удаления играет само сердечко: снял лайк — трек ушёл из плейлиста.
  const group=pl.group||'';
  S.plDetail={
    url:pl.url, title:pl.title, tracks:[], id:pl.id, group,
    editable:(group==='created'),
  };
  S.pendingRemovals={};
  S.likedRemovals={};
  S.plTrackQuery='';
  const qel=document.getElementById('plTrackSearch');
  if(qel) qel.value='';
  _clearSel('playlist_detail');
  _showPlSubView('detail');
  document.getElementById('plDetailTitle').textContent=pl.title;
  const delBtn=document.getElementById('btnPlDelete');
  if(delBtn) delBtn.style.display=S.plDetail.editable?'':'none';

  // Уже открытый однажды плейлист показываем из кэша сразу, не заставляя ждать сеть
  const cached=S.plTracksCache[pl.url];
  if(cached && cached.length){
    _applyDlList(cached);
    S.plDetail.tracks=cached;
    _updatePlDetailCount();
    renderPlaylistDetail();
    const ts=S.plTracksTs[pl.url]||0;
    if(ts && Date.now()-ts<CACHE.TTL) return;
  } else {
    document.getElementById('plDetailCount').textContent='Загрузка...';
    document.getElementById('plDetailBody').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем треки...</p></div>`;
  }
  window.pywebview.api.open_playlist(pl.url);
}
function closePlaylistDetail(){
  S.plView='grid';
  _showPlSubView('grid');
}
window.addEventListener('py:playlist_tracks', e=>{
  const{url,tracks}=e.detail;
  const fresh=_applyDlList(tracks||[]);
  S.plTracksCache[url]=fresh;
  S.plTracksTs[url]=Date.now();
  _persistPlTracks();
  if(S.pendingPlaylistPlay && S.pendingPlaylistPlay.url===url){
    const pl=S.pendingPlaylistPlay;
    S.pendingPlaylistPlay=null;
    if(fresh.length) _startPlaylistPlayback(pl, fresh);
  }
  if(S.plView!=='detail'||S.plDetail.url!==url) return;
  // Состав не изменился — оставляем DOM и статусы скачивания нетронутыми
  const prev=S.plDetail.tracks||[];
  if(prev.length===fresh.length && prev.every((t,i)=>t.id===fresh[i].id)){
    _updatePlDetailCount();
    return;
  }
  S.plDetail.tracks=fresh;
  _clearSel('playlist_detail');
  _updatePlDetailCount();
  renderPlaylistDetail();
  _playListEnter(document.getElementById('plDetailBody'));
});
function renderPlaylistDetail(){
  const body=document.getElementById('plDetailBody');
  if(!body) return;
  if(!S.plDetail.tracks.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🎵</span><p>Треков нет или не удалось загрузить</p></div>`;
    return;
  }
  const visible=_plDetailVisibleTracks();
  if(!visible.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🔍</span><p>В плейлисте нет треков по запросу «${esc(S.plTrackQuery.trim())}»</p></div>`;
    _updateSelBtn('playlist_detail');
    return;
  }
  const keepScroll=body.scrollTop;
  body.innerHTML=visible.map(t=>exRowHTML(t,'playlist_detail')).join('');
  body.scrollTop=keepScroll;
  _updateSelBtn('playlist_detail');
}
function downloadAllPlaylistDetail(){
  if(!S.plDetail.tracks.length) return;
  window.pywebview.api.start_download(S.plDetail.tracks);
  S.plDetail.tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  renderPlaylistDetail();
  addLog(`В очереди: ${S.plDetail.tracks.length} треков из плейлиста «${S.plDetail.title}»`,'info');
}

/* Дополнительная функция: добавить ссылку плейлиста в старую вкладку «По ссылке» */
function addPlaylistUrl(url){
  if(!url) return;
  const navBtns=document.querySelectorAll('.nav-item');
  showPage('download', navBtns[navBtns.length-1]);
  if(!S.urls.includes(url)){ S.urls.push(url); STORE.set('ym_urls',S.urls); renderUrlTags(); }
  addLog('Добавлен плейлист: '+url.slice(0,60),'ok');
}

/* ═══════════════════════════════════════════════════════════════════
   МОЯ ВОЛНА
═══════════════════════════════════════════════════════════════════ */
function _waveTitle(){
  if(S.waveStation && S.waveStation.startsWith('track:')){
    return S.waveSeedTitle ? `🌊 Волна · ${S.waveSeedTitle}` : '🌊 Волна по треку';
  }
  return '🌊 Моя волна';
}
function _paintWaveTitle(){
  const el=document.getElementById('waveTitle');
  if(el) el.textContent=_waveTitle();
}
function _goPlaylistsWave(){
  const nav=document.querySelectorAll('.nav-item')[1];
  showPage('playlists', nav);
  S.plView='wave';
  _showPlSubView('wave');
}
function startTrackWave(evt,source,id){
  if(evt) evt.stopPropagation();
  const t=_trackFor(source,id) || _listFor(source).find(x=>x.id===id);
  if(!t || t.local) return;
  _openWaveStation('track:'+t.id, t);
}
function startTrackWaveCurrent(){
  const t=_currentPlayingTrack();
  if(!t || S.playerSource==='downloaded') return;
  startTrackWave(null, S.playerSource, t.id);
}
function _startMyWaveAuto(){
  addLog('Список закончился — включаем Мою волну','info');
  S.playingPlaylistUrl='';
  S.playingCardKey='';
  S.pendingAlbumPlay='';
  S.pendingArtistPlay='';
  _paintCardPlayBtns();
  S.pendingWavePlay=true;
  S.waveSeedTitle='';
  S.waveStation='user:onyourwave';
  S.waveTracks=[];
  S.waveSeenIds=[];
  S.waveLoading=true;
  _paintWaveTitle();
  window.pywebview.api.start_wave('');
}
function _openWaveStation(station, seed){
  S.waveStation=station||'user:onyourwave';
  S.waveSeedTitle=seed?((seed.artist?seed.artist+' — ':'')+(seed.title||'')):'';
  S.waveTracks=[];
  S.waveSeenIds=[];
  S.sel.wave=new Set();
  S.waveLoading=true;
  S.pendingWavePlay=seed?'seed':true;
  _goPlaylistsWave();
  _paintWaveTitle();
  const body=document.getElementById('waveBody');
  if(body) body.innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Запускаем волну...</p></div>`;
  _updateWaveBtns();
  if(seed) _playTrack(seed, 'wave', [seed]);
  window.pywebview.api.start_wave(S.waveStation);
}
function openWave(){
  S.plView='wave';
  _showPlSubView('wave');
  _paintWaveTitle();
  if(!S.waveTracks.length){
    document.getElementById('waveBody').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Запускаем волну...</p></div>`;
    S.waveSeenIds=[];
    S.waveStation='user:onyourwave';
    S.waveSeedTitle='';
    S.sel.wave=new Set();
    S.waveLoading=true;
    S.pendingWavePlay=true;
    _updateWaveBtns();
    window.pywebview.api.start_wave('');
  } else {
    renderWave();
  }
}
function closeWave(){
  S.plView='grid';
  _showPlSubView('grid');
}
function loadMoreWave(){
  if(S.waveLoading) return;
  S.waveLoading=true;
  _updateWaveBtns();
  window.pywebview.api.wave_next(S.waveSeenIds, S.waveTracks.length+1, S.waveStation);
  addLog('Загружаем ещё треки волны...','info');
}
function resetWave(){
  S.waveTracks=[];
  S.waveSeenIds=[];
  S.sel.wave=new Set();
  S.waveLoading=true;
  S.pendingWavePlay=true;
  _updateWaveBtns();
  _paintWaveTitle();
  document.getElementById('waveBody').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Перезапускаем волну...</p></div>`;
  window.pywebview.api.start_wave(S.waveStation||'');
}
function _updateWaveBtns(){
  const more=document.getElementById('btnWaveMore');
  if(more){
    more.disabled=S.waveLoading;
    more.textContent=S.waveLoading?'⏳ Загрузка...':'▶ Ещё треки';
  }
  const cnt=document.getElementById('waveCount');
  if(cnt) cnt.textContent=S.waveTracks.length?`${S.waveTracks.length} треков`:'';
}
window.addEventListener('py:wave_tracks', e=>{
  const{tracks,seen,append,station}=e.detail;
  const incoming=tracks||[];
  S.waveLoading=false;
  if(station) S.waveStation=station;
  _paintWaveTitle();

  const playMode=S.pendingWavePlay;
  S.pendingWavePlay=false;
  let fresh=incoming;

  if(append){
    const have=new Set(S.waveTracks.map(t=>t.id));
    fresh=_applyDlList(incoming.filter(t=>!have.has(t.id)));
    fresh.forEach(t=>S.waveTracks.push(t));
    S.waveTracks.forEach((t,i)=>t.num=i+1);
    if(!fresh.length) addLog('Новых треков в волне не нашлось','err');
  } else {
    const seed=S.playerSource==='wave' && S.playerTrack && playMode==='seed' ? S.playerTrack : null;
    S.waveTracks=_applyDlList(incoming.slice());
    if(seed && !S.waveTracks.some(t=>t.id===seed.id)) S.waveTracks.unshift(seed);
    S.waveTracks.forEach((t,i)=>t.num=i+1);
  }

  S.waveSeenIds=seen||S.waveSeenIds;
  if(S.playerSource==='wave') S.playerQueue=S.waveTracks;
  _updateWaveBtns();
  if(S.plView==='wave') renderWave();

  if(playMode==='next' && fresh.length){
    _playTrack(fresh[0], 'wave', S.waveTracks);
  } else if(playMode==='seed'){
    S.playerSource='wave';
    S.playerQueue=S.waveTracks;
  } else if(playMode && S.waveTracks.length){
    _playTrack(S.waveTracks[0], 'wave', S.waveTracks);
  }
  // Следующую порцию тянем сразу, не дожидаясь конца списка
  if(!append && incoming.length){
    setTimeout(()=>{ if(!S.waveLoading) loadMoreWave(); }, 200);
  }
});
function renderWave(){
  const body=document.getElementById('waveBody');
  if(!body) return;
  if(!S.waveTracks.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🌊</span><p>${S.waveLoading?'Загружаем...':'Не удалось загрузить волну — нужна авторизация'}</p></div>`;
    return;
  }
  const keepScroll=body.scrollTop;
  body.innerHTML=S.waveTracks.map(t=>exRowHTML(t,'wave')).join('')
    +`<div style="padding:10px;text-align:center;color:var(--hint);font-size:11px">
        ${S.waveLoading?'⏳ Подгружаем ещё...':'Прокрутите вниз или нажмите «Ещё треки»'}
      </div>`;
  body.scrollTop=keepScroll;  // не теряем позицию при подгрузке
  _updateWaveBtns();
  _updateSelBtn('wave');
  // Автоподгрузка при прокрутке до конца списка
  if(!body.dataset.scrollBound){
    body.dataset.scrollBound='1';
    body.addEventListener('scroll',()=>{
      if(S.plView!=='wave'||S.waveLoading) return;
      if(body.scrollTop+body.clientHeight>=body.scrollHeight-60) loadMoreWave();
    });
  }
}
function downloadAllWave(){
  if(!S.waveTracks.length) return;
  window.pywebview.api.start_download(S.waveTracks);
  S.waveTracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  renderWave();
  addLog(`В очереди: ${S.waveTracks.length} треков из волны`,'info');
}

/* ═══════════════════════════════════════════════════════════════════
   ВЫБОР ТРЕКОВ ДЛЯ СКАЧИВАНИЯ (волна / плейлист / исполнитель / альбом)
═══════════════════════════════════════════════════════════════════ */
const SELECTABLE_SOURCES=['wave','playlist_detail','browse'];
const SEL_BTN_ID={wave:'btnWaveDownloadSel', playlist_detail:'btnPlDownloadSel', browse:'btnBrowseDownloadSel'};
function _selectable(source){ return SELECTABLE_SOURCES.includes(source); }
function _selSet(source){ return S.sel[source] || (S.sel[source]=new Set()); }
function _clearSel(source){ S.sel[source]=new Set(); _updateSelBtn(source); }

function toggleSel(source,id,checked){
  const set=_selSet(source);
  if(checked) set.add(id); else set.delete(id);
  _updateSelBtn(source);
}
/* Отмечаем чекбоксы на месте — перерисовывать весь список ради галочек незачем */
function selectAllIn(source,v){
  const list=source==='playlist_detail'?_plDetailVisibleTracks():_listFor(source);
  S.sel[source]= v ? new Set(list.map(t=>t.id)) : new Set();
  list.forEach(t=>{
    const row=document.getElementById('exrow-'+source+'-'+t.id);
    const cb=row&&row.querySelector('.cb');
    if(cb) cb.checked=v;
  });
  _updateSelBtn(source);
}
function _updateSelBtn(source){
  const btn=document.getElementById(SEL_BTN_ID[source]);
  if(!btn) return;
  const n=_selSet(source).size;
  btn.style.display = n>0 ? '' : 'none';
  btn.textContent = `⬇ Скачать выбранные (${n})`;
}
function downloadSelected(source){
  const set=_selSet(source);
  const tracks=_listFor(source).filter(t=>set.has(t.id));
  if(!tracks.length) return;
  window.pywebview.api.start_download(tracks);
  tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  _clearSel(source);
  tracks.forEach(t=>_updateExRow(source,t.id));
  addLog(`В очереди: ${tracks.length} выбранных трек(ов)`,'info');
}

/* ═══════════════════════════════════════════════════════════════════
   СТРАНИЦЫ ИСПОЛНИТЕЛЯ И АЛЬБОМА
   Отдельный слой поверх интерфейса со своим стеком переходов: открыть
   исполнителя можно откуда угодно, а «Назад» вернёт ровно туда, где были.
═══════════════════════════════════════════════════════════════════ */
function _browseTop(){ return S.browseStack[S.browseStack.length-1] || null; }

function openArtist(id,title){ _browsePush('artist', id, title||'Исполнитель'); }
function openAlbum(id,title){ _browsePush('album', id, title||'Альбом'); }
function openArtistTracks(id,title){
  const top=_browseTop();
  const name=(top && top.info && top.info.name) || title || 'Исполнитель';
  _browsePush('artist_tracks', id || (top && top.id), 'Все треки · '+name);
}

function _browsePush(type,id,title){
  if(!id) return;
  id=String(id);
  const top=_browseTop();
  if(top){
    if(top.type===type && top.id===id) return;   // уже на этой странице
    // Переход с альбома на его же исполнителя — это возврат, а не новый шаг
    const prev=S.browseStack[S.browseStack.length-2];
    if(prev && prev.type===type && prev.id===id){ browseBack(); return; }
    top.scroll=document.getElementById('browseBody').scrollTop;
  }
  if(S.bigViewOpen) closeBigView();
  const cached=S.browseCache[type+':'+id];
  const entry={type, id, title, tracks:[], albums:[], info:null, loading:!cached,
    error:'', scroll:0, page:0, hasMore:false, total:0, loadingMore:false};
  if(type==='artist_tracks' && top && top.id===id && top.info) entry.info=top.info;
  if(cached){
    if(type==='artist_tracks') _browseFillTracks(entry,cached);
    else _browseFill(entry,cached);
  }
  S.browseStack.push(entry);
  _clearSel('browse');
  _openBrowseView();
  renderBrowse();
  const key=type+':'+id;
  const fresh=cached && S.browseCacheTs[key] && (Date.now()-S.browseCacheTs[key]<CACHE.TTL);
  if(fresh && type!=='artist_tracks') return;
  if(type==='artist') window.pywebview.api.open_artist(id);
  else if(type==='album') window.pywebview.api.open_album(id);
  else if(type==='artist_tracks') window.pywebview.api.open_artist_tracks(id, 0);
}
function _browseFill(entry,d){
  entry.loading=false;
  entry.error='';
  entry.tracks=_applyDlList(d.tracks||[]);
  entry.albums=d.albums||[];
  entry.info=d.artist||d.album||null;
  if(entry.info) entry.title=entry.info.name||entry.info.title||entry.title;
}
function _browseFillTracks(entry,d){
  entry.loading=false;
  entry.error='';
  entry.tracks=_applyDlList(d.tracks||[]);
  entry.page=d.page||0;
  entry.hasMore=!!d.has_more;
  entry.total=d.total||entry.tracks.length;
  if(d.artist) entry.info=d.artist;
}
function _browseReceive(type,d){
  if(!d) return;
  const id=String(d.id);
  if(d.ok){
    S.browseCache[type+':'+id]=d;
    S.browseCacheTs[type+':'+id]=Date.now();
    _persistBrowseCache();
  }
  if(type==='album' && S.pendingAlbumPlay===id){
    S.pendingAlbumPlay='';
    if(d.ok && (d.tracks||[]).length) _startAlbumPlayback(id, d.tracks);
    else _paintCardPlayBtns();
  }
  let topChanged=false;
  S.browseStack.forEach((en,i)=>{
    if(en.type!==type || en.id!==id) return;
    if(d.ok) _browseFill(en,d);
    else { en.loading=false; if(!en.tracks.length) en.error=d.msg||'Не удалось загрузить'; }
    if(i===S.browseStack.length-1) topChanged=true;
  });
  if(topChanged && S.browseOpen) renderBrowse();
}
window.addEventListener('py:artist_page', e=>_browseReceive('artist', e.detail));
window.addEventListener('py:album_page',  e=>_browseReceive('album',  e.detail));
window.addEventListener('py:artist_tracks_page', e=>{
  const d=e.detail||{};
  const id=String(d.id||'');
  const page=d.page||0;
  let topChanged=false;
  S.browseStack.forEach((en,i)=>{
    if(en.type!=='artist_tracks' || en.id!==id) return;
    if(!d.ok){
      en.loading=false; en.loadingMore=false;
      if(!en.tracks.length) en.error=d.msg||'Не удалось загрузить';
    } else if(page===0){
      _browseFillTracks(en,d);
      S.browseCache['artist_tracks:'+id]=Object.assign({}, d, {tracks:en.tracks.slice()});
    } else {
      const have=new Set(en.tracks.map(t=>t.id));
      _applyDlList(d.tracks||[]).forEach(t=>{ if(!have.has(t.id)) en.tracks.push(t); });
      en.page=d.page||en.page;
      en.hasMore=!!d.has_more;
      en.total=d.total||en.tracks.length;
      en.loadingMore=false;
      S.browseCache['artist_tracks:'+id]=Object.assign({}, d, {tracks:en.tracks.slice(), page:en.page, has_more:en.hasMore});
    }
    if(i===S.browseStack.length-1) topChanged=true;
  });
  if(d.ok && !S.browseStack.some(en=>en.type==='artist_tracks' && en.id===id)){
    const prev=S.browseCache['artist_tracks:'+id];
    const have=new Set(((prev && prev.tracks) || []).map(t=>t.id));
    const merged=((prev && prev.tracks) || []).slice();
    _applyDlList(d.tracks||[]).forEach(t=>{ if(!have.has(t.id)) merged.push(t); });
    S.browseCache['artist_tracks:'+id]=Object.assign({}, d, {
      tracks:merged, page, has_more:!!d.has_more,
    });
  }
  if(S.pendingArtistPlay===id){
    if(d.ok && (d.tracks||[]).length) _startArtistPlayback(id, d.tracks, !!d.has_more, page);
    else { S.pendingArtistPlay=''; _paintCardPlayBtns(); }
  } else if(d.ok && S.playingCardKey==='artist:'+id && page>0){
    _appendArtistPlayback(id, d.tracks, !!d.has_more, page);
  }
  if(topChanged && S.browseOpen){
    const body=document.getElementById('browseBody');
    const keep=body?body.scrollTop:0;
    renderBrowse();
    if(body) body.scrollTop=keep;
  }
});

/* Показывает страницу, запомнив, куда вернуться по «Назад» */
function _openBrowseView(){
  if(!S.browseOpen){
    const active=document.querySelector('.page.active');
    S.browseReturn=active?active.id:'page-search';
    S.browseOpen=true;
  }
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById('page-browse');
  void el.offsetWidth;   // форсируем reflow, иначе появление будет без анимации
  el.classList.add('active');
}
function browseBack(){
  S.browseStack.pop();
  if(!S.browseStack.length){ closeBrowse(); return; }
  _clearSel('browse');
  renderBrowse();
  document.getElementById('browseBody').scrollTop=_browseTop().scroll||0;
}
function browseGoTo(i){
  if(i<0 || i>=S.browseStack.length-1) return;
  S.browseStack.length=i+1;
  _clearSel('browse');
  renderBrowse();
}
function closeBrowse(){
  if(!S.browseOpen) return;
  _resetBrowse();
  document.getElementById('page-browse').classList.remove('active');
  const back=document.getElementById(S.browseReturn||'page-search');
  if(back) back.classList.add('active');
  S.browseReturn=null;
}
function _resetBrowse(){
  S.browseOpen=false;
  S.browseStack=[];
  _clearSel('browse');
}

function renderBrowse(){
  const en=_browseTop();
  if(!en) return;
  document.getElementById('browseBack').textContent=S.browseStack.length>1?'← Назад':'← Закрыть';
  document.getElementById('browseCrumb').innerHTML=S.browseStack.map((x,i)=>{
    const fallback={artist:'Исполнитель', album:'Альбом', artist_tracks:'Все треки'}[x.type]||'';
    const label=esc(x.title||fallback);
    return i===S.browseStack.length-1
      ? `<b>${label}</b>`
      : `<span class="lnk" onclick="browseGoTo(${i})">${label}</span>`;
  }).join('<span class="br-sep">›</span>');

  const body=document.getElementById('browseBody');
  if(en.loading){
    body.innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем...</p></div>`;
  } else if(en.error){
    body.innerHTML=`<div class="empty"><span class="empty-icon">✗</span><p>${esc(en.error)}</p></div>`;
  } else {
    body.innerHTML=en.type==='artist'?_artistPageHTML(en)
      : en.type==='artist_tracks'?_artistTracksPageHTML(en)
      : _albumPageHTML(en);
    _playListEnter(body.querySelector('.br-list'));
    _bindArtistTracksScroll(body);
  }
  _updateSelBtn('browse');
  _paintCardPlayBtns();
}

function _browseHeroCover(url,ph){
  return url
    ? `<img class="br-hero-cover" src="${esc(url)}" alt="" onerror="this.style.display='none'">`
    : `<div class="br-hero-cover br-hero-ph">${ph}</div>`;
}
function _artistPageHTML(en){
  const a=en.info||{};
  const parts=[];
  if(en.tracks.length) parts.push(`${Math.min(en.tracks.length,10)} популярных`);
  if(a.tracks_count) parts.push(`${a.tracks_count} треков`);
  if(en.albums.length) parts.push(`${en.albums.length} альбомов`);
  return `
    <div class="br-hero">
      ${_browseHeroCover(a.cover,'🎤')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Исполнитель</div>
        <div class="br-hero-title">${esc(a.name||en.title)}</div>
        <div class="br-hero-sub">${parts.join(' · ')}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('artist', en.id, true)}
          <button class="btn accent sm" onclick="playArtistCard('${esc(en.id)}')">▶ Играть все</button>
          ${en.tracks.length?`<button class="btn sm" onclick="browseDownloadAll()">⬇ Скачать треки (${en.tracks.length})</button>`:''}
          <button class="btn sm ghost" onclick="window.pywebview.api.open_link('https://music.yandex.ru/artist/${esc(en.id)}')">🔗 В Яндекс.Музыке</button>
        </div>
      </div>
    </div>
    ${en.tracks.length?`
      <div class="br-sec">Популярные треки</div>
      <div class="br-list">${en.tracks.slice(0,10).map(t=>exRowHTML(t,'browse')).join('')}
        ${_artistShowAllBtn(en)}
      </div>`:''}
    ${en.albums.length?`
      <div class="br-sec">Альбомы</div>
      <div class="pl-grid">${en.albums.map(al=>_albumCardHTML(al)).join('')}</div>`:''}
  `;
}
function _artistShowAllBtn(en){
  const total=(en.info && en.info.tracks_count) || 0;
  if(total<=10 && en.tracks.length<10) return '';
  const extra=total>10 ? ` · ${total}` : '';
  return `<div class="br-more">
    <button class="btn sm" onclick="event.stopPropagation();openArtistTracks('${esc(en.id)}')">Показать все${extra}</button>
  </div>`;
}
function _artistTracksPageHTML(en){
  const a=en.info||{};
  const total=en.total || a.tracks_count || en.tracks.length;
  const more=en.hasMore
    ? `<div class="br-more"><button class="btn sm" id="btnArtistMore" onclick="loadMoreArtistTracks()" ${en.loadingMore?'disabled':''}>
        ${en.loadingMore?'⏳ Загрузка...':'Показать ещё'}
      </button></div>` : '';
  return `
    <div class="br-hero">
      ${_browseHeroCover(a.cover,'🎤')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Все треки</div>
        <div class="br-hero-title">${esc(a.name||en.title||'Исполнитель')}</div>
        <div class="br-hero-sub">${total?`${total} треков`:''}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('artist', en.id, true)}
          ${en.tracks.length?`<button class="btn accent sm" onclick="playArtistCard('${esc(en.id)}')">▶ Играть все</button>`:''}
          ${en.tracks.length?`<button class="btn sm" onclick="browseDownloadAll()">⬇ Скачать все (${en.tracks.length})</button>`:''}
        </div>
      </div>
    </div>
    ${en.tracks.length
      ? `<div class="br-list">${en.tracks.map(t=>exRowHTML(t,'browse')).join('')}${more}</div>`
      : `<div class="empty"><span class="empty-icon">${en.loading?'⏳':'🎵'}</span><p>${en.loading?'Загружаем...':'Треки недоступны'}</p></div>`}
  `;
}
function loadMoreArtistTracks(){
  const en=_browseTop();
  if(!en || en.type!=='artist_tracks' || en.loadingMore || !en.hasMore) return;
  en.loadingMore=true;
  const btn=document.getElementById('btnArtistMore');
  if(btn){ btn.disabled=true; btn.textContent='⏳ Загрузка...'; }
  window.pywebview.api.open_artist_tracks(en.id, (en.page||0)+1);
}
function _bindArtistTracksScroll(body){
  if(!body || body.dataset.artistScroll) return;
  body.dataset.artistScroll='1';
  body.addEventListener('scroll',()=>{
    const top=_browseTop();
    if(!top || top.type!=='artist_tracks' || top.loadingMore || !top.hasMore) return;
    if(body.scrollTop+body.clientHeight>=body.scrollHeight-90) loadMoreArtistTracks();
  });
}
function _albumPageHTML(en){
  const al=en.info||{};
  const parts=[];
  if(al.year) parts.push(esc(al.year));
  if(en.tracks.length) parts.push(`${en.tracks.length} треков`);
  if(al.genre) parts.push(esc(al.genre));
  const artists=(al.artists||[]).filter(x=>x&&x.name).map(x=>x.id
    ?`<span class="lnk" onclick="openArtist('${esc(x.id)}')">${esc(x.name)}</span>`
    :esc(x.name)).join(', ');
  return `
    <div class="br-hero">
      ${_browseHeroCover(al.cover,'💿')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Альбом</div>
        <div class="br-hero-title">${esc(al.title||en.title)}</div>
        <div class="br-hero-sub">${artists||''}</div>
        <div class="br-hero-sub">${parts.join(' · ')}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('album', en.id, true)}
          ${en.tracks.length?`<button class="btn accent sm" onclick="playAlbumCard('${esc(en.id)}')">▶ Играть</button>`:''}
          ${en.tracks.length?`<button class="btn sm" onclick="browseDownloadAll()">⬇ Скачать альбом (${en.tracks.length})</button>`:''}
          <button class="btn sm ghost" onclick="window.pywebview.api.open_link('https://music.yandex.ru/album/${esc(en.id)}')">🔗 В Яндекс.Музыке</button>
        </div>
      </div>
    </div>
    ${en.tracks.length?`<div class="br-list">${en.tracks.map(t=>exRowHTML(t,'browse')).join('')}</div>`
      :`<div class="empty"><span class="empty-icon">🎵</span><p>Треки недоступны</p></div>`}
  `;
}
function _albumCardHTML(al){
  const sub=[al.year, al.track_count?`${al.track_count} треков`:''].filter(Boolean).join(' · ');
  const artists=(al.artists||[]).map(x=>x&&x.name).filter(Boolean).join(', ');
  return `
    <div class="pl-card" data-kind="album" onclick="openAlbum('${esc(al.id)}')" title="${esc(al.title)}">
      ${al.cover
        ?`<img class="pl-cover" src="${esc(al.cover)}" alt="" onerror="this.style.display='none'">`
        :`<div class="pl-cover-ph">💿</div>`}
      <button class="iBtn card-play" data-play-key="album:${esc(al.id)}" title="Играть альбом"
        onclick="event.stopPropagation();playAlbumCard('${esc(al.id)}')">▶</button>
      ${_entityLikeBtn('album', al.id, false)}
      <div class="pl-info">
        <div class="pl-name">${esc(al.title)}</div>
        <div class="pl-count">${esc(artists||sub)}</div>
      </div>
    </div>`;
}
function browseDownloadAll(){
  const en=_browseTop();
  if(!en || !en.tracks.length) return;
  window.pywebview.api.start_download(en.tracks);
  en.tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  en.tracks.forEach(t=>_updateExRow('browse',t.id));
  addLog(`В очереди: ${en.tracks.length} треков — ${en.title}`,'info');
}

/* ═══════════════════════════════════════════════════════════════════
   ПОИСК
   Печать в поле сразу идёт в API (с паузой 200–400 мс). Ответы помечаются
   номером запроса: кто печатает быстрее сети, тот не увидит устаревшую выдачу.
═══════════════════════════════════════════════════════════════════ */
function onSearchInput(){
  const q=document.getElementById('searchInput').value.trim();
  if(S.searchTimer) clearTimeout(S.searchTimer);
  if(!q){ _clearSearch(); return; }
  if(q.length<2){
    document.getElementById('searchHint').textContent='Ещё буква — и начнём искать';
    return;
  }
  document.getElementById('searchHint').textContent='ищем…';
  // Короткие запросы чаще опечатки — ждём чуть дольше, чтобы не дёргать API
  S.searchTimer=setTimeout(()=>_runSearch(q,true), q.length<3?380:220);
}
function doSearch(){
  if(S.searchTimer){ clearTimeout(S.searchTimer); S.searchTimer=null; }
  const q=document.getElementById('searchInput').value.trim();
  if(!q){addLog('Введите поисковый запрос','err');return;}
  _runSearch(q,false);
}
function _runSearch(q, live){
  S.searchDone=true;
  const seq=++S.searchSeq;
  const body=document.getElementById('searchBody');
  const have=S.searchResults.length||S.searchArtists.length||S.searchAlbums.length;
  if(!live || !have){
    body.innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Ищем «${esc(q)}»...</p></div>`;
  }
  document.getElementById('searchHint').textContent='ищем…';
  window.pywebview.api.search_tracks(q, seq);
}
function _clearSearch(){
  S.searchDone=false;
  S.searchResults=[]; S.searchArtists=[]; S.searchAlbums=[];
  S.searchSeq++;
  document.getElementById('searchHint').textContent='Начните вводить — результаты появятся сами';
  document.getElementById('searchBody').innerHTML=
    `<div class="empty"><span class="empty-icon">🔍</span><p>Начните вводить — найдутся треки, исполнители и альбомы</p></div>`;
}
window.addEventListener('py:search_results', e=>{
  const d=e.detail;
  if(!d) return;
  // Старый формат (просто массив треков) — на всякий случай
  if(Array.isArray(d)){
    S.searchResults=_applyDlList(d); S.searchArtists=[]; S.searchAlbums=[];
    renderSearchResults(true);
    return;
  }
  if(d.seq!=null && d.seq!==S.searchSeq) return;  // уже набрали дальше
  S.searchResults=_applyDlList(d.tracks||[]);
  S.searchArtists=d.artists||[];
  S.searchAlbums=d.albums||[];
  const q=(d.query||'').trim();
  const hint=document.getElementById('searchHint');
  const n=S.searchResults.length+S.searchArtists.length+S.searchAlbums.length;
  hint.textContent = n ? (q?`по запросу «${q}»`:'') : (q?`ничего по «${q}»`:'');
  renderSearchResults(!S.searchResults.length && !S.searchArtists.length);
});
function renderSearchResults(animate){
  if(!S.searchDone) return;
  const body=document.getElementById('searchBody');
  if(!body) return;
  const arts=S.searchArtists||[], albs=S.searchAlbums||[], tracks=S.searchResults||[];
  if(!arts.length && !albs.length && !tracks.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🔍</span><p>Ничего не найдено</p></div>`;
    return;
  }
  let html='';
  if(arts.length){
    html+=`<div class="search-sec">Исполнители</div><div class="search-cards">`;
    html+=arts.slice(0,8).map(a=>_artistCardHTML(a)).join('');
    html+='</div>';
  }
  if(albs.length){
    html+=`<div class="search-sec">Альбомы</div><div class="search-cards">`;
    html+=albs.slice(0,8).map(al=>_albumCardHTML(al)).join('');
    html+='</div>';
  }
  if(tracks.length){
    html+=`<div class="search-sec">Треки</div>`;
    html+=tracks.map(t=>exRowHTML(t,'search')).join('');
  }
  const keep=body.scrollTop;
  body.innerHTML=html;
  body.scrollTop=keep;
  if(animate) _playListEnter(body);
  _paintCardPlayBtns();
}

/* ═══════════════════════════════════════════════════════════════════
   DOWNLOADED FILES
═══════════════════════════════════════════════════════════════════ */
function scanDownloaded(){
  window.pywebview.api.scan_downloaded();
}
function renderDownloaded(files){
  _updateDlCount();
  const el=document.getElementById('dlList');
  if(!files.length){
    el.innerHTML=`<div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов в папке загрузки</p></div>`;
    _updateDlSelUI();
    return;
  }
  el.innerHTML=files.map(f=>dlRowHTML(f)).join('');
  _playListEnter(el);
  _updateDlSelUI();
}
function _updateDlCount(){
  document.getElementById('dlCount').textContent=S.dlFiles.length?`${S.dlFiles.length} файлов`:'';
}
function dlRowHTML(f){
  const isPlaying=S.playerSource==='downloaded'&&S.playerTrackId===f.rel_path;
  let playIcon='▶';
  if(isPlaying){
    const audio=document.getElementById('audioEl');
    if(audio && !audio.paused) playIcon='⏸';
  }
  const cover=f.cover_uri
    ?`<img class="dl-cover" src="${esc(f.cover_uri)}" alt=""
        onclick="openDownloadedBig(event,'${f.uid}')" title="Развернуть плеер">`
    :`<div class="dl-cover-ph" onclick="openDownloadedBig(event,'${f.uid}')" title="Развернуть плеер">🎵</div>`;
  const sub=[f.artist,f.album].filter(Boolean).join(' · ');
  return `<div class="dl-row${isPlaying?' dl-playing':''}" id="dlrow-${f.uid}"
    onclick="rowPlayDownloaded(event,'${f.uid}')">
    <input type="checkbox" class="cb" ${S.dlSelected.has(f.rel_path)?'checked':''}
      onchange="toggleDlSelect('${f.uid}',this.checked)">
    ${cover}
    <div class="dl-meta">
      <div class="dl-name" title="${esc(f.path)}">${esc(f.title||f.name)}</div>
      ${sub?`<div class="dl-sub">${esc(sub)}</div>`:''}
    </div>
    <span class="dl-ext">${esc(f.ext)}</span>
    <span class="dl-size">${fmtBytes(f.size)}</span>
    <button class="btn sm ghost play-btn" onclick="playDownloaded('${f.uid}')"
      title="${isPlaying?'Играет':'Воспроизвести'}">${playIcon}</button>
    <button class="iBtn del-btn" onclick="deleteDownloaded('${f.uid}')" title="Удалить файл с диска">🗑</button>
  </div>`;
}
/* Точечное обновление строки скачанного файла (id строки — по rel_path трека) */
function _updateDlRow(relPath){
  const f=S.dlFiles.find(x=>x.rel_path===relPath);
  if(!f) return;
  const el=document.getElementById('dlrow-'+f.uid);
  if(!el) return;
  const tmp=document.createElement('div');
  tmp.innerHTML=dlRowHTML(f);
  el.replaceWith(tmp.firstElementChild);
}
function playDownloaded(uid){
  const f=S.dlFiles.find(x=>x.uid===uid);
  if(f) playLocalFile(f);
}
async function playLocalFile(f){
  const audio=document.getElementById('audioEl');
  if(S.playerSource==='downloaded'&&S.playerTrackId===f.rel_path){
    if(audio.paused) audio.play(); else audio.pause();
    _updatePlayBtn(); return;
  }
  const url=await window.pywebview.api.get_file_url(f.rel_path);
  _loadAndPlay(_dlAsTrack(f), url,'downloaded');
}
async function openDownloadedBig(evt,uid){
  evt.stopPropagation();
  const f=S.dlFiles.find(x=>x.uid===uid);
  if(!f) return;
  if(!(S.playerSource==='downloaded' && S.playerTrackId===f.rel_path)){
    await playLocalFile(f);
  }
  openBigView();
}

/* ── Массовый выбор скачанных файлов ── */
function toggleDlSelect(uid,checked){
  const f=S.dlFiles.find(x=>x.uid===uid);
  if(!f) return;
  if(checked) S.dlSelected.add(f.rel_path); else S.dlSelected.delete(f.rel_path);
  _updateDlSelUI();
}
function dlSelectAll(v){
  S.dlSelected = v ? new Set(S.dlFiles.map(f=>f.rel_path)) : new Set();
  // правим только галочки — перерисовывать весь список ради них не нужно
  document.querySelectorAll('#dlList .dl-row .cb').forEach(cb=>{ cb.checked=v; });
  _updateDlSelUI();
}
function _updateDlSelUI(){
  const n=S.dlSelected.size;
  const btn=document.getElementById('btnDlDeleteSel');
  if(btn){
    btn.style.display=n?'':'none';
    btn.textContent=`🗑 Удалить выбранные (${n})`;
  }
  const info=document.getElementById('dlSelInfo');
  if(info){
    const bytes=S.dlFiles.filter(f=>S.dlSelected.has(f.rel_path))
      .reduce((sum,f)=>sum+(f.size||0),0);
    info.textContent = n ? `выбрано ${n} · ${fmtBytes(bytes)}` : '';
  }
}
function deleteSelectedDownloaded(){
  const files=S.dlFiles.filter(f=>S.dlSelected.has(f.rel_path) && !S.pendingFileDeletes[f.rel_path]);
  if(!files.length) return;
  const bytes=files.reduce((sum,f)=>sum+(f.size||0),0);
  showConfirm({
    title:`Удалить файлы (${files.length})?`,
    text:`С диска будет безвозвратно удалено ${files.length} файл(ов) — ${fmtBytes(bytes)}.`,
    okLabel:'Удалить',
    onOk:()=>_doDeleteManyDownloaded(files),
  });
}
function _doDeleteManyDownloaded(files){
  const paths=files.map(f=>f.rel_path);
  const doomed=new Set(paths);
  const wasPlaying = S.playerSource==='downloaded' && doomed.has(S.playerTrackId);
  const playingIdx = S.dlFiles.findIndex(f=>f.rel_path===S.playerTrackId);

  files.forEach(f=>{
    const idx=S.dlFiles.findIndex(x=>x.rel_path===f.rel_path);
    if(idx<0) return;
    S.pendingFileDeletes[f.rel_path]={file:f, index:idx};
    S.dlFiles.splice(idx,1);
    S.dlSelected.delete(f.rel_path);
    _dropDlFileMark(f);
    _animateElOut(document.getElementById('dlrow-'+f.uid));
  });
  _persistDlMarks();
  _syncDlMarks();
  _updateDlCount();
  _updateDlSelUI();
  if(!S.dlFiles.length) setTimeout(()=>{ if(!S.dlFiles.length) renderDownloaded(S.dlFiles); },430);

  // Пока плеер держит файл открытым, Windows не даст его удалить
  if(wasPlaying){
    if(S.dlFiles.length) playLocalFile(S.dlFiles[Math.min(Math.max(playingIdx,0),S.dlFiles.length-1)]);
    else playerClose();
  }
  setTimeout(()=>window.pywebview.api.delete_downloaded_many(paths), wasPlaying?350:0);
}
window.addEventListener('py:downloaded_deleted_many', e=>{
  const{deleted,failed}=e.detail;
  (deleted||[]).forEach(p=>{ delete S.pendingFileDeletes[p]; });
  if((deleted||[]).length){
    showToast({kind:'ok', icon:'🗑', message:`Удалено файлов: ${deleted.length}`});
  }
  if((failed||[]).length){
    // Что не получилось удалить — возвращаем в список
    (failed||[]).forEach(({rel_path})=>{
      const info=S.pendingFileDeletes[rel_path];
      delete S.pendingFileDeletes[rel_path];
      if(info){
        S.dlFiles.splice(Math.min(info.index,S.dlFiles.length),0,info.file);
        _restoreDlFileMark(info.file);
      }
    });
    _persistDlMarks();
    _syncDlMarks();
    renderDownloaded(S.dlFiles);
    showToast({kind:'err', icon:'✗', message:`Не удалось удалить файлов: ${failed.length}`});
  }
});

/* ── Удаление скачанного файла ── */
function deleteDownloaded(uid){
  const f=S.dlFiles.find(x=>x.uid===uid);
  if(!f || S.pendingFileDeletes[f.rel_path]) return;
  showConfirm({
    title:'Удалить файл?',
    text:`«${f.name}» будет удалён с диска безвозвратно.`,
    okLabel:'Удалить',
    onOk:()=>_doDeleteDownloaded(f),
  });
}
function _doDeleteDownloaded(f){
  const idx=S.dlFiles.findIndex(x=>x.rel_path===f.rel_path);
  if(idx<0) return;
  const wasPlaying = S.playerSource==='downloaded' && S.playerTrackId===f.rel_path;

  S.pendingFileDeletes[f.rel_path]={file:f, index:idx};
  S.dlFiles.splice(idx,1);
  S.dlSelected.delete(f.rel_path);
  _forgetDlFile(f);
  _updateDlCount();
  _updateDlSelUI();
  _animateElOut(document.getElementById('dlrow-'+f.uid),()=>{
    if(!S.dlFiles.length) renderDownloaded(S.dlFiles);
  });

  // Пока плеер держит файл открытым, Windows не даст его удалить. Переключаемся
  // на следующий трек — а если удаляли последний, то на новый последний.
  if(wasPlaying){
    if(S.dlFiles.length) playLocalFile(S.dlFiles[Math.min(idx,S.dlFiles.length-1)]);
    else playerClose();
  }
  // Даём потоку закрыться, прежде чем просить удалить файл
  setTimeout(()=>window.pywebview.api.delete_downloaded(f.rel_path), wasPlaying?350:0);
}
window.addEventListener('py:downloaded_deleted', e=>{
  const{rel_path,ok,msg}=e.detail;
  const info=S.pendingFileDeletes[rel_path];
  delete S.pendingFileDeletes[rel_path];
  if(ok){
    showToast({kind:'ok', icon:'🗑', message:`Файл «${esc(info?info.file.name:'')}» удалён`});
    return;
  }
  // Не удалось — возвращаем файл в список на прежнее место
  if(info){
    S.dlFiles.splice(Math.min(info.index,S.dlFiles.length),0,info.file);
    _restoreDlFileMark(info.file);
    _persistDlMarks();
    _syncDlMarks();
    renderDownloaded(S.dlFiles);
  }
  showToast({kind:'err', icon:'✗', message:`Не удалось удалить файл${msg?': '+esc(msg):''}`});
});

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
  return c;
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
   КЛАВИАТУРА
═══════════════════════════════════════════════════════════════════ */
document.addEventListener('keydown', e=>{
  const tag=((e.target&&e.target.tagName)||'').toLowerCase();
  if(tag==='input'||tag==='textarea'||tag==='select') return;

  if(e.key==='Escape'){
    if(document.getElementById('addMenu')){ closeAddMenu(); return; }
    if(_promptOpen()){ closePrompt(); return; }
    if(_confirmOpen()){ closeConfirm(); return; }
    if(S.bigViewOpen){ closeBigView(); return; }
    if(S.browseOpen){ browseBack(); return; }
    return;
  }
  if(e.key==='Enter' && _confirmOpen()){ e.preventDefault(); acceptConfirm(); return; }
  if(!S.bigViewOpen) return;

  // Управление воспроизведением работает только в полноэкранном режиме,
  // чтобы не перехватывать клавиши у остального интерфейса
  if(e.code==='Space'){ e.preventDefault(); playerToggle(); }
  else if(e.key==='ArrowRight'){ e.preventDefault(); playerSkip(5); }
  else if(e.key==='ArrowLeft'){ e.preventDefault(); playerSkip(-5); }
});

/* ═══════════════════════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════════════════════ */
window.addEventListener('pywebviewready',async ()=>{
  // Восстановить сохранённые URL
  renderUrlTags();
  // Восстановить состояние лога
  const box=document.getElementById('logBox');
  box.classList.add(S.logVisible?'expanded':'collapsed');
  document.getElementById('btnLog').classList.toggle('active-mode',S.logVisible);
  // Восстановить режимы плеера
  _applyModeUI();
  // Загрузить настройки
  const cfg=await loadSettings();
  // Подтянуть список плейлистов заранее — он нужен для кнопки «добавить в плейлист»,
  // но только если уже есть токен, иначе получим лишнюю ошибку в логе
  if(cfg && cfg.token) refreshStaleCaches(false);
  scanDownloaded();
  addLog('Приложение готово к работе','info');
});
</script>
</body>
</html>
"""
