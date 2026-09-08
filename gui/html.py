"""
HTML-интерфейс приложения.
Импортируется из app.py как строка HTML.
"""

HTML = r"""<!DOCTYPE html>
<html lang="ru" data-theme="amber" data-mode="dark">
<head>
<meta charset="UTF-8">
<script>
try{
  var _ui=JSON.parse(localStorage.getItem('ym_ui')||'null');
  if(_ui){
    if(_ui.theme) document.documentElement.setAttribute('data-theme', _ui.theme);
    if(_ui.mode) document.documentElement.setAttribute('data-mode', _ui.mode);
  }
}catch(e){}
</script>
<title>YM Downloader</title>
<style>
:root {
  --r:10px; --rsm:6px;
  --ease:cubic-bezier(.22,1,.36,1);
  --ease-soft:cubic-bezier(.4,0,.2,1);
  --spring:cubic-bezier(.34,1.4,.64,1);
  --green:#4ade80; --green-dim:rgba(74,222,128,.1);
  --red:#f87171; --red-dim:rgba(248,113,113,.1);
  --blue:#60a5fa; --blue-dim:rgba(96,165,250,.1);
}
html[data-theme="amber"][data-mode="dark"],:root{
  --bg:#0f0f11; --surface:#1a1a1f; --surface2:#22222a; --surface3:#2a2a35;
  --border:#2e2e3a; --border2:#3e3e50;
  --text:#e8e8f0; --muted:#888899; --hint:#55556a;
  --accent:#ffcc00; --accent-dim:rgba(255,204,0,.12); --accent-mid:rgba(255,204,0,.22);
  --accent-ink:#1a1400; --accent-glow:rgba(255,204,0,.28); --btn-hover:#353544;
}
html[data-theme="amber"][data-mode="light"]{
  --bg:#f3efe6; --surface:#fffdf8; --surface2:#ece6d8; --surface3:#e2dac8;
  --border:#ddd3c0; --border2:#cfc3ab;
  --text:#1c1914; --muted:#6f685c; --hint:#9a9184;
  --accent:#c49200; --accent-dim:rgba(196,146,0,.14); --accent-mid:rgba(196,146,0,.24);
  --accent-ink:#fff8e8; --accent-glow:rgba(196,146,0,.28); --btn-hover:#d8d0be;
  --green:#16a34a; --green-dim:rgba(22,163,74,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#2563eb; --blue-dim:rgba(37,99,235,.1);
}
html[data-theme="ocean"][data-mode="dark"]{
  --bg:#0a1016; --surface:#121a22; --surface2:#18232e; --surface3:#1e2c3a;
  --border:#243140; --border2:#33475a;
  --text:#e4eef6; --muted:#7e93a6; --hint:#4e6274;
  --accent:#3ec4e8; --accent-dim:rgba(62,196,232,.14); --accent-mid:rgba(62,196,232,.24);
  --accent-ink:#042028; --accent-glow:rgba(62,196,232,.3); --btn-hover:#274050;
}
html[data-theme="ocean"][data-mode="light"]{
  --bg:#eaf3f7; --surface:#ffffff; --surface2:#ddecef; --surface3:#cfe0e8;
  --border:#c5d6e0; --border2:#adc4d2;
  --text:#12202a; --muted:#5b7384; --hint:#8aa0ae;
  --accent:#0284b8; --accent-dim:rgba(2,132,184,.12); --accent-mid:rgba(2,132,184,.22);
  --accent-ink:#f4fcff; --accent-glow:rgba(2,132,184,.26); --btn-hover:#c5d7e0;
  --green:#16a34a; --green-dim:rgba(22,163,74,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#0284c7; --blue-dim:rgba(2,132,199,.1);
}
html[data-theme="forest"][data-mode="dark"]{
  --bg:#0c110e; --surface:#151c17; --surface2:#1c251f; --surface3:#24332a;
  --border:#2a3a30; --border2:#3b5043;
  --text:#e6f0e8; --muted:#84968b; --hint:#55665c;
  --accent:#6bcb7a; --accent-dim:rgba(107,203,122,.14); --accent-mid:rgba(107,203,122,.24);
  --accent-ink:#07210c; --accent-glow:rgba(107,203,122,.28); --btn-hover:#2c4033;
}
html[data-theme="forest"][data-mode="light"]{
  --bg:#eef4ee; --surface:#ffffff; --surface2:#e3ece3; --surface3:#d5e2d6;
  --border:#c5d4c6; --border2:#adc0af;
  --text:#142018; --muted:#5d7262; --hint:#8a9b8e;
  --accent:#2f9e4f; --accent-dim:rgba(47,158,79,.12); --accent-mid:rgba(47,158,79,.22);
  --accent-ink:#f3fff5; --accent-glow:rgba(47,158,79,.26); --btn-hover:#c5d6c7;
  --green:#15803d; --green-dim:rgba(21,128,61,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#2563eb; --blue-dim:rgba(37,99,235,.1);
}
html[data-theme="sunset"][data-mode="dark"]{
  --bg:#120d0c; --surface:#1c1514; --surface2:#261c1a; --surface3:#322623;
  --border:#3a2c29; --border2:#52403c;
  --text:#f3eae6; --muted:#a08b84; --hint:#6d5a55;
  --accent:#ff8a5b; --accent-dim:rgba(255,138,91,.14); --accent-mid:rgba(255,138,91,.24);
  --accent-ink:#2a1008; --accent-glow:rgba(255,138,91,.3); --btn-hover:#3d2e2a;
}
html[data-theme="sunset"][data-mode="light"]{
  --bg:#f7efe9; --surface:#fffaf7; --surface2:#f0e3da; --surface3:#e6d4c8;
  --border:#e0cdc2; --border2:#cfb6a8;
  --text:#271c18; --muted:#7a635a; --hint:#a08a80;
  --accent:#e05a2b; --accent-dim:rgba(224,90,43,.12); --accent-mid:rgba(224,90,43,.22);
  --accent-ink:#fff6f1; --accent-glow:rgba(224,90,43,.26); --btn-hover:#e4d0c4;
  --green:#16a34a; --green-dim:rgba(22,163,74,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#2563eb; --blue-dim:rgba(37,99,235,.1);
}
html[data-theme="violet"][data-mode="dark"]{
  --bg:#100e16; --surface:#191622; --surface2:#211e2d; --surface3:#2b273a;
  --border:#342f46; --border2:#48425e;
  --text:#eee8f8; --muted:#938aab; --hint:#625c78;
  --accent:#c084fc; --accent-dim:rgba(192,132,252,.14); --accent-mid:rgba(192,132,252,.24);
  --accent-ink:#1c0a2e; --accent-glow:rgba(192,132,252,.3); --btn-hover:#352f48;
}
html[data-theme="violet"][data-mode="light"]{
  --bg:#f3eef8; --surface:#fcfaff; --surface2:#e8e0f2; --surface3:#dcd0ea;
  --border:#d0c4e0; --border2:#bbaed0;
  --text:#1d1728; --muted:#6c6380; --hint:#948aa8;
  --accent:#7c3aed; --accent-dim:rgba(124,58,237,.12); --accent-mid:rgba(124,58,237,.22);
  --accent-ink:#f8f2ff; --accent-glow:rgba(124,58,237,.26); --btn-hover:#d4c8e4;
  --green:#16a34a; --green-dim:rgba(22,163,74,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#6d28d9; --blue-dim:rgba(109,40,217,.1);
}
html[data-theme="graphite"][data-mode="dark"]{
  --bg:#0e0e10; --surface:#18181c; --surface2:#202026; --surface3:#2a2a32;
  --border:#33333c; --border2:#474752;
  --text:#ececf0; --muted:#8c8c98; --hint:#5c5c68;
  --accent:#a8b4c4; --accent-dim:rgba(168,180,196,.14); --accent-mid:rgba(168,180,196,.24);
  --accent-ink:#12141a; --accent-glow:rgba(168,180,196,.28); --btn-hover:#32323c;
}
html[data-theme="graphite"][data-mode="light"]{
  --bg:#f0f1f3; --surface:#ffffff; --surface2:#e6e7eb; --surface3:#d9dbe1;
  --border:#cfd2d8; --border2:#b8bcc4;
  --text:#1a1b1f; --muted:#646872; --hint:#8d9199;
  --accent:#4b5563; --accent-dim:rgba(75,85,99,.12); --accent-mid:rgba(75,85,99,.22);
  --accent-ink:#f7f8fa; --accent-glow:rgba(75,85,99,.22); --btn-hover:#cfd3da;
  --green:#16a34a; --green-dim:rgba(22,163,74,.12);
  --red:#dc2626; --red-dim:rgba(220,38,38,.1);
  --blue:#2563eb; --blue-dim:rgba(37,99,235,.1);
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
@keyframes playingGlow{
  0%,100%{background:var(--accent-dim);}
  50%{background:var(--accent-mid);}
}
@keyframes nowEq{
  0%,100%{transform:scaleY(.35);}
  50%{transform:scaleY(1);}
}
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
.nav-icon{flex-shrink:0;width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;}
.sidebar-footer{margin-top:auto;padding-top:8px;border-top:1px solid var(--border);
  padding-left:4px;padding-right:4px;}
.about-btn{width:100%;background:none;border:none;color:var(--hint);font-size:11px;
  cursor:pointer;text-align:left;padding:8px 10px;border-radius:var(--rsm);
  font-weight:500;letter-spacing:.02em;}
.about-btn:hover{color:var(--text);background:var(--surface2);}
.about-links{display:flex;flex-direction:column;gap:6px;}
.about-link{display:flex;flex-direction:column;align-items:flex-start;gap:2px;
  text-align:left;padding:10px 12px;width:100%;cursor:pointer;
  background:var(--surface2);border:1px solid var(--border);border-radius:var(--rsm);
  color:inherit;transition:border-color .15s,background .15s;}
.about-link:hover{border-color:var(--border2);background:var(--surface3);}
.about-k{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;}
.about-v{font-size:13px;color:var(--accent);}
.about-url{font-size:11px;color:var(--hint);}

/* ── Main / Pages ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.page{display:none;flex-direction:column;flex:1;overflow:hidden;padding:16px 18px;gap:12px;
  background:var(--bg);}
.page.active{display:flex;animation:fadeInUp .3s var(--ease);}
#page-settings{overflow-y:auto;}

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
.btn:hover{background:var(--btn-hover);}
.btn:active{transform:scale(.97);}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none;}
.btn.accent{background:var(--accent);color:var(--accent-ink);border-color:transparent;font-weight:700;
  box-shadow:0 4px 14px var(--accent-glow);}
.btn.accent:hover{opacity:.92;box-shadow:0 6px 18px var(--accent-glow);}
.btn.danger{color:var(--red);background:var(--red-dim);border-color:transparent;}
.btn.danger:hover{background:rgba(248,113,113,.22);}
.btn.sm{height:28px;padding:0 11px;font-size:12px;border-radius:8px;}
.btn.ghost{background:transparent;border-color:transparent;color:var(--muted);
  box-shadow:none;}
.btn.ghost:hover{background:var(--surface2);color:var(--text);}
.btn.active-mode{color:var(--accent);background:var(--accent-dim);box-shadow:none;}
@keyframes authGlow{
  0%,100%{box-shadow:0 0 8px var(--accent-glow);}
  50%{box-shadow:0 0 18px var(--accent-mid);}
}
.btn.logged-in{color:var(--accent);background:var(--accent-dim);
  border-color:var(--accent-glow);animation:authGlow 1.8s ease-in-out infinite;}
.btn.logged-in:hover{background:var(--accent-mid);color:var(--accent);}
#btnPlDeadFilter[hidden],#btnPlDeadRemove[hidden]{display:none!important;}

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
.toolbar-right{margin-left:auto;display:flex;align-items:center;gap:6px;}
#plDetailWrap .pl-detail-head{display:flex;flex-direction:column;gap:6px;flex-shrink:0;}
#plDetailWrap .toolbar{align-items:center;flex-wrap:nowrap;}
#plDetailWrap .toolbar-right{flex-shrink:0;}
#plDetailWrap .pl-detail-name{display:inline-flex;align-items:center;gap:4px;min-width:0;flex-shrink:1;}
#plDetailTitle{font-size:13px;font-weight:600;line-height:28px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
#plDetailCount{font-size:12px;color:var(--muted);line-height:28px;flex-shrink:0;}
#plDeadRow{display:flex;justify-content:flex-end;align-items:center;gap:6px;}
#plDeadRow[hidden]{display:none!important;}
#plAddPanel{display:none;flex-direction:column;gap:6px;}
#plAddPanel.open{display:flex;}
#plAddSearch{width:100%;height:28px;padding:0 10px;font-size:12px;}
#plAddHint{font-size:11px;color:var(--muted);min-height:14px;}
#plAddResults{max-height:min(240px,32vh);overflow-y:auto;border:1px solid var(--border);
  border-radius:var(--rsm);background:var(--bg);}
#plAddResults[hidden]{display:none!important;}
.pl-add-row{display:grid;grid-template-columns:1fr 140px 52px 28px;gap:6px;
  align-items:center;padding:6px 10px;border-bottom:1px solid var(--border);cursor:default;}
.pl-add-row:last-child{border-bottom:none;}
.pl-add-row:hover{background:var(--surface2);}
.pl-add-row.in-pl{opacity:.72;}
.pl-add-meta{min-width:0;}
.pl-add-album,.pl-add-dur{font-size:11px;color:var(--muted);white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;}
.pl-add-dur{text-align:right;color:var(--hint);}
.ex-row.pl-just-added{animation:plJustAdded 1.4s ease;}
@keyframes plJustAdded{from{background:var(--accent-dim);}to{background:transparent;}}

/* ── Track List ── */
.tl-wrap{flex:1;overflow:hidden;display:flex;flex-direction:column;min-height:0;
  border:1px solid var(--border);border-radius:var(--r);background:var(--bg);}
.tl-head{display:grid;grid-template-columns:20px 40px 1fr 150px 64px 72px 28px 28px;
  gap:6px;padding:7px 10px;background:var(--surface);
  border-bottom:1px solid var(--border);font-size:10px;color:var(--hint);
  font-weight:600;letter-spacing:.06em;flex-shrink:0;align-items:center;z-index:3;}
.tl-head:empty{display:none;padding:0;border:none;}
.tl-body,.ex-body{flex:1;overflow-y:auto;scrollbar-gutter:stable;background:var(--bg);min-height:0;
  overscroll-behavior:contain;-webkit-overflow-scrolling:touch;}
.th-sort{background:none;border:none;color:inherit;font:inherit;letter-spacing:inherit;
  cursor:pointer;text-align:left;padding:0;min-width:0;width:100%;max-width:100%;
  display:inline-flex;align-items:center;gap:3px;user-select:none;white-space:nowrap;}
.th-sort:hover{color:var(--text);}
.th-sort.on{color:var(--accent);}
.th-sort.right{margin-left:auto;justify-content:flex-end;text-align:right;}
.th-dir{font-size:9px;line-height:1;opacity:.9;flex-shrink:0;}
.sticky-table{border:1px solid var(--border);border-radius:var(--r);overflow:hidden;min-width:0;
  background:var(--bg);display:flex;flex-direction:column;}
.sticky-table .tl-head{position:static;flex-shrink:0;background:var(--surface);
  border:none;border-bottom:1px solid var(--border);}
.sticky-table .ex-row:last-of-type{border-bottom:none;}
.tl-row{display:grid;grid-template-columns:20px 40px 1fr 150px 64px 72px 28px 28px;
  gap:6px;padding:8px 10px;align-items:center;
  border-bottom:1px solid var(--border);cursor:pointer;
  contain:content;content-visibility:auto;contain-intrinsic-size:auto 46px;
  transition:background-color .12s var(--ease);}
.tl-row:last-child{border-bottom:none;}
.tl-row:hover{background:var(--surface2);}
.tl-row.downloading{background:var(--blue-dim);}
.tl-row.done{background:var(--green-dim);}
.tl-row.error{background:var(--red-dim);}
.tl-row.playing-row,.ex-row.playing-row{content-visibility:visible;}
.tl-row.playing-row{outline:none;background:var(--accent-dim);
  box-shadow:inset 3px 0 0 var(--accent);animation:playingGlow 2.2s ease-in-out infinite;}
.tl-row.playing-row .tl-title{color:var(--accent);}
.tl-row.playing-row.is-paused,.ex-row.playing-row.is-paused{animation:none;}
.now-eq{display:none;align-items:flex-end;justify-content:flex-end;gap:2px;height:12px;width:14px;}
.now-eq i{display:block;width:2px;border-radius:1px;background:var(--accent);
  transform-origin:bottom;animation:nowEq .85s ease-in-out infinite;}
.now-eq i:nth-child(1){height:5px;animation-delay:0s;}
.now-eq i:nth-child(2){height:12px;animation-delay:.15s;}
.now-eq i:nth-child(3){height:8px;animation-delay:.3s;}
.playing-row .tl-num-val{display:none;}
.playing-row .now-eq{display:inline-flex;}
.playing-row.is-paused .now-eq i{animation-play-state:paused;}
.tl-num{font-size:11px;color:var(--hint);text-align:right;
  display:flex;align-items:center;justify-content:flex-end;min-height:12px;}
.tl-title{font-weight:500;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tl-sub{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;}
.tl-album{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tl-dur{font-size:11px;color:var(--hint);text-align:right;}
.tl-status{font-size:11px;text-align:right;}
.s-idle{color:var(--hint);} .s-queued,.s-downloading{color:var(--blue);}
.s-done{color:var(--green);} .s-error{color:var(--red);}
.cb{appearance:none;-webkit-appearance:none;width:15px;height:15px;margin:0;
  border:1.5px solid var(--border2);border-radius:4px;background:transparent;
  cursor:pointer;flex-shrink:0;position:relative;
  transition:background .15s var(--ease),border-color .15s var(--ease),box-shadow .15s var(--ease);}
.cb:hover{border-color:var(--accent);}
.cb:checked{background:var(--accent);border-color:var(--accent);}
.cb:checked::after{content:'';position:absolute;left:4px;top:1px;width:4px;height:8px;
  border:solid var(--accent-ink);border-width:0 1.8px 1.8px 0;transform:rotate(45deg);}
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
.iBtn.active-mode{background:var(--accent-dim);color:var(--accent);}
.iBtn svg,.btn svg,.nav-icon svg,.empty-icon svg,.skip-btn svg,.card-play svg{display:block;flex-shrink:0;}
.ico{width:16px;height:16px;}
.iBtn svg.ico{width:15px;height:15px;pointer-events:none;}
.btn svg,.play-btn svg,.play-btn .ico{pointer-events:none;}
.nav-icon{width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;}
.nav-icon svg.ico{width:17px;height:17px;}
.empty-icon{display:flex;align-items:center;justify-content:center;color:var(--hint);}
.empty-icon svg.ico{width:34px;height:34px;opacity:.85;}
.ico-spin{animation:icoSpin .8s linear infinite;transform-origin:center;}
@keyframes icoSpin{to{transform:rotate(360deg);}}
.ico-play{transform:translateX(1px);}
.btn.play-main{width:36px;height:36px;padding:0;border-radius:50%;justify-content:center;}
.btn.play-main svg.ico{width:18px;height:18px;}
.btn.play-main-lg{width:48px;height:48px;}
.btn.play-main-lg svg.ico{width:22px;height:22px;}
.player-controls .btn.sm.ghost{width:32px;padding:0;justify-content:center;}
.skip-btn{width:auto!important;padding:0 7px!important;gap:2px;font-size:10px;font-weight:700;
  letter-spacing:.02em;color:var(--muted);}
.skip-btn svg.ico{width:14px;height:14px;}
.player-mode .btn.sm.ghost{width:32px;padding:0;justify-content:center;}
#page-browse .toolbar-right .btn.ghost{width:32px;padding:0;justify-content:center;}
.bigview-actions .btn.sm.ghost{width:36px;padding:0;justify-content:center;}
.bigview-actions .skip-btn{width:auto!important;padding:0 8px!important;}
.like-btn.liked svg.ico[fill="currentColor"], .like-btn.liked .ico{color:var(--red);}
.btn.like-btn,.btn.dislike-btn{gap:6px;}
.btn.like-btn svg.ico,.btn.dislike-btn svg.ico{width:14px;height:14px;}
.iBtn.playing{background:var(--blue-dim);color:var(--blue);}
.playing-row .iBtn.playing{background:var(--accent-dim);color:var(--accent);}
.iBtn.done{color:var(--green);background:var(--green-dim);}
.iBtn.error{color:var(--red);background:var(--red-dim);}
.like-btn.liked{color:var(--red);background:var(--red-dim);}
.like-btn.liked:hover{background:rgba(248,113,113,.28);color:var(--red);}
.btn.like-btn.liked{color:var(--red);background:var(--red-dim);border-color:transparent;}
.btn.like-btn.liked:hover{background:rgba(248,113,113,.22);color:var(--red);}
.dislike-btn.disliked{color:#c4b5fd;background:rgba(167,139,250,.14);}
.dislike-btn.disliked:hover{background:rgba(167,139,250,.26);color:#ddd6fe;}
.btn.dislike-btn.disliked{color:#c4b5fd;background:rgba(167,139,250,.14);border-color:transparent;}
.del-btn:hover{background:var(--red-dim);color:var(--red);}

/* ── Empty State ── */
.empty{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:var(--hint);gap:10px;}
.empty-icon{font-size:36px;display:flex;align-items:center;justify-content:center;} .empty p{font-size:13px;}

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
.player-cover-slot{position:relative;width:36px;height:36px;flex-shrink:0;cursor:pointer;
  border-radius:4px;overflow:hidden;background:var(--surface2);transition:transform .15s;}
.player-cover-slot:hover{transform:scale(1.08);}
.player-cover,.player-cover-ph{width:36px;height:36px;border-radius:4px;object-fit:cover;}
.player-cover-ph{display:flex;align-items:center;justify-content:center;color:var(--hint);
  background:var(--surface2);}
.player-cover-ph svg.ico{width:16px;height:16px;opacity:.55;}
.player-cover[hidden],.player-cover-ph[hidden]{display:none !important;}
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
.bigview-body{position:relative;flex:1;min-height:0;display:flex;gap:36px;padding:0 48px 28px;
  overflow:hidden;align-items:stretch;}
.bigview-cover-slot{width:min(340px,32vw);height:min(340px,32vw);flex-shrink:0;border-radius:14px;
  position:relative;overflow:hidden;background:var(--surface2);box-shadow:0 20px 60px rgba(0,0,0,.5);
  align-self:center;cursor:pointer;transition:transform .3s var(--ease),box-shadow .3s var(--ease);}
.bigview-cover-slot:hover{transform:scale(1.02);box-shadow:0 26px 70px rgba(0,0,0,.6);}
.bigview-cover{width:100%;height:100%;object-fit:cover;display:block;background:var(--surface2);}
.bigview-cover-ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  background:var(--surface2);color:var(--hint);border-radius:14px;}
.bigview-cover-ph svg.ico{width:72px;height:72px;opacity:.55;}
.bigview-cover[hidden],.bigview-cover-ph[hidden]{display:none !important;}
.bigview-cover.swap{animation:coverSwap .35s var(--ease);}
@keyframes coverSwap{from{opacity:.35;transform:scale(.97);}to{opacity:1;transform:none;}}
.bigview.show .bigview-cover-slot{animation:bvCoverIn .45s var(--ease) both;}
.bigview.show .bigview-info{animation:bvInfoIn .45s .05s var(--ease) both;}
.bigview-info{flex:1;min-width:0;min-height:0;display:flex;flex-direction:column;overflow:hidden;}
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
.bigview-lyrics-wrap{flex:1 1 0;min-height:0;overflow-x:hidden;overflow-y:auto;
  border-top:1px solid var(--border);padding-top:12px;scrollbar-width:none;}
.bigview-lyrics-wrap::-webkit-scrollbar{width:0;height:0;}
.bigview-lyrics{white-space:pre-wrap;line-height:1.55;font-size:15px;color:var(--text);
  max-width:640px;}
.bigview-lyrics.muted{color:var(--hint);font-style:italic;white-space:normal;}
.bigview-lyrics.synced{white-space:normal;}
.lyric-line{color:var(--muted);padding:1px 0;transition:color .28s var(--ease);}
.lyric-line.on{color:var(--text);font-weight:600;}
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
#page-browse{padding:0;gap:0;}
#page-browse > .toolbar{background:var(--surface);z-index:8;padding:12px 18px;
  border-bottom:1px solid var(--border);}
.br-crumb{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:6px;
  min-width:0;overflow:hidden;white-space:nowrap;}
.br-crumb b{color:var(--text);font-weight:600;}
.br-sep{color:var(--hint);}
.browse-body{flex:1;overflow:hidden;display:flex;flex-direction:column;gap:0;min-height:0;
  background:var(--bg);padding:0 18px 16px;}
.br-hero{display:flex;gap:18px;align-items:center;flex-shrink:0;background:var(--surface);
  margin:0 -18px;padding:14px 18px 12px;z-index:7;}
.br-hero-cover{width:150px;height:150px;border-radius:12px;object-fit:cover;flex-shrink:0;
  background:var(--surface2);box-shadow:0 14px 34px rgba(0,0,0,.35);}
.br-hero-ph{display:flex;align-items:center;justify-content:center;font-size:48px;}
.br-hero-info{min-width:0;display:flex;flex-direction:column;gap:5px;}
.br-hero-kind{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.br-hero-title{font-size:26px;font-weight:700;line-height:1.15;}
.br-hero-sub{font-size:12px;color:var(--muted);}
.br-hero-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;}
.br-scroll{flex:1 1 0;min-height:0;overflow:hidden;display:flex;flex-direction:column;
  background:var(--bg);}
.br-subbar{flex-shrink:0;background:var(--surface);z-index:7;margin:0 -18px;padding:0 18px 12px;}
.br-pin{flex-shrink:0;background:var(--surface);padding:0;}
.br-pin .br-sec{position:static;border-bottom:none;padding:8px 10px;background:var(--surface);}
.br-pin .tl-head{margin:0;}
.br-block{min-width:0;}
.br-sticky{position:sticky;top:0;z-index:5;background:var(--surface);}
.br-block > .br-sec{position:sticky;top:0;z-index:5;background:var(--surface);
  padding:12px 10px 8px;margin:0;border-bottom:1px solid var(--border);border-radius:0;
  box-sizing:border-box;}
.br-sticky > .br-sec{position:static;padding:12px 10px 8px;margin:0;
  border-bottom:none;background:var(--surface);border-radius:0;}
.br-sticky > .tl-head{border-radius:0;}
.br-rest{background:var(--bg);}
.br-rest .pl-grid{padding:12px 10px 16px;}
.br-sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid var(--border);padding-bottom:5px;}
.br-list{border:1px solid var(--border);border-radius:var(--r);overflow:hidden;flex-shrink:0;}
.browse-body > .tl-wrap{flex:1;min-height:0;margin-top:10px;overflow:hidden;background:var(--bg);}
@media (max-height:720px){
  .br-hero-cover{width:112px;height:112px;}
  .br-hero-title{font-size:22px;}
  .br-hero-ph{font-size:36px;}
}

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
.code-copy-btn:hover{background:var(--accent);color:var(--accent-ink);border-color:transparent;}
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

.theme-swatches{display:flex;flex-wrap:wrap;gap:8px;}
.theme-swatch{width:42px;height:42px;border-radius:10px;border:2px solid var(--border);
  cursor:pointer;padding:0;display:flex;align-items:center;justify-content:center;
  background:var(--sw-bg, var(--surface2));
  transition:transform .15s var(--ease),border-color .15s var(--ease),box-shadow .15s var(--ease);}
.theme-swatch:hover{transform:translateY(-1px);border-color:var(--border2);}
.theme-swatch.on{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);}
.theme-swatch i{width:16px;height:16px;border-radius:50%;background:var(--sw-a, var(--accent));display:block;}
.theme-swatch span{display:none;}
.mode-seg{display:flex;background:var(--surface2);border:1px solid var(--border);border-radius:8px;overflow:hidden;}
.mode-seg button{height:30px;padding:0 12px;border:none;background:transparent;color:var(--muted);
  font-size:12px;cursor:pointer;}
.mode-seg button.on{background:var(--accent);color:var(--accent-ink);font-weight:600;}

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
.pl-card:hover .card-like,.card-like.liked,.card-like.disliked,.pl-card:hover .card-del,.pl-card:hover .card-rename{opacity:1;}
.card-del{position:absolute;top:6px;right:6px;z-index:2;opacity:0;
  background:rgba(15,15,17,.72);backdrop-filter:blur(6px);}
.card-rename{position:absolute;top:6px;right:38px;z-index:2;opacity:0;
  background:rgba(15,15,17,.72);backdrop-filter:blur(6px);}
.card-play{position:absolute;left:8px;top:8px;z-index:2;opacity:0;width:34px;height:34px;
  border-radius:50%;background:rgba(15,15,17,.75);font-size:15px;}
.pl-card:hover .card-play,.card-play.on{opacity:1;}
.card-play.on{background:var(--accent);color:var(--accent-ink);}
.card-play svg.ico{width:16px;height:16px;color:inherit;}
input.pl-search{width:min(220px,36vw);height:28px;padding:0 10px;font-size:12px;flex:0 1 220px;}

/* ── Extra track rows (search / wave / playlist detail) ── */
.ex-row{display:grid;grid-template-columns:40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;
  gap:6px;padding:8px 10px;align-items:center;cursor:pointer;
  border-bottom:1px solid var(--border);
  contain:content;content-visibility:auto;contain-intrinsic-size:auto 46px;
  transition:background-color .12s var(--ease);}
.br-more{display:flex;justify-content:center;padding:12px 10px;}
.ex-row.selectable{grid-template-columns:18px 40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;}
.ex-row.removable{grid-template-columns:40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px 28px;}
.ex-row.selectable.removable{grid-template-columns:18px 40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px 28px;}
.ex-head{grid-template-columns:40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;}
.ex-head.selectable{grid-template-columns:18px 40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px;}
.ex-head.removable{grid-template-columns:40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px 28px;}
.ex-head.selectable.removable{grid-template-columns:18px 40px 1fr 150px 64px 28px 28px 28px 28px 28px 28px 28px;}
.ex-row:last-child{border-bottom:none;}
.ex-row:hover{background:var(--surface2);}
.ex-row.downloading{background:var(--blue-dim);}
.ex-row.done{background:var(--green-dim);}
.ex-row.unavailable{cursor:default;}
.ex-row.unavailable .tl-title,
.ex-row.unavailable .tl-sub,
.ex-row.unavailable .tl-album,
.ex-row.unavailable .tl-dur,
.ex-row.unavailable .tl-num{opacity:.45;}
.ex-row.unavailable .iBtn:not(.del-btn){opacity:.28;pointer-events:none;}
.ex-row.unavailable .del-btn{color:var(--red);background:var(--red-dim);opacity:1;}
.ex-row.unavailable .del-btn:hover{background:rgba(248,113,113,.32);color:var(--red);}
.ex-row.unavailable:hover{background:var(--surface2);}
.ex-row.error{background:var(--red-dim);}
.ex-row.playing-row{background:var(--accent-dim);box-shadow:inset 3px 0 0 var(--accent);
  animation:playingGlow 2.2s ease-in-out infinite;}
.ex-row.playing-row .tl-title{color:var(--accent);}
.ex-row.playing-row.done,.ex-row.playing-row.downloading{background:var(--accent-dim);}
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
.toast-action{flex-shrink:0;background:var(--accent);color:var(--accent-ink);border:none;border-radius:6px;
  padding:5px 9px;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap;
  transition:opacity .15s;}
.toast-action:hover{opacity:.85;}
.toast-close{flex-shrink:0;cursor:pointer;color:var(--hint);font-size:14px;line-height:1;
  transition:color .15s;}
.toast-close:hover{color:var(--text);}

/* ── Downloaded ── */
.dl-head,.dl-row{display:grid;grid-template-columns:18px 40px 1fr 48px 72px 28px 28px;
  gap:10px;align-items:center;padding:8px 12px;}
.dl-head{padding:7px 12px;}
.dl-row{overflow:hidden;cursor:pointer;
  border-bottom:1px solid var(--border);
  contain:content;content-visibility:auto;contain-intrinsic-size:auto 56px;
  transition:background-color .12s var(--ease);}
.dl-row:hover{background:var(--surface2);}
.dl-row.dl-playing{background:var(--blue-dim);}
.dl-cover-slot{position:relative;width:40px;height:40px;border-radius:6px;flex-shrink:0;
  background:var(--surface2);cursor:pointer;overflow:hidden;}
.dl-cover,.dl-cover-ph{width:40px;height:40px;border-radius:6px;flex-shrink:0;
  background:var(--surface2);object-fit:cover;}
.dl-cover-slot .dl-cover,.dl-cover-slot .dl-cover-ph{position:absolute;inset:0;width:100%;height:100%;}
.dl-cover{cursor:pointer;}
.dl-cover-ph{display:flex;align-items:center;justify-content:center;font-size:16px;color:var(--hint);cursor:pointer;}
.dl-cover-ph svg.ico{width:18px;height:18px;}
.dl-cover[hidden],.dl-cover-ph[hidden]{display:none !important;}
.dl-row .btn.play-btn{width:32px;padding:0;justify-content:center;}
.pl-cover-ph svg.ico{width:40px;height:40px;opacity:.55;}
.dl-meta{flex:1;min-width:0;}
.dl-ext{font-size:10px;font-weight:700;color:var(--accent);min-width:36px;text-align:center;
  background:var(--accent-dim);padding:2px 5px;border-radius:4px;flex-shrink:0;}
.dl-name{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.dl-sub{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;}
.dl-size{font-size:11px;color:var(--muted);flex-shrink:0;text-align:right;}

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

<!-- ══ О проекте ══ -->
<div class="modal-bg hidden" id="aboutModal" onclick="if(event.target===this)closeAbout()">
  <div class="modal" style="width:420px">
    <div style="display:flex;align-items:center;gap:8px">
      <h2 style="flex:1">О проекте</h2>
      <button type="button" class="btn sm ghost" onclick="closeAbout()" title="Закрыть" data-icon="x"></button>
    </div>
    <p>YM Downloader — графическая оболочка. Каталог и плеер работают через неофициальный API Яндекс.Музыки, файлы качает консольный загрузчик.</p>
    <div class="about-links">
      <button type="button" class="about-link" onclick="openExt('https://github.com/MarshalX/yandex-music-api')">
        <span class="about-k">API</span>
        <span class="about-v">MarshalX / yandex-music-api</span>
        <span class="about-url">github.com/MarshalX/yandex-music-api</span>
      </button>
      <button type="button" class="about-link" onclick="openExt('https://github.com/llistochek/yandex-music-downloader')">
        <span class="about-k">Загрузчик</span>
        <span class="about-v">llistochek / yandex-music-downloader</span>
        <span class="about-url">github.com/llistochek/yandex-music-downloader</span>
      </button>
      <button type="button" class="about-link" onclick="openExt('https://github.com/Siellph/yamd')">
        <span class="about-k">Этот проект</span>
        <span class="about-v">Siellph / yamd</span>
        <span class="about-url">github.com/Siellph/yamd</span>
      </button>
    </div>
    <div style="display:flex;justify-content:flex-end">
      <button class="btn" onclick="closeAbout()">Закрыть</button>
    </div>
  </div>
</div>

<!-- ══ Titlebar ══ -->
<div class="titlebar">
  <span style="font-size:18px;-webkit-app-region:no-drag">🎵</span>
  <h1>Yandex Music Downloader</h1>
  <span class="tb-badge">GUI</span>
  <div style="margin-left:auto;display:flex;gap:6px;-webkit-app-region:no-drag;align-items:center">
    <span id="saveStatus" style="font-size:12px;color:var(--green);opacity:0;transition:opacity .4s"></span>
    <span id="authInfo" style="font-size:11px;color:var(--muted)"></span>
    <button class="btn sm ghost" id="btnLogin" onclick="onAuthBtn()">Войти</button>
  </div>
</div>

<!-- ══ Layout ══ -->
<div class="layout">
  <nav class="sidebar">
    <button class="nav-item active" data-nav="search" onclick="navTo('search',this)"><span class="nav-icon" data-icon="search"></span>Поиск</button>
    <button class="nav-item" data-nav="playlists" onclick="navTo('playlists',this)"><span class="nav-icon" data-icon="list"></span>Плейлисты</button>
    <button class="nav-item" data-nav="artists" onclick="navTo('artists',this)"><span class="nav-icon" data-icon="mic"></span>Исполнители</button>
    <button class="nav-item" data-nav="albums" onclick="navTo('albums',this)"><span class="nav-icon" data-icon="disc"></span>Альбомы</button>
    <button class="nav-item" data-nav="dislikes" onclick="navTo('dislikes',this)"><span class="nav-icon" data-icon="heart-break"></span>Дизлайки</button>
    <button class="nav-item" data-nav="downloaded" onclick="navTo('downloaded',this)"><span class="nav-icon" data-icon="music"></span>Скачанные</button>
    <button class="nav-item" data-nav="settings" onclick="navTo('settings',this)"><span class="nav-icon" data-icon="settings"></span>Настройки</button>
    <div style="height:1px;background:var(--border);margin:8px 6px"></div>
    <button class="nav-item" data-nav="download" onclick="navTo('download',this)" style="opacity:.65" title="Дополнительно: скачивание по прямой ссылке">
      <span class="nav-icon" data-icon="link"></span>По ссылке
      <span style="font-size:9px;color:var(--hint);margin-left:auto;flex-shrink:0">доп.</span>
    </button>
    <div class="sidebar-footer">
      <button type="button" class="about-btn" onclick="showAbout()">О проекте</button>
    </div>
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
        <span id="selInfo" style="font-size:12px;color:var(--muted)"></span>
        <div class="toolbar-right">
          <button class="btn accent" id="btnDownload" onclick="startDownload()" style="display:none">▶ Скачать</button>
          <button class="btn danger" id="btnStop" onclick="cancelDownloads()" style="display:none">⏹ Стоп</button>
          <button class="btn ghost sm" id="btnLog" onclick="toggleLog()" title="Показать/скрыть лог">📋 Лог</button>
        </div>
      </div>

      <div class="tl-wrap">
        <div id="tracksHead"></div>
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
        <div class="pl-detail-head">
          <div class="toolbar">
            <button class="btn sm" onclick="closePlaylistDetail()" data-icon="back" data-icon-label="Плейлисты"></button>
            <div class="pl-detail-name">
              <span id="plDetailTitle"></span>
              <button class="iBtn" id="btnPlRename" onclick="promptRenameCurrentPlaylist()" style="display:none" title="Переименовать" data-icon="pencil"></button>
            </div>
            <span id="plDetailCount"></span>
            <input type="text" id="plTrackSearch" class="pl-search" placeholder="Поиск по плейлисту…"
              oninput="onPlTrackSearch()">
            <div class="toolbar-right">
              <button class="iBtn" id="btnPlAddTracks" onclick="togglePlAddPanel()" style="display:none" title="Добавить треки" data-icon="plus"></button>
              <button class="btn accent sm" id="btnPlDownloadAll" onclick="downloadVisibleOrSelected('playlist_detail')" data-icon="download" data-icon-label="Скачать все"></button>
              <button class="iBtn del-btn" id="btnPlDelete" onclick="confirmDeleteCurrentPlaylist()" style="display:none" title="Удалить" data-icon="trash"></button>
            </div>
          </div>
          <div id="plAddPanel">
            <input type="text" id="plAddSearch" placeholder="Найти трек в Яндекс.Музыке…"
              oninput="onPlAddSearchInput()"
              onkeydown="if(event.key==='Escape'){event.preventDefault();closePlAddPanel();}
                else if(event.key==='Enter'){event.preventDefault();runPlAddSearch();}">
            <div id="plAddHint"></div>
            <div id="plAddResults" hidden></div>
          </div>
          <div class="pl-dead-row" id="plDeadRow" hidden>
            <button class="btn sm" id="btnPlDeadFilter" onclick="togglePlDeadFilter()" hidden
              title="Показать только треки, снятые с сервиса">Недоступные</button>
            <button class="btn sm danger" id="btnPlDeadRemove" onclick="confirmRemoveUnavailable()" hidden
              title="Удалить из плейлиста все треки, снятые с сервиса">Удалить недоступные</button>
          </div>
        </div>
        <div class="tl-wrap">
          <div id="plDetailHead"></div>
          <div class="tl-body" id="plDetailBody"></div>
        </div>
      </div>

      <!-- Моя волна -->
      <div id="plWaveWrap" style="display:none;flex-direction:column;flex:1;overflow:hidden;gap:10px">
        <div class="toolbar">
          <button class="btn sm" onclick="closeWave()" data-icon="back" data-icon-label="Плейлисты"></button>
          <span style="font-size:13px;font-weight:600" id="waveTitle">🌊 Моя волна</span>
          <span id="waveCount" style="font-size:12px;color:var(--muted)"></span>
          <div class="toolbar-right">
            <button class="btn sm" onclick="resetWave()" title="Начать волну заново">↻ Заново</button>
            <button class="btn sm" id="btnWaveMore" onclick="loadMoreWave()">▶ Ещё треки</button>
            <button class="btn accent sm" id="btnWaveDownloadAll" onclick="downloadVisibleOrSelected('wave')" data-icon="download" data-icon-label="Скачать все"></button>
          </div>
        </div>
        <div class="tl-wrap">
          <div id="waveHead"></div>
          <div class="tl-body" id="waveBody"></div>
        </div>
      </div>

    </div>

    <!-- ══ ДИЗЛАЙКИ ══ -->
    <div class="page" id="page-dislikes">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Дизлайки</span>
        <button class="btn sm" id="disTabTracks" onclick="showDislikesTab('tracks')">Треки</button>
        <button class="btn sm" id="disTabArtists" onclick="showDislikesTab('artists')">Исполнители</button>
        <button class="btn sm" onclick="loadDislikedLibrary(true)">↻ Обновить</button>
        <span id="dislikesCount" style="font-size:12px;color:var(--muted)"></span>
        <div class="toolbar-right" id="disTracksTools">
          <button class="btn sm accent" id="btnDisDownloadAll" onclick="downloadVisibleOrSelected('dislikes')" data-icon="download" data-icon-label="Скачать все"></button>
        </div>
      </div>
      <div class="tl-wrap" id="dislikesTable" style="flex:1;display:none">
        <div id="dislikesHead"></div>
        <div class="tl-body" id="dislikesBody"></div>
      </div>
      <div id="dislikesAlt" style="flex:1;overflow-y:auto">
        <div class="empty"><span class="empty-icon" data-icon="heart-break"></span><p>Войдите в аккаунт — здесь появятся треки и исполнители, которые вы скрыли из рекомендаций</p></div>
      </div>
    </div>

    <!-- ══ СКАЧАННЫЕ ══ -->
    <div class="page" id="page-downloaded">
      <div class="toolbar">
        <span style="font-size:13px;font-weight:600">Скачанные треки</span>
        <button class="btn sm" onclick="scanDownloaded()">↻ Обновить</button>
        <span id="dlCount" style="font-size:12px;color:var(--muted)"></span>
        <span id="dlSelInfo" style="font-size:12px;color:var(--accent)"></span>
        <div class="toolbar-right">
          <button class="btn sm danger" id="btnDlDeleteSel" onclick="deleteSelectedDownloaded()" style="display:none">🗑 Удалить выбранные</button>
          <button class="btn sm" onclick="window.pywebview.api.open_download_folder()">📂 Открыть папку</button>
        </div>
      </div>
      <div class="tl-wrap" style="flex:1">
        <div id="dlHead"></div>
        <div class="tl-body" id="dlList">
          <div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов</p></div>
        </div>
      </div>
    </div>

    <!-- ══ ИСПОЛНИТЕЛЬ / АЛЬБОМ ══ -->
    <div class="page" id="page-browse">
      <div class="toolbar">
        <button class="btn sm" id="browseBack" onclick="browseBack()"><span data-icon="back"></span><span id="browseBackLabel">Назад</span></button>
        <div class="br-crumb" id="browseCrumb"></div>
        <div class="toolbar-right">
          <button class="btn ghost sm" onclick="closeBrowse()" title="Закрыть (Esc)" data-icon="x"></button>
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
          <div class="s-card-title">ОФОРМЛЕНИЕ</div>
          <div class="s-row">
            <div class="s-label">
              <div class="s-name">Цветовая гамма</div>
              <div class="s-desc">Акцент и оттенки поверхностей. Сохраняется после перезапуска</div>
            </div>
            <div class="s-ctrl"><div class="theme-swatches" id="themeSwatches"></div></div>
          </div>
          <div class="s-row">
            <div class="s-label">
              <div class="s-name">Режим</div>
              <div class="s-desc">Светлая или тёмная тема для выбранной гаммы</div>
            </div>
            <div class="s-ctrl">
              <div class="mode-seg">
                <button type="button" id="btnModeDark" onclick="setUiMode('dark')">Тёмная</button>
                <button type="button" id="btnModeLight" onclick="setUiMode('light')">Светлая</button>
              </div>
            </div>
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
            <div class="s-label">
              <div class="s-name">Плавное переключение</div>
              <div class="s-desc">Приглушение текущего трека и нарастание следующего</div>
            </div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgCrossfadeOn" onchange="onCrossfadeToggle()"><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
          </div>
          <div class="s-row" id="rowCrossfadeSec">
            <div class="s-label">
              <div class="s-name">Длительность перехода, сек</div>
              <div class="s-desc">От 0.5 до 12 · 0 выключает эффект</div>
            </div>
            <div class="s-ctrl"><input type="number" id="cfgCrossfadeSec" value="3" min="0.5" max="12" step="0.5" onchange="onCrossfadeSec()"></div>
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
            <div class="s-label"><div class="s-name">Скачивать текст песен</div><div class="s-desc">LRC и обычный текст в данные приложения, по id трека — не зависят от папки и имени файла</div></div>
            <div class="s-ctrl"><label class="toggle"><input type="checkbox" id="cfgDownloadLyrics"><div class="toggle-track"></div><div class="toggle-thumb"></div></label></div>
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
    </div>

  </div><!-- .main -->
</div><!-- .layout -->

<!-- ══ Mini Player ══ -->
<div class="player hidden" id="player">
  <div class="player-cover-slot" id="plCoverSlot" onclick="openBigView()" title="Развернуть">
    <div class="player-cover-ph" id="plCoverPh" data-icon="music"></div>
    <img class="player-cover" id="plCover" src="" alt="" hidden>
  </div>
  <div class="player-info" onclick="openBigView()" title="Развернуть">
    <div class="player-title" id="plTitle">—</div>
    <div class="player-artist" id="plArtist">—</div>
  </div>
  <button class="iBtn" id="plLocateBtn" onclick="locatePlayingInList()" title="Показать в списке" data-icon="locate"></button>
  <button class="iBtn like-btn" id="plLikeBtn" onclick="toggleLikeCurrent()" title="Мне нравится" data-icon="heart"></button>
  <button class="iBtn dislike-btn" id="plDislikeBtn" onclick="toggleDislikeCurrent()" title="Не рекомендовать" data-icon="heart-break"></button>
  <button class="iBtn" id="plAddBtn" onclick="miniPlayerAdd(event)" title="Добавить в плейлист" data-icon="plus"></button>
  <button class="iBtn" id="plDlBtn" onclick="downloadCurrent()" title="Скачать" data-icon="download"></button>
  <div class="player-controls">
    <button class="btn sm ghost" onclick="playerPrev()" title="Предыдущий трек" data-icon="prev"></button>
    <button class="btn sm ghost skip-btn" onclick="playerSkip(-10)" title="-10 сек" data-icon="skip-back" data-icon-suffix="10"></button>
    <button class="btn sm accent play-main" id="plPlayBtn" onclick="playerToggle()" title="Плей / пауза" data-icon="play"></button>
    <button class="btn sm ghost skip-btn" onclick="playerSkip(10)" title="+10 сек" data-icon="skip-fwd" data-icon-prefix="10"></button>
    <button class="btn sm ghost" onclick="playerNext()" title="Следующий трек" data-icon="next"></button>
  </div>
  <span class="player-time" id="plTime">0:00 / 0:00</span>
  <input type="range" class="player-seek" id="plSeek" value="0" min="0" max="100" step="0.1"
    onpointerdown="_seekPointerDown()" oninput="playerSeek(this.value)" onchange="_seekPointerUp()">
  <div class="player-mode">
    <button class="btn sm ghost" id="btnShuffle" onclick="toggleShuffle()" title="Перемешать" data-icon="shuffle"></button>
    <button class="btn sm ghost" id="btnRepeat" onclick="cycleRepeat()" title="Повтор" data-icon="repeat"></button>
  </div>
  <button class="btn sm ghost" onclick="playerClose()" title="Закрыть плеер" data-icon="x"></button>
  <audio id="audioEl"
    onplay="_onAudioPlay(this)"
    onpause="_onAudioPause(this)"
    onended="_onAudioEnded(this)"
    ontimeupdate="_onAudioTime(this)"
    ondurationchange="_onAudioTime(this)"
    oncanplay="_onAudioCanPlay(this)"
    onerror="_onAudioError(this)"></audio>
  <audio id="audioElB"
    onplay="_onAudioPlay(this)"
    onpause="_onAudioPause(this)"
    onended="_onAudioEnded(this)"
    ontimeupdate="_onAudioTime(this)"
    ondurationchange="_onAudioTime(this)"
    oncanplay="_onAudioCanPlay(this)"
    onerror="_onAudioError(this)"></audio>
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
    <button class="btn sm ghost" style="margin-left:auto" onclick="closeBigView()" title="Свернуть (Esc)" data-icon="x" data-icon-label="Свернуть"></button>
  </div>
  <div class="bigview-body">
    <div class="bigview-cover-slot" id="bigViewCoverSlot" onclick="playerToggle()" title="Плей / пауза">
      <div class="bigview-cover-ph" id="bigViewCoverPh" data-icon="music"></div>
      <img class="bigview-cover" id="bigViewCover" src="" alt="" hidden>
    </div>
    <div class="bigview-info">
      <div class="bigview-title" id="bigViewTitle">—</div>
      <div class="bigview-artist" id="bigViewArtist">—</div>
      <div class="bigview-album" id="bigViewAlbum"></div>

      <div class="bigview-seek">
        <span class="bv-time" id="bvCur">0:00</span>
        <input type="range" class="player-seek" id="bvSeek" value="0" min="0" max="100" step="0.1"
          onpointerdown="_seekPointerDown()" oninput="playerSeek(this.value)" onchange="_seekPointerUp()">
        <span class="bv-time right" id="bvDur">0:00</span>
      </div>

      <div class="bigview-actions">
        <button class="btn sm ghost" id="bvShuffle" onclick="toggleShuffle()" title="Перемешать" data-icon="shuffle"></button>
        <button class="btn sm ghost" onclick="playerPrev()" title="Предыдущий трек" data-icon="prev"></button>
        <button class="btn sm ghost skip-btn" onclick="playerSkip(-10)" title="-10 сек" data-icon="skip-back" data-icon-suffix="10"></button>
        <button class="btn accent play-main play-main-lg" id="bigViewPlayBtn" onclick="playerToggle()" title="Плей / пауза (Пробел)" data-icon="play"></button>
        <button class="btn sm ghost skip-btn" onclick="playerSkip(10)" title="+10 сек" data-icon="skip-fwd" data-icon-prefix="10"></button>
        <button class="btn sm ghost" onclick="playerNext()" title="Следующий трек" data-icon="next"></button>
        <button class="btn sm ghost" id="bvRepeat" onclick="cycleRepeat()" title="Повтор трека" data-icon="repeat"></button>
      </div>

      <div class="bigview-tools">
        <button class="iBtn like-btn" id="bigViewLikeBtn" onclick="toggleLikeCurrent()" title="Мне нравится" data-icon="heart"></button>
        <button class="iBtn dislike-btn" id="bigViewDislikeBtn" onclick="toggleDislikeCurrent()" title="Не рекомендовать" data-icon="heart-break"></button>
        <button class="iBtn" id="bvAddBtn" onclick="bigViewAdd(event)" title="Добавить в плейлист" data-icon="plus"></button>
        <button class="iBtn" id="bvLocateBtn" onclick="locatePlayingInList()" title="Показать в списке" data-icon="locate"></button>
        <button class="iBtn" id="bvWaveBtn" onclick="startTrackWaveCurrent()" title="Волна по треку" data-icon="wave"></button>
        <button class="iBtn" id="bvDlBtn" onclick="downloadCurrent()" title="Скачать трек" data-icon="download"></button>
        <button class="iBtn del-btn" id="bvDelBtn" onclick="bigViewRemove()" title="Удалить из плейлиста" style="display:none" data-icon="trash"></button>
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
   ICONS — единый stroke-набор (24 viewBox)
═══════════════════════════════════════════════════════════════════ */
const _ICONS={
  play:'<path fill="currentColor" stroke="none" d="M8 5.55v12.9c0 .9 1 1.45 1.76.97l10.15-6.45a1.12 1.12 0 0 0 0-1.94L9.76 4.58C9 4.1 8 4.65 8 5.55z"/>',
  pause:'<rect fill="currentColor" stroke="none" x="6.4" y="5" width="3.7" height="14" rx="1.55"/><rect fill="currentColor" stroke="none" x="13.9" y="5" width="3.7" height="14" rx="1.55"/>',
  prev:'<path fill="currentColor" stroke="none" d="M18.7 5.5v13L8 12z"/><rect fill="currentColor" stroke="none" x="5" y="5.5" width="2.15" height="13" rx="1"/>',
  next:'<path fill="currentColor" stroke="none" d="M5.3 5.5v13L16 12z"/><rect fill="currentColor" stroke="none" x="16.85" y="5.5" width="2.15" height="13" rx="1"/>',
  'skip-back':'<path fill="currentColor" stroke="none" d="M19 5.6v12.8L8.4 12z"/><path d="M5 19V5"/>',
  'skip-fwd':'<path fill="currentColor" stroke="none" d="M5 5.6v12.8L15.6 12z"/><path d="M19 5v14"/>',
  heart:'<path d="M19.5 12.57 12 20l-7.5-7.43A5 5 0 1 1 12 6.22a5 5 0 1 1 7.5 6.35z"/>',
  'heart-fill':'<path fill="currentColor" stroke="none" d="M19.5 12.57 12 20l-7.5-7.43A5 5 0 1 1 12 6.22a5 5 0 1 1 7.5 6.35z"/>',
  'heart-break':'<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="m12 7-1.7 2.8 3.2 1.5-2.6 2.7 2.6 1.8"/>',
  'heart-break-fill':'<path fill="currentColor" stroke="none" d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="m12 7-1.7 2.8 3.2 1.5-2.6 2.7 2.6 1.8" stroke="var(--bg)" stroke-width="1.9"/>',
  plus:'<path d="M12 5v14M5 12h14"/>',
  download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/>',
  check:'<path d="M20 6 9 17l-5-5"/>',
  loader:'<path d="M12 3a9 9 0 1 1-8 4.5"/>',
  retry:'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
  trash:'<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/>',
  x:'<path d="M18 6 6 18M6 6l12 12"/>',
  shuffle:'<path d="M16 3h5v5"/><path d="m4 20 17-17"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/>',
  repeat:'<path d="m17 2 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
  'repeat-1':'<path d="m17 2 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/><path d="M11 10h1v5"/>',
  wave:'<path d="M2 10v4M6 7v10M10 4v16M14 7v10M18 10v4"/>',
  search:'<circle cx="11" cy="11" r="6.5"/><path d="m20 20-3.2-3.2"/>',
  list:'<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
  mic:'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M9 21h6"/>',
  disc:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.4"/>',
  music:'<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
  settings:'<circle cx="12" cy="12" r="3"/><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.38a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>',
  link:'<path d="M10 13a5 5 0 0 0 7.07 0l1.42-1.42a5 5 0 0 0-7.07-7.07L10 5.93"/><path d="M14 11a5 5 0 0 0-7.07 0L5.5 12.41a5 5 0 0 0 7.07 7.07L14 18.07"/>',
  external:'<path d="M14 4h6v6"/><path d="M10 14 20 4"/><path d="M20 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h5"/>',
  pencil:'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
  folder:'<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
  refresh:'<path d="M21 12a9 9 0 1 1-2.6-6.3L21 8"/><path d="M21 3v5h-5"/>',
  stop:'<rect fill="currentColor" stroke="none" x="6" y="6" width="12" height="12" rx="2.2"/>',
  log:'<path d="M8 6h13M8 12h13M8 18h8"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
  error:'<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16.5h.01"/>',
  back:'<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
  locate:'<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.15" fill="currentColor" stroke="none"/><path d="M12 2v3.2M12 18.8V22M2 12h3.2M18.8 12H22"/>',
};
_ICONS.gear=_ICONS.settings;
_ICONS['arrow-left']=_ICONS.back;
function icon(name){
  const d=_ICONS[name];
  if(!d) return '';
  const extra=(name==='play'?' ico-play':'')+(name==='loader'?' ico-spin':'');
  return `<svg class="ico${extra}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
}
function _setIcon(el, name){
  if(!el) return;
  el.innerHTML=icon(name);
}
function _dlIconName(st){
  if(st==='done') return 'check';
  if(st==='error') return 'retry';
  if(st==='queued'||st==='downloading') return 'loader';
  return 'download';
}
function _playIconName(playing){ return playing?'pause':'play'; }
function _likeIconHTML(liked, labeled){
  return icon(liked?'heart-fill':'heart')+(labeled?'<span>Нравится</span>':'');
}
function _dislikeIconHTML(on, labeled){
  return icon(on?'heart-break-fill':'heart-break')+(labeled?'<span>'+(on?'Скрыт':'Не рекомендовать')+'</span>':'');
}
function _emptyIcon(name){ return `<span class="empty-icon">${icon(name)}</span>`; }
function _hydrateIcons(root){
  (root||document).querySelectorAll('[data-icon]').forEach(el=>{
    if(el.hasAttribute('data-icon-ok')) return;
    const name=el.getAttribute('data-icon');
    const label=el.getAttribute('data-icon-label');
    const prefix=el.getAttribute('data-icon-prefix');
    const suffix=el.getAttribute('data-icon-suffix');
    el.innerHTML=(prefix?`<span>${prefix}</span>`:'')+icon(name)+(label?`<span>${label}</span>`:'')+(suffix?`<span>${suffix}</span>`:'');
    el.setAttribute('data-icon-ok','');
  });
}
_hydrateIcons();

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
  sortBy: {},
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
  // shuffled play order — permutation of queue indices, walked by next/prev
  shuffleOrder: [],
  shufflePos: -1,
  _shuffleIds: [],
  _awaitingPreview: false,
  _xfadeArmed: false,
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
  pendingPlaylistRenames: {},
  pendingDeadRemoval: false,
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
  sel: { wave: new Set(), playlist_detail: new Set(), browse: new Set(), dislikes: new Set() },
  // страницы исполнителя/альбома: стек переходов + кэш загруженного
  browseStack: [],
  browseCache: {},
  browseOpen: false,
  browseReturn: null,       // id страницы, на которую вернёт «Назад»
  browseOrigin: null,       // вкладка, с которой открыли исполнителя/альбом
  tabBrowse: {},            // вкладка → сохранённый стек страницы исполнителя/альбома
  pendingAdds: {},
  plAddOpen: false,
  plAddResults: [],
  plAddSeq: 0,
  plAddTimer: null,
  plAddQuery: '',
  _plJumpTrackId: '',
  // снимки удалённых строк — чтобы вернуть их назад, если сервер отказал
  pendingRemovals: {},
  likedRemovals: {},
  pendingFileDeletes: {},
  searchDone: false,
  searchArtists: [],
  searchAlbums: [],
  searchSeq: 0,             // отсекает ответы на уже устаревший запрос
  searchTimer: null,
  hasToken: false,
  settingsSaved: null,
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
  dislikedIds: new Set(),
  dislikedPending: new Set(),
  dislikedArtistIds: new Set(),
  dislikedArtists: [],
  dislikedTracks: [],
  dislikedArtistPending: new Set(),
  dislikesTab: 'tracks',
  skipStreak: 0,
  previewRetry: 0,
  previewRetryId: '',
  plTrackQuery: '',
  plDeadFilter: false,
  lyricsCache: {},
  lyricsPending: new Set(),
  lyricLines: null,
  lyricIdx: -1,
  lyricsUserScroll: 0,
  _lyricsAutoScrolling: false,
  coverToken: 0,            // отсекает загрузку обложки уже неактуального трека
  coverColors: {},          // url обложки → 3 цвета для фона
  auroraOn: 'A',            // какой слой aurora сейчас виден
  // заранее подготовленный следующий трек: ссылка + прогретое аудио
  prefetch: { id: null, url: null, audio: null },
  usedPrefetchUrl: false,
  prefetchTimer: null,
  audioId: 'audioEl',
  xfadeRAF: 0,
  uiTheme: 'amber',
  uiMode: 'dark',
  crossfadeSec: 0,
  _jumpPlayingBrowse: false,
  _jumpPlayingList: false,
  _locatePin: false,
  _locatePinTimer: 0,
  _plLocateWait: false,
  _browseLocateWait: false,
  _scrollPlayingRAF: 0,
  _scrollPlayingFix: 0,
  _scrollPlayingTries: 0,
  bigViewOpen: false,
  bigViewTrackId: null,
  bigViewHideTimer: null,
  // снимок играющего трека — переживает смену плейлиста/поиска
  playerTrack: null,
  likeUiTrackId: null,
  likeUiLiked: false,
  confirmAction: null,
  promptAction: null,
  _lastPlaySaveTimer: 0,
  _lastPlayCfgTimer: 0,
  _lastPlaySavedAt: 0,
  _lastPlayPosAt: 0,
  _lastPlayPayload: null,
  _playingPainted: [],
  _savedPosition: 0,
  _resumeAt: 0,
  _queueTruncated: false,
  _restoringPlay: false,
  _seekDrag: false,
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
  const dis=CACHE.read('ym_disliked_library');
  if(dis.data && typeof dis.data==='object'){
    S.dislikedTracks=_applyDlList(dis.data.tracks||[]);
    S.dislikedArtists=dis.data.artists||[];
    S.dislikedIds=new Set(S.dislikedTracks.map(t=>String(t.id)).filter(Boolean));
    S.dislikedArtistIds=new Set(S.dislikedArtists.map(a=>String(a.id)).filter(Boolean));
  }
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
  if(S.myPlaylistsFlat.length){
    S.myPlaylistsFlat=_fillPlaylistCovers(S.myPlaylistsFlat.map(pl=>{
      if(!pl || !pl.cover) return pl;
      const cover=_coverWithSize(pl.cover, '100x100') || pl.cover;
      return cover!==pl.cover ? Object.assign({}, pl, {cover}) : pl;
    }));
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
function _persistDislikes(){
  CACHE.write('ym_disliked_library', {tracks:S.dislikedTracks, artists:S.dislikedArtists});
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
  if(!t || !t.id) return false;
  if(t.status==='downloading' || t.status==='queued') return false;
  const prev=t.status||'idle';
  if(_isDownloaded(t)) t.status='done';
  else if(t.status==='done') t.status='idle';
  return (t.status||'idle')!==prev;
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
  const changed=new Set();
  const bump=t=>{ if(_applyDlStatus(t)) changed.add(String(t.id)); };
  [S.tracks, S.searchResults, S.waveTracks, S.dislikedTracks,
   S.plDetail && S.plDetail.tracks].forEach(list=>(list||[]).forEach(bump));
  Object.values(S.plTracksCache||{}).forEach(list=>{ if(Array.isArray(list)) list.forEach(bump); });
  Object.values(S.browseCache||{}).forEach(d=>{ if(d && Array.isArray(d.tracks)) d.tracks.forEach(bump); });
  (S.browseStack||[]).forEach(en=>{ if(en && en.tracks) en.tracks.forEach(bump); });
  if(!changed.size) return;
  S.tracks.forEach(t=>{
    if(!changed.has(String(t.id))) return;
    const row=document.getElementById('row-'+t.id);
    if(row) updateRow(row,t);
  });
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>{
    (_listFor(src)||[]).forEach(t=>{
      if(changed.has(String(t.id))) _updateExRow(src,t.id);
    });
  });
  if(S.bigViewOpen && changed.has(String(S.playerTrackId))) _fillBigView();
  if(changed.has(String(S.playerTrackId))) _paintPlayerDlBtn();
}

function refreshStaleCaches(force){
  if(force || !CACHE.fresh('ym_pl_cache')) window.pywebview.api.get_my_playlists();
  if(force || !CACHE.fresh('ym_liked_ids')) window.pywebview.api.get_liked_ids();
  if(force || !CACHE.fresh('ym_liked_library')) window.pywebview.api.get_liked_library();
  if(force || !CACHE.fresh('ym_disliked_library')) window.pywebview.api.get_disliked_library();
}
hydrateCaches();
(function(){
  const u=STORE.get('ym_ui', {})||{};
  const ids=['amber','ocean','forest','sunset','violet','graphite'];
  if(ids.includes(u.theme)) S.uiTheme=u.theme;
  if(u.mode==='light' || u.mode==='dark') S.uiMode=u.mode;
  const xf=Number(u.crossfade);
  if(isFinite(xf) && xf>=0) S.crossfadeSec=xf;
  document.documentElement.setAttribute('data-theme', S.uiTheme||'amber');
  document.documentElement.setAttribute('data-mode', S.uiMode||'dark');
})();

/* ═══════════════════════════════════════════════════════════════════
   UTILS
═══════════════════════════════════════════════════════════════════ */
function esc(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function _ruN(n, one, few, many){
  const k=Math.abs(n)%100, k1=k%10;
  if(k>10 && k<20) return n+' '+many;
  if(k1===1) return n+' '+one;
  if(k1>=2 && k1<=4) return n+' '+few;
  return n+' '+many;
}
const COVER_SIZES=['100x100','200x200','300x300','400x400'];
function _coverWithSize(url, size){
  if(!url) return '';
  let s=String(url).replace(/^https:\/\/https:\/\//i,'https://').replace(/^https:\/\/http:\/\//i,'http://');
  if(/\d+x\d+/.test(s)) return s.replace(/\d+x\d+/g, size);
  return s.replace('%%', size);
}
function _playlistGridVisible(){
  const page=document.getElementById('page-playlists');
  const wrap=document.getElementById('plGridWrap');
  return !!(page && page.classList.contains('active') && wrap && wrap.style.display!=='none');
}
function _setCoverSrc(img, url){
  if(!img || !url) return;
  const token=String((parseInt(img.dataset.coverToken||'0',10)||0)+1);
  img.dataset.coverToken=token;
  img.dataset.coverUrl=url;
  img.referrerPolicy='no-referrer';
  img.alt='';
  img.onerror=function(){
    if(img.dataset.coverToken!==token) return;
    plCoverError(img);
  };
  img.onload=function(){ img.dataset.needRetry=''; };
  if(img.getAttribute('src')===url){
    img.removeAttribute('src');
    img.src=url;
  } else {
    img.src=url;
  }
}
function plCoverError(img){
  if(!img) return;
  if(!_playlistGridVisible()){
    img.dataset.needRetry='1';
    return;
  }
  const src=img.dataset.coverUrl || img.getAttribute('src') || '';
  const tried=parseInt(img.dataset.sizeTry||'0',10)||0;
  if(tried<COVER_SIZES.length-1){
    const next=_coverWithSize(src, COVER_SIZES[tried+1]);
    if(next && next!==src){
      img.dataset.sizeTry=String(tried+1);
      _setCoverSrc(img, next);
      return;
    }
  }
  const card=img.closest('.pl-card');
  if(card && card.dataset.kind==='pl' && !img.dataset.trackTried){
    const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===card.dataset.key);
    const trackCover=pl && _firstTrackCover(S.plTracksCache[pl.url]);
    if(trackCover && trackCover!==src){
      img.dataset.trackTried='1';
      img.dataset.sizeTry='0';
      _setCoverSrc(img, trackCover);
      return;
    }
  }
  const kind=card && card.dataset.kind;
  const ph=document.createElement('div');
  ph.className='pl-cover-ph';
  ph.textContent=kind==='artist'?'🎤':(kind==='album'?'💿':'🎵');
  img.replaceWith(ph);
}
function fmtBytes(b){ return b>1e6?(b/1e6).toFixed(1)+' MB':(b/1e3).toFixed(0)+' KB'; }
function fmtTime(s){ s=Math.floor(s||0); if(!isFinite(s)||s<0) s=0; return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`; }
function _apiDurationSec(t){
  if(!t) t=_currentPlayingTrack();
  const ms=t && Number(t.duration_ms);
  return (ms>0 && isFinite(ms)) ? ms/1000 : 0;
}
function _audioDurationSec(a){
  if(!a) return 0;
  const d=Number(a.duration);
  return (isFinite(d) && d>0) ? d : 0;
}
function _playDuration(a, t){
  const media=_audioDurationSec(a);
  const api=_apiDurationSec(t);
  if(media && api) return Math.min(media, api);
  return media || api || 0;
}
function _paintPlaybackTimes(pos, dur, pct){
  pos=Math.max(0, Number(pos)||0);
  dur=Math.max(0, Number(dur)||0);
  if(dur && pos>dur) pos=dur;
  const timeEl=document.getElementById('plTime');
  if(timeEl) timeEl.textContent=`${fmtTime(pos)} / ${fmtTime(dur)}`;
  const cur=document.getElementById('bvCur'), tot=document.getElementById('bvDur');
  if(cur) cur.textContent=fmtTime(pos);
  if(tot) tot.textContent=fmtTime(dur);
  if(S._seekDrag) return;
  if(pct==null) pct=dur ? Math.min(100, pos/dur*100) : 0;
  const val=Number(pct).toFixed(1);
  ['plSeek','bvSeek'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.value=val;
  });
}
function _seekPointerDown(){ S._seekDrag=true; }
function _seekPointerUp(){
  if(!S._seekDrag) return;
  S._seekDrag=false;
  ['plSeek','bvSeek'].forEach(id=>{
    const el=document.getElementById(id);
    if(el && document.activeElement===el){ try{ el.blur(); }catch(_e){} }
  });
  playerTimeUpdate();
}
window.addEventListener('pointerup', _seekPointerUp);
window.addEventListener('pointercancel', _seekPointerUp);

/* Имена исполнителей и альбома как ссылки на их страницы */
function _artistLinks(t){
  const list=(t.artists||[]).filter(a=>a&&a.name);
  if(!list.length) return esc(t.artist||'');
  return list.map(a=>a.id
    ?`<span class="lnk" data-ym-url="${esc(_ymArtistUrl(a.id))}" onclick="event.stopPropagation();openArtist('${esc(a.id)}')">${esc(a.name)}</span>`
    :esc(a.name)).join(', ');
}
function _albumLink(t){
  if(!t.album) return '';
  if(!t.album_id) return esc(t.album);
  return `<span class="lnk" data-ym-url="${esc(_ymAlbumUrl(t.album_id))}" onclick="event.stopPropagation();openAlbum('${esc(t.album_id)}')">${esc(t.album)}</span>`;
}

/* Каскадное появление только что отрисованного списка */
function _playListEnter(el){
  if(!el || S._locatePin) return;
  if(el.childElementCount>24) return;
  el.classList.remove('list-enter');
  void el.offsetWidth;
  el.classList.add('list-enter');
  clearTimeout(el._enterTimer);
  el._enterTimer=setTimeout(()=>el.classList.remove('list-enter'), 550);
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
      const n=el.querySelector('.tl-num-val')||el.querySelector('.tl-num');
      if(n) n.textContent=t.num;
    }
  });
}

/* ═══════════════════════════════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════════════════════════════ */
const NAV_LABELS={
  search:'Поиск', playlists:'Плейлисты', artists:'Исполнители', albums:'Альбомы',
  dislikes:'Дизлайки', downloaded:'Скачанные', settings:'Настройки', download:'По ссылке',
};
function _navBtn(id){ return document.querySelector('.nav-item[data-nav="'+id+'"]'); }
function _visibleTab(){
  if(S.browseOpen) return S.browseOrigin||'search';
  const p=document.querySelector('.page.active');
  if(!p || p.id==='page-browse') return S.browseOrigin||'search';
  return p.id.replace(/^page-/,'');
}
function _activateNav(id){
  document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
  const b=_navBtn(id);
  if(b) b.classList.add('active');
}
function _parkBrowse(){
  if(!S.browseOpen) return;
  const origin=S.browseOrigin||'search';
  S.tabBrowse[origin]={stack:S.browseStack.slice(), scroll:_browseGetScroll()};
  S.browseOpen=false;
  S.browseStack=[];
  const el=document.getElementById('page-browse');
  if(el) el.classList.remove('active');
}
function _restoreBrowse(id){
  const saved=S.tabBrowse[id];
  if(!saved || !saved.stack || !saved.stack.length) return false;
  S.browseStack=saved.stack.slice();
  S.browseOrigin=id;
  S.browseReturn='page-'+id;
  S.browseOpen=true;
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById('page-browse');
  if(el) el.classList.add('active');
  S._jumpPlayingBrowse=!!S.playerTrackId;
  const en=_browseTop();
  const body=document.getElementById('browseBody');
  if(en && body && body.dataset.browseKey===en.type+':'+en.id){
    _paintBrowseChrome(en);
    _paintPlaying();
    _updateSelBtn('browse');
    _paintCardPlayBtns();
    if(S._jumpPlayingBrowse) _tryJumpPlayingBrowse();
    else _browseSetScroll(saved.scroll);
    return true;
  }
  renderBrowse();
  if(!S._jumpPlayingBrowse) _browseSetScroll(saved.scroll);
  return true;
}
function _openTabRoot(id){
  if(id==='playlists') openPlaylistsList();
  else if(id==='artists') openArtistsPage();
  else if(id==='albums') openAlbumsPage();
  else if(id==='dislikes') openDislikesPage();
  else if(id==='downloaded') scanDownloaded();
}
function navTo(id,btn){
  const current=_visibleTab();
  if(current===id){
    delete S.tabBrowse[id];
    if(S.browseOpen){
      S.browseOpen=false;
      S.browseStack=[];
      S.browseOrigin=null;
      S.browseReturn=null;
      const el=document.getElementById('page-browse');
      if(el) el.classList.remove('active');
    }
    showPage(id,btn);
    _openTabRoot(id);
    return;
  }
  showPage(id,btn);
  if(_restoreBrowse(id)) return;
  if(id==='playlists'){
    if(S.plView==='detail'){ _showPlSubView('detail'); _scrollPlayingIntoView(true); }
    else if(S.plView==='wave'){ _showPlSubView('wave'); _scrollPlayingIntoView(true); }
    else openPlaylistsList();
    return;
  }
  _openTabRoot(id);
}
function showPage(id,btn){
  if(S.browseOpen) _parkBrowse();
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const page=document.getElementById('page-'+id);
  if(page) page.classList.add('active');
  _activateNav(id);
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
  ['tracks','search','wave','playlist_detail','browse','dislikes'].forEach(src=>{
    const t=_listFor(src).find(x=>String(x.id)===String(id));
    if(t) t.status=status;
  });
  if(status==='done'){
    const t=['tracks','search','wave','playlist_detail','browse','dislikes']
      .map(src=>_listFor(src).find(x=>String(x.id)===String(id))).find(Boolean);
    _rememberDlTrack(t||{id, title:'', artist:''});
  }
  updateProgress();
  const tMain=S.tracks.find(x=>String(x.id)===String(id));
  const row=tMain && document.getElementById('row-'+tMain.id);
  if(row && tMain) updateRow(row,tMain);
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>_updateExRow(src,id));
  if(status==='done') _syncDlMarks();
  if(S.playerTrack && String(S.playerTrack.id)===String(id)) S.playerTrack.status=status;
  (S.playerQueue||[]).forEach(x=>{ if(String(x.id)===String(id)) x.status=status; });
  if(String(S.playerTrackId)===String(id)) _paintPlayerDlBtn();
  if(S.bigViewOpen && String(S.playerTrackId)===String(id)) _fillBigView();
});

window.addEventListener('py:preview_url', e=>{
  const{track_id,url}=e.detail;
  if(url) S.previewUrls[track_id]=url;
  if(S.previewRetryId===track_id){ S.previewRetry=0; S.previewRetryId=''; }
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
  const d=e.detail||{};
  const id=d.track_id;
  addLog('Превью: '+(d.msg||'ошибка'), d.transient?'info':'err');
  if(id && S.playerTrackId===id){
    const t=_trackFor(S.playerSource, id);
    if(d.transient || d.reason==='no_client' || d.reason==='no_auth'){
      _onPreviewTransient(t||{id, title:id}, d);
      return;
    }
    _skipFromTrack(t||{id, title:id});
    return;
  }
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
  if(S.playerSource==='downloaded'){
    _adoptRestoredSourceQueue('downloaded', _rowsFor('downloaded'));
    if(S.playerTrack){
      const rel=S.playerTrack.rel_path||S.playerTrack.id;
      const f=S.dlFiles.find(x=>x.rel_path===rel || x.id===rel);
      if(f){
        S.playerTrack.cover_uri=f.cover_uri||S.playerTrack.cover_uri||'';
        _paintMiniPlayer(S.playerTrack);
        if(S.bigViewOpen){ S.bigViewTrackId=null; _fillBigView(); }
      }
    }
  }
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
  if(S.settingsSaved) S.settingsSaved.token=e.detail.token;
  _paintAuthBtn(true);
  refreshStaleCaches(true);
});

window.addEventListener('py:auth_error', e=>{
  document.getElementById('authStatus').textContent='Ошибка: '+e.detail.msg;
});

/* ═══════════════════════════════════════════════════════════════════
   AUTH MODAL
═══════════════════════════════════════════════════════════════════ */
function openExt(url){
  if(window.pywebview && window.pywebview.api) window.pywebview.api.open_link(url);
}
function showAbout(){ document.getElementById('aboutModal').classList.remove('hidden'); }
function closeAbout(){ document.getElementById('aboutModal').classList.add('hidden'); }
function _aboutOpen(){
  const el=document.getElementById('aboutModal');
  return !!(el && !el.classList.contains('hidden'));
}
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
  const head=document.getElementById('tracksHead');
  if(!S.tracks.length){
    body.innerHTML=`<div class="empty"><span class="empty-icon">🎵</span><p>Добавьте URL и нажмите «Получить треки»</p></div>`;
    if(head) head.innerHTML='';
    const dl=document.getElementById('btnDownload'); if(dl) dl.style.display='none';
    document.getElementById('selInfo').textContent='';
    return;
  }
  if(head) head.innerHTML=_exHeadHTML('tracks');
  body.innerHTML=_rowsFor('tracks').map(t=>trackRowHTML(t)).join('');
  updateSelUI();
}

function _nowEqHTML(num){
  return `<span class="tl-num-val">${num||''}</span><span class="now-eq" aria-hidden="true"><i></i><i></i><i></i></span>`;
}
function trackRowHTML(t){
  const checked=S.selected.has(t.id)?'checked':'';
  const statusLabel={idle:'—',queued:'В очереди',downloading:'↓',done:'✓ Готово',error:'✗ Ошибка'}[t.status]||'—';
  const dlName=_dlIconName(t.status);
  const dlCls={done:'done',error:'error'}[t.status]||'';
  const dlDis=t.status==='downloading'||t.status==='queued'?'disabled':'';

  const isPlaying=String(S.playerTrackId)===String(t.id);
  const prvCls=isPlaying?'playing':'';
  const playingRow=isPlaying?'playing-row':'';
  const audioEl=isPlaying && _audioNow();
  const pausedCls=isPlaying && audioEl && audioEl.paused?' is-paused':'';
  const playing=isPlaying && audioEl && !audioEl.paused;

  return `<div class="tl-row ${t.status} ${playingRow}${pausedCls}" id="row-${t.id}"
    data-src="tracks" data-tid="${esc(t.id)}"
    onclick="rowPlay(event,'tracks','${t.id}')">
    <input type="checkbox" class="cb" ${checked} onchange="toggleTrack('${t.id}',this.checked)">
    <span class="tl-num">${_nowEqHTML(t.num)}</span>
    <div style="min-width:0">
      <div class="tl-title" title="${esc(t.title)}">${esc(t.title)}</div>
      <div class="tl-sub" title="${esc(t.artist)}">${_artistLinks(t)}</div>
    </div>
    <div class="tl-album" title="${esc(t.album)}">${_albumLink(t)}</div>
    <span class="tl-dur">${t.duration}</span>
    <span class="tl-status s-${t.status}">${statusLabel}</span>
    <button class="iBtn play-btn ${prvCls}" title="Прослушать" onclick="stopRow(event);previewTrack('${t.id}')">${icon(_playIconName(playing))}</button>
    <button class="iBtn ${dlCls}" ${dlDis} title="${t.status==='done'?'Скачан':'Скачать'}" onclick="stopRow(event);downloadOne('${t.id}')">${icon(dlName)}</button>
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
  document.querySelectorAll('#tlBody .tl-row .cb').forEach(cb=>{ cb.checked=v; });
  updateSelUI();
}
function updateSelUI(){
  const n=S.selected.size,total=S.tracks.length;
  document.getElementById('selInfo').textContent=`Выбрано: ${n} из ${total}`;
  _syncHeadCheck('tracks');
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

function _audioNow(){ return document.getElementById(S.audioId||'audioEl'); }
function _audioIdle(){ return document.getElementById((S.audioId||'audioEl')==='audioEl'?'audioElB':'audioEl'); }
function _stopAudioEl(a){
  if(!a) return;
  try{
    a.pause();
    if(a.getAttribute('src')){ a.removeAttribute('src'); a.load(); }
    a.volume=1;
  }catch(_e){}
}
function _cancelCrossfade(){
  if(S.xfadeRAF){ cancelAnimationFrame(S.xfadeRAF); S.xfadeRAF=0; }
}
function _runCrossfade(fromEl, toEl, sec){
  _cancelCrossfade();
  const dur=Math.max(0.15, Number(sec)||0)*1000;
  const t0=performance.now();
  fromEl.volume=1;
  toEl.volume=0;
  const tick=(now)=>{
    const p=Math.min(1, (now-t0)/dur);
    const g=p*p*(3-2*p);
    try{ fromEl.volume=Math.max(0, 1-g); }catch(_e){}
    try{ toEl.volume=Math.min(1, g); }catch(_e){}
    if(p<1){ S.xfadeRAF=requestAnimationFrame(tick); return; }
    S.xfadeRAF=0;
    _stopAudioEl(fromEl);
    try{ toEl.volume=1; }catch(_e2){}
  };
  S.xfadeRAF=requestAnimationFrame(tick);
}

/* ═══════════════════════════════════════════════════════════════════
   PLAYER — ядро
═══════════════════════════════════════════════════════════════════ */
const LAST_PLAY_KEY='ym_last_play';
const LAST_PLAY_CFG_DEBOUNCE=400;

function _compactTrack(t){
  if(!t || typeof t!=='object') return null;
  const id=t.id || t.rel_path || '';
  if(!id && !t.title && !t.name) return null;
  return {
    id: id || t.rel_path || '',
    title: t.title||t.name||'',
    name: t.name||t.title||'',
    artist: t.artist||'',
    album: t.album||'',
    album_id: t.album_id||null,
    cover_uri: t.cover_uri||'',
    cover_uri_tmpl: t.cover_uri_tmpl||'',
    duration: t.duration||'',
    duration_ms: Number(t.duration_ms)||0,
    available: t.available,
    local: !!t.local,
    rel_path: t.rel_path||(t.local?id:''),
    track_id: t.track_id||'',
  };
}
function _validLastPlay(v){
  return !!(v && typeof v==='object' && (v.track || v.trackId));
}
function _syncLastPlayPosition(){
  const a=_audioNow();
  if(a && a.getAttribute('src') && isFinite(a.currentTime)) S._savedPosition=a.currentTime;
}
function _buildLastPlayPayload(){
  if(!S.playerTrackId || !S.playerTrack) return null;
  _syncLastPlayPosition();
  return {
    source: S.playerSource,
    trackId: S.playerTrackId,
    track: _compactTrack(S.playerTrack),
    playingPlaylistUrl: S.playingPlaylistUrl||'',
    playingCardKey: S.playingCardKey||'',
    waveStation: S.playerSource==='wave' ? (S.waveStation||'') : '',
    position: Number(S._savedPosition)||0,
  };
}
function _writeLastPlayPython(payload){
  const api=window.pywebview && window.pywebview.api;
  if(!api) return;
  try{
    const ret=api.save_last_play
      ? api.save_last_play(payload || null)
      : api.save_config({last_play: payload || false});
    if(ret && typeof ret.then==='function') ret.catch(()=>{});
  }catch(_e){}
}
function _scheduleSaveLastPlay(kind){
  if(S._restoringPlay) return;
  if(kind==='time'){
    _syncLastPlayPosition();
    return;
  }
  if(kind==='pos'){
    _syncLastPlayPosition();
    if(S._lastPlayPayload) S._lastPlayPayload.position=Number(S._savedPosition)||0;
    _queueLastPlayWrite();
    return;
  }
  _saveLastPlayIdentity();
}
function _saveLastPlayIdentity(){
  const payload=_buildLastPlayPayload();
  if(!payload) return;
  S._lastPlayPayload=payload;
  try{ STORE.set(LAST_PLAY_KEY, payload); }catch(_e){}
  _queueLastPlayWrite();
}
function _queueLastPlayWrite(){
  if(!S._lastPlayPayload) return;
  if(S._lastPlayCfgTimer) clearTimeout(S._lastPlayCfgTimer);
  S._lastPlayCfgTimer=setTimeout(()=>{
    S._lastPlayCfgTimer=0;
    if(!S._lastPlayPayload) return;
    _syncLastPlayPosition();
    S._lastPlayPayload.position=Number(S._savedPosition)||0;
    _writeLastPlayPython(S._lastPlayPayload);
  }, LAST_PLAY_CFG_DEBOUNCE);
}
function _clearLastPlay(){
  if(S._lastPlaySaveTimer){ clearTimeout(S._lastPlaySaveTimer); S._lastPlaySaveTimer=0; }
  if(S._lastPlayCfgTimer){ clearTimeout(S._lastPlayCfgTimer); S._lastPlayCfgTimer=0; }
  S._savedPosition=0;
  S._resumeAt=0;
  S._queueTruncated=false;
  S._lastPlayPayload=null;
  try{ STORE.del(LAST_PLAY_KEY); }catch(_e){}
  _writeLastPlayPython(null);
}
function _paintRestoredPosition(t, pos){
  const a=_audioNow();
  const mediaReady=a && a.getAttribute('src');
  const dur=_playDuration(mediaReady?a:null, t);
  _paintPlaybackTimes(Math.max(0, Number(pos)||0), dur);
}
function _adoptRestoredSourceQueue(source, tracks){
  if(S.playerSource!==source) return;
  if(!tracks || !tracks.length) return;
  if(S.playerQueue && S.playerQueue.length && !S._queueTruncated) return;
  S.playerQueue=tracks.slice();
  S._queueTruncated=false;
  if(source==='wave') S.waveTracks=S.playerQueue.slice();
  if(S.shuffle) _syncShuffleOrder(_currentIdx());
  if(S.bigViewOpen) _fillBigView();
  _scheduleSaveLastPlay('identity');
}
function _refillRestoredQueue(allowFetch){
  if(!S.playerTrackId) return;
  if(S.playerQueue && S.playerQueue.length>1 && !S._queueTruncated) return;
  const src=S.playerSource;
  const api=allowFetch && window.pywebview && window.pywebview.api;
  if(src==='playlist_detail' && S.playingPlaylistUrl){
    const cached=S.plTracksCache[S.playingPlaylistUrl];
    if(cached && cached.length){ _adoptRestoredSourceQueue(src, cached); return; }
    if(api) api.open_playlist(S.playingPlaylistUrl);
    return;
  }
  if(src==='browse'){
    const key=S.playingCardKey||'';
    if(key.startsWith('album:')){
      const id=key.slice(6);
      const cached=S.browseCache['album:'+id];
      if(cached && cached.tracks && cached.tracks.length){
        _adoptRestoredSourceQueue(src, _applyDlList(cached.tracks.slice()));
        return;
      }
      if(api) api.open_album(id);
      return;
    }
    if(key.startsWith('artist:')){
      const id=key.slice(7);
      const cached=S.browseCache['artist_tracks:'+id] || S.browseCache['artist:'+id];
      if(cached && cached.tracks && cached.tracks.length){
        _adoptRestoredSourceQueue(src, _applyDlList(cached.tracks.slice()));
        if(api && cached.has_more) api.open_artist_tracks(id, (cached.page||0)+1);
        return;
      }
      if(api) api.open_artist_tracks(id, 0);
      return;
    }
  }
  if(src==='dislikes' && (S.dislikedTracks||[]).length)
    _adoptRestoredSourceQueue(src, _rowsFor('dislikes'));
  if(src==='downloaded' && (S.dlFiles||[]).length)
    _adoptRestoredSourceQueue(src, _rowsFor('downloaded'));
  if(src==='wave' && (S.waveTracks||[]).length)
    _adoptRestoredSourceQueue(src, _rowsFor('wave'));
}
function _restoreLastPlay(fromConfig){
  const ls=STORE.get(LAST_PLAY_KEY, null);
  const saved=_validLastPlay(fromConfig) ? fromConfig : (_validLastPlay(ls) ? ls : null);
  if(!saved) return;
  const track=saved.track;
  let id=saved.trackId || (track && (track.id || track.rel_path));
  if(!track || !id) return;
  S._restoringPlay=true;
  S.playerSource=saved.source || 'tracks';
  S.playerTrack=_compactTrack(track) || track;
  S.playerTrackId=id;
  if(S.playerSource==='downloaded'){
    S.playerTrack.local=true;
    S.playerTrack.rel_path=S.playerTrack.rel_path||S.playerTrack.id;
    S.playerTrack.id=S.playerTrack.rel_path;
    S.playerTrackId=S.playerTrack.rel_path;
  }
  S.playingPlaylistUrl=saved.playingPlaylistUrl||'';
  S.playingCardKey=saved.playingCardKey||'';
  if(saved.waveStation) S.waveStation=saved.waveStation;
  if(Array.isArray(saved.waveSeenIds) && saved.waveSeenIds.length) S.waveSeenIds=saved.waveSeenIds;
  const q=(saved.queue||[]).map(x=>_compactTrack(x)||x).filter(Boolean);
  if(S.playerSource==='downloaded'){
    q.forEach(x=>{
      x.local=true;
      x.rel_path=x.rel_path||x.id;
      x.id=x.rel_path;
    });
  }
  S.playerQueue=q.length?q:[S.playerTrack].filter(Boolean);
  S._queueTruncated=q.length<=1;
  S._savedPosition=Math.max(0, Number(saved.position)||0);
  S._resumeAt=0;
  if(S.playerSource==='wave' && q.length){
    S.waveTracks=q.slice();
    S.waveTracks.forEach((t,i)=>{ if(!t.num) t.num=i+1; });
  }
  if(S.playerQueue) _applyDlList(S.playerQueue);
  _refillRestoredQueue(false);
  _setPlaying(S.playerSource, S.playerTrackId);
  if(S.playerTrack) _paintMiniPlayer(S.playerTrack);
  const playerEl=document.getElementById('player');
  if(playerEl) playerEl.classList.remove('hidden');
  const playBtn=document.getElementById('plPlayBtn');
  if(playBtn) _setIcon(playBtn, 'play');
  _paintRestoredPosition(S.playerTrack, S._savedPosition);
  _paintCardPlayBtns();
  S._lastPlayPayload=_buildLastPlayPayload();
  S._restoringPlay=false;
  if(S._lastPlayPayload) _writeLastPlayPython(S._lastPlayPayload);
}
function _resumeLastPlay(){
  const t=_currentPlayingTrack();
  if(!t) return;
  S._resumeAt=Math.max(0, Number(S._savedPosition)||0);
  if(S.playerSource==='downloaded'){
    const rel=t.rel_path||t.id;
    const f=(S.dlFiles||[]).find(x=>x.rel_path===rel)
      || (S.playerQueue||[]).find(x=>x.rel_path===rel || x.id===rel)
      || Object.assign({}, t, {rel_path:rel});
    playLocalFile(f);
    return;
  }
  _playTrack(t, S.playerSource);
}

function _loadAndPlay(trackInfo, url, source){
  if(!url){ S._awaitingPreview=false; return; }
  S.previewUrls[trackInfo.id]=url;
  const awaiting=!!S._awaitingPreview;
  S._awaitingPreview=false;
  _setPlaying(source, trackInfo.id);
  _paintMiniPlayer(trackInfo);
  _warmNowPlaying(trackInfo);
  document.getElementById('player').classList.remove('hidden');
  const fade=Math.max(0, Number(S.crossfadeSec)||0);
  const cur=_audioNow();
  const next=_audioIdle();
  // Кроссфейд только если ссылка уже была (prefetch/кэш). Поздний ответ
  // API не должен накладывать новый трек на доигрывающий старый.
  const canFade=!awaiting && fade>0 && cur && next && cur.getAttribute('src') && !cur.paused && !cur.ended;
  _cancelCrossfade();
  if(canFade){
    next.volume=0;
    next.src=url;
    S.audioId=next.id;
    next.play().catch(()=>{});
    _runCrossfade(cur, next, fade);
  } else {
    _stopAudioEl(next);
    if(cur){
      cur.volume=1;
      cur.src=url;
      cur.play().catch(()=>{});
    }
  }
  _schedulePrefetch();
}

function _trackPlayable(t){
  if(!t) return false;
  if(t.local) return true;
  // Только явный available===false от API. Нет duration / нет превью — не «снят».
  return t.available!==false;
}
function _onPreviewTransient(t, d){
  S.skipStreak=0;
  const id=t && t.id;
  const reason=d && d.reason;
  if(reason==='no_auth'){
    _updatePlayBtn();
    showToast({kind:'err', icon:'⊘', message:'Войдите в Яндекс.Музыку'});
    return;
  }
  const tries=(S.previewRetryId===id)?(S.previewRetry||0):0;
  if(tries>=1){
    S.previewRetry=0;
    S.previewRetryId='';
    _updatePlayBtn();
    showToast({kind:'err', icon:'⊘', message:'Нет связи с Яндекс.Музыкой. Нажмите Play ещё раз.'});
    return;
  }
  S.previewRetry=tries+1;
  S.previewRetryId=id||'';
  setTimeout(()=>{
    if(!id || S.playerTrackId!==id) return;
    if(window.pywebview && window.pywebview.api) window.pywebview.api.get_preview_url(id);
  }, 600);
}
function _fisherYates(arr){
  for(let i=arr.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    const t=arr[i]; arr[i]=arr[j]; arr[j]=t;
  }
  return arr;
}
function _shuffleListIds(){
  const list=_queue();
  const field=_idField(S.playerSource);
  return list.map(x=>String(x[field]||x.id||''));
}
function _clearShuffleOrder(){
  S.shuffleOrder=[];
  S.shufflePos=-1;
  S._shuffleIds=[];
}
function _syncShuffleOrder(curIdx){
  const ids=_shuffleListIds();
  const n=ids.length;
  if(!S.shuffle){
    _clearShuffleOrder();
    return;
  }
  if(!n){
    S.shuffleOrder=[];
    S.shufflePos=-1;
    S._shuffleIds=ids;
    return;
  }
  const prev=S._shuffleIds||[];
  const prefixLen=Math.min(prev.length, n);
  const samePrefix=!prev.length || prev.slice(0, prefixLen).every((id,i)=>ids[i]===id);
  const compatible=S.shuffleOrder.length && samePrefix && prev.length>0;

  if(compatible){
    let order=S.shuffleOrder.filter(i=>i>=0 && i<n);
    if(n>prev.length){
      const fresh=[];
      for(let i=prev.length;i<n;i++) fresh.push(i);
      const pos=(curIdx>=0 && order.indexOf(curIdx)>=0)
        ? order.indexOf(curIdx)
        : Math.max(0, S.shufflePos);
      const head=order.slice(0, pos+1);
      const mixed=_fisherYates(order.slice(pos+1).concat(fresh));
      order=head.concat(mixed);
    }
    S.shuffleOrder=order;
    S._shuffleIds=ids;
    if(curIdx>=0){
      const p=order.indexOf(curIdx);
      S.shufflePos=p>=0?p:0;
    } else if(S.shufflePos<0 || S.shufflePos>=order.length){
      S.shufflePos=0;
    }
    return;
  }

  const order=[];
  for(let i=0;i<n;i++) order.push(i);
  _fisherYates(order);
  if(curIdx>=0){
    const p=order.indexOf(curIdx);
    if(p>0) S.shuffleOrder=order.slice(p).concat(order.slice(0,p));
    else S.shuffleOrder=order;
    S.shufflePos=0;
  } else {
    S.shuffleOrder=order;
    S.shufflePos=0;
  }
  S._shuffleIds=ids;
}
function _nextPlayableIndex(fromIdx, dir, opts){
  opts=opts||{};
  const list=_queue();
  const len=list.length;
  if(!len) return -1;
  const start=fromIdx>=0?fromIdx:-1;
  if(opts.shuffle){
    _syncShuffleOrder(start);
    const order=S.shuffleOrder;
    if(!order.length) return -1;
    let pos=start>=0 ? order.indexOf(start) : S.shufflePos;
    if(pos<0) pos=S.shufflePos>=0?S.shufflePos:0;
    for(let n=1;n<=order.length;n++){
      let p=pos+dir*n;
      if(opts.wrap) p=((p%order.length)+order.length)%order.length;
      else if(p<0||p>=order.length) return -1;
      if(p===pos) return -1;
      const idx=order[p];
      if(idx!==start && _trackPlayable(list[idx])) return idx;
    }
    return -1;
  }
  for(let n=1;n<=len;n++){
    let idx=start+dir*n;
    if(opts.wrap) idx=((idx%len)+len)%len;
    else if(idx<0||idx>=len) return -1;
    if(idx===start) return -1;
    if(_trackPlayable(list[idx])) return idx;
  }
  return -1;
}
function _firstPlayable(list){
  return (list||[]).find(_trackPlayable) || null;
}
function _skipFromTrack(t, reason){
  S.skipStreak=(S.skipStreak||0)+1;
  const title=(t && (t.title||t.name)) || 'трек';
  addLog(reason==='dead'?`Пропуск: «${title}» недоступен`:`Пропуск: «${title}»`,'info');
  const list=_queue();
  const from=t ? list.findIndex(x=>x.id===t.id) : _currentIdx();
  if(S.skipStreak>Math.max(12, list.length||0)){
    S.skipStreak=0;
    _updatePlayBtn();
    return;
  }
  const idx=_nextPlayableIndex(from, 1, {shuffle:S.shuffle, wrap:_queueWrap()});
  if(idx<0){
    if(S.playerSource==='wave'){
      S.pendingWavePlay='next';
      loadMoreWave();
      return;
    }
    _startMyWaveAuto();
    return;
  }
  _goToIndex(idx);
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
  if(source && source!=='downloaded' && !_trackPlayable(t)){
    if(source) S.playerSource=source;
    _skipFromTrack(t, 'dead');
    return;
  }
  document.getElementById('player').classList.remove('hidden');
  document.getElementById('plPlayBtn').innerHTML=icon('loader');
  const cached=S.previewUrls[t.id] || (S.prefetch.id===t.id && S.prefetch.url);
  S._awaitingPreview=!cached;
  if(cached){
    _loadAndPlay(t, cached, source);
    return;
  }
  _setPlaying(source, t.id);
  _paintMiniPlayer(t);
  _warmNowPlaying(t);
  window.pywebview.api.get_preview_url(t.id);
}

function _queueWrap(){
  // Shuffle держит свою перестановку по кругу — как старый random, без ухода в волну.
  // Волна wrap не делает: в конце подгружаем ещё треки.
  return !!(S.shuffle && S.playerSource!=='wave');
}
function _peekNextIndex(){
  const cur=_currentIdx();
  if(cur<0 || _listLen()<=1) return -1;
  return _nextPlayableIndex(cur, 1, {shuffle:S.shuffle, wrap:_queueWrap()});
}
function _peekNextTrack(){
  const idx=_peekNextIndex();
  if(idx<0) return null;
  return _queue()[idx] || null;
}
function _peekNext(){
  if(S.playerSource==='downloaded') return null;
  return _peekNextTrack();
}
function _nextUrl(t){
  if(!t) return '';
  return S.previewUrls[t.id] || (S.prefetch.id===t.id && S.prefetch.url) || '';
}
function _maybeCrossfadeAdvance(a, dur, pos){
  const fade=Math.max(0, Number(S.crossfadeSec)||0);
  if(fade<=0 || S.repeat==='one' || S._awaitingPreview) return;
  if(!a || a.paused || a.ended || S.xfadeRAF) return;
  if(!dur || pos < dur - fade){
    if(dur && pos < dur - fade - 0.4) S._xfadeArmed=false;
    return;
  }
  if(S._xfadeArmed) return;
  const idx=_peekNextIndex();
  if(idx<0) return;
  const next=_queue()[idx];
  if(!next || next.id===S.playerTrackId) return;
  if(!_nextUrl(next)) return;
  S._xfadeArmed=true;
  _goToIndex(idx);
}
function _schedulePrefetch(){
  if(S.prefetchTimer) clearTimeout(S.prefetchTimer);
  // Даём текущему треку первым занять сеть, потом готовим следующий
  S.prefetchTimer=setTimeout(_prefetchNext, S.shuffle ? 200 : 500);
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
  _requestLyrics(_lyricsLookupId(t) || t.id);
  _prefetchCover(t, true);
}
function _lyricsLookupId(t){
  if(!t) return '';
  if(t.local || S.playerSource==='downloaded'){
    let tid=String(t.track_id||'');
    if(!tid){
      const rel=String(t.rel_path||t.id||'');
      const f=(S.dlFiles||[]).find(x=>x.rel_path===rel || x.id===rel);
      if(f && f.track_id) tid=String(f.track_id);
    }
    return tid;
  }
  return String(t.id||'');
}
function _lyricsCacheKey(id){
  id=String(id||'');
  if(!id) return '';
  return S.playerSource==='downloaded' ? 'local:'+id : id;
}
function _requestLyrics(trackId){
  if(!trackId) return;
  const key=_lyricsCacheKey(trackId);
  if(!key) return;
  if(Object.prototype.hasOwnProperty.call(S.lyricsCache, key)) return;
  if(S.lyricsPending.has(key)) return;
  S.lyricsPending.add(key);
  if(S.playerSource==='downloaded')
    window.pywebview.api.get_local_lyrics(trackId);
  else
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
  const ph=document.getElementById('plCoverPh');
  const url=_bigCoverUrl(t,'100x100') || t.cover_uri || _localFileCoverUrl(t) || '';
  if(!url){
    _showCoverPlaceholder(cover, ph);
  } else {
    const token=String((parseInt(cover.dataset.coverToken||'0',10)||0)+1);
    cover.dataset.coverToken=token;
    cover.onload=()=>{ if(cover.dataset.coverToken===token) _revealCoverImage(cover, ph); };
    cover.onerror=()=>{ if(cover.dataset.coverToken===token) _showCoverPlaceholder(cover, ph); };
    if(cover.getAttribute('src')===url && cover.naturalWidth){
      _revealCoverImage(cover, ph);
    } else {
      cover.src=url;
      if(cover.complete){
        if(cover.naturalWidth) _revealCoverImage(cover, ph);
        else _showCoverPlaceholder(cover, ph);
      }
    }
  }
  _paintPlayerDlBtn();
  _updateMediaSession();
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
function _paintPlaying(){
  const audio=_audioNow();
  const playing=!!(S.playerTrackId && audio && !audio.paused);
  (S._playingPainted||[]).forEach(row=>{
    if(!row || !row.isConnected) return;
    row.classList.remove('playing-row','is-paused','dl-playing');
    const btn=row.querySelector('.play-btn');
    if(btn){
      btn.classList.remove('playing');
      _setIcon(btn,'play');
    }
  });
  const next=[];
  _playingRowEls().forEach(row=>{
    if(row.classList.contains('dl-row')){
      row.classList.add('dl-playing');
      const btn=row.querySelector('.play-btn');
      if(btn){ _setIcon(btn, playing?'pause':'play'); btn.title=playing?'Играет':'Воспроизвести'; }
      next.push(row);
      return;
    }
    row.classList.add('playing-row');
    row.classList.toggle('is-paused', !playing);
    const btn=row.querySelector('.play-btn');
    if(btn){
      btn.classList.add('playing');
      _setIcon(btn, playing?'pause':'play');
    }
    next.push(row);
  });
  S._playingPainted=next;
}
function _playingRowEls(){
  const id=S.playerTrackId;
  if(id==null || id==='') return [];
  const out=[];
  const add=el=>{ if(el) out.push(el); };
  add(document.getElementById('row-'+id));
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>add(document.getElementById('exrow-'+src+'-'+id)));
  if(S.playerSource==='downloaded'){
    const f=(S.dlFiles||[]).find(x=>x.rel_path===id || x.id===id);
    if(f) add(document.getElementById('dlrow-'+f.uid));
  }
  return out;
}
function _locateActive(){
  return !!(S._locatePin || S._jumpPlayingBrowse || S._jumpPlayingList);
}
function _beginLocatePin(){
  S._locatePin=true;
  S._jumpPlayingBrowse=true;
  S._jumpPlayingList=true;
  S._scrollPlayingTries=0;
  if(S._locatePinTimer) clearTimeout(S._locatePinTimer);
  S._locatePinTimer=setTimeout(_endLocatePin, 8000);
}
function _endLocatePin(){
  if(S._locatePinTimer){ clearTimeout(S._locatePinTimer); S._locatePinTimer=0; }
  if(S._jumpPlayingTimer){ clearTimeout(S._jumpPlayingTimer); S._jumpPlayingTimer=0; }
  if(S._scrollPlayingFix){ clearTimeout(S._scrollPlayingFix); S._scrollPlayingFix=0; }
  S._locatePin=false;
  S._jumpPlayingBrowse=false;
  S._jumpPlayingList=false;
  S._plLocateWait=false;
  S._browseLocateWait=false;
  S._scrollPlayingTries=0;
}
function _activePlayingRow(){
  const page=document.querySelector('.page.active');
  if(!page) return null;
  return _playingRowEls().find(el=>page.contains(el)) || null;
}
function _isTrackRow(el){
  return !!(el && el.classList && (el.classList.contains('ex-row') || el.classList.contains('tl-row') || el.classList.contains('dl-row')));
}
function _flatListRowIndex(row, scroller){
  if(!row || !scroller || row.parentElement!==scroller) return -1;
  let idx=0, n=scroller.firstElementChild;
  while(n){
    if(n===row) return idx;
    if(_isTrackRow(n)) idx++;
    n=n.nextElementSibling;
  }
  return -1;
}
function _offsetInScroller(row, scroller){
  const idx=_flatListRowIndex(row, scroller);
  const h=row.offsetHeight||46;
  if(idx>=0) return idx*h;
  let y=0, n=row;
  while(n && n!==scroller){
    y+=n.offsetTop;
    const next=n.offsetParent;
    if(!next || next===n) break;
    if(next===scroller || scroller.contains(next)){ n=next; continue; }
    const er=row.getBoundingClientRect(), sr=scroller.getBoundingClientRect();
    return scroller.scrollTop+(er.top-sr.top);
  }
  if(n===scroller) return y;
  const er=row.getBoundingClientRect(), sr=scroller.getBoundingClientRect();
  return scroller.scrollTop+(er.top-sr.top);
}
function _setScrollTop(scroller, top){
  const max=Math.max(0, scroller.scrollHeight-scroller.clientHeight);
  top=Math.max(0, Math.min(top, max));
  if(typeof scroller.scrollTo==='function') scroller.scrollTo({top, behavior:'auto'});
  else scroller.scrollTop=top;
}
function _playingRowInView(){
  const row=_activePlayingRow();
  if(!row || !row.isConnected) return false;
  const scroller=_rowScroller(row);
  const rr=row.getBoundingClientRect();
  if(!rr.height) return false;
  if(!scroller) return rr.bottom>0 && rr.top<window.innerHeight;
  const sr=scroller.getBoundingClientRect();
  return rr.bottom>sr.top+8 && rr.top<sr.bottom-8;
}
function _browseJumpSettled(){
  const en=_browseTop();
  if(!en || en.loading || en.loadingMore || en.error) return false;
  if(en.type==='artist_tracks') return !en.hasMore && !!(en.tracks&&en.tracks.length);
  return true;
}
function _tryFinishLocate(){
  if(!_locateActive()) return;
  if(!_playingRowInView()) return;
  if(S.playerSource==='browse' && !_browseJumpSettled()) return;
  if(S._plLocateWait || S._browseLocateWait) return;
  _endLocatePin();
}
function _scrollPlayingIntoView(force){
  const id=S.playerTrackId;
  if(id==null || id==='') return;
  if(S._scrollPlayingRAF) cancelAnimationFrame(S._scrollPlayingRAF);
  const go=()=>{
    S._scrollPlayingRAF=0;
    const row=_activePlayingRow();
    if(!row) return;
    const scroller=_rowScroller(row);
    if(!scroller){
      row.scrollIntoView({block:'center', behavior:'auto'});
      _tryFinishLocate();
      return;
    }
    if(!force){
      const rr=row.getBoundingClientRect(), sr=scroller.getBoundingClientRect();
      if(rr.height && rr.top>=sr.top+10 && rr.bottom<=sr.bottom-10){
        _tryFinishLocate();
        return;
      }
    }
    const h=row.offsetHeight||46;
    const top=_offsetInScroller(row, scroller)-(scroller.clientHeight-h)/2;
    _setScrollTop(scroller, top);
    requestAnimationFrame(()=>{
      if(!row.isConnected) return;
      const rr=row.getBoundingClientRect(), sr=scroller.getBoundingClientRect();
      if(rr.height && sr.height){
        const mid=sr.top+(sr.height-rr.height)/2;
        if(Math.abs(rr.top-mid)>6)
          _setScrollTop(scroller, scroller.scrollTop+(rr.top-mid));
      }
      if(S._scrollPlayingFix) clearTimeout(S._scrollPlayingFix);
      S._scrollPlayingFix=setTimeout(()=>{
        S._scrollPlayingFix=0;
        if(!_locateActive() && !force) return;
        if(!_playingRowInView() && (S._scrollPlayingTries||0)<3){
          S._scrollPlayingTries=(S._scrollPlayingTries||0)+1;
          _scrollPlayingIntoView(true);
          return;
        }
        _tryFinishLocate();
      }, 80);
    });
  };
  S._scrollPlayingRAF=requestAnimationFrame(()=>requestAnimationFrame(go));
}
function _rowScroller(el){
  let p=el && el.parentElement;
  let named=null;
  while(p && p!==document.body){
    if(p.classList && (p.classList.contains('tl-body') || p.classList.contains('ex-body'))){
      const s=getComputedStyle(p);
      if(s.overflowY==='auto' || s.overflowY==='scroll'){
        if(p.scrollHeight>p.clientHeight+4) return p;
        if(!named) named=p;
      }
    }
    p=p.parentElement;
  }
  if(named) return named;
  p=el && el.parentElement;
  while(p && p!==document.body){
    const s=getComputedStyle(p);
    if((s.overflowY==='auto'||s.overflowY==='scroll') && p.scrollHeight>p.clientHeight+4)
      return p;
    p=p.parentElement;
  }
  return null;
}
function _browseJumpReady(){
  const en=_browseTop();
  if(!en || en.loading || en.error) return false;
  if(en.type==='artist_tracks'){
    if(!(en.tracks&&en.tracks.length) || (en.loadingMore && !_browsePlayingRow())) return false;
    return !en.hasMore || !!_browsePlayingRow();
  }
  return true;
}
function _browsePlayingRow(){
  const page=document.getElementById('page-browse');
  if(!page || !page.classList.contains('active')) return null;
  const en=_browseTop();
  if(en && en.loading) return null;
  return _playingRowEls().find(el=>page.contains(el)) || null;
}
function _tryJumpPlayingBrowse(){
  if(!S._jumpPlayingBrowse && !S._locatePin) return false;
  if(S.playerTrackId==null || S.playerTrackId===''){
    _endLocatePin();
    return false;
  }
  const page=document.getElementById('page-browse');
  if(!page || !page.classList.contains('active')) return false;
  if(!_browseJumpReady()) return false;
  const row=_browsePlayingRow();
  if(!row){
    if(S._jumpPlayingTimer) clearTimeout(S._jumpPlayingTimer);
    S._jumpPlayingTimer=setTimeout(()=>{
      S._jumpPlayingTimer=0;
      if(!_locateActive() || !_browseJumpReady()) return;
      if(_browsePlayingRow()){
        _scrollPlayingIntoView(true);
        return;
      }
      if(!_locateActive() || _browseJumpSettled()) _endLocatePin();
    }, 160);
    return false;
  }
  _scrollPlayingIntoView(true);
  return true;
}

function _playingRowOnActivePage(){
  const page=document.querySelector('.page.active');
  if(!page) return false;
  return !!_playingRowEls().find(el=>page.contains(el));
}
function _playingSourceVisible(){
  const src=S.playerSource;
  if(src==='playlist_detail'){
    const page=document.getElementById('page-playlists');
    return !!(page && page.classList.contains('active') && S.plView==='detail'
      && (!S.playingPlaylistUrl || S.plDetail.url===S.playingPlaylistUrl));
  }
  if(src==='wave'){
    const page=document.getElementById('page-playlists');
    return !!(page && page.classList.contains('active') && S.plView==='wave');
  }
  if(src==='browse'){
    const page=document.getElementById('page-browse');
    if(!S.browseOpen || !page || !page.classList.contains('active')) return false;
    const en=_browseTop();
    if(!en) return false;
    const key=S.playingCardKey||'';
    if(key.startsWith('album:')) return en.type==='album' && String(en.id)===key.slice(6);
    if(key.startsWith('artist:')){
      const id=key.slice(7);
      return en.type==='artist_tracks' && String(en.id)===id;
    }
    return true;
  }
  if(src==='search'){
    const page=document.getElementById('page-search');
    return !S.browseOpen && !!(page && page.classList.contains('active'));
  }
  if(src==='dislikes'){
    const page=document.getElementById('page-dislikes');
    return !S.browseOpen && !!(page && page.classList.contains('active'));
  }
  if(src==='downloaded'){
    const page=document.getElementById('page-downloaded');
    return !S.browseOpen && !!(page && page.classList.contains('active'));
  }
  if(src==='tracks'){
    const page=document.getElementById('page-download');
    return !S.browseOpen && !!(page && page.classList.contains('active'));
  }
  return false;
}
function locatePlayingInList(){
  if(!S.playerTrackId){
    showToast({kind:'info', icon:'⊘', message:'Сейчас ничего не играет'});
    return;
  }
  if(S.bigViewOpen) closeBigView();
  _beginLocatePin();
  if(_playingSourceVisible() && _playingRowOnActivePage()){
    _scrollPlayingIntoView(true);
    return;
  }
  _revealPlayingSource();
}
function _revealPlayingSource(){
  const src=S.playerSource;
  const key=S.playingCardKey||'';
  if(src==='playlist_detail'){
    const url=S.playingPlaylistUrl || (S.plDetail && S.plDetail.url) || '';
    showPage('playlists', _navBtn('playlists'));
    const pl=(S.myPlaylistsFlat||[]).find(p=>p.url===url);
    if(pl){ openPlaylist(pl); return; }
    S.plView='detail';
    _showPlSubView('detail');
    if((S.plDetail.tracks||[]).length) renderPlaylistDetail({jumpPlaying:true});
    else _scrollPlayingIntoView(true);
    return;
  }
  if(src==='wave'){
    _goPlaylistsWave();
    _scrollPlayingIntoView(true);
    return;
  }
  if(src==='browse'){
    if(key.startsWith('album:')){
      openAlbum(key.slice(6));
      return;
    }
    if(key.startsWith('artist:')){
      openArtistTracks(key.slice(7));
      return;
    }
    if(S.browseStack.length){
      _openBrowseView();
      S._jumpPlayingBrowse=true;
      _tryJumpPlayingBrowse();
      return;
    }
    showToast({kind:'info', icon:'⊘', message:'Список этого трека уже закрыт'});
    return;
  }
  if(src==='search'){
    showPage('search', _navBtn('search'));
    _scrollPlayingIntoView(true);
    return;
  }
  if(src==='dislikes'){
    showPage('dislikes', _navBtn('dislikes'));
    _scrollPlayingIntoView(true);
    return;
  }
  if(src==='downloaded'){
    showPage('downloaded', _navBtn('downloaded'));
    _scrollPlayingIntoView(true);
    return;
  }
  if(src==='tracks'){
    showPage('download', _navBtn('download'));
    _scrollPlayingIntoView(true);
    return;
  }
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
    ? (_listFor(source).find(x=>String(x.rel_path||x.id)===String(id))
      || (S.playerQueue||[]).find(x=>String(x.rel_path||x.id)===String(id)))
    : (_listFor(source).find(x=>String(x.id)===String(id)) || (S.playerQueue||[]).find(x=>String(x.id)===String(id)));
  S.playerTrack = found
    ? (source==='downloaded' ? (found.local ? found : _dlAsTrack(found)) : found)
    : (S.playerTrack && (String(S.playerTrack.id)===String(id) || String(S.playerTrack.rel_path||'')===String(id)) ? S.playerTrack : null);
  const changed = prevSource!==source || prevId!==id;
  if(changed) S._xfadeArmed=false;
  if(S.shuffle) _syncShuffleOrder(_currentIdx());
  else if(changed) _clearShuffleOrder();
  if(changed){
    // Старый трек нужно остановить сразу же, иначе он продолжает двигать
    // полосу перемотки, пока в шапке уже показан следующий
    if(!S._restoringPlay){
      S._savedPosition=0;
      S._resumeAt=0;
      _resetPlaybackUI(found || S.playerTrack);
    }
  }
  _paintPlaying();
  _updateLikeButtons();
  if(S.bigViewOpen) _fillBigView();
  if(!S._restoringPlay && changed) _scheduleSaveLastPlay('identity');
}

/* Обнуляет прогресс и показывает длительность нового трека до его загрузки */
function _resetPlaybackUI(t){
  S._seekDrag=false;
  _paintPlaybackTimes(0, _apiDurationSec(t), 0);
}

/* Полная перерисовка — нужна только когда меняется сразу весь набор данных */
function _rerenderActive(){
  renderTracks();
  renderDownloaded(S.dlFiles);
  renderSearchResults();
  if(S.plView==='detail') renderPlaylistDetail();
  if(S.plView==='wave') renderWave();
  if(S.browseOpen) renderBrowse();
  renderDislikes();
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
  const rel=f.rel_path||f.id||'';
  return {
    id:rel,
    title:f.title||f.name||'—',
    artist:f.artist||'',
    artists:[],
    album:f.album||'',
    album_id:null,
    track_id:f.track_id||'',
    cover_uri:_dlCoverUrl(f),
    cover_uri_tmpl:'',
    duration:f.duration||'',
    duration_ms:f.duration_ms||0,
    local:true,
    rel_path:rel,
  };
}
function _trackFor(source,id){
  if(!source||!id) return null;
  if(source==='downloaded'){
    const f=_listFor('downloaded').find(x=>String(x.rel_path||x.id)===String(id));
    if(f) return _dlAsTrack(f);
    const q=(S.playerQueue||[]).find(x=>String(x.rel_path||x.id)===String(id));
    if(q) return q.local ? q : _dlAsTrack(q);
    return (S.playerTrack && (String(S.playerTrack.id)===String(id) || String(S.playerTrack.rel_path||'')===String(id))) ? S.playerTrack : null;
  }
  return _listFor(source).find(x=>String(x.id)===String(id))
    || (S.playerQueue||[]).find(x=>String(x.id)===String(id))
    || (S.playerTrack && String(S.playerTrack.id)===String(id) ? S.playerTrack : null);
}
function _currentPlayingTrack(){
  return _trackFor(S.playerSource, S.playerTrackId);
}
function _updateLikeButtons(){
  const t=_currentPlayingTrack();
  const liked=!!(t && S.likedIds.has(t.id));
  const disliked=!!(t && S.dislikedIds.has(t.id));
  const id=t?t.id:null;
  const vis=(t && S.playerSource!=='downloaded')?'':'hidden';
  // «Пшик» сердечка только когда лайк поставили у того же трека, а не при его смене
  const pop = liked && id===S.likeUiTrackId && !S.likeUiLiked;
  S.likeUiTrackId=id;
  S.likeUiLiked=liked;
  [document.getElementById('plLikeBtn'), document.getElementById('bigViewLikeBtn')].forEach(btn=>{
    if(!btn) return;
    btn.classList.toggle('liked', liked);
    _setIcon(btn, liked?'heart-fill':'heart');
    btn.style.visibility=vis;
    if(pop){
      btn.classList.remove('pop');
      void btn.offsetWidth;
      btn.classList.add('pop');
    }
  });
  [document.getElementById('plDislikeBtn'), document.getElementById('bigViewDislikeBtn')].forEach(btn=>{
    if(!btn) return;
    btn.classList.toggle('disliked', disliked);
    _setIcon(btn, disliked?'heart-break-fill':'heart-break');
    btn.style.visibility=vis;
  });
  const add=document.getElementById('plAddBtn');
  if(add) add.style.visibility=vis;
  _paintPlayerDlBtn();
}
function _paintPlayerDlBtn(){
  const t=_currentPlayingTrack();
  const local=S.playerSource==='downloaded' || !!(t && t.local);
  const dead=!!(t && !_trackPlayable(t));
  const st=(t && t.status) || 'idle';
  const extra={done:'done',error:'error'}[st]||'';
  const busy=st==='downloading'||st==='queued';
  const hide=!t || local;
  const title=!t?'':(local?'Уже на диске':dead?'Недоступен':st==='done'?'Скачан':st==='error'?'Повторить':'Скачать');
  const disabled=!t || local || dead || busy || st==='done';
  const paint=(btn, useVis)=>{
    if(!btn) return;
    btn.className='iBtn'+(extra?' '+extra:'');
    btn.disabled=disabled;
    btn.title=title;
    _setIcon(btn, _dlIconName(st));
    if(useVis) btn.style.visibility=hide?'hidden':'';
  };
  paint(document.getElementById('plDlBtn'), true);
  paint(document.getElementById('bvDlBtn'), false);
}
function toggleLike(source,id){
  const t=_listFor(source).find(x=>x.id===id) || _trackFor(source,id);
  if(!t || S.likedPending.has(id)) return;
  const nextLiked=!S.likedIds.has(id);
  S.likedPending.add(id);
  if(nextLiked){
    S.likedIds.add(id);
    S.dislikedIds.delete(id);
    S.dislikedTracks=(S.dislikedTracks||[]).filter(x=>x.id!==id);
    _addToLikedPlaylist(t);
  } else {
    S.likedIds.delete(id);
    _dropFromLikedPlaylist(id);
  }

  const dropped = !nextLiked && S.plView==='detail' && S.plDetail.group==='system';
  if(!dropped) _updateExRow(source,id,true);

  _updateLikeButtons();
  if(nextLiked){ _persistDislikes(); renderDislikes(); }
  window.pywebview.api.toggle_like(id, nextLiked);
}
function toggleLikeCurrent(){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleLike(S.playerSource, t.id);
}

function toggleDislike(source,id){
  const t=_listFor(source).find(x=>x.id===id) || _trackFor(source,id);
  if(!t || S.dislikedPending.has(id) || !_trackPlayable(t)) return;
  const next=!S.dislikedIds.has(id);
  S.dislikedPending.add(id);
  if(next){
    S.dislikedIds.add(id);
    const wasLiked=S.likedIds.has(id);
    S.likedIds.delete(id);
    if(!S.dislikedTracks.some(x=>x.id===id)) S.dislikedTracks=[t, ...S.dislikedTracks];
    if(wasLiked) _dropFromLikedPlaylist(id);
  } else {
    S.dislikedIds.delete(id);
    S.dislikedTracks=S.dislikedTracks.filter(x=>x.id!==id);
  }
  _updateExRow(source,id);
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>{
    if(src!==source) _updateExRow(src,id);
  });
  _updateLikeButtons();
  _persistLikedIds();
  _persistDislikes();
  renderDislikes();
  window.pywebview.api.toggle_track_dislike(id, next);
  if(next && S.playerTrackId===id) _advanceQueue(false);
}
function toggleDislikeCurrent(){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleDislike(S.playerSource, t.id);
}
window.addEventListener('py:dislike_result', e=>{
  const{track_id,disliked,ok,msg}=e.detail||{};
  S.dislikedPending.delete(track_id);
  if(disliked){
    S.dislikedIds.add(track_id);
    S.likedIds.delete(track_id);
  } else {
    S.dislikedIds.delete(track_id);
    S.dislikedTracks=(S.dislikedTracks||[]).filter(x=>x.id!==track_id);
  }
  if(!ok){
    addLog(`✗ Не удалось изменить дизлайк: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось изменить дизлайк${msg?': '+esc(msg):''}`});
  } else {
    _persistLikedIds();
    _persistDislikes();
  }
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>_updateExRow(src,track_id));
  _updateLikeButtons();
  renderDislikes();
});

/* «Мне нравится» в сетке и в кэше треков — сразу, без перезапуска */
function _likedPlaylist(){
  return (S.myPlaylistsFlat||[]).find(p=>p.group==='system')||null;
}
function _likedTracksRef(){
  const pl=_likedPlaylist();
  if(S.plView==='detail' && S.plDetail.group==='system' && Array.isArray(S.plDetail.tracks)){
    if(pl && pl.url) S.plTracksCache[pl.url]=S.plDetail.tracks;
    return S.plDetail.tracks;
  }
  if(pl && Array.isArray(S.plTracksCache[pl.url])) return S.plTracksCache[pl.url];
  return null;
}
function _syncLikedPlaylistCount(delta){
  const pl=_likedPlaylist();
  if(!pl) return;
  pl.count=Math.max(0,(Number(pl.count)||0)+delta);
  CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
  const el=card&&card.querySelector('.pl-count');
  if(el) el.textContent=`${pl.count} треков`;
}
function _addToLikedPlaylist(t){
  if(!t||!t.id) return;
  const pl=_likedPlaylist();
  const copy=Object.assign({}, t);
  const list=_likedTracksRef();
  if(list){
    if(list.some(x=>x.id===t.id)) return;
    S.likedRemovals[t.id]={op:'add', track:copy, index:0, url:pl&&pl.url};
    list.unshift(copy);
    list.forEach((x,i)=>x.num=i+1);
    if(pl){ S.plTracksCache[pl.url]=list; _persistPlTracks(); }
    _syncLikedPlaylistCount(1);
    if(S.plView==='detail' && S.plDetail.group==='system'){
      _updatePlDetailCount();
      renderPlaylistDetail();
    }
    return;
  }
  S.likedRemovals[t.id]={op:'add', track:copy, index:-1, url:pl&&pl.url, countOnly:true};
  _syncLikedPlaylistCount(1);
}
function _dropFromLikedPlaylist(id){
  const pl=_likedPlaylist();
  const list=_likedTracksRef();
  if(list){
    const idx=list.findIndex(x=>x.id===id);
    if(idx<0) return false;
    S.likedRemovals[id]={op:'remove', track:list[idx], index:idx, url:pl&&pl.url};
    list.splice(idx,1);
    if(pl){ S.plTracksCache[pl.url]=list; _persistPlTracks(); }
    _syncLikedPlaylistCount(-1);
    if(S.plView==='detail' && S.plDetail.group==='system'){
      S.plDetail.tracks=list;
      _finishPlaylistRowRemoval(id);
    }
    return true;
  }
  if(pl){
    S.likedRemovals[id]={op:'remove', track:null, index:-1, url:pl.url, countOnly:true};
    _syncLikedPlaylistCount(-1);
    return true;
  }
  return false;
}
function _restoreToLikedPlaylist(id){
  const info=S.likedRemovals[id];
  delete S.likedRemovals[id];
  if(!info) return;
  if(info.op==='add'){
    const list=_likedTracksRef();
    if(list){
      const idx=list.findIndex(x=>x.id===id);
      if(idx>=0) list.splice(idx,1);
      list.forEach((x,i)=>x.num=i+1);
      const pl=_likedPlaylist();
      if(pl){ S.plTracksCache[pl.url]=list; _persistPlTracks(); }
      if(S.plView==='detail' && S.plDetail.group==='system'){
        _updatePlDetailCount();
        renderPlaylistDetail();
      }
    }
    _syncLikedPlaylistCount(-1);
    return;
  }
  if(info.countOnly){ _syncLikedPlaylistCount(1); return; }
  const list=_likedTracksRef();
  if(list && info.track && !list.some(x=>x.id===id)){
    list.splice(Math.min(info.index,list.length),0,info.track);
    list.forEach((x,i)=>x.num=i+1);
    const pl=_likedPlaylist();
    if(pl){ S.plTracksCache[pl.url]=list; _persistPlTracks(); }
  }
  _syncLikedPlaylistCount(1);
  if(S.plView==='detail' && S.plDetail.group==='system'){
    _updatePlDetailCount();
    renderPlaylistDetail();
  }
}

/* Общий финал удаления строки плейлиста: анимация → перенумерация → счётчик */
function _finishPlaylistRowRemoval(id){
  const after=()=>{
    _renumberList('playlist_detail');
    if(S.plDetail.url){
      S.plTracksCache[S.plDetail.url]=S.plDetail.tracks;
      _persistPlTracks();
    }
    if(!S.plDetail.tracks.length && S.plView==='detail') renderPlaylistDetail();
  };
  if(document.getElementById('exrow-playlist_detail-'+id)) _animateRowOut('playlist_detail',id,after);
  else after();
  _updatePlDetailCount();
}
function _plDeadTracks(list){
  return (list||[]).filter(t=>!_trackPlayable(t));
}
function _plDetailVisibleTracks(){
  const q=(S.plTrackQuery||'').trim().toLowerCase();
  let list=S.plDetail.tracks||[];
  if(S.plDeadFilter) list=_plDeadTracks(list);
  if(q) list=list.filter(t=>_trackMatchesQuery(t,q));
  return _sortedCopy(list, 'playlist_detail');
}
function onPlTrackSearch(){
  const el=document.getElementById('plTrackSearch');
  S.plTrackQuery=el?el.value:'';
  renderPlaylistDetail();
  _updatePlDetailCount();
  _syncPlayingQueue('playlist_detail');
}
function togglePlDeadFilter(){
  S.plDeadFilter=!S.plDeadFilter;
  renderPlaylistDetail();
  _updatePlDetailCount();
  _syncPlayingQueue('playlist_detail');
}
function _paintPlDeadFilterBtn(){
  const n=_plDeadTracks(S.plDetail.tracks).length;
  const has=n>0;
  if(!has && S.plDeadFilter) S.plDeadFilter=false;
  const btn=document.getElementById('btnPlDeadFilter');
  const rm=document.getElementById('btnPlDeadRemove');
  if(btn){
    btn.hidden=!has;
    btn.classList.toggle('active-mode', has && !!S.plDeadFilter);
    btn.textContent=has?`Недоступные · ${n}`:'Недоступные';
  }
  if(rm){
    const showRm=has && (S.plDetail.editable || S.plDetail.group==='system');
    rm.hidden=!showRm;
    rm.disabled=!!S.pendingDeadRemoval;
    rm.textContent=S.pendingDeadRemoval?'Удаляем…':(has?`Удалить недоступные · ${n}`:'Удалить недоступные');
  }
  const row=document.getElementById('plDeadRow');
  if(row) row.hidden=!((btn && !btn.hidden) || (rm && !rm.hidden));
}
function confirmRemoveUnavailable(){
  if(S.pendingDeadRemoval) return;
  if(!(S.plDetail.editable || S.plDetail.group==='system')) return;
  const dead=_plDeadTracks(S.plDetail.tracks);
  if(!dead.length) return;
  const n=dead.length;
  showConfirm({
    title:'Удалить недоступные треки?',
    text:`Из «${S.plDetail.title}» будет удалено ${_ruN(n, 'трек', 'трека', 'треков')}, которые больше нельзя слушать. Живые треки не трогаем.`,
    okLabel: n===1?'Удалить':'Удалить все',
    onOk:()=>_doRemoveUnavailable(dead.map(t=>t.id)),
  });
}
function _doRemoveUnavailable(ids){
  if(!ids || !ids.length || S.pendingDeadRemoval) return;
  if(!S.plDetail.id) return;
  S.pendingDeadRemoval=true;
  _paintPlDeadFilterBtn();
  window.pywebview.api.remove_unavailable_from_playlist(S.plDetail.id, ids);
}
function _dropTracksFromPlaylist(ids){
  const want=new Set((ids||[]).map(String));
  if(!want.size) return 0;
  const before=(S.plDetail.tracks||[]).length;
  S.plDetail.tracks=(S.plDetail.tracks||[]).filter(t=>!want.has(String(t.id)));
  const removed=before-S.plDetail.tracks.length;
  if(removed){
    S.plDetail.tracks.forEach((t,i)=>t.num=i+1);
    if(S.plDetail.url){
      S.plTracksCache[S.plDetail.url]=S.plDetail.tracks;
      S.plTracksTs[S.plDetail.url]=Date.now();
      _persistPlTracks();
    }
    _adjustCurrentPlaylistCount(-removed);
    _clearSel('playlist_detail');
    _updatePlDetailCount();
    if(S.plView==='detail') renderPlaylistDetail();
  }
  return removed;
}
function _adjustCurrentPlaylistCount(delta){
  const id=S.plDetail.id, group=S.plDetail.group;
  if(!id) return;
  const pl=(S.myPlaylistsFlat||[]).find(p=>p.group===group && String(p.id)===String(id));
  if(!pl) return;
  pl.count=Math.max(0,(Number(pl.count)||0)+delta);
  CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
  const el=card&&card.querySelector('.pl-count');
  if(el) el.textContent=`${pl.count} треков`;
}
window.addEventListener('py:remove_unavailable_result', e=>{
  const{ok,playlist_id,removed,track_ids,msg}=e.detail||{};
  S.pendingDeadRemoval=false;
  if(String(S.plDetail.id)!==String(playlist_id||'')){
    _paintPlDeadFilterBtn();
    return;
  }
  if(ok){
    _dropTracksFromPlaylist(track_ids||[]);
    if(S.plDeadFilter && !_plDeadTracks(S.plDetail.tracks).length) S.plDeadFilter=false;
    _updatePlDetailCount();
    if(S.plView==='detail') renderPlaylistDetail();
    const n=Number(removed)||0;
    showToast({kind:'ok', icon:'🗑', message:n?`Удалено недоступных: ${n}`:'Недоступных треков не осталось'});
    return;
  }
  _paintPlDeadFilterBtn();
  if(S.plDetail.url) window.pywebview.api.open_playlist(S.plDetail.url);
  showToast({kind:'err', icon:'✗', message:`Не удалось удалить недоступные треки${msg?': '+esc(msg):''}`});
});
function _updatePlDetailCount(){
  const el=document.getElementById('plDetailCount');
  if(!el) return;
  const dead=_plDeadTracks(S.plDetail.tracks).length;
  if(!dead && S.plDeadFilter){
    S.plDeadFilter=false;
    if(S.plView==='detail') renderPlaylistDetail();
  }
  const tot=(S.plDetail.tracks||[]).length;
  const vis=_plDetailVisibleTracks().length;
  const q=(S.plTrackQuery||'').trim();
  if(S.plDeadFilter){
    el.textContent=q?`${vis} из ${dead} недоступных`:`${dead} недоступных`;
  } else if(q){
    el.textContent=`${vis} из ${tot}`;
  } else {
    el.textContent=dead?`${tot} треков · ${dead} недоступных`:`${tot} треков`;
  }
  _paintPlDeadFilterBtn();
}

window.addEventListener('py:liked_ids', e=>{
  S.likedIds = new Set(e.detail || []);
  _persistLikedIds();
  _rerenderActive();
});
window.addEventListener('py:like_result', e=>{
  const{track_id,liked,ok,msg}=e.detail;
  S.likedPending.delete(track_id);
  if(liked){
    S.likedIds.add(track_id);
    S.dislikedIds.delete(track_id);
    S.dislikedTracks=(S.dislikedTracks||[]).filter(x=>x.id!==track_id);
  } else S.likedIds.delete(track_id);
  if(ok){
    delete S.likedRemovals[track_id];
  } else {
    _restoreToLikedPlaylist(track_id);
    addLog(`✗ Не удалось изменить лайк: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось изменить лайк${msg?': '+esc(msg):''}`});
  }
  if(ok) _persistLikedIds();
  ['search','wave','playlist_detail','browse','dislikes'].forEach(src=>_updateExRow(src,track_id));
  _updateLikeButtons();
  renderDislikes();
});

/* ── Лайки исполнителей и альбомов (коллекция Яндекса) ── */
function _artistById(id){
  id=String(id||'');
  const top=_browseTop();
  if(top && (top.type==='artist'||top.type==='artist_tracks') && top.id===id && top.info) return top.info;
  return (S.likedArtists||[]).find(a=>String(a.id)===id)
    || (S.dislikedArtists||[]).find(a=>String(a.id)===id)
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
  const label=_likeIconHTML(liked, labeled);
  const cls=labeled?'btn sm like-btn':'iBtn card-like like-btn';
  return `<button class="${cls}${liked?' liked':''}" ${attr}="${esc(id)}"${labeled?' data-like-label="1"':''}
    title="${liked?'Убрать из любимых':'Нравится'}"
    onclick="event.stopPropagation();${fn}('${esc(id)}')">${label}</button>`;
}
function _entityDislikeBtn(id,labeled){
  id=String(id||'');
  const on=S.dislikedArtistIds.has(id);
  const label=_dislikeIconHTML(on, labeled);
  const cls=labeled?'btn sm dislike-btn':'iBtn card-like dislike-btn';
  return `<button class="${cls}${on?' disliked':''}" data-dislike-artist="${esc(id)}"${labeled?' data-dislike-label="1"':''}
    title="${on?'Вернуть в рекомендации':'Не рекомендовать исполнителя'}"
    onclick="event.stopPropagation();toggleArtistDislike('${esc(id)}')">${label}</button>`;
}
function toggleArtistDislike(id){
  id=String(id||'');
  if(!id || S.dislikedArtistPending.has(id)) return;
  const next=!S.dislikedArtistIds.has(id);
  S.dislikedArtistPending.add(id);
  if(next){
    S.dislikedArtistIds.add(id);
    S.likedArtistIds.delete(id);
    S.likedArtists=S.likedArtists.filter(x=>String(x.id)!==id);
    const a=_artistById(id);
    if(a && !S.dislikedArtists.some(x=>String(x.id)===id)) S.dislikedArtists=[a, ...S.dislikedArtists];
  } else {
    S.dislikedArtistIds.delete(id);
    S.dislikedArtists=S.dislikedArtists.filter(x=>String(x.id)!==id);
  }
  _paintEntityLikes();
  renderLikedArtists();
  renderDislikes();
  _persistLibrary();
  _persistDislikes();
  window.pywebview.api.toggle_artist_dislike(id, next);
}
function _paintEntityLikes(){
  document.querySelectorAll('[data-like-artist]').forEach(el=>{
    const liked=S.likedArtistIds.has(el.dataset.likeArtist);
    el.classList.toggle('liked', liked);
    el.innerHTML=_likeIconHTML(liked, !!el.dataset.likeLabel);
    el.title=liked?'Убрать из любимых':'Нравится';
  });
  document.querySelectorAll('[data-like-album]').forEach(el=>{
    const liked=S.likedAlbumIds.has(el.dataset.likeAlbum);
    el.classList.toggle('liked', liked);
    el.innerHTML=_likeIconHTML(liked, !!el.dataset.likeLabel);
    el.title=liked?'Убрать из понравившихся':'Нравится';
  });
  document.querySelectorAll('[data-dislike-artist]').forEach(el=>{
    const on=S.dislikedArtistIds.has(el.dataset.dislikeArtist);
    el.classList.toggle('disliked', on);
    el.innerHTML=_dislikeIconHTML(on, !!el.dataset.dislikeLabel);
    el.title=on?'Вернуть в рекомендации':'Не рекомендовать исполнителя';
  });
}
function toggleArtistLike(id){
  id=String(id||'');
  if(!id || S.likedArtistPending.has(id)) return;
  const next=!S.likedArtistIds.has(id);
  S.likedArtistPending.add(id);
  if(next){
    S.likedArtistIds.add(id);
    S.dislikedArtistIds.delete(id);
    S.dislikedArtists=S.dislikedArtists.filter(x=>String(x.id)!==id);
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
  if(liked){
    S.likedArtistIds.add(key);
    S.dislikedArtistIds.delete(key);
    S.dislikedArtists=S.dislikedArtists.filter(x=>String(x.id)!==key);
  } else S.likedArtistIds.delete(key);
  if(!liked) S.likedArtists=S.likedArtists.filter(x=>String(x.id)!==key);
  if(!ok){
    addLog(`✗ Не удалось изменить лайк исполнителя: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось сохранить исполнителя${msg?': '+esc(msg):''}`});
  }
  if(ok){ _persistLibrary(); _persistDislikes(); }
  _paintEntityLikes();
  renderLikedArtists();
  renderDislikes();
});
window.addEventListener('py:artist_dislike_result', e=>{
  const{id,disliked,ok,msg}=e.detail||{};
  const key=String(id||'');
  S.dislikedArtistPending.delete(key);
  if(disliked){
    S.dislikedArtistIds.add(key);
    S.likedArtistIds.delete(key);
    S.likedArtists=S.likedArtists.filter(x=>String(x.id)!==key);
  } else {
    S.dislikedArtistIds.delete(key);
    S.dislikedArtists=S.dislikedArtists.filter(x=>String(x.id)!==key);
  }
  if(!ok){
    addLog(`✗ Не удалось изменить дизлайк исполнителя: ${msg||''}`,'err');
    showToast({kind:'err', icon:'✗', message:`Не удалось скрыть исполнителя${msg?': '+esc(msg):''}`});
  }
  if(ok){ _persistLibrary(); _persistDislikes(); }
  _paintEntityLikes();
  renderLikedArtists();
  renderDislikes();
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
  _adjustCurrentPlaylistCount(-1);
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
    _adjustCurrentPlaylistCount(1);
    _updatePlDetailCount();
    if(S.plView==='detail') renderPlaylistDetail();
  }
  showToast({kind:'err', icon:'✗', message:`Не удалось удалить «${esc(title)}»${msg?': '+esc(msg):''}`});
});

function _localFileCoverUrl(t){
  if(!t) return '';
  const rel=t.rel_path || ((t.local || S.playerSource==='downloaded') ? t.id : '');
  if(!rel) return '';
  const isLocal=!!(t.local || t.rel_path || S.playerSource==='downloaded'
    || /\.(mp3|flac|m4a|aac|ogg|opus|wav)$/i.test(String(rel)));
  if(!isLocal) return '';
  return 'http://127.0.0.1:5000/cover/'+String(rel).split('/').map(encodeURIComponent).join('/');
}
function _dlCoverUrl(f){
  if(!f) return '';
  return _localFileCoverUrl({
    local:true,
    rel_path:f.rel_path||f.id||'',
    id:f.rel_path||f.id||'',
  }) || f.cover_uri || '';
}
function _showCoverPlaceholder(img, ph){
  if(img){
    img.hidden=true;
    img.removeAttribute('src');
  }
  if(ph){
    if(!ph.querySelector('svg')) ph.innerHTML=icon('music');
    ph.hidden=false;
  }
}
function _revealCoverImage(img, ph){
  if(img) img.hidden=false;
  if(ph) ph.hidden=true;
}
/* ── Полноэкранный просмотр обложки / текста песни ── */
function _bigCoverUrl(t,size){
  if(!t) return '';
  if(t.cover_uri_tmpl) return t.cover_uri_tmpl.replace('%%', size);
  return t.cover_uri || _localFileCoverUrl(t) || '';
}
/*
  Обложку подменяем только когда новая уже раскодирована: если присвоить src
  сразу, картинка на секунду пропадает, и смена трека выглядит рвано.
*/
function _setBigCover(t){
  const img=document.getElementById('bigViewCover');
  const ph=document.getElementById('bigViewCoverPh');
  const wash=document.getElementById('bvWash');
  const hq=_bigCoverUrl(t,'600x600')||'';
  const lo=t.cover_uri || _localFileCoverUrl(t) || '';
  const token=++S.coverToken;
  if(!hq && !lo){
    _showCoverPlaceholder(img, ph);
    if(wash) wash.style.backgroundImage='none';
    _paintAurora(null, token);
    return;
  }
  const url=hq||lo;
  const fail=()=>{
    if(token!==S.coverToken) return;
    _showCoverPlaceholder(img, ph);
    if(wash) wash.style.backgroundImage='none';
    _paintAurora(null, token);
  };
  img.onload=()=>{
    if(token!==S.coverToken) return;
    if(img.naturalWidth) _revealCoverImage(img, ph);
    else fail();
  };
  img.onerror=fail;
  if(img.getAttribute('src')===url && img.naturalWidth){
    _revealCoverImage(img, ph);
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
    img.onload=null;
    img.onerror=fail;
    img.src=url;
    _revealCoverImage(img, ph);
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
    plain.onerror=fail;
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
    case 'dislikes': return 'Дизлайки';
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
    }
    _loadLyricsFor(_lyricsLookupId(t) || t.id);
  }

  document.getElementById('bigViewSrc').textContent=_bigViewSourceLabel();

  _paintPlayerDlBtn();
  const canRemove = !local && S.playerSource==='playlist_detail' && S.plDetail.editable
    && S.plDetail.tracks.some(x=>x.id===t.id);
  document.getElementById('bvDelBtn').style.display=canRemove?'':'none';
  document.getElementById('bvOpenBtn').style.display=(!local && t.album_id)?'':'none';
  ['bigViewLikeBtn','bigViewDislikeBtn','bvAddBtn','bvDlBtn','bvWaveBtn'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.style.display=local?'none':'';
  });
  const locateBtn=document.getElementById('bvLocateBtn');
  if(locateBtn) locateBtn.style.display='';
  const toolsRow=document.querySelector('.bigview-tools');
  if(toolsRow) toolsRow.style.display='';
  const lyricsWrap=document.querySelector('.bigview-lyrics-wrap');
  if(lyricsWrap) lyricsWrap.style.display='';

  // «Далее» — тот же трек, что сыграет playerNext (в т.ч. из shuffleOrder)
  const nextT=_peekNextTrack();
  const atEnd=!nextT && S.playerSource!=='wave' && S.repeat!=='one';
  const nextTitle=nextT?(nextT.title||nextT.name||''):'';
  const nextArtist=nextT?(nextT.artist||''):'';
  document.getElementById('bvNext').innerHTML=
    atEnd?'<b>Далее:</b> 🌊 Моя волна'
    :(nextT?`<b>Далее:</b> ${esc(nextArtist)}${nextArtist?' — ':''}${esc(nextTitle)}`:'');

  _applyModeUI();
  _updatePlayBtn();
}
function downloadCurrent(){
  const t=_currentPlayingTrack();
  if(!t || S.playerSource==='downloaded' || t.local) return;
  if(t.status==='downloading' || t.status==='queued' || t.status==='done') return;
  if(!_trackPlayable(t)){
    showToast({kind:'err', icon:'⊘', message:'Нельзя скачать недоступный трек'});
    return;
  }
  if(t.status==='error') t.status='idle';
  window.pywebview.api.start_download([t]);
  t.status='queued';
  if(S.playerTrack && String(S.playerTrack.id)===String(t.id)) S.playerTrack.status='queued';
  (S.playerQueue||[]).forEach(x=>{ if(String(x.id)===String(t.id)) x.status='queued'; });
  _refreshRow(S.playerSource, t.id);
  _paintPlayerDlBtn();
  if(S.bigViewOpen) _fillBigView();
  addLog('В очереди на скачивание: '+t.title,'info');
}
function bigViewDownload(){ downloadCurrent(); }
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
  const url=_ymTrackUrl(_currentPlayingTrack());
  if(url) window.pywebview.api.open_link(url);
}
function _isYmTrackId(id){
  id=String(id||'');
  if(!id || id.startsWith('unknown_')) return false;
  if(id.includes('/') || id.includes('\\')) return false;
  if(/\.(mp3|flac|m4a|aac|ogg|opus|wav)$/i.test(id)) return false;
  return true;
}
function _ymArtistUrl(id){ return id?`https://music.yandex.ru/artist/${id}`:''; }
function _ymAlbumUrl(id){ return id?`https://music.yandex.ru/album/${id}`:''; }
function _ymTrackUrl(t){
  if(!t) return '';
  let id=t.id, albumId=t.album_id||null;
  if(t.local || t.track_id){
    const f=(S.dlFiles||[]).find(x=>x.rel_path===t.id || x.rel_path===t.rel_path || x.uid===t.uid);
    const tid=String(t.track_id || (f && f.track_id) || '');
    if(!tid) return '';
    id=tid;
    albumId=t.album_id || (f && f.album_id) || null;
  }
  if(!_isYmTrackId(id)) return '';
  return albumId
    ? `https://music.yandex.ru/album/${albumId}/track/${id}`
    : `https://music.yandex.ru/track/${id}`;
}
function _copyText(text){
  if(navigator.clipboard && navigator.clipboard.writeText){
    return navigator.clipboard.writeText(text).then(()=>true).catch(()=>_copyTextFallback(text));
  }
  return Promise.resolve(_copyTextFallback(text));
}
function _copyTextFallback(text){
  const ta=document.createElement('textarea');
  ta.value=text;
  ta.setAttribute('readonly','');
  ta.style.cssText='position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  ta.setSelectionRange(0, text.length);
  let ok=false;
  try{ ok=document.execCommand('copy'); }catch(_e){}
  ta.remove();
  return ok;
}
async function copyYmUrl(url){
  url=String(url||'').trim();
  if(!url){
    showToast({kind:'err', icon:'⊘', message:'Нет ссылки Яндекс.Музыки', duration:2200});
    return false;
  }
  const ok=await _copyText(url);
  if(!ok){
    showToast({kind:'err', icon:'✗', message:'Не удалось скопировать', duration:2200});
    return false;
  }
  showToast({kind:'ok', icon:'✓', message:'Ссылка скопирована', duration:2200});
  return true;
}
function copyYmTrackLink(t){ return copyYmUrl(_ymTrackUrl(t)); }
function _firstArtistId(t){
  if(!t) return '';
  const a=(t.artists||[]).find(x=>x&&x.id);
  return a?String(a.id):'';
}
function _ymUrlFromCard(card){
  if(!card) return '';
  const tagged=card.getAttribute('data-ym-url');
  if(tagged) return tagged;
  const kind=card.getAttribute('data-kind');
  if(kind==='artist') return _ymArtistUrl(card.getAttribute('data-id'));
  if(kind==='album') return _ymAlbumUrl(card.getAttribute('data-id'));
  if(kind==='pl'){
    const key=card.getAttribute('data-key');
    const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===key);
    return (pl && pl.url) || '';
  }
  return '';
}
function _lyricsEntry(v){
  if(!v) return null;
  if(typeof v==='string') return {text:v, sync:null};
  return v;
}
function _loadLyricsFor(trackId){
  const box=document.getElementById('bigViewLyrics');
  if(!box) return;
  if(!trackId){
    _paintLyrics('muted','Текст песни недоступен для этого трека', false);
    return;
  }
  const key=_lyricsCacheKey(trackId);
  if(Object.prototype.hasOwnProperty.call(S.lyricsCache,key)){
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
  const cur=_lyricsLookupId(t) || (t && t.id);
  if(!t || String(cur)!==String(trackId)) return; // трек уже сменился — не показываем чужой текст
  const entry=_lyricsEntry(S.lyricsCache[_lyricsCacheKey(trackId)]);
  if(entry && entry.sync && entry.sync.length){
    _paintSyncedLyrics(entry.sync);
    return;
  }
  if(entry && entry.text) _paintLyrics('', entry.text, true);
  else _paintLyrics('muted','Текст песни недоступен для этого трека', false);
}
function _paintSyncedLyrics(sync){
  const box=document.getElementById('bigViewLyrics');
  if(!box) return;
  box.className='bigview-lyrics synced';
  box.style.paddingTop='';
  box.style.paddingBottom='';
  box.innerHTML=sync.map((row,i)=>
    `<div class="lyric-line" data-i="${i}" data-t="${Number(row.t)||0}">${esc(row.text||' ')}</div>`
  ).join('');
  const wrap=box.parentElement;
  if(wrap){
    wrap.scrollTop=0;
    if(!wrap.dataset.lyricScroll){
      wrap.dataset.lyricScroll='1';
      wrap.addEventListener('wheel', ()=>{
        S._lyricsUserScroll=true;
        if(S._lyricRaf){ cancelAnimationFrame(S._lyricRaf); S._lyricRaf=0; }
        clearTimeout(S._lyricsUserScrollTimer);
        S._lyricsUserScrollTimer=setTimeout(()=>{ S._lyricsUserScroll=false; }, 2800);
      }, {passive:true});
    }
  }
  S._lyricOn=-1;
  S._lyricScrollTarget=0;
  const a=_audioNow();
  const sec=a && isFinite(a.currentTime) ? a.currentTime : (S._savedPosition||0);
  const apply=()=>_syncLyricsHighlight(sec, sec>1.5);
  apply();
  requestAnimationFrame(apply);
}
function _lyricScrollTick(){
  S._lyricRaf=0;
  const wrap=document.querySelector('.bigview-lyrics-wrap');
  if(!wrap || S._lyricsUserScroll) return;
  const dest=S._lyricScrollTarget;
  const cur=wrap.scrollTop;
  const next=cur+(dest-cur)*0.16;
  if(Math.abs(dest-next)<0.6){ wrap.scrollTop=dest; return; }
  wrap.scrollTop=next;
  S._lyricRaf=requestAnimationFrame(_lyricScrollTick);
}
function _lyricLineAt(lines, sec){
  const t=Number(sec)||0;
  let idx=0;
  for(let i=0;i<lines.length;i++){
    const a=Number(lines[i].dataset.t);
    if(a-0.02<=t) idx=i;
    else break;
  }
  return idx;
}
function _lyricTargetScroll(wrap, line){
  const view=wrap.clientHeight;
  const maxScroll=Math.max(0, wrap.scrollHeight-view);
  if(!maxScroll) return 0;
  const wr=wrap.getBoundingClientRect();
  const lr=line.getBoundingClientRect();
  const lineMid=(lr.top-wr.top)+wrap.scrollTop+lr.height/2;
  return Math.max(0, Math.min(maxScroll, lineMid-view*0.45));
}
function _syncLyricsHighlight(sec, snap){
  const box=document.getElementById('bigViewLyrics');
  if(!box || !box.classList.contains('synced')) return;
  const lines=box.children;
  if(!lines.length) return;
  const idx=_lyricLineAt(lines, sec);
  if(idx!==S._lyricOn){
    if(S._lyricOn>=0 && lines[S._lyricOn]) lines[S._lyricOn].classList.remove('on');
    lines[idx].classList.add('on');
    S._lyricOn=idx;
  }
  const wrap=box.parentElement;
  if(!wrap || S._lyricsUserScroll) return;
  const target=_lyricTargetScroll(wrap, lines[idx]);
  S._lyricScrollTarget=target;
  if(snap){
    if(S._lyricRaf){ cancelAnimationFrame(S._lyricRaf); S._lyricRaf=0; }
    wrap.scrollTop=target;
    return;
  }
  if(!S._lyricRaf && Math.abs(wrap.scrollTop-target)>0.8)
    S._lyricRaf=requestAnimationFrame(_lyricScrollTick);
}
/* animate — только когда пришёл настоящий текст, не на очистке */
function _paintLyrics(cls,text,animate){
  const box=document.getElementById('bigViewLyrics');
  if(!box) return;
  S._lyricOn=-1;
  if(S._lyricRaf){ cancelAnimationFrame(S._lyricRaf); S._lyricRaf=0; }
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
  const d=e.detail||{};
  const id=d.track_id;
  const localKey='local:'+id;
  const key=S.lyricsPending.has(localKey) ? localKey : id;
  S.lyricsPending.delete(key);
  S.lyricsPending.delete(id);
  S.lyricsCache[key]=(d.text || (d.sync&&d.sync.length)) ? {text:d.text||'', sync:d.sync||null} : null;
  _renderLyrics(id);
});

/* ── Универсальные превью / скачивание для поиска / волны / плейлиста ── */
/* Клик по строке — плей/пауза; кнопки, галочки и ссылки не перехватываем */
function stopRow(evt){
  if(!evt) return;
  evt.stopPropagation();
  if(typeof evt.preventDefault==='function') evt.preventDefault();
}
function _fromRowControl(evt){
  if(!evt || evt.defaultPrevented) return true;
  const el=evt.target;
  if(el && typeof el.closest==='function' && el.closest('button, input, .lnk, a, .dl-cover, .dl-cover-ph, .dl-cover-slot')) return true;
  const path=typeof evt.composedPath==='function' ? evt.composedPath() : null;
  if(path && path.some(n=>n && n.tagName && /^(BUTTON|INPUT|A)$/.test(n.tagName))) return true;
  return false;
}
function rowPlay(evt,source,id){
  if(_fromRowControl(evt)) return;
  previewGeneric(source,id);
}
function rowPlayDownloaded(evt,uid){
  if(_fromRowControl(evt)) return;
  playDownloaded(uid);
}
function _contextCopyIgnore(el){
  return !!(el && el.closest && el.closest('button, input, textarea, select'));
}
function _ymUrlFromContext(el){
  const tagged=el.closest('[data-ym-url]');
  if(tagged){
    const u=tagged.getAttribute('data-ym-url');
    if(u) return u;
  }
  const card=el.closest('.pl-card');
  if(card) return _ymUrlFromCard(card);
  if(el.closest('#plArtist, #bigViewArtist')){
    const t=_currentPlayingTrack();
    return _ymArtistUrl(_firstArtistId(t));
  }
  if(el.closest('#bigViewAlbum')){
    const t=_currentPlayingTrack();
    return _ymAlbumUrl(t && t.album_id);
  }
  if(el.closest('#player .player-cover-slot, #player .player-cover, #player .player-cover-ph, #player .player-info, #plTitle, #bigViewCoverSlot, #bigViewCover, #bigViewTitle')){
    return _ymTrackUrl(_currentPlayingTrack());
  }
  const hero=el.closest('.br-hero');
  if(hero){
    const en=_browseTop();
    if(en && (en.type==='artist' || en.type==='artist_tracks')) return _ymArtistUrl(en.id);
    if(en && en.type==='album') return _ymAlbumUrl(en.id);
  }
  if(el.closest('#plDetailTitle')) return (S.plDetail && S.plDetail.url) || '';
  const ex=el.closest('.ex-row');
  if(ex) return _ymTrackUrl(_trackFor(ex.dataset.src, ex.dataset.tid));
  const tl=el.closest('.tl-row');
  if(tl) return _ymTrackUrl(_trackFor(tl.dataset.src||'tracks', tl.dataset.tid));
  const dl=el.closest('.dl-row');
  if(dl){
    const f=(S.dlFiles||[]).find(x=>x.uid===dl.dataset.uid);
    return _ymTrackUrl(f?_dlAsTrack(f):null);
  }
  return '';
}
document.addEventListener('contextmenu', e=>{
  const el=e.target;
  if(!el || !el.closest || _contextCopyIgnore(el)) return;
  const url=_ymUrlFromContext(el);
  if(!url) return;
  e.preventDefault();
  copyYmUrl(url);
});
function miniPlayerAdd(evt){
  const t=_currentPlayingTrack();
  if(!t) return;
  toggleAddMenu(evt, S.playerSource, t.id);
}
function previewGeneric(source,id){
  const list=_listFor(source);
  const t=list.find(x=>x.id===id);
  if(!t) return;
  if(!_trackPlayable(t)){
    showToast({kind:'err', icon:'⊘', message:'Трек удалён из Яндекс.Музыки'});
    return;
  }
  if(S.playerTrackId===id && S.playerSource===source){
    playerToggle();
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
  _playTrack(t, source, _rowsFor(source));
}
function downloadGeneric(source,id){
  const list=_listFor(source);
  const t=list.find(x=>x.id===id);
  if(!t||t.status==='downloading'||t.status==='queued') return;
  if(!_trackPlayable(t)){
    showToast({kind:'err', icon:'⊘', message:'Нельзя скачать недоступный трек'});
    return;
  }
  if(t.status==='error') t.status='idle';
  window.pywebview.api.start_download([t]);
  t.status='queued';
  _updateExRow(source,id);
  addLog('В очереди на скачивание: '+t.title,'info');
}
function exRowHTML(t,source){
  const isPlaying=String(S.playerTrackId)===String(t.id);
  const audio=_audioNow();
  const playing=isPlaying && audio && !audio.paused;
  const dead=!_trackPlayable(t);
  const prvCls=isPlaying?'playing':'';
  const audioEl=isPlaying && audio;
  const pausedCls=isPlaying && audioEl && audioEl.paused?' is-paused':'';
  const st=t.status||'idle';
  const dlCls={done:'done',error:'error'}[st]||'';
  const dlDis=(dead||st==='downloading'||st==='queued')?'disabled':'';
  const liked=S.likedIds.has(t.id);
  const likeCls=liked?'liked':'';
  const disliked=S.dislikedIds.has(t.id);
  const sourceSelectable=_selectable(source);
  const likedDead=source==='playlist_detail' && S.plDetail.group==='system' && dead;
  const removable=source==='playlist_detail' && S.plDetail.editable;
  const cbHtml=sourceSelectable
    ? (dead ? '<span></span>'
      : `<input type="checkbox" class="cb" ${_selSet(source).has(t.id)?'checked':''} onchange="toggleSel('${source}','${t.id}',this.checked)">`)
    :'';
  const rmHtml=removable
    ?`<button class="iBtn del-btn" title="Удалить из плейлиста" onclick="stopRow(event);removeFromPlaylist('${t.id}')">${icon('trash')}</button>`
    :'';
  const likeHtml=likedDead
    ?`<button class="iBtn del-btn" title="Удалить из «Мне нравится»" onclick="stopRow(event);removeFromPlaylist('${t.id}')">${icon('trash')}</button>`
    : (dead
      ?`<button class="iBtn like-btn" disabled title="Трек недоступен">${icon('heart')}</button>`
      :`<button class="iBtn like-btn ${likeCls}" title="Мне нравится" onclick="stopRow(event);toggleLike('${source}','${t.id}')">${icon(liked?'heart-fill':'heart')}</button>`);
  const waveHtml=dead
    ?`<button class="iBtn" disabled title="Трек недоступен">${icon('wave')}</button>`
    :`<button class="iBtn" title="Волна по треку" onclick="stopRow(event);startTrackWave(event,'${source}','${t.id}')">${icon('wave')}</button>`;
  const playHtml=dead
    ?`<button class="iBtn play-btn" disabled title="Трек недоступен">${icon('play')}</button>`
    :`<button class="iBtn play-btn ${prvCls}" title="Прослушать" onclick="stopRow(event);previewGeneric('${source}','${t.id}')">${icon(_playIconName(playing))}</button>`;
  const addHtml=dead
    ?`<button class="iBtn" disabled title="Трек недоступен">${icon('plus')}</button>`
    :`<button class="iBtn" title="Добавить в плейлист" onclick="stopRow(event);toggleAddMenu(event,'${source}','${t.id}')">${icon('plus')}</button>`;
  const dislikeHtml=dead
    ?`<button class="iBtn dislike-btn" disabled title="Трек недоступен">${icon('heart-break')}</button>`
    :`<button class="iBtn dislike-btn ${disliked?'disliked':''}" title="Не рекомендовать" onclick="stopRow(event);toggleDislike('${source}','${t.id}')">${icon(disliked?'heart-break-fill':'heart-break')}</button>`;
  return `<div class="ex-row ${sourceSelectable?'selectable':''} ${removable?'removable':''} ${st}${dead?' unavailable':''}${isPlaying?' playing-row':''}${pausedCls}" id="exrow-${source}-${t.id}"
    data-src="${source}" data-tid="${esc(t.id)}"
    onclick="rowPlay(event,'${source}','${t.id}')">
    ${cbHtml}
    <span class="tl-num">${_nowEqHTML(t.num||'')}</span>
    <div style="min-width:0">
      <div class="tl-title" title="${esc(t.title)}">${esc(t.title)}</div>
      <div class="tl-sub" title="${esc(t.artist)}">${_artistLinks(t)}</div>
    </div>
    <div class="tl-album" title="${esc(t.album)}">${_albumLink(t) || (dead?'—':'')}</div>
    <span class="tl-dur">${t.duration|| (dead?'—':'')}</span>
    ${playHtml}
    ${waveHtml}
    ${likeHtml}
    ${dislikeHtml}
    ${addHtml}
    <button class="iBtn ${dlCls}" ${dlDis} title="${dead?'Недоступен':(st==='done'?'Скачан':'Скачать')}" onclick="stopRow(event);downloadGeneric('${source}','${t.id}')">${icon(_dlIconName(st))}</button>
    ${rmHtml}
  </div>`;
}
function _updateExRow(source,id,popLike){
  const list=_listFor(source);
  const t=list.find(x=>String(x.id)===String(id));
  if(!t) return;
  const el=document.getElementById('exrow-'+source+'-'+t.id)
    || document.getElementById('exrow-'+source+'-'+id);
  if(!el) return;
  const tmp=document.createElement('div');
  tmp.innerHTML=exRowHTML(t,source);
  const fresh=tmp.firstElementChild;
  el.replaceWith(fresh);
  if(popLike){
    const btn=fresh.querySelector('.like-btn');
    if(btn) btn.classList.add('pop');
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
  const t=list.find(x=>String(x.id)===String(trackId));
  if(!t) return;
  const pl=S.myPlaylistsFlat.find(p=>String(p.id)===String(playlistId));
  const key=trackId+'|'+playlistId;
  S.pendingAdds[key]={playlist:pl, trackTitle:t.title, track:t};
  window.pywebview.api.add_to_playlist(playlistId, t.id, t.album_id||null);
  addLog(`Добавляем «${t.title}» в плейлист «${pl?pl.title:''}»...`,'info');
  if(source==='pl_add') _renderPlAddResults();
}
window.addEventListener('py:add_to_playlist_result', e=>{
  const{ok,track_id,playlist_id,msg}=e.detail;
  const key=track_id+'|'+playlist_id;
  const info=S.pendingAdds[key]||{};
  delete S.pendingAdds[key];
  const plTitle=info.playlist?info.playlist.title:'плейлист';
  const trackTitle=info.trackTitle||'Трек';
  const viewing=S.plView==='detail' && String(S.plDetail.id)===String(playlist_id);
  if(ok){
    const pl=info.playlist
      || (S.myPlaylistsFlat||[]).find(p=>String(p.id)===String(playlist_id) && p.group==='created');
    if(pl){
      pl.count=(Number(pl.count)||0)+1;
      CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
      if(pl.url) delete S.plTracksTs[pl.url];
      if(S.plView==='grid') _drawLibraryGrid(true);
    }
    if(viewing){
      if(info.track) _patchTrackIntoOpenPlaylist(info.track);
      S._plJumpTrackId=String(track_id);
      if(S.plDetail.url) window.pywebview.api.open_playlist(S.plDetail.url);
      _jumpToPlTrack(track_id);
    }
    addLog(`✓ «${trackTitle}» добавлен в «${plTitle}»`,'ok');
    showToast({
      kind:'ok',
      icon:'✓',
      message:`«${esc(trackTitle)}» добавлен в плейлист «${esc(plTitle)}»`,
      actionLabel: (!viewing && (info.playlist||pl)) ? 'Открыть плейлист' : null,
      onAction: (!viewing && (info.playlist||pl)) ? ()=>{
        showPage('playlists', _navBtn('playlists'));
        openPlaylist(info.playlist||pl);
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
  if(S.plAddOpen) _renderPlAddResults();
});

/* Поиск каталога Яндекса внутри своего плейлиста — как «Добавить треки» на сайте */
function togglePlAddPanel(){
  if(!S.plDetail.editable) return;
  if(S.plAddOpen) closePlAddPanel();
  else openPlAddPanel();
}
function openPlAddPanel(){
  if(!S.plDetail.editable) return;
  S.plAddOpen=true;
  const panel=document.getElementById('plAddPanel');
  if(panel) panel.classList.add('open');
  _paintPlAddChrome();
  const hint=document.getElementById('plAddHint');
  if(hint && !(S.plAddQuery||'').trim())
    hint.textContent='Начните вводить название или исполнителя';
  const inp=document.getElementById('plAddSearch');
  if(inp){ inp.focus(); if(inp.value) inp.select(); }
}
function closePlAddPanel(){
  S.plAddOpen=false;
  S.plAddSeq++;
  if(S.plAddTimer){ clearTimeout(S.plAddTimer); S.plAddTimer=null; }
  const panel=document.getElementById('plAddPanel');
  if(panel) panel.classList.remove('open');
  _paintPlAddChrome();
}
function _resetPlAddPanel(){
  S.plAddOpen=false;
  S.plAddSeq++;
  if(S.plAddTimer){ clearTimeout(S.plAddTimer); S.plAddTimer=null; }
  S.plAddResults=[];
  S.plAddQuery='';
  S._plJumpTrackId='';
  const panel=document.getElementById('plAddPanel');
  if(panel) panel.classList.remove('open');
  const inp=document.getElementById('plAddSearch');
  if(inp) inp.value='';
  const hint=document.getElementById('plAddHint');
  if(hint) hint.textContent='';
  const box=document.getElementById('plAddResults');
  if(box){ box.hidden=true; box.innerHTML=''; }
  _paintPlAddChrome();
}
function _paintPlAddChrome(){
  const btn=document.getElementById('btnPlAddTracks');
  const show=!!(S.plDetail && S.plDetail.editable);
  if(btn){
    btn.style.display=show?'':'none';
    btn.classList.toggle('active-mode', show && !!S.plAddOpen);
  }
  if(!show){
    S.plAddOpen=false;
    const panel=document.getElementById('plAddPanel');
    if(panel) panel.classList.remove('open');
  }
}
function onPlAddSearchInput(){
  const q=(document.getElementById('plAddSearch').value||'').trim();
  S.plAddQuery=q;
  if(S.plAddTimer) clearTimeout(S.plAddTimer);
  const hint=document.getElementById('plAddHint');
  if(!q){
    S.plAddSeq++;
    S.plAddResults=[];
    if(hint) hint.textContent='Начните вводить название или исполнителя';
    const box=document.getElementById('plAddResults');
    if(box){ box.hidden=true; box.innerHTML=''; }
    return;
  }
  if(q.length<2){
    if(hint) hint.textContent='Ещё буква — и начнём искать';
    return;
  }
  if(hint) hint.textContent='ищем…';
  S.plAddTimer=setTimeout(()=>runPlAddSearch(), q.length<3?380:220);
}
function runPlAddSearch(){
  if(S.plAddTimer){ clearTimeout(S.plAddTimer); S.plAddTimer=null; }
  const q=(document.getElementById('plAddSearch').value||'').trim();
  S.plAddQuery=q;
  if(!q) return;
  const seq=++S.plAddSeq;
  const hint=document.getElementById('plAddHint');
  if(hint) hint.textContent='ищем…';
  window.pywebview.api.search_tracks(q, seq, 'pl_add');
}
function _onPlAddSearchResults(d){
  if(!S.plAddOpen) return;
  if(d.seq!=null && d.seq!==S.plAddSeq) return;
  S.plAddResults=_applyDlList(d.tracks||[]);
  const q=(d.query||'').trim();
  const hint=document.getElementById('plAddHint');
  const n=S.plAddResults.length;
  if(hint) hint.textContent=n?(q?`${n} · «+» добавит в этот плейлист`:''):(q?`Ничего по «${q}»`:'');
  _renderPlAddResults();
}
function _renderPlAddResults(){
  const box=document.getElementById('plAddResults');
  if(!box) return;
  const list=S.plAddResults||[];
  if(!list.length){
    box.hidden=true;
    box.innerHTML='';
    return;
  }
  box.hidden=false;
  box.innerHTML=list.map(t=>_plAddRowHTML(t)).join('');
}
function _plAddRowHTML(t){
  const inPl=_plHasCatalogTrack(t.id);
  const pending=!!S.pendingAdds[t.id+'|'+S.plDetail.id];
  const dead=!_trackPlayable(t);
  const title=esc(t.title||'');
  const artist=esc(t.artist||'');
  let plus;
  if(dead) plus=`<button class="iBtn" disabled title="Трек недоступен">${icon('plus')}</button>`;
  else if(inPl) plus=`<button class="iBtn" disabled title="Уже в плейлисте">${icon('check')}</button>`;
  else if(pending) plus=`<button class="iBtn" disabled title="Добавляем…">${icon('loader')}</button>`;
  else plus=`<button class="iBtn" title="Добавить в этот плейлист" onclick="event.stopPropagation();addCatalogTrackToCurrentPlaylist('${esc(t.id)}')">${icon('plus')}</button>`;
  return `<div class="pl-add-row${inPl?' in-pl':''}${dead?' unavailable':''}">
    <div class="pl-add-meta">
      <div class="tl-title" title="${title}">${title}</div>
      <div class="tl-sub" title="${artist}">${artist}</div>
    </div>
    <div class="pl-add-album" title="${esc(t.album||'')}">${esc(t.album||'')}</div>
    <span class="pl-add-dur">${esc(t.duration||'')}</span>
    ${plus}
  </div>`;
}
function _plHasCatalogTrack(id){
  return (S.plDetail.tracks||[]).some(x=>String(x.id)===String(id));
}
function addCatalogTrackToCurrentPlaylist(trackId){
  if(!S.plDetail.editable || !S.plDetail.id) return;
  const t=(S.plAddResults||[]).find(x=>String(x.id)===String(trackId));
  if(!t || !_trackPlayable(t)) return;
  if(_plHasCatalogTrack(trackId)){
    showToast({kind:'info', icon:'✓', message:'Уже в этом плейлисте'});
    _jumpToPlTrack(trackId);
    return;
  }
  const key=trackId+'|'+S.plDetail.id;
  if(S.pendingAdds[key]) return;
  addToPlaylist(S.plDetail.id, 'pl_add', trackId);
}
function _patchTrackIntoOpenPlaylist(track){
  if(!track || !S.plDetail.editable) return false;
  const id=String(track.id);
  const list=S.plDetail.tracks||(S.plDetail.tracks=[]);
  if(list.some(x=>String(x.id)===id)) return true;
  list.unshift(Object.assign({}, track, {num:1}));
  list.forEach((t,i)=>t.num=i+1);
  if(S.plDetail.url){
    S.plTracksCache[S.plDetail.url]=list;
    S.plTracksTs[S.plDetail.url]=Date.now();
    _persistPlTracks();
  }
  _updatePlDetailCount();
  if(S.playerSource==='playlist_detail') _syncPlayingQueue('playlist_detail');
  return true;
}
function _jumpToPlTrack(id){
  id=String(id||'');
  if(!id) return;
  if(S.plDeadFilter) S.plDeadFilter=false;
  if(!(S.plDetail.tracks||[]).some(t=>String(t.id)===id)) return;
  if(!_plDetailVisibleTracks().some(t=>String(t.id)===id)){
    S.plTrackQuery='';
    const qel=document.getElementById('plTrackSearch');
    if(qel) qel.value='';
  }
  if(S.plView==='detail') renderPlaylistDetail();
  requestAnimationFrame(()=>{
    const el=document.getElementById('exrow-playlist_detail-'+id);
    if(!el) return;
    el.scrollIntoView({block:'center', behavior:'smooth'});
    el.classList.add('pl-just-added');
    setTimeout(()=>el.classList.remove('pl-just-added'), 1600);
  });
}
function _finishPlJump(){
  const id=S._plJumpTrackId;
  if(!id) return;
  S._plJumpTrackId='';
  _jumpToPlTrack(id);
  if(S.plAddOpen) _renderPlAddResults();
}

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
function showPrompt({title='Новый плейлист', text='', placeholder='Название', okLabel='Создать', value='', onOk=null}){
  S.promptAction=onOk;
  document.getElementById('promptTitle').textContent=title;
  const p=document.getElementById('promptText');
  if(text){ p.style.display=''; p.textContent=text; } else p.style.display='none';
  const inp=document.getElementById('promptInput');
  inp.placeholder=placeholder;
  inp.value=value||'';
  document.getElementById('promptOk').textContent=okLabel;
  document.getElementById('promptModal').classList.remove('hidden');
  setTimeout(()=>{ inp.focus(); if(value) inp.select(); },0);
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
function promptRenamePlaylist(key){
  const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===key);
  if(!pl) return;
  if(pl.group && pl.group!=='created') return;
  showPrompt({
    title:'Переименовать плейлист',
    placeholder:'Название плейлиста',
    okLabel:'Сохранить',
    value:pl.title||'',
    onOk:(name)=>{
      if(name===pl.title) return;
      _renamePlaylist(pl, name);
    },
  });
}
function promptRenameCurrentPlaylist(){
  if(!S.plDetail.editable || !S.plDetail.id) return;
  promptRenamePlaylist(_plKey({group:S.plDetail.group, id:S.plDetail.id}));
}
function _renamePlaylist(pl, title){
  if(!pl || pl.id==null || pl.id==='') return;
  const key=String(pl.id);
  if(S.pendingPlaylistRenames[key]) return;
  S.pendingPlaylistRenames[key]={oldTitle:pl.title, playlist:pl};
  _applyPlaylistTitle(key, title);
  window.pywebview.api.rename_playlist(String(pl.id), title);
}
function _applyPlaylistTitle(id, title){
  const key=String(id);
  const pl=(S.myPlaylistsFlat||[]).find(p=>String(p.id)===key && (!p.group || p.group==='created'));
  if(pl){
    pl.title=title;
    CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
    const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
    const name=card&&card.querySelector('.pl-name');
    if(name) name.textContent=title;
  }
  if(S.plDetail.editable && String(S.plDetail.id)===key){
    S.plDetail.title=title;
    const el=document.getElementById('plDetailTitle');
    if(el) el.textContent=title;
  }
}
window.addEventListener('py:playlist_renamed', e=>{
  const{ok,playlist_id,title,playlist,msg}=e.detail||{};
  const key=String(playlist_id||'');
  const pending=S.pendingPlaylistRenames[key];
  delete S.pendingPlaylistRenames[key];
  if(ok){
    const name=(playlist&&playlist.title)||title;
    _applyPlaylistTitle(key, name);
    if(playlist && playlist.cover){
      const pl=(S.myPlaylistsFlat||[]).find(p=>p.group==='created' && String(p.id)===key);
      if(pl && playlist.cover){
        pl.cover=playlist.cover;
        if(pl.url){
          const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
          _paintPlaylistCover(card, pl.cover);
        }
        CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
      }
    }
    showToast({kind:'ok', icon:'✎', message:`Плейлист переименован: «${esc(name)}»`});
    return;
  }
  if(pending) _applyPlaylistTitle(key, pending.oldTitle);
  showToast({kind:'err', icon:'✗', message:`Не удалось переименовать плейлист${msg?': '+esc(msg):''}`});
});
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
  document.querySelectorAll('.iBtn.playing').forEach(b=>{b.classList.remove('playing');_setIcon(b,'play');});
  document.querySelectorAll('.playing-row').forEach(r=>r.classList.remove('playing-row','is-paused'));
}

/* ── Список треков по источнику (для унификации плеера) ── */
function _listFor(source){
  switch(source){
    case 'tracks': return S.tracks;
    case 'downloaded': return S.dlFiles;
    case 'search': return S.searchResults;
    case 'wave': return S.waveTracks;
    case 'playlist_detail': return S.plDetail.tracks;
    case 'pl_add': return S.plAddResults;
    case 'browse': return (_browseTop() || {}).tracks || [];
    case 'dislikes': return S.dislikedTracks || [];
    default: return [];
  }
}
function _idField(source){ return source==='downloaded' ? 'rel_path' : 'id'; }

/*
  Очередь — это список, из которого запустили трек. Держим её отдельно: иначе
  новый поиск или переход на страницу альбома подменяли бы «следующий трек».
*/
function _queue(){
  if(S.playerQueue && S.playerQueue.length) return S.playerQueue;
  return _rowsFor(S.playerSource);
}

/* ── Текущий индекс и получение следующего трека ── */
function _currentIdx(){
  const field=_idField(S.playerSource);
  const id=S.playerTrackId;
  return _queue().findIndex(x=>String(x[field]||x.id)===String(id));
}
function _listLen(){
  return _queue().length;
}
function _goToIndex(idx){
  const t=_queue()[idx];
  if(!t) return;
  if(S.playerSource==='downloaded'){
    playLocalFile(t);
    return;
  }
  _playTrack(t, S.playerSource);
}

/* ── Публичные кнопки ── */
function previewTrack(id){
  previewGeneric('tracks', id);
}
function playerToggle(){
  const a=_audioNow();
  if(!a) return;
  if(a.paused){
    if(!a.getAttribute('src')){
      _resumeLastPlay();
      return;
    }
    a.play().catch(()=>{});
  } else {
    a.pause();
    _cancelCrossfade();
    _stopAudioEl(_audioIdle());
  }
  _updatePlayBtn();
}
let _hwMediaAt=0;
function _fromHardware(fn){
  const now=Date.now();
  if(now-_hwMediaAt<180) return;
  _hwMediaAt=now;
  fn();
}
function mediaPlayPause(){ _fromHardware(playerToggle); }
function mediaPrev(){ _fromHardware(playerPrev); }
function mediaNext(){ _fromHardware(playerNext); }
function _bindMediaSession(){
  if(!('mediaSession' in navigator)) return;
  const set=(name, fn)=>{ try{ navigator.mediaSession.setActionHandler(name, fn); }catch(_e){} };
  set('play', ()=>mediaPlayPause());
  set('pause', ()=>mediaPlayPause());
  set('previoustrack', ()=>mediaPrev());
  set('nexttrack', ()=>mediaNext());
  set('seekbackward', d=>playerSkip(-(d && d.seekOffset || 10)));
  set('seekforward', d=>playerSkip(d && d.seekOffset || 10));
}
function _updateMediaSession(){
  if(!('mediaSession' in navigator)) return;
  const t=S.playerTrack;
  try{
    if(t){
      const art=_bigCoverUrl(t,'300x300') || t.cover_uri || '';
      navigator.mediaSession.metadata=new MediaMetadata({
        title: t.title||t.name||'',
        artist: t.artist||'',
        album: t.album||'',
        artwork: art?[{src:art, sizes:'300x300'}]:[],
      });
    }
    const a=_audioNow();
    navigator.mediaSession.playbackState=(a && !a.paused)?'playing':'paused';
  }catch(_e){}
}
function _lyricsFollowTime(sec){
  S._lyricsUserScroll=false;
  _syncLyricsHighlight(sec, true);
}
function playerSkip(sec){
  const a=_audioNow();
  if(!a) return;
  const media=_audioDurationSec(a);
  const dur=_playDuration(a) || media;
  a.currentTime=Math.max(0, Math.min(dur||0, a.currentTime+sec));
  if(isFinite(a.currentTime)){
    S._savedPosition=a.currentTime;
    _scheduleSaveLastPlay('pos');
    _lyricsFollowTime(a.currentTime);
    playerTimeUpdate();
  }
}
function playerSeek(v){
  const a=_audioNow();
  const t=_currentPlayingTrack();
  const media=_audioDurationSec(a);
  const dur=_playDuration(a, t);
  if(!dur) return;
  const pos=Math.max(0, Math.min(dur, dur*(Number(v)||0)/100));
  _paintPlaybackTimes(pos, dur, v);
  if(a && a.getAttribute('src') && media){
    try{ a.currentTime=Math.min(pos, Math.max(0, media-0.05)); }catch(_e){}
    if(isFinite(a.currentTime)) S._savedPosition=a.currentTime;
  } else {
    S._savedPosition=pos;
    S._resumeAt=pos;
  }
  _scheduleSaveLastPlay('pos');
  _lyricsFollowTime(pos);
}
function playerPrev(){
  const cur=_currentIdx();
  if(cur<0) return;
  const idx=_nextPlayableIndex(cur, -1, {shuffle:S.shuffle, wrap:true});
  if(idx<0) return;
  _goToIndex(idx);
}
function playerNext(){
  // Кнопки Prev/Next всегда переключают трек — повтор влияет только на авто-переход
  _advanceQueue(false);
}
function playerEnded(){
  if(S.repeat==='one'){ const a=_audioNow(); if(a) a.play(); return; }
  _advanceQueue(true);
}
function _onAudioPlay(el){ if(el===_audioNow()) _updatePlayBtn(); }
function _onAudioPause(el){
  if(el!==_audioNow()) return;
  _updatePlayBtn();
  _scheduleSaveLastPlay('pos');
}
function _onAudioEnded(el){
  if(el!==_audioNow()) return;
  S._seekDrag=false;
  const dur=_playDuration(el);
  if(dur) _paintPlaybackTimes(dur, dur, 100);
  playerEnded();
}
function _onAudioTime(el){ if(el===_audioNow()) playerTimeUpdate(); }
function _onAudioCanPlay(el){ if(el===_audioNow()) playerCanPlay(); }
function _onAudioError(el){ if(el===_audioNow()) playerError(); }
function _advanceQueue(fromEnd){
  const cur=_currentIdx();
  const len=_listLen();
  if(cur<0||!len){
    if(fromEnd && S.playerSource!=='wave') _startMyWaveAuto();
    else _updatePlayBtn();
    return;
  }
  if(S.playerSource==='wave'){
    if(!S.waveLoading && (cur>=len-3 || (S.shuffle && S.shufflePos>=(S.shuffleOrder.length-3)))) loadMoreWave();
    const idx=_nextPlayableIndex(cur, 1, {shuffle:S.shuffle});
    if(idx>=0){ _goToIndex(idx); return; }
    S.pendingWavePlay='next';
    loadMoreWave();
    return;
  }
  const idx=_nextPlayableIndex(cur, 1, {shuffle:S.shuffle, wrap:_queueWrap()});
  if(idx<0){
    _startMyWaveAuto();
    return;
  }
  _goToIndex(idx);
}
function playerClose(){
  _cancelCrossfade();
  _stopAudioEl(_audioNow());
  _stopAudioEl(_audioIdle());
  S.audioId='audioEl';
  S._seekDrag=false;
  document.getElementById('player').classList.add('hidden');
  const prevSource=S.playerSource, prevId=S.playerTrackId;
  S.playerTrackId=null;
  S.playerTrack=null;
  S.playerQueue=null;
  if(S.prefetchTimer){ clearTimeout(S.prefetchTimer); S.prefetchTimer=null; }
  _disposePrefetchAudio();
  S.prefetch={id:null,url:null,audio:null};
  S._awaitingPreview=false;
  S._xfadeArmed=false;
  _clearShuffleOrder();
  closeBigView();
  S.playingPlaylistUrl='';
  S.playingCardKey='';
  S.pendingAlbumPlay='';
  S.pendingArtistPlay='';
  _clearLastPlay();
  _paintPlaying();
  _paintCardPlayBtns();
  _updateLikeButtons();
}
function playerCanPlay(){
  const a=_audioNow();
  if(!a || !a.getAttribute('src')) return;
  S.skipStreak=0;
  const applyResume=()=>{
    if(!(S._resumeAt>0)) return;
    const dur=_playDuration(a);
    if(!dur) return;
    try{ a.currentTime=Math.min(S._resumeAt, Math.max(0, dur-0.25)); }catch(_e){}
    S._resumeAt=0;
  };
  applyResume();
  if(S._resumeAt>0) a.addEventListener('loadedmetadata', applyResume, {once:true});
  playerTimeUpdate();
  _setIcon(document.getElementById('plPlayBtn'), 'pause');
  _schedulePrefetch();
}
function playerError(){
  const a=_audioNow();
  if(!a || !a.getAttribute('src')) return;  // сброс src при переключении — не ошибка
  addLog('Ошибка воспроизведения','err');
  const t=_currentPlayingTrack();
  // Сбой превью/сети не значит, что трек снят с сервиса
  _skipFromTrack(t||{id:S.playerTrackId, title:S.playerTrackId});
}
function playerTimeUpdate(){
  const a=_audioNow();
  if(!a || !a.getAttribute('src')) return;
  if(S._seekDrag){
    if(S.bigViewOpen) _syncLyricsHighlight(a.currentTime);
    return;
  }
  const dur=_playDuration(a);
  const pos=isFinite(a.currentTime) ? a.currentTime : 0;
  if(dur){
    const ended=!!a.ended || pos>=dur-0.05;
    const show=ended ? dur : Math.min(pos, dur);
    _paintPlaybackTimes(show, dur, ended ? 100 : show/dur*100);
    S._savedPosition=pos;
    if(!ended) _maybeCrossfadeAdvance(a, dur, pos);
  } else if(isFinite(a.currentTime)){
    S._savedPosition=a.currentTime;
    const api=_apiDurationSec();
    if(api) _paintPlaybackTimes(a.currentTime, api);
  }
  if(S.bigViewOpen) _syncLyricsHighlight(a.currentTime);
}
function _updatePlayBtn(){
  const audio=_audioNow();
  const paused=audio?audio.paused:true;
  _setIcon(document.getElementById('plPlayBtn'), paused?'play':'pause');
  const bigBtn=document.getElementById('bigViewPlayBtn');
  if(bigBtn) _setIcon(bigBtn, paused?'play':'pause');
  _paintPlaying();
  _paintPlaylistPlayBtns();
  _updateMediaSession();
}

/* ── Режимы ── */
function toggleShuffle(){
  S.shuffle=!S.shuffle;
  STORE.set('ym_shuffle',S.shuffle);
  if(S.shuffle) _syncShuffleOrder(_currentIdx());
  else _clearShuffleOrder();
  _applyModeUI();
  if(S.bigViewOpen) _fillBigView();
  _schedulePrefetch();
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
    _setIcon(b, isOne?'repeat-1':'repeat');
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
  if(which==='grid') _revivePlaylistCovers();
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
  } else {
    _revivePlaylistCovers();
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
  pls=_fillPlaylistCovers(pls||[]);
  (pls||[]).forEach(pl=>{
    const cached=S.plTracksCache[pl.url];
    if(Array.isArray(cached) && cached.length) pl.count=cached.length;
  });
  if(pls.length) CACHE.write('ym_pl_cache', pls);
  // Картинки в display:none в WebView часто падают в onerror и навсегда
  // заменяются заглушкой. Рисуем сетку только когда она на экране.
  if(!_playlistGridVisible()){
    S.myPlaylistsFlat=pls;
    S.plRendered=false;
    return;
  }
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
function _artistCardHTML(a, forDislikes){
  return `
    <div class="pl-card artist-card" data-kind="artist" data-id="${esc(a.id)}" data-ym-url="${esc(_ymArtistUrl(a.id))}" onclick="openArtist('${esc(a.id)}')" title="${esc(a.name)}">
      ${a.cover
        ?`<img class="pl-cover" src="${esc(a.cover)}" alt="" onerror="this.style.display='none'">`
        :`<div class="pl-cover-ph">${icon('mic')}</div>`}
      <button class="iBtn card-play" data-play-key="artist:${esc(a.id)}" title="Играть все треки"
        onclick="event.stopPropagation();playArtistCard('${esc(a.id)}')">${icon('play')}</button>
      ${forDislikes?_entityDislikeBtn(a.id, false):_entityLikeBtn('artist', a.id, false)}
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
function openDislikesPage(){
  renderDislikes();
  loadDislikedLibrary(false);
}
function showDislikesTab(tab){
  S.dislikesTab=tab==='artists'?'artists':'tracks';
  renderDislikes();
}
function loadDislikedLibrary(force){
  if(!force && CACHE.fresh('ym_disliked_library')) return;
  window.pywebview.api.get_disliked_library();
}
function _applyDislikedLibrary(d){
  S.dislikedTracks=_applyDlList((d&&d.tracks)||[]);
  S.dislikedArtists=(d&&d.artists)||[];
  S.dislikedIds=new Set(S.dislikedTracks.map(t=>String(t.id)).filter(Boolean));
  S.dislikedArtistIds=new Set(S.dislikedArtists.map(a=>String(a.id)).filter(Boolean));
  _persistDislikes();
  renderDislikes();
  _paintEntityLikes();
  _updateLikeButtons();
  if(S.playerSource==='dislikes') _adoptRestoredSourceQueue('dislikes', _rowsFor('dislikes'));
}
window.addEventListener('py:disliked_library', e=>_applyDislikedLibrary(e.detail||{}));
function renderDislikes(){
  const body=document.getElementById('dislikesBody');
  const table=document.getElementById('dislikesTable');
  const alt=document.getElementById('dislikesAlt');
  if(!body) return;
  const tab=S.dislikesTab||'tracks';
  const tabT=document.getElementById('disTabTracks');
  const tabA=document.getElementById('disTabArtists');
  if(tabT) tabT.classList.toggle('active-mode', tab==='tracks');
  if(tabA) tabA.classList.toggle('active-mode', tab==='artists');
  const tools=document.getElementById('disTracksTools');
  if(tools) tools.style.display=tab==='tracks'?'':'none';
  const count=document.getElementById('dislikesCount');
  if(tab==='artists'){
    if(table) table.style.display='none';
    if(alt) alt.style.display='';
    if(count) count.textContent=S.dislikedArtists.length?`${S.dislikedArtists.length}`:'';
    if(!S.dislikedArtists.length){
      alt.innerHTML=`<div class="empty">${_emptyIcon('heart-break')}<p>Нет скрытых исполнителей — нажмите «Не рекомендовать» на странице артиста</p></div>`;
      return;
    }
    alt.innerHTML=`<div class="pl-grid" style="padding-bottom:20px;">${S.dislikedArtists.map(a=>_artistCardHTML(a,true)).join('')}</div>`;
    _paintCardPlayBtns();
    return;
  }
  if(alt) alt.style.display='none';
  if(table) table.style.display='flex';
  if(count) count.textContent=S.dislikedTracks.length?`${S.dislikedTracks.length} треков`:'';
  if(!S.dislikedTracks.length){
    _paintExHead('dislikesHead','dislikes',false);
    body.innerHTML=`<div class="empty">${_emptyIcon('heart-break')}<p>Нет скрытых треков — нажмите «Не рекомендовать» у трека</p></div>`;
    _updateSelBtn('dislikes');
    return;
  }
  _paintExHead('dislikesHead','dislikes',true);
  body.innerHTML=_rowsFor('dislikes').map(t=>exRowHTML(t,'dislikes')).join('');
  _updateSelBtn('dislikes');
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
function _firstTrackCover(tracks){
  const t=(tracks||[]).find(x=>x && _trackPlayable(x) && (x.cover_uri_tmpl||x.cover_uri));
  if(!t) return '';
  if(t.cover_uri_tmpl) return t.cover_uri_tmpl.replace('%%','100x100');
  return t.cover_uri;
}
function _playlistCover(pl){
  if(!pl) return '';
  if(pl.cover) return pl.cover;
  return _firstTrackCover(S.plTracksCache[pl.url]);
}
function _fillPlaylistCovers(pls){
  const prev={};
  (S.myPlaylistsFlat||[]).forEach(p=>{ if(p && p.cover) prev[_plKey(p)]=p.cover; });
  return (pls||[]).map(pl=>{
    if(pl.cover) return pl;
    const cover=_firstTrackCover(S.plTracksCache[pl.url]) || prev[_plKey(pl)] || '';
    return cover ? Object.assign({}, pl, {cover}) : pl;
  });
}
function _paintPlaylistCover(card, cover){
  if(!card || !cover) return;
  let img=card.querySelector('.pl-cover');
  const ph=card.querySelector('.pl-cover-ph');
  if(img && !_coverImgBroken(img) && img.naturalWidth
     && (img.dataset.coverUrl===cover || img.getAttribute('src')===cover)){
    img.style.display='';
    return;
  }
  if(img){
    img.style.display='';
    img.dataset.sizeTry='0';
    img.dataset.trackTried='';
    _setCoverSrc(img, cover);
    return;
  }
  img=document.createElement('img');
  img.className='pl-cover';
  img.referrerPolicy='no-referrer';
  if(ph) ph.replaceWith(img);
  else card.insertBefore(img, card.firstChild);
  _setCoverSrc(img, cover);
}
function _coverImgBroken(img){
  return !img || img.dataset.needRetry==='1' || (img.complete && !img.naturalWidth);
}
function _revivePlaylistCovers(){
  if(!_playlistGridVisible()) return;
  document.querySelectorAll('#plGrid .pl-card[data-kind="pl"]').forEach(card=>{
    const pl=(S.myPlaylistsFlat||[]).find(p=>_plKey(p)===card.dataset.key);
    const cover=_playlistCover(pl);
    if(!cover) return;
    const img=card.querySelector('.pl-cover');
    if(img){
      if(img.naturalWidth) return;
      if(!img.complete && img.dataset.needRetry!=='1') return;
    }
    _paintPlaylistCover(card, cover);
  });
}
function _syncPlaylistCount(url, n){
  const pl=(S.myPlaylistsFlat||[]).find(p=>p.url===url);
  if(!pl || Number(pl.count)===Number(n)) return;
  pl.count=n;
  CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
  const el=card && card.querySelector('.pl-count');
  if(el) el.textContent=n+' треков';
}
function _applyPlaylistCoverFromTracks(url, tracks){
  const cover=_firstTrackCover(tracks);
  if(!cover) return;
  const pl=(S.myPlaylistsFlat||[]).find(p=>p.url===url);
  if(!pl) return;
  const card=document.querySelector('#plGrid .pl-card[data-kind="pl"][data-key="'+_plKey(pl)+'"]');
  const img=card && card.querySelector('.pl-cover');
  if(pl.cover && img && !_coverImgBroken(img) && img.naturalWidth) return;
  if(!pl.cover){
    pl.cover=cover;
    CACHE.write('ym_pl_cache', S.myPlaylistsFlat);
  }
  _paintPlaylistCover(card, pl.cover || cover);
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
      <div class="pl-card" data-kind="pl" data-key="${esc(_plKey(pl))}" data-ym-url="${esc(pl.url||'')}" onclick="openPlaylistByKey('${esc(_plKey(pl))}')" title="Открыть плейлист">
        ${_playlistCover(pl)
          ?`<img class="pl-cover" src="${esc(_playlistCover(pl))}" alt="" referrerpolicy="no-referrer" onerror="plCoverError(this)">`
          :`<div class="pl-cover-ph">${icon('music')}</div>`}
        <button class="iBtn card-play" data-play-key="pl:${esc(pl.url)}" title="Играть"
          onclick="event.stopPropagation();playPlaylistCard('${esc(_plKey(pl))}')">${icon('play')}</button>
        ${pl.group==='created'
          ?`<button class="iBtn card-rename" title="Переименовать"
              onclick="event.stopPropagation();promptRenamePlaylist('${esc(_plKey(pl))}')">${icon('pencil')}</button>
            <button class="iBtn card-del del-btn" title="Удалить плейлист"
              onclick="event.stopPropagation();confirmDeletePlaylist('${esc(_plKey(pl))}')">${icon('trash')}</button>`
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
    const countText=`${pl.count} треков`;
    if(name && name.textContent!==pl.title && !S.pendingPlaylistRenames[String(pl.id)]) name.textContent=pl.title;
    if(count && count.textContent!==countText) count.textContent=countText;
    if(pl.url) card.setAttribute('data-ym-url', pl.url);
    _paintPlaylistCover(card, _playlistCover(pl));
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
  if(cached && cached.length && _firstPlayable(cached)){
    _startPlaylistPlayback(pl, cached);
  } else {
    S.pendingPlaylistPlay=pl;
    _paintCardPlayBtns();
  }
  window.pywebview.api.open_playlist(pl.url);
}
function _startPlaylistPlayback(pl, tracks){
  if(!pl || !tracks || !tracks.length) return;
  const first=_firstPlayable(tracks);
  if(!first){
    showToast({kind:'err', icon:'⊘', message:'В плейлисте нет доступных треков'});
    return;
  }
  S.playingPlaylistUrl=pl.url;
  _setPlayingCard('pl', pl.url);
  _playTrack(first, 'playlist_detail', tracks);
}
function _setPlayingCard(kind, id){
  S.playingCardKey=(kind && id) ? kind+':'+id : '';
  if(kind!=='pl') S.playingPlaylistUrl='';
  if(kind!=='album') S.pendingAlbumPlay='';
  if(kind!=='artist') S.pendingArtistPlay='';
  _paintCardPlayBtns();
}
function _paintCardPlayBtns(){
  const audio=_audioNow();
  const paused=!audio || audio.paused;
  document.querySelectorAll('.card-play[data-play-key]').forEach(btn=>{
    const key=btn.dataset.playKey;
    const pending=(S.pendingAlbumPlay && key==='album:'+S.pendingAlbumPlay)
      || (S.pendingArtistPlay && key==='artist:'+S.pendingArtistPlay)
      || (S.pendingPlaylistPlay && key==='pl:'+S.pendingPlaylistPlay.url);
    const on=S.playingCardKey===key;
    btn.classList.toggle('on', !!(pending || (on && !paused)));
    btn.innerHTML=icon(pending?'loader':((on && !paused)?'pause':'play'));
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
  const first=_firstPlayable(list);
  if(!first) return;
  S.pendingAlbumPlay='';
  S.playingPlaylistUrl='';
  _setPlayingCard('album', id);
  _playTrack(first, 'browse', list);
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
  const first=_firstPlayable(list);
  if(!first){
    if(hasMore){
      S.pendingArtistPlay=id;
      window.pywebview.api.open_artist_tracks(id, (page||0)+1);
    }
    return;
  }
  S.pendingArtistPlay='';
  S.playingPlaylistUrl='';
  _setPlayingCard('artist', id);
  _playTrack(first, 'browse', list);
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
  const top=_browseTop();
  if(S.playerSource==='browse' && top && top.type==='artist_tracks')
    S.playerQueue=_rowsFor('browse');
  else
    S.playerQueue=q;
  if(S.shuffle) _syncShuffleOrder(_currentIdx());
  if(S.bigViewOpen) _fillBigView();
  _schedulePrefetch();
  _scheduleSaveLastPlay('identity');
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
  S.plDeadFilter=false;
  S.pendingDeadRemoval=false;
  const qel=document.getElementById('plTrackSearch');
  if(qel) qel.value='';
  _paintPlDeadFilterBtn();
  S.sortBy.playlist_detail={key:'num', dir:1};
  _clearSel('playlist_detail');
  _showPlSubView('detail');
  const titleEl=document.getElementById('plDetailTitle');
  titleEl.textContent=pl.title;
  if(pl.url) titleEl.setAttribute('data-ym-url', pl.url);
  else titleEl.removeAttribute('data-ym-url');
  const delBtn=document.getElementById('btnPlDelete');
  if(delBtn) delBtn.style.display=S.plDetail.editable?'':'none';
  const renameBtn=document.getElementById('btnPlRename');
  if(renameBtn) renameBtn.style.display=S.plDetail.editable?'':'none';
  _resetPlAddPanel();

  // Уже открытый однажды плейлист показываем из кэша сразу, не заставляя ждать сеть
  const isPlayingPl=S.playerSource==='playlist_detail' && S.playingPlaylistUrl===pl.url;
  if(S._locatePin || isPlayingPl) S._jumpPlayingList=true;
  const cached=S.plTracksCache[pl.url];
  const ts=S.plTracksTs[pl.url]||0;
  const fresh=!!(cached && cached.length && ts && Date.now()-ts<CACHE.TTL);
  const countMismatch=Number(pl.count)>0 && cached && cached.length!==Number(pl.count);
  S._plLocateWait=!!((S._locatePin || S._jumpPlayingList) && !(fresh && !countMismatch));
  if(cached && cached.length){
    _applyDlList(cached);
    S.plDetail.tracks=cached;
    _applyPlaylistCoverFromTracks(pl.url, cached);
    _updatePlDetailCount();
    renderPlaylistDetail({jumpPlaying:S._jumpPlayingList});
  } else {
    document.getElementById('plDetailCount').textContent='Загрузка...';
    document.getElementById('plDetailBody').innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем треки...</p></div>`;
  }
  // Всегда ходим в API: состав могли поменять в вебе, а кэш живёт 30 минут.
  window.pywebview.api.open_playlist(pl.url);
}
function closePlaylistDetail(){
  _resetPlAddPanel();
  S.plView='grid';
  _showPlSubView('grid');
  if(!S.plRendered && S.myPlaylistsFlat.length) renderMyPlaylists(S.myPlaylistsFlat);
}
window.addEventListener('py:playlist_tracks', e=>{
  const{url,tracks}=e.detail;
  let fresh=_applyDlList(tracks||[]);
  const prevList=(S.plView==='detail' && S.plDetail.url===url ? S.plDetail.tracks : S.plTracksCache[url])||[];
  if(!fresh.length && prevList.length){
    fresh=prevList.slice();
  }
  const jumpId=S._plJumpTrackId;
  if(jumpId && S.plView==='detail' && S.plDetail.url===url
     && !fresh.some(t=>String(t.id)===String(jumpId))){
    const have=(S.plDetail.tracks||[]).find(t=>String(t.id)===String(jumpId));
    if(have) fresh=[have, ...fresh];
  }
  S.plTracksCache[url]=fresh;
  S.plTracksTs[url]=Date.now();
  _persistPlTracks();
  _applyPlaylistCoverFromTracks(url, fresh);
  if(S.pendingPlaylistPlay && S.pendingPlaylistPlay.url===url){
    const pl=S.pendingPlaylistPlay;
    S.pendingPlaylistPlay=null;
    if(fresh.length) _startPlaylistPlayback(pl, fresh);
  }
  if(S.playerSource==='playlist_detail' && S.playingPlaylistUrl===url)
    _adoptRestoredSourceQueue('playlist_detail', fresh);
  if(S.plView!=='detail'||S.plDetail.url!==url) return;
  S._plLocateWait=false;
  const jump=!!(S._jumpPlayingList || S._locatePin);
  const prev=S.plDetail.tracks||[];
  const cardCount=Number((S.myPlaylistsFlat||[]).find(p=>p.url===url)?.count||0);
  const longer=fresh.length>prev.length;
  const same=!longer && prev.length===fresh.length && prev.every((t,i)=>
    t.id===fresh[i].id && t.available===fresh[i].available && t.title===fresh[i].title);
  _syncPlaylistCount(url, fresh.length);
  if(same && !(cardCount>prev.length)){
    _updatePlDetailCount();
    if(jump) _scrollPlayingIntoView(true);
    _finishPlJump();
    return;
  }
  S.plDetail.tracks=fresh;
  _clearSel('playlist_detail');
  _updatePlDetailCount();
  renderPlaylistDetail({jumpPlaying:jump});
  _playListEnter(document.getElementById('plDetailBody'));
  _finishPlJump();
});
function renderPlaylistDetail(opts){
  const body=document.getElementById('plDetailBody');
  if(!body) return;
  _paintPlDeadFilterBtn();
  if(!S.plDetail.tracks.length){
    _paintExHead('plDetailHead','playlist_detail',false);
    const empty=S.plDetail.editable
      ? 'Плейлист пуст. Нажмите «+», чтобы найти треки в Яндекс.Музыке'
      : 'Треков нет или не удалось загрузить';
    body.innerHTML=`<div class="empty"><span class="empty-icon">🎵</span><p>${empty}</p></div>`;
    return;
  }
  const visible=_plDetailVisibleTracks();
  if(!visible.length){
    _paintExHead('plDetailHead','playlist_detail',false);
    const q=(S.plTrackQuery||'').trim();
    const msg=S.plDeadFilter
      ? (q?`Нет недоступных треков по запросу «${esc(q)}»`:'Недоступных треков нет')
      : (q?`В плейлисте нет треков по запросу «${esc(q)}»`:'Треков нет или не удалось загрузить');
    body.innerHTML=`<div class="empty"><span class="empty-icon">${S.plDeadFilter||q?'🔍':'🎵'}</span><p>${msg}</p></div>`;
    _updateSelBtn('playlist_detail');
    return;
  }
  _paintExHead('plDetailHead','playlist_detail',true);
  const keepScroll=body.scrollTop;
  const jump=(opts && opts.jumpPlaying) || S._jumpPlayingList || S._locatePin;
  body.innerHTML=visible.map(t=>exRowHTML(t,'playlist_detail')).join('');
  if(jump) _scrollPlayingIntoView(true);
  else body.scrollTop=keepScroll;
  _updateSelBtn('playlist_detail');
  _paintPlaying();
}
function downloadAllPlaylistDetail(){
  const tracks=(S.plDetail.tracks||[]).filter(_trackPlayable);
  if(!tracks.length) return;
  window.pywebview.api.start_download(tracks);
  tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  renderPlaylistDetail();
  addLog(`В очереди: ${tracks.length} треков из плейлиста «${S.plDetail.title}»`,'info');
}

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
  showPage('playlists', _navBtn('playlists'));
  S.plView='wave';
  _showPlSubView('wave');
}
function startTrackWave(evt,source,id){
  if(evt) evt.stopPropagation();
  const t=_trackFor(source,id) || _listFor(source).find(x=>x.id===id);
  if(!t || t.local || !_trackPlayable(t)) return;
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
  _paintExHead('waveHead','wave',false);
  _updateWaveBtns();
  if(seed) _playTrack(seed, 'wave', [seed]);
  window.pywebview.api.start_wave(S.waveStation);
}
function openWave(){
  S.plView='wave';
  _showPlSubView('wave');
  _paintWaveTitle();
  if(!S.waveTracks.length){
    _paintExHead('waveHead','wave',false);
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
    _scrollPlayingIntoView(true);
  }
}
function closeWave(){
  S.plView='grid';
  _showPlSubView('grid');
  if(!S.plRendered && S.myPlaylistsFlat.length) renderMyPlaylists(S.myPlaylistsFlat);
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
  _paintExHead('waveHead','wave',false);
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
  if(S.playerSource==='wave') S.playerQueue=_rowsFor('wave');
  if(S.playerSource==='wave' && S.shuffle) _syncShuffleOrder(_currentIdx());
  _updateWaveBtns();
  if(S.plView==='wave') renderWave();

  if(playMode==='next' && fresh.length){
    _playTrack(fresh[0], 'wave', _rowsFor('wave'));
  } else if(playMode==='seed'){
    S.playerSource='wave';
    S.playerQueue=_rowsFor('wave');
  } else if(playMode && S.waveTracks.length){
    _playTrack(S.waveTracks[0], 'wave', _rowsFor('wave'));
  } else if(S.playerSource==='wave'){
    _scheduleSaveLastPlay('identity');
    if(S.bigViewOpen) _fillBigView();
    _schedulePrefetch();
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
    _paintExHead('waveHead','wave',false);
    body.innerHTML=`<div class="empty"><span class="empty-icon">🌊</span><p>${S.waveLoading?'Загружаем...':'Не удалось загрузить волну — нужна авторизация'}</p></div>`;
    return;
  }
  _paintExHead('waveHead','wave',true);
  const keepScroll=body.scrollTop;
  body.innerHTML=_rowsFor('wave').map(t=>exRowHTML(t,'wave')).join('')
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
  const tracks=(S.waveTracks||[]).filter(_trackPlayable);
  if(!tracks.length) return;
  window.pywebview.api.start_download(tracks);
  tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  renderWave();
  addLog(`В очереди: ${tracks.length} треков из волны`,'info');
}

/* ═══════════════════════════════════════════════════════════════════
   ВЫБОР ТРЕКОВ ДЛЯ СКАЧИВАНИЯ (волна / плейлист / исполнитель / альбом)
═══════════════════════════════════════════════════════════════════ */
const SELECTABLE_SOURCES=['wave','playlist_detail','browse','dislikes'];
const DL_ALL_BTN={wave:'btnWaveDownloadAll', playlist_detail:'btnPlDownloadAll', browse:'btnBrowseDownloadAll', dislikes:'btnDisDownloadAll'};
function _selectable(source){ return SELECTABLE_SOURCES.includes(source); }
function _selSet(source){ return S.sel[source] || (S.sel[source]=new Set()); }
function _clearSel(source){ S.sel[source]=new Set(); _updateSelBtn(source); }

function _sortState(source){
  return S.sortBy[source] || {key: source==='downloaded'?'title':'num', dir:1};
}
function _durMs(t){
  if(t && t.duration_ms) return Number(t.duration_ms)||0;
  const s=String((t&&t.duration)||'');
  const m=s.match(/(\d+):(\d+)/);
  return m?(+m[1]*60+ +m[2])*1000:0;
}
const _NUM_SORT={num:1,dur:1,size:1,status:1};
function _sortVal(item, key){
  if(!item) return '';
  if(item.rel_path!=null && item.uid){
    if(key==='title') return String(item.title||item.name||'').toLowerCase();
    if(key==='artist') return String(item.artist||'').toLowerCase();
    if(key==='ext') return String(item.ext||'').toLowerCase();
    if(key==='size') return Number(item.size)||0;
    return String(item.title||item.name||'').toLowerCase();
  }
  if(key==='num') return Number(item.num)||0;
  if(key==='title') return String(item.title||'').toLowerCase();
  if(key==='artist') return String(item.artist||'').toLowerCase();
  if(key==='album') return String(item.album||'').toLowerCase();
  if(key==='dur') return _durMs(item);
  if(key==='status') return ({idle:0,queued:1,downloading:2,done:3,error:4}[item.status]||0);
  if(key==='size') return Number(item.size)||0;
  return String(item.title||'').toLowerCase();
}
function _cmpSort(a,b,key,dir){
  const va=_sortVal(a,key), vb=_sortVal(b,key);
  let r=0;
  if(_NUM_SORT[key] || (typeof va==='number' && typeof vb==='number')) r=(Number(va)||0)-(Number(vb)||0);
  else r=String(va).localeCompare(String(vb),'ru',{numeric:true,sensitivity:'base'});
  if(!r) r=(Number(a.num)||0)-(Number(b.num)||0);
  if(!r) r=String(a.id||a.uid||a.rel_path||'').localeCompare(String(b.id||b.uid||b.rel_path||''),'en');
  return r*dir;
}
function _sortedCopy(list, source){
  const arr=(list||[]).slice();
  if(arr.length<2) return arr;
  const st=_sortState(source);
  arr.sort((a,b)=>_cmpSort(a,b,st.key,st.dir));
  return arr;
}
function _rowsFor(source){
  if(source==='playlist_detail') return _plDetailVisibleTracks();
  if(source==='browse'){
    const en=_browseTop();
    if(!en) return [];
    if(en.type==='artist') return _sortedCopy((en.tracks||[]).slice(0,10), source);
    if(en.type==='artist_tracks') return _sortedCopy(_artistTracksVisible(en), source);
    return _sortedCopy(en.tracks||[], source);
  }
  return _sortedCopy(_listFor(source)||[], source);
}
function sortTable(source, key){
  const cur=_sortState(source);
  S.sortBy[source]={key, dir: cur.key===key ? -cur.dir : 1};
  if(source==='tracks') renderTracks();
  else if(source==='playlist_detail') renderPlaylistDetail();
  else if(source==='wave') renderWave();
  else if(source==='search') renderSearchResults(false);
  else if(source==='dislikes') renderDislikes();
  else if(source==='browse'){
    const en=_browseTop();
    if(en && en.type==='artist_tracks' && document.getElementById('artistTracksList'))
      _paintArtistTracksList(en, true);
    else renderBrowse();
  }
  else if(source==='downloaded') renderDownloaded(S.dlFiles);
  _syncPlayingQueue(source);
}
function _syncPlayingQueue(source){
  if(S.playerSource!==source) return;
  S.playerQueue=_rowsFor(source);
  _scheduleSaveLastPlay('identity');
}
function _headVis(source){
  return _rowsFor(source);
}
function _th(source,key,label,align){
  const st=_sortState(source);
  const on=st.key===key;
  const mark=on?(st.dir>0?'▲':'▼'):'';
  return `<button type="button" class="th-sort${on?' on':''}${align==='right'?' right':''}" onclick="event.stopPropagation();sortTable('${source}','${key}')">${label}${mark?`<span class="th-dir">${mark}</span>`:''}</button>`;
}
function _exHeadHTML(source){
  if(source==='tracks'){
    const n=S.selected.size, total=S.tracks.length;
    return `<div class="tl-head">
      <input type="checkbox" class="cb head-cb" data-src="tracks" style="margin:auto" ${total&&n===total?'checked':''} onchange="selAll(this.checked)">
      ${_th('tracks','num','#','right')}
      ${_th('tracks','title','Трек')}
      ${_th('tracks','album','Альбом')}
      ${_th('tracks','dur','Длит.','right')}
      ${_th('tracks','status','Статус','right')}
      <span></span><span></span>
    </div>`;
  }
  if(source==='downloaded'){
    const n=S.dlSelected.size, total=S.dlFiles.length;
    return `<div class="tl-head dl-head">
      <input type="checkbox" class="cb head-cb" data-src="downloaded" ${total&&n===total?'checked':''} onchange="dlSelectAll(this.checked)">
      <span></span>
      ${_th('downloaded','title','Файл')}
      ${_th('downloaded','ext','Тип')}
      ${_th('downloaded','size','Размер','right')}
      <span></span><span></span>
    </div>`;
  }
  const selectable=_selectable(source);
  const removable=source==='playlist_detail' && S.plDetail.editable;
  const vis=_headVis(source);
  const playable=vis.filter(_trackPlayable);
  const selected=playable.filter(t=>_selSet(source).has(t.id)).length;
  const all=playable.length;
  const cb=selectable
    ? `<input type="checkbox" class="cb head-cb" data-src="${source}" ${all&&selected===all?'checked':''} onchange="selectAllIn('${source}',this.checked)">`
    : '';
  const cls=['tl-head','ex-head', selectable?'selectable':'', removable?'removable':''].filter(Boolean).join(' ');
  const actions=6+(removable?1:0);
  return `<div class="${cls}">
    ${cb}
    ${_th(source,'num','#','right')}
    ${_th(source,'title','Трек')}
    ${_th(source,'album','Альбом')}
    ${_th(source,'dur','Длит.','right')}
    ${'<span></span>'.repeat(actions)}
  </div>`;
}
function _exTableHTML(source, rowsHtml, extra, tableId, pinTitle){
  const id=tableId?` id="${esc(tableId)}"`:'';
  const pin=pinTitle
    ? `<div class="br-pin"><div class="br-sec">${pinTitle}</div>${_exHeadHTML(source)}</div>`
    : _exHeadHTML(source);
  return `<div class="tl-wrap"${id}>${pin}<div class="tl-body ex-body">${rowsHtml||''}${extra||''}</div></div>`;
}
function _paintExHead(id, source, hasRows){
  const el=document.getElementById(id);
  if(!el) return;
  el.innerHTML=hasRows?_exHeadHTML(source):'';
  if(hasRows) _syncHeadCheck(source);
}
function _syncHeadCheck(source){
  const cb=document.querySelector('.head-cb[data-src="'+source+'"]');
  if(!cb) return;
  let total=0, selected=0;
  if(source==='downloaded'){
    total=S.dlFiles.length;
    selected=S.dlSelected.size;
  } else if(source==='tracks'){
    total=S.tracks.length;
    selected=S.selected.size;
  } else {
    const playable=_headVis(source).filter(_trackPlayable);
    total=playable.length;
    selected=playable.filter(t=>_selSet(source).has(t.id)).length;
  }
  cb.indeterminate=selected>0&&selected<total;
  cb.checked=total>0&&selected===total;
}

function toggleSel(source,id,checked){
  const set=_selSet(source);
  if(checked) set.add(id); else set.delete(id);
  _updateSelBtn(source);
}
/* Отмечаем чекбоксы на месте — перерисовывать весь список ради галочек незачем */
function selectAllIn(source,v){
  const raw=source==='playlist_detail'?_plDetailVisibleTracks()
    : source==='browse'?_browseVisibleTracks()
    : _listFor(source);
  const list=(raw||[]).filter(_trackPlayable);
  S.sel[source]= v ? new Set(list.map(t=>t.id)) : new Set();
  list.forEach(t=>{
    const row=document.getElementById('exrow-'+source+'-'+t.id);
    const box=row&&row.querySelector('.cb');
    if(box) box.checked=v;
  });
  _updateSelBtn(source);
}
function _downloadAllLabel(source){
  if(source==='browse'){
    const en=_browseTop();
    const n=((en&&en.tracks)||[]).filter(_trackPlayable).length;
    if(en && en.type==='album') return `Скачать альбом (${n})`;
    if(en && en.type==='artist') return `Скачать треки (${n})`;
    return `Скачать все (${n})`;
  }
  return 'Скачать все';
}
function _downloadAllInner(source, selectedN){
  const label=selectedN>0?`Скачать выбранные (${selectedN})`:_downloadAllLabel(source);
  return `${icon('download')}<span>${label}</span>`;
}
function downloadVisibleOrSelected(source){
  if(_selSet(source).size) downloadSelected(source);
  else if(source==='playlist_detail') downloadAllPlaylistDetail();
  else if(source==='wave') downloadAllWave();
  else if(source==='browse') browseDownloadAll();
  else if(source==='dislikes') downloadAllDislikes();
}
function downloadAllDislikes(){
  const tracks=(S.dislikedTracks||[]).filter(_trackPlayable);
  if(!tracks.length) return;
  window.pywebview.api.start_download(tracks);
  tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  renderDislikes();
  addLog(`В очереди: ${tracks.length} треков из дизлайков`,'info');
}
function _updateSelBtn(source){
  _syncHeadCheck(source);
  const btn=document.getElementById(DL_ALL_BTN[source]);
  if(!btn) return;
  const n=_selSet(source).size;
  btn.innerHTML=_downloadAllInner(source, n);
}
function downloadSelected(source){
  const set=_selSet(source);
  const tracks=_listFor(source).filter(t=>set.has(t.id) && _trackPlayable(t));
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

function _browseGetScroll(){
  const page=document.getElementById('browseBody');
  const table=page && (page.querySelector('.tl-body') || page.querySelector('.ex-body') || page.querySelector('.br-scroll'));
  return {
    page: table?table.scrollTop:(page?page.scrollTop:0),
    table: table?table.scrollTop:0
  };
}
function _browseSetScroll(pos){
  const page=document.getElementById('browseBody');
  if(!page) return;
  const table=page.querySelector('.tl-body') || page.querySelector('.ex-body') || page.querySelector('.br-scroll');
  const top=typeof pos==='number' ? pos : ((pos && (pos.table||pos.page))||0);
  if(table) table.scrollTop=top;
  else page.scrollTop=top;
}
function _artistTracksCacheReady(cached){
  return !!(cached && !cached.has_more && (cached.tracks||[]).length);
}
function _browseArtistInfo(id, top){
  if(top && top.id===id && top.info) return top.info;
  const art=S.browseCache['artist:'+id];
  return (art && art.artist) || null;
}
function _browsePush(type,id,title){
  if(!id) return;
  id=String(id);
  const top=_browseTop();
  if(top){
    if(top.type===type && top.id===id){
      if(!S.browseOpen) _openBrowseView();
      if(S._jumpPlayingBrowse || S._locatePin) _tryJumpPlayingBrowse();
      return;
    }
    // Переход с альбома на его же исполнителя — это возврат, а не новый шаг
    const prev=S.browseStack[S.browseStack.length-2];
    if(prev && prev.type===type && prev.id===id){
      const jump=!!(S._jumpPlayingBrowse || S._locatePin);
      browseBack();
      if(jump){
        S._jumpPlayingBrowse=true;
        _tryJumpPlayingBrowse();
      }
      return;
    }
    top.scroll=_browseGetScroll();
  }
  if(S.bigViewOpen) closeBigView();
  const cached=S.browseCache[type+':'+id];
  const cacheReady=type==='artist_tracks' ? _artistTracksCacheReady(cached) : !!cached;
  const entry={type, id, title, tracks:[], albums:[], info:null, loading:!cacheReady,
    error:'', scroll:0, page:0, hasMore:false, total:0, loadingMore:false, trackQuery:''};
  if(type==='artist_tracks') entry.info=_browseArtistInfo(id, top);
  if(cacheReady){
    if(type==='artist_tracks') _browseFillTracks(entry,cached);
    else _browseFill(entry,cached);
  }
  S.browseStack.push(entry);
  S.sortBy.browse={key:'num', dir:1};
  _clearSel('browse');
  _openBrowseView();
  if(S._locatePin) S._jumpPlayingBrowse=true;
  renderBrowse();
  if(type==='artist_tracks'){
    if(S._locatePin) S._browseLocateWait=!cacheReady;
    if(cacheReady) return;
    window.pywebview.api.open_artist_tracks(id, 0);
    return;
  }
  const key=type+':'+id;
  const fresh=cached && S.browseCacheTs[key] && (Date.now()-S.browseCacheTs[key]<CACHE.TTL);
  if(S._locatePin) S._browseLocateWait=!fresh;
  if(fresh) return;
  if(type==='artist') window.pywebview.api.open_artist(id);
  else if(type==='album') window.pywebview.api.open_album(id);
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
  } else if(type==='album' && d.ok && S.playerSource==='browse' && S.playingCardKey==='album:'+id){
    _adoptRestoredSourceQueue('browse', _applyDlList((d.tracks||[]).slice()));
  }
  let topChanged=false;
  S.browseStack.forEach((en,i)=>{
    if(en.type!==type || en.id!==id) return;
    if(d.ok) _browseFill(en,d);
    else { en.loading=false; if(!en.tracks.length) en.error=d.msg||'Не удалось загрузить'; }
    if(i===S.browseStack.length-1) topChanged=true;
  });
  if(topChanged && S.browseOpen){
    S._browseLocateWait=false;
    if(S._locatePin) S._jumpPlayingBrowse=true;
    renderBrowse();
  }
}
window.addEventListener('py:artist_page', e=>_browseReceive('artist', e.detail));
window.addEventListener('py:album_page',  e=>_browseReceive('album',  e.detail));
window.addEventListener('py:artist_tracks_page', e=>{
  const d=e.detail||{};
  const id=String(d.id||'');
  const page=d.page||0;
  let topChanged=false;
  let skipPaint=false;
  S.browseStack.forEach((en,i)=>{
    if(en.type!=='artist_tracks' || en.id!==id) return;
    if(!d.ok){
      en.loading=false; en.loadingMore=false;
      if(!en.tracks.length) en.error=d.msg||'Не удалось загрузить';
    } else if(page===0){
      if(!en.loading && !en.hasMore && (en.tracks||[]).length) skipPaint=skipPaint||i===S.browseStack.length-1;
      _browseFillTracks(en,d);
      S.browseCache['artist_tracks:'+id]=Object.assign({}, d, {tracks:en.tracks.slice()});
      S.browseCacheTs['artist_tracks:'+id]=Date.now();
    } else {
      const have=new Set(en.tracks.map(t=>t.id));
      _applyDlList(d.tracks||[]).forEach(t=>{ if(!have.has(t.id)) en.tracks.push(t); });
      en.page=d.page||en.page;
      en.hasMore=!!d.has_more;
      en.total=d.total||en.tracks.length;
      en.loadingMore=false;
      S.browseCache['artist_tracks:'+id]=Object.assign({}, d, {tracks:en.tracks.slice(), page:en.page, has_more:en.hasMore});
      S.browseCacheTs['artist_tracks:'+id]=Date.now();
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
    S.browseCacheTs['artist_tracks:'+id]=Date.now();
  }
  if(S.pendingArtistPlay===id){
    if(d.ok && (d.tracks||[]).length) _startArtistPlayback(id, d.tracks, !!d.has_more, page);
    else { S.pendingArtistPlay=''; _paintCardPlayBtns(); }
  } else if(d.ok && S.playingCardKey==='artist:'+id){
    if(page===0) _adoptRestoredSourceQueue('browse', _applyDlList((d.tracks||[]).slice()));
    if(page>0) _appendArtistPlayback(id, d.tracks, !!d.has_more, page);
  }
  if(topChanged && S.browseOpen && !skipPaint){
    const top=_browseTop();
    const jumping=!!(S._jumpPlayingBrowse || S._locatePin);
    const keep=jumping?null:_browseGetScroll();
    if(top && !top.hasMore && !top.loadingMore) S._browseLocateWait=false;
    if(_artistTracksDomReady(top)){
      _paintArtistTracksList(top);
      if(!jumping && keep) _browseSetScroll(keep);
    } else {
      renderBrowse();
      if(jumping) _tryJumpPlayingBrowse();
      else if(keep) _browseSetScroll(keep);
    }
    if(top && top.type==='artist_tracks' && top.hasMore && !top.loadingMore) loadMoreArtistTracks();
  } else if(topChanged && skipPaint){
    const top=_browseTop();
    if(top && !top.hasMore && !top.loadingMore) S._browseLocateWait=false;
    if(S._locatePin || S._jumpPlayingBrowse) _tryJumpPlayingBrowse();
  }
});

/* Показывает страницу, запомнив, куда вернуться по «Назад» */
function _openBrowseView(){
  if(!S.browseOpen){
    const active=document.querySelector('.page.active');
    const pid=(active && active.id!=='page-browse')?active.id:'page-search';
    S.browseReturn=pid;
    S.browseOrigin=pid.replace(/^page-/,'')||'search';
    S.browseOpen=true;
  }
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById('page-browse');
  void el.offsetWidth;   // форсируем reflow, иначе появление будет без анимации
  el.classList.add('active');
}
function _browseBackLabel(){
  if(S.browseStack.length>1){
    const prev=S.browseStack[S.browseStack.length-2];
    let t=String((prev && prev.title)||'').replace(/^Все треки · /,'').trim();
    if(t.length>32) t=t.slice(0,31)+'…';
    return t||'Назад';
  }
  return NAV_LABELS[S.browseOrigin||'search']||'Закрыть';
}
function browseBack(){
  S.browseStack.pop();
  if(!S.browseStack.length){ closeBrowse(); return; }
  _clearSel('browse');
  renderBrowse();
  _browseSetScroll(_browseTop().scroll||0);
}
function browseGoTo(i){
  if(i<0 || i>=S.browseStack.length-1) return;
  S.browseStack.length=i+1;
  _clearSel('browse');
  renderBrowse();
}
function closeBrowse(){
  if(!S.browseOpen) return;
  const origin=S.browseOrigin||'search';
  const backId=S.browseReturn||('page-'+origin);
  delete S.tabBrowse[origin];
  _resetBrowse();
  document.getElementById('page-browse').classList.remove('active');
  const back=document.getElementById(backId)||document.getElementById('page-search');
  if(back) back.classList.add('active');
  _activateNav(origin);
}
function _resetBrowse(){
  S.browseOpen=false;
  S.browseStack=[];
  S.browseOrigin=null;
  S.browseReturn=null;
  _clearSel('browse');
}

function _paintBrowseChrome(en){
  const lab=document.getElementById('browseBackLabel');
  if(lab) lab.textContent=_browseBackLabel();
  document.getElementById('browseCrumb').innerHTML=S.browseStack.map((x,i)=>{
    const fallback={artist:'Исполнитель', album:'Альбом', artist_tracks:'Все треки'}[x.type]||'';
    const label=esc(x.title||fallback);
    return i===S.browseStack.length-1
      ? `<b>${label}</b>`
      : `<span class="lnk" onclick="browseGoTo(${i})">${label}</span>`;
  }).join('<span class="br-sep">›</span>');
}
function renderBrowse(){
  const en=_browseTop();
  if(!en) return;
  _paintBrowseChrome(en);

  const body=document.getElementById('browseBody');
  if(en.loading && en.type!=='artist_tracks'){
    body.removeAttribute('data-browse-key');
    body.innerHTML=`<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем...</p></div>`;
  } else if(en.error && en.type!=='artist_tracks'){
    body.removeAttribute('data-browse-key');
    body.innerHTML=`<div class="empty"><span class="empty-icon">✗</span><p>${esc(en.error)}</p></div>`;
  } else {
    body.dataset.browseKey=en.type+':'+en.id;
    body.innerHTML=en.type==='artist'?_artistPageHTML(en)
      : en.type==='artist_tracks'?_artistTracksPageHTML(en)
      : _albumPageHTML(en);
    const skipEnter=en.type==='artist_tracks' && (en.loading || !en.tracks.length);
    if(!skipEnter)
      _playListEnter(body.querySelector('.ex-body')||body.querySelector('.tl-wrap')||body.querySelector('.br-list'));
    _bindArtistTracksScroll();
    _paintPlaying();
    _tryJumpPlayingBrowse();
    if(en.type==='artist_tracks' && en.hasMore && !en.loadingMore) loadMoreArtistTracks();
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
  const albumsHtml=en.albums.length?`
      <section class="br-block br-rest">
        <div class="br-sec">Альбомы</div>
        <div class="pl-grid">${en.albums.map(al=>_albumCardHTML(al)).join('')}</div>
      </section>`:'';
  const popular=en.tracks.length
    ? `<section class="br-block">
        <div class="br-sticky">
          <div class="br-sec">Популярные треки</div>
          ${_exHeadHTML('browse')}
        </div>
        ${_rowsFor('browse').map(t=>exRowHTML(t,'browse')).join('')}
        ${_artistShowAllBtn(en)}
      </section>`
    : '';
  const table=(popular||albumsHtml)
    ? `<div class="tl-wrap"><div class="tl-body ex-body">${popular}${albumsHtml}</div></div>`
    : '';
  return `
    <div class="br-hero" data-ym-url="${esc(_ymArtistUrl(en.id))}">
      ${_browseHeroCover(a.cover,'🎤')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Исполнитель</div>
        <div class="br-hero-title">${esc(a.name||en.title)}</div>
        <div class="br-hero-sub">${parts.join(' · ')}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('artist', en.id, true)}
          ${_entityDislikeBtn(en.id, true)}
          <button class="btn accent sm" onclick="playArtistCard('${esc(en.id)}')">▶ Играть все</button>
          ${en.tracks.length?`<button class="btn sm" id="btnBrowseDownloadAll" onclick="downloadVisibleOrSelected('browse')">${_downloadAllInner('browse')}</button>`:''}
          <button class="btn sm ghost" onclick="window.pywebview.api.open_link('https://music.yandex.ru/artist/${esc(en.id)}')">🔗 В Яндекс.Музыке</button>
        </div>
      </div>
    </div>
    ${table}
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
function _trackMatchesQuery(t,q){
  if(!q) return true;
  const hay=[t.title,t.artist,t.album,(t.artists||[]).map(a=>a&&a.name).filter(Boolean).join(' ')].join(' ').toLowerCase();
  return hay.includes(q);
}
function _artistTracksVisible(en){
  const q=(en.trackQuery||'').trim().toLowerCase();
  const list=en.tracks||[];
  if(!q) return list;
  return list.filter(t=>_trackMatchesQuery(t,q));
}
function _browseVisibleTracks(){
  const en=_browseTop();
  if(!en) return [];
  if(en.type==='artist_tracks') return _artistTracksVisible(en);
  return en.tracks||[];
}
function onArtistTrackSearch(){
  const en=_browseTop();
  const el=document.getElementById('artistTrackSearch');
  if(!en || en.type!=='artist_tracks' || !el) return;
  en.trackQuery=el.value;
  _paintArtistTracksList(en);
  _syncPlayingQueue('browse');
}
function _artistTracksMoreHTML(en){
  if(!en.hasMore) return '';
  return `<div class="br-more"><button class="btn sm" id="btnArtistMore" onclick="loadMoreArtistTracks()" ${en.loadingMore?'disabled':''}>
        ${en.loadingMore?'⏳ Загрузка...':'Показать ещё'}
      </button></div>`;
}
function _artistTracksDomReady(en){
  const list=document.getElementById('artistTracksList');
  const body=document.getElementById('browseBody');
  return !!(en && en.type==='artist_tracks' && list && body && body.contains(list)
    && body.querySelector('.br-hero'));
}
function _artistTracksHeroName(en){
  const a=en.info||{};
  return a.name || String(en.title||'').replace(/^Все треки · /,'').trim() || 'Исполнитель';
}
function _artistTracksBodyHTML(en){
  const vis=_rowsFor('browse');
  const q=(en.trackQuery||'').trim();
  const more=_artistTracksMoreHTML(en);
  if(vis.length) return vis.map(t=>exRowHTML(t,'browse')).join('')+more;
  if(en.loading) return `<div class="empty"><span class="empty-icon">⏳</span><p>Загружаем все треки...</p></div>`;
  if(en.error && !(en.tracks||[]).length) return `<div class="empty"><span class="empty-icon">✗</span><p>${esc(en.error)}</p></div>`;
  if((en.tracks||[]).length) return `<div class="empty"><span class="empty-icon">🔍</span><p>Нет треков по запросу «${esc(q)}»</p></div>${more}`;
  return `<div class="empty"><span class="empty-icon">🎵</span><p>Треки недоступны</p></div>`;
}
function _syncArtistTracksHero(en){
  const hero=document.querySelector('#browseBody .br-hero');
  if(!hero || !en) return;
  const ym=_ymArtistUrl(en.id);
  if(ym) hero.setAttribute('data-ym-url', ym);
  const a=en.info||{};
  const title=hero.querySelector('.br-hero-title');
  if(title && a.name) title.textContent=a.name;
  const total=en.total || a.tracks_count || (en.tracks||[]).length;
  const sub=hero.querySelector('.br-hero-sub');
  if(sub) sub.textContent=total?`${total} треков`:'';
  const actions=hero.querySelector('.br-hero-actions');
  if(!actions || !(en.tracks||[]).length) return;
  if(!actions.querySelector('[onclick*="playArtistCard"]')){
    actions.insertAdjacentHTML('beforeend',
      `<button class="btn accent sm" onclick="playArtistCard('${esc(en.id)}')">▶ Играть все</button>`);
  }
  const inner=_downloadAllInner('browse');
  const dl=document.getElementById('btnBrowseDownloadAll');
  if(!dl){
    actions.insertAdjacentHTML('beforeend',
      `<button class="btn sm" id="btnBrowseDownloadAll" onclick="downloadVisibleOrSelected('browse')">${inner}</button>`);
  } else {
    dl.innerHTML=inner;
  }
}
function _paintArtistTracksList(en, refreshHead){
  const list=document.getElementById('artistTracksList');
  if(!list) return;
  const vis=_rowsFor('browse');
  const q=(en.trackQuery||'').trim();
  const cnt=document.getElementById('artistTrackSearchCount');
  if(cnt) cnt.textContent=q?`${vis.length} из ${en.tracks.length}`:'';
  let head=list.querySelector(':scope > .tl-head');
  if(!head) list.insertAdjacentHTML('afterbegin', _exHeadHTML('browse'));
  else if(refreshHead) head.outerHTML=_exHeadHTML('browse');
  let body=list.querySelector(':scope > .tl-body') || list.querySelector(':scope > .ex-body');
  if(!body){
    body=document.createElement('div');
    body.className='tl-body ex-body';
    list.appendChild(body);
  }
  body.innerHTML=_artistTracksBodyHTML(en);
  _syncArtistTracksHero(en);
  _updateSelBtn('browse');
  _bindArtistTracksScroll();
  _paintPlaying();
  _tryJumpPlayingBrowse();
}
function _artistTracksPageHTML(en){
  const a=en.info||{};
  const total=en.total || a.tracks_count || en.tracks.length;
  const vis=_rowsFor('browse');
  const q=en.trackQuery||'';
  const name=_artistTracksHeroName(en);
  return `
    <div class="br-hero" data-ym-url="${esc(_ymArtistUrl(en.id))}">
      ${_browseHeroCover(a.cover,'🎤')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Все треки</div>
        <div class="br-hero-title">${esc(name)}</div>
        <div class="br-hero-sub">${total?`${total} треков`:''}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('artist', en.id, true)}
          ${_entityDislikeBtn(en.id, true)}
          <button class="btn accent sm" onclick="playArtistCard('${esc(en.id)}')">▶ Играть все</button>
          ${en.tracks.length?`<button class="btn sm" id="btnBrowseDownloadAll" onclick="downloadVisibleOrSelected('browse')">${_downloadAllInner('browse')}</button>`:''}
        </div>
      </div>
    </div>
    <div class="toolbar br-subbar">
      <input type="text" id="artistTrackSearch" class="pl-search" placeholder="Поиск по трекам исполнителя..."
        value="${esc(q)}" oninput="onArtistTrackSearch()">
      <span id="artistTrackSearchCount" style="font-size:12px;color:var(--muted)">${q.trim()?`${vis.length} из ${en.tracks.length}`:''}</span>
    </div>
    <div class="tl-wrap" id="artistTracksList">${_exHeadHTML('browse')}<div class="tl-body ex-body">${_artistTracksBodyHTML(en)}</div></div>
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
function _bindArtistTracksScroll(){
  const body=document.getElementById('browseBody');
  if(!body || body.dataset.artistScroll) return;
  body.dataset.artistScroll='1';
  body.addEventListener('scroll', e=>{
    const el=e.target;
    if(!el || el===body) return;
    if(!el.classList.contains('tl-body') && !el.classList.contains('br-scroll') && !el.classList.contains('ex-body')) return;
    const top=_browseTop();
    if(!top || top.type!=='artist_tracks' || top.loadingMore || !top.hasMore) return;
    if(el.scrollTop+el.clientHeight>=el.scrollHeight-90) loadMoreArtistTracks();
  }, true);
}
function _albumPageHTML(en){
  const al=en.info||{};
  const parts=[];
  if(al.year) parts.push(esc(al.year));
  if(en.tracks.length) parts.push(`${en.tracks.length} треков`);
  if(al.genre) parts.push(esc(al.genre));
  const artists=(al.artists||[]).filter(x=>x&&x.name).map(x=>x.id
    ?`<span class="lnk" data-ym-url="${esc(_ymArtistUrl(x.id))}" onclick="openArtist('${esc(x.id)}')">${esc(x.name)}</span>`
    :esc(x.name)).join(', ');
  return `
    <div class="br-hero" data-ym-url="${esc(_ymAlbumUrl(en.id))}">
      ${_browseHeroCover(al.cover,'💿')}
      <div class="br-hero-info">
        <div class="br-hero-kind">Альбом</div>
        <div class="br-hero-title">${esc(al.title||en.title)}</div>
        <div class="br-hero-sub">${artists||''}</div>
        <div class="br-hero-sub">${parts.join(' · ')}</div>
        <div class="br-hero-actions">
          ${_entityLikeBtn('album', en.id, true)}
          ${en.tracks.length?`<button class="btn accent sm" onclick="playAlbumCard('${esc(en.id)}')">▶ Играть</button>`:''}
          ${en.tracks.length?`<button class="btn sm" id="btnBrowseDownloadAll" onclick="downloadVisibleOrSelected('browse')">${_downloadAllInner('browse')}</button>`:''}
          <button class="btn sm ghost" onclick="window.pywebview.api.open_link('https://music.yandex.ru/album/${esc(en.id)}')">🔗 В Яндекс.Музыке</button>
        </div>
      </div>
    </div>
    ${en.tracks.length?_exTableHTML('browse', _rowsFor('browse').map(t=>exRowHTML(t,'browse')).join(''))
      :`<div class="empty"><span class="empty-icon">🎵</span><p>Треки недоступны</p></div>`}
  `;
}
function _albumCardHTML(al){
  const sub=[al.year, al.track_count?`${al.track_count} треков`:''].filter(Boolean).join(' · ');
  const artists=(al.artists||[]).map(x=>x&&x.name).filter(Boolean).join(', ');
  return `
    <div class="pl-card" data-kind="album" data-id="${esc(al.id)}" data-ym-url="${esc(_ymAlbumUrl(al.id))}" onclick="openAlbum('${esc(al.id)}')" title="${esc(al.title)}">
      ${al.cover
        ?`<img class="pl-cover" src="${esc(al.cover)}" alt="" onerror="this.style.display='none'">`
        :`<div class="pl-cover-ph">${icon('disc')}</div>`}
      <button class="iBtn card-play" data-play-key="album:${esc(al.id)}" title="Играть альбом"
        onclick="event.stopPropagation();playAlbumCard('${esc(al.id)}')">${icon('play')}</button>
      ${_entityLikeBtn('album', al.id, false)}
      <div class="pl-info">
        <div class="pl-name">${esc(al.title)}</div>
        <div class="pl-count">${esc(artists||sub)}</div>
      </div>
    </div>`;
}
function browseDownloadAll(){
  const en=_browseTop();
  if(!en) return;
  const tracks=(en.tracks||[]).filter(_trackPlayable);
  if(!tracks.length) return;
  window.pywebview.api.start_download(tracks);
  tracks.forEach(t=>{ if(t.status!=='done') t.status='queued'; });
  tracks.forEach(t=>_updateExRow('browse',t.id));
  addLog(`В очереди: ${tracks.length} треков — ${en.title}`,'info');
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
  if(!Array.isArray(d) && d.ctx==='pl_add'){
    _onPlAddSearchResults(d);
    return;
  }
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
    html+=`<div class="search-sec">Треки</div><div class="tl-wrap" style="flex:0 1 auto">`;
    html+=_exHeadHTML('search');
    html+=`<div class="tl-body" style="overflow:visible;flex:none">${_rowsFor('search').map(t=>exRowHTML(t,'search')).join('')}</div></div>`;
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
  const head=document.getElementById('dlHead');
  if(!files.length){
    if(head) head.innerHTML='';
    el.innerHTML=`<div class="empty"><span class="empty-icon">📂</span><p>Нет скачанных файлов в папке загрузки</p></div>`;
    _updateDlSelUI();
    return;
  }
  if(head) head.innerHTML=_exHeadHTML('downloaded');
  el.innerHTML=_rowsFor('downloaded').map(f=>dlRowHTML(f)).join('');
  _bindDlCovers(el);
  _playListEnter(el);
  _updateDlSelUI();
}
function _updateDlCount(){
  document.getElementById('dlCount').textContent=S.dlFiles.length?`${S.dlFiles.length} файлов`:'';
}
function dlCoverError(img){
  if(!img) return;
  const slot=img.closest('.dl-cover-slot');
  const ph=slot ? slot.querySelector('.dl-cover-ph') : img.previousElementSibling;
  _showCoverPlaceholder(img, ph);
}
function _bindDlCover(row, f){
  if(!row) return;
  const img=row.querySelector('.dl-cover');
  const ph=row.querySelector('.dl-cover-ph');
  const url=_dlCoverUrl(f);
  if(!img || !url){
    _showCoverPlaceholder(img, ph);
    return;
  }
  const token=String((parseInt(img.dataset.coverToken||'0',10)||0)+1);
  img.dataset.coverToken=token;
  const ok=()=>{
    if(img.dataset.coverToken!==token) return;
    if(img.naturalWidth) _revealCoverImage(img, ph);
    else _showCoverPlaceholder(img, ph);
  };
  const fail=()=>{
    if(img.dataset.coverToken!==token) return;
    _showCoverPlaceholder(img, ph);
  };
  img.onload=ok;
  img.onerror=fail;
  if(img.getAttribute('src')===url && img.naturalWidth){
    _revealCoverImage(img, ph);
  } else {
    img.src=url;
    if(img.complete && img.naturalWidth) _revealCoverImage(img, ph);
  }
}
function _bindDlCovers(root){
  (root||document).querySelectorAll('.dl-row').forEach(row=>{
    const uid=row.dataset.uid;
    const f=(S.dlFiles||[]).find(x=>x.uid===uid);
    if(f) _bindDlCover(row, f);
  });
}
function dlRowHTML(f){
  const isPlaying=S.playerSource==='downloaded'&&S.playerTrackId===f.rel_path;
  const audio=_audioNow();
  const playing=isPlaying && audio && !audio.paused;
  const url=_dlCoverUrl(f);
  const cover=`<div class="dl-cover-slot" onclick="openDownloadedBig(event,'${f.uid}')" title="Развернуть плеер">
    <div class="dl-cover-ph">${icon('music')}</div>
    ${url?`<img class="dl-cover" alt="" hidden>`:''}
  </div>`;
  const sub=[f.artist,f.album].filter(Boolean).join(' · ');
  return `<div class="dl-row${isPlaying?' dl-playing':''}" id="dlrow-${f.uid}"
    data-uid="${esc(f.uid)}"
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
    <button class="btn sm ghost play-btn" onclick="stopRow(event);playDownloaded('${f.uid}')"
      title="${isPlaying?'Играет':'Воспроизвести'}">${icon(_playIconName(playing))}</button>
    <button class="iBtn del-btn" onclick="stopRow(event);deleteDownloaded('${f.uid}')" title="Удалить файл с диска">${icon('trash')}</button>
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
  const fresh=tmp.firstElementChild;
  el.replaceWith(fresh);
  _bindDlCover(fresh, f);
}
function playDownloaded(uid){
  const f=S.dlFiles.find(x=>x.uid===uid);
  if(f) playLocalFile(f);
}
async function playLocalFile(f){
  if(!f) return;
  const rel=f.rel_path||f.id;
  const audio=_audioNow();
  if(S.playerSource==='downloaded'&&S.playerTrackId===rel && audio && audio.getAttribute('src')){
    playerToggle();
    return;
  }
  const url=await window.pywebview.api.get_file_url(rel);
  if(S.dlFiles && S.dlFiles.length) S.playerQueue=_rowsFor('downloaded');
  else if(!S.playerQueue || !S.playerQueue.length)
    S.playerQueue=[Object.assign({}, f, {rel_path:rel})];
  _loadAndPlay(_dlAsTrack(Object.assign({}, f, {rel_path:rel})), url,'downloaded');
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
  _syncHeadCheck('downloaded');
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
function _audioIsPlaying(){
  const a=_audioNow();
  return !!(a && a.getAttribute('src') && !a.paused && !a.ended);
}
function _playerHasSrc(){
  const a=_audioNow();
  const b=_audioIdle();
  return !!((a && a.getAttribute('src')) || (b && b.getAttribute('src')));
}
function _pruneDownloadedQueue(rels){
  if(S.playerSource!=='downloaded' || !Array.isArray(S.playerQueue)) return;
  const gone=new Set((rels||[]).map(String));
  S.playerQueue=S.playerQueue.filter(x=>!gone.has(String(x.rel_path||x.id)));
}
/* Текущий скачанный файл в плеере: играл → skip/stop; пауза/idle → только освободить, не запускать следующий. */
function _afterDeleteDownloadedCurrent(wasCurrent, wasPlaying, nextFile){
  if(!wasCurrent) return;
  if(wasPlaying){
    if(nextFile) playLocalFile(nextFile);
    else playerClose();
    return;
  }
  playerClose();
}
function _doDeleteManyDownloaded(files){
  const paths=files.map(f=>f.rel_path);
  const doomed=new Set(paths);
  const isCurrent = S.playerSource==='downloaded' && doomed.has(S.playerTrackId);
  const wasPlaying = isCurrent && _audioIsPlaying();
  const holdsFile = isCurrent && _playerHasSrc();
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
  _pruneDownloadedQueue(paths);
  _persistDlMarks();
  _syncDlMarks();
  _updateDlCount();
  _updateDlSelUI();
  if(!S.dlFiles.length) setTimeout(()=>{ if(!S.dlFiles.length) renderDownloaded(S.dlFiles); },430);

  const nextFile=wasPlaying && S.dlFiles.length
    ? S.dlFiles[Math.min(Math.max(playingIdx,0),S.dlFiles.length-1)]
    : null;
  _afterDeleteDownloadedCurrent(isCurrent, wasPlaying, nextFile);
  setTimeout(()=>window.pywebview.api.delete_downloaded_many(paths), (wasPlaying||holdsFile)?350:0);
}
window.addEventListener('py:downloaded_deleted_many', e=>{
  const{deleted,failed}=e.detail;
  (deleted||[]).forEach(p=>{
    const info=S.pendingFileDeletes[p];
    delete S.pendingFileDeletes[p];
    _dropLyricsCache((info && info.file && info.file.track_id) || p);
  });
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
  const isCurrent = S.playerSource==='downloaded' && S.playerTrackId===f.rel_path;
  const wasPlaying = isCurrent && _audioIsPlaying();
  const holdsFile = isCurrent && _playerHasSrc();

  S.pendingFileDeletes[f.rel_path]={file:f, index:idx};
  S.dlFiles.splice(idx,1);
  S.dlSelected.delete(f.rel_path);
  _forgetDlFile(f);
  _pruneDownloadedQueue([f.rel_path]);
  _updateDlCount();
  _updateDlSelUI();
  _animateElOut(document.getElementById('dlrow-'+f.uid),()=>{
    if(!S.dlFiles.length) renderDownloaded(S.dlFiles);
  });

  const nextFile=wasPlaying && S.dlFiles.length
    ? S.dlFiles[Math.min(idx,S.dlFiles.length-1)]
    : null;
  _afterDeleteDownloadedCurrent(isCurrent, wasPlaying, nextFile);
  setTimeout(()=>window.pywebview.api.delete_downloaded(f.rel_path), (wasPlaying||holdsFile)?350:0);
}
window.addEventListener('py:downloaded_deleted', e=>{
  const{rel_path,ok,msg}=e.detail;
  const info=S.pendingFileDeletes[rel_path];
  delete S.pendingFileDeletes[rel_path];
  if(ok){
    _dropLyricsCache((info && info.file && info.file.track_id) || rel_path);
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
function _lyricsSettingOn(c){
  if(!c) return false;
  if(Object.prototype.hasOwnProperty.call(c,'download_lyrics')) return !!c.download_lyrics;
  const fmt=String(c.lyrics_format||'none').toLowerCase();
  return fmt!=='' && fmt!=='none';
}
function _dropLyricsCache(trackId){
  if(!trackId) return;
  delete S.lyricsCache[trackId];
  delete S.lyricsCache['local:'+trackId];
  S.lyricsPending.delete(trackId);
  S.lyricsPending.delete('local:'+trackId);
}
function _readSettingsForm(){
  return {
    token:document.getElementById('cfgToken').value.trim(),
    quality:document.getElementById('cfgQuality').value,
    embed_cover:document.getElementById('cfgEmbedCover').checked,
    cover_resolution:document.getElementById('cfgCoverRes').value,
    download_lyrics:document.getElementById('cfgDownloadLyrics').checked,
    lyrics_format:document.getElementById('cfgDownloadLyrics').checked?'lrc':'none',
    path_pattern:document.getElementById('cfgPathPattern').value,
    download_dir:document.getElementById('cfgDownloadDir').value.trim(),
    skip_existing:document.getElementById('cfgSkipExisting').checked,
    stick_to_artist:document.getElementById('cfgStickToArtist').checked,
    only_music:document.getElementById('cfgOnlyMusic').checked,
    compatibility_level:document.getElementById('cfgCompatLevel').value,
    parallel:document.getElementById('cfgParallel').value,
    delay:String(document.getElementById('cfgDelay').value),
    timeout:String(document.getElementById('cfgTimeout').value),
    tries:String(document.getElementById('cfgTries').value),
    retry_delay:String(document.getElementById('cfgRetryDelay').value),
    ui_theme:S.uiTheme||'amber',
    ui_mode:S.uiMode||'dark',
    crossfade_sec:String(S.crossfadeSec||0),
  };
}
const UI_THEMES=[
  {id:'amber', name:'Янтарь', dark:{bg:'#1a1a1f', a:'#ffcc00'}, light:{bg:'#ece6d8', a:'#c49200'}},
  {id:'ocean', name:'Океан', dark:{bg:'#121a22', a:'#3ec4e8'}, light:{bg:'#ddecef', a:'#0284b8'}},
  {id:'forest', name:'Лес', dark:{bg:'#151c17', a:'#6bcb7a'}, light:{bg:'#e3ece3', a:'#2f9e4f'}},
  {id:'sunset', name:'Закат', dark:{bg:'#1c1514', a:'#ff8a5b'}, light:{bg:'#f0e3da', a:'#e05a2b'}},
  {id:'violet', name:'Лаванда', dark:{bg:'#191622', a:'#c084fc'}, light:{bg:'#e8e0f2', a:'#7c3aed'}},
  {id:'graphite', name:'Графит', dark:{bg:'#18181c', a:'#a8b4c4'}, light:{bg:'#e6e7eb', a:'#4b5563'}},
];
function _applyTheme(){
  document.documentElement.setAttribute('data-theme', S.uiTheme||'amber');
  document.documentElement.setAttribute('data-mode', S.uiMode||'dark');
}
function _paintThemeSwatches(){
  const box=document.getElementById('themeSwatches');
  if(box){
    const mode=S.uiMode==='light'?'light':'dark';
    box.innerHTML=UI_THEMES.map(th=>{
      const p=th[mode]||th.dark;
      return `<button type="button" class="theme-swatch${S.uiTheme===th.id?' on':''}" title="${esc(th.name)}"
      style="--sw-bg:${p.bg};--sw-a:${p.a}" onclick="setUiTheme('${th.id}')"><i></i></button>`;
    }).join('');
  }
  const d=document.getElementById('btnModeDark'), l=document.getElementById('btnModeLight');
  if(d) d.classList.toggle('on', S.uiMode!=='light');
  if(l) l.classList.toggle('on', S.uiMode==='light');
  _paintCrossfadeRow();
}
function setUiTheme(id){
  S.uiTheme=id;
  _applyTheme();
  _paintThemeSwatches();
  _persistAppearance();
}
function setUiMode(mode){
  S.uiMode=mode==='light'?'light':'dark';
  _applyTheme();
  _paintThemeSwatches();
  _persistAppearance();
}
function onCrossfadeToggle(){
  const on=document.getElementById('cfgCrossfadeOn');
  const inp=document.getElementById('cfgCrossfadeSec');
  if(on && on.checked){
    let v=Number(inp && inp.value);
    if(!isFinite(v) || v<=0) v=3;
    v=Math.max(0.5, Math.min(12, v));
    S.crossfadeSec=v;
    if(inp) inp.value=String(v);
  } else S.crossfadeSec=0;
  _paintCrossfadeRow();
  _persistAppearance();
}
function onCrossfadeSec(){
  const on=document.getElementById('cfgCrossfadeOn');
  const inp=document.getElementById('cfgCrossfadeSec');
  let v=Number(inp && inp.value);
  if(!isFinite(v)) v=3;
  v=Math.max(0, Math.min(12, v));
  if(inp) inp.value=String(v);
  if(on && !on.checked){ S.crossfadeSec=0; _persistAppearance(); return; }
  S.crossfadeSec=v;
  if(on) on.checked=v>0;
  _paintCrossfadeRow();
  _persistAppearance();
}
function _paintCrossfadeRow(){
  const on=document.getElementById('cfgCrossfadeOn');
  const inp=document.getElementById('cfgCrossfadeSec');
  const row=document.getElementById('rowCrossfadeSec');
  const active=(Number(S.crossfadeSec)||0)>0;
  if(on) on.checked=active;
  if(inp && active) inp.value=String(S.crossfadeSec);
  if(inp && !active && !(Number(inp.value)>0)) inp.value='3';
  if(row) row.style.opacity=active?'1':'.45';
  if(inp) inp.disabled=!active;
}
async function _persistAppearance(){
  STORE.set('ym_ui', {theme:S.uiTheme, mode:S.uiMode, crossfade:S.crossfadeSec});
  if(S.settingsSaved){
    S.settingsSaved.ui_theme=S.uiTheme;
    S.settingsSaved.ui_mode=S.uiMode;
    S.settingsSaved.crossfade_sec=String(S.crossfadeSec||0);
  }
  if(!window.pywebview || !window.pywebview.api) return;
  try{
    await window.pywebview.api.save_config({
      ui_theme:S.uiTheme,
      ui_mode:S.uiMode,
      crossfade_sec:String(S.crossfadeSec||0),
    });
    _flashSettingsSaved();
  }catch(_e){}
}
function _flashSettingsSaved(){
  const st=document.getElementById('saveStatus');
  if(!st) return;
  st.textContent='✓ Сохранено';
  st.style.opacity='1';
  clearTimeout(st._hideTimer);
  st._hideTimer=setTimeout(()=>{ st.style.opacity='0'; }, 2000);
}
function _onSettingsFormChange(){
  if(S.settingsLoading) return;
  if(S.settingsSaveTimer) clearTimeout(S.settingsSaveTimer);
  S.settingsSaveTimer=setTimeout(()=>{ S.settingsSaveTimer=0; saveSettings(); }, 500);
}
function _paintAuthBtn(hasToken){
  S.hasToken=!!hasToken;
  const btn=document.getElementById('btnLogin');
  const info=document.getElementById('authInfo');
  if(S.hasToken){
    btn.textContent='Выйти';
    btn.classList.remove('ghost');
    btn.classList.add('logged-in');
    info.textContent='✓ Авторизован';
  } else {
    btn.textContent='Войти';
    btn.classList.add('ghost');
    btn.classList.remove('logged-in');
    info.textContent='';
  }
}
function onAuthBtn(){
  if(S.hasToken) logoutAccount();
  else showAuthModal();
}
async function logoutAccount(){
  await window.pywebview.api.logout();
  document.getElementById('cfgToken').value='';
  if(S.settingsSaved) S.settingsSaved.token='';
  _paintAuthBtn(false);
}
async function loadSettings(){
  S.settingsLoading=true;
  try{
    const c=await window.pywebview.api.get_config();
    document.getElementById('cfgToken').value=c.token||'';
    document.getElementById('cfgQuality').value=c.quality||'2';
    document.getElementById('cfgEmbedCover').checked=!!c.embed_cover;
    document.getElementById('cfgCoverRes').value=c.cover_resolution||'original';
    document.getElementById('cfgDownloadLyrics').checked=_lyricsSettingOn(c);
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
    const ids=['amber','ocean','forest','sunset','violet','graphite'];
    if(ids.includes(c.ui_theme)) S.uiTheme=c.ui_theme;
    if(c.ui_mode==='light' || c.ui_mode==='dark') S.uiMode=c.ui_mode;
    const xf=Number(c.crossfade_sec);
    if(isFinite(xf) && xf>=0) S.crossfadeSec=xf;
    STORE.set('ym_ui', {theme:S.uiTheme, mode:S.uiMode, crossfade:S.crossfadeSec});
    _applyTheme();
    _paintThemeSwatches();
    S.settingsSaved=_readSettingsForm();
    const tok=(c.token||'').trim();
    if(tok) S.settingsSaved.token=tok;
    _paintAuthBtn(!!tok);
    return c;
  } finally {
    S.settingsLoading=false;
  }
}
async function saveSettings(){
  if(S.settingsLoading) return;
  if(S.settingsSaving){ S.settingsSaveAgain=true; return; }
  const data=_readSettingsForm();
  if(!(data.token||'').trim() && S.settingsSaved && (S.settingsSaved.token||'').trim())
    data.token=S.settingsSaved.token;
  if(S.settingsSaved && JSON.stringify(data)===JSON.stringify(S.settingsSaved)) return;
  S.settingsSaving=true;
  try{
    await window.pywebview.api.save_config(data);
    S.settingsSaved=data;
    if((data.token||'').trim()) _paintAuthBtn(true);
    _flashSettingsSaved();
  }catch(_e){
    addLog('Не удалось сохранить настройки','err');
  } finally {
    S.settingsSaving=false;
    if(S.settingsSaveAgain){
      S.settingsSaveAgain=false;
      saveSettings();
    }
  }
}
async function chooseFolder(){
  const f=await window.pywebview.api.choose_folder();
  if(f){
    document.getElementById('cfgDownloadDir').value=f;
    saveSettings();
  }
}

/* ═══════════════════════════════════════════════════════════════════
   КЛАВИАТУРА
═══════════════════════════════════════════════════════════════════ */
document.addEventListener('keydown', e=>{
  const k=e.key, c=e.code;
  if(k==='MediaPlayPause'||c==='MediaPlayPause'){ e.preventDefault(); mediaPlayPause(); return; }
  if(k==='MediaTrackNext'||c==='MediaTrackNext'){ e.preventDefault(); mediaNext(); return; }
  if(k==='MediaTrackPrevious'||c==='MediaTrackPrevious'){ e.preventDefault(); mediaPrev(); return; }

  const tag=((e.target&&e.target.tagName)||'').toLowerCase();
  if(tag==='input'||tag==='textarea'||tag==='select') return;

  if(e.key==='Escape'){
    if(document.getElementById('addMenu')){ closeAddMenu(); return; }
    if(S.plAddOpen){ closePlAddPanel(); return; }
    if(_aboutOpen()){ closeAbout(); return; }
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
_paintThemeSwatches();
_applyModeUI();
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
  const settingsPage=document.getElementById('page-settings');
  settingsPage.addEventListener('input', _onSettingsFormChange);
  settingsPage.addEventListener('change', _onSettingsFormChange);
  _restoreLastPlay(cfg && cfg.last_play);
  // Подтянуть список плейлистов заранее — он нужен для кнопки «добавить в плейлист»,
  // но только если уже есть токен, иначе получим лишнюю ошибку в логе
  if(cfg && cfg.token){
    refreshStaleCaches(false);
    _refillRestoredQueue(true);
  } else {
    _refillRestoredQueue(false);
  }
  scanDownloaded();
  _bindMediaSession();
  addLog('Приложение готово к работе','info');
});
</script>
</body>
</html>
"""
