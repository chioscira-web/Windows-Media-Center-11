import os, threading, http.server, socketserver, functools, webview, sys, subprocess
from tkinter import messagebox

# --- COSA DEL SETUP ---
cartella = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(cartella, "installato.txt")):
    setup = os.path.join(cartella, "Setup.pyw")
    if os.path.exists(setup):
        subprocess.Popen(["pythonw", setup])
        try:
            messagebox.showinfo("Setup richiesto", "Devi prima fare il setup!")
        except:
            pass
    else:
        try:
            messagebox.showerror("Errore", "Setup non trovato!")
        except:
            pass
    sys.exit()
# --- FINE SETUP ---

HOME = os.path.expanduser("~")
VIDEO_DIR = os.path.join(HOME, "Videos")
MUSIC_DIR = os.path.join(HOME, "Music")
PHOTO_DIR = os.path.join(HOME, "Pictures")
PORT = 8765

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=HOME)
httpd = socketserver.TCPServer(("", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

# LINK TV NUOVI - funzionano
RAI1 = "https://dash2.antik.sk/live/test_rai_uno_tizen/playlist.m3u8"
RAI2 = "https://raidue3-live.akamaized.net/hls/live/2017983/raidue3/raidue3/playlist.m3u8"
RAI3 = "https://dash2.antik.sk/live/test_rai_tre_tizen/playlist.m3u8"
RAI_NEWS = "https://rainews24-live.akamaized.net/hls/live/2017983/rainews24/rainews24/playlist.m3u8"

def lista(cartella, estensioni):
    if not os.path.exists(cartella):
        return "<p style='color:white'>Cartella non trovata</p>"
    files = [f for f in os.listdir(cartella) if f.lower().endswith(estensioni)]
    if not files:
        return "<p style='color:white'>Nessun file. Metti i file in questa cartella di Windows.</p>"
    rel = os.path.relpath(cartella, HOME).replace("\\", "/")
    out = "<div class='grid2'>"
    for f in files:
        url = f"http://127.0.0.1:{PORT}/{rel}/{f}"
        out += f"<div class='card2' onclick=\"apri('{url}','{f}')\"><div class='card-icon'>▶</div><b>{f[:24]}</b></div>"
    out += "</div>"
    return out

video_html = lista(VIDEO_DIR, (".mp4",".mkv",".avi",".mov"))
musica_html = lista(MUSIC_DIR, (".mp3",".wav",".m4a"))
foto_html = lista(PHOTO_DIR, (".jpg",".jpeg",".png",".webp"))

HTML = f"""
<html><head><meta charset='utf-8'>
<script src='https://cdn.jsdelivr.net/npm/hls.js@latest'></script>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#0f6fce;color:white;font-family:Segoe UI;display:flex;height:100vh;overflow:hidden}}
aside{{width:280px;background:rgba(110,130,160,0.85);border-radius:14px;margin:22px 0 22px 28px;padding:14px 10px;flex-shrink:0}}
.menu{{display:flex;align-items:center;gap:12px;padding:13px 12px;border-radius:8px;cursor:pointer;font-size:18px}}
.menu svg{{width:24px;height:24px;fill:white;flex-shrink:0}}
.menu.attivo{{background:linear-gradient(90deg, rgba(255,255,255,0.45), rgba(255,255,255,0.05))}}
main{{flex:1;padding:12px 35px 20px;overflow-y:auto}}
.top{{text-align:right}} .top b{{font-size:21px}} .top span{{color:#8ee63a;font-size:22px}} .top small{{display:block;font-size:11px;opacity:0.7}}
.titolo{{display:flex;gap:70px;align-items:baseline;margin:28px 0 25px 25px}}
.titolo h1{{font-size:58px;font-weight:300;margin:0;letter-spacing:2px}}
.titolo h2{{font-size:62px;font-weight:300;margin:0;opacity:0.45}}
.grid{{display:flex;gap:18px;margin-left:25px;flex-wrap:wrap}}
.card{{width:205px;height:195px;background:linear-gradient(180deg,#7aa8d6,#5a8ec2);border-radius:12px;padding:16px;cursor:pointer;display:flex;flex-direction:column;justify-content:space-between}}
.card:hover{{background:linear-gradient(180deg,#8ab8e6,#6a9ed2)}}
.card b{{font-size:18px;font-weight:500}}
.card-icon{{height:95px;display:flex;align-items:center;justify-content:center}}
.card-icon svg{{width:70px;height:70px;fill:white;opacity:0.9}}
.card-icon .cerchio{{width:72px;height:72px;border:2px solid rgba(255,255,255,0.7);border-radius:50%;display:flex;align-items:center;justify-content:center}}
.card-icon .cerchio svg{{width:36px;height:36px}}
.sezione{{display:none}} .sezione.attiva{{display:block}}
.player{{background:rgba(0,0,0,0.25);border-radius:12px;padding:15px;margin:0 0 20px 25px}}
video,audio{{width:100%;background:black;border-radius:8px}} img{{max-width:100%;border-radius:10px}}
.grid2{{display:flex;gap:14px;flex-wrap:wrap;margin-left:25px}} .card2{{width:180px;background:rgba(255,255,255,0.18);border-radius:10px;padding:14px;cursor:pointer}}
input{{width:80%;padding:12px;border-radius:8px;border:0;font-size:16px;margin-left:25px}}
.tvbtn{{background:white;color:#0f6fce;border:0;padding:12px 20px;border-radius:8px;font-size:16px;font-weight:bold;cursor:pointer;margin:5px}}
.errore{{color:#ffcccc;font-size:14px;margin-top:10px}}
</style></head><body>

<aside>
<div class='menu' onclick="mostra('foto',this)"><svg viewBox='0 0 24 24'><path d='M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z'/></svg> Immagini + Video</div>
<div class='menu' onclick="mostra('musica',this)"><svg viewBox='0 0 24 24'><path d='M12 3v10.55A4 4 0 1 0 14 17V7h4V3h-6z'/></svg> Musica</div>
<div class='menu' onclick="mostra('video',this)"><svg viewBox='0 0 24 24'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-8 11l-4-3 4-3v6zm6-2h-2v2h-2v-2h-2v-2h2V7h2v2h2v2z'/></svg> Filmati</div>
<div class='menu attivo' onclick="mostra('tv',this)"><svg viewBox='0 0 24 24'><path d='M21 3H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h5v2h8v-2h5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 14H3V5h18v12z'/></svg> TV</div>
<div class='menu' onclick="mostra('video',this)"><svg viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm0-13c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z'/></svg> Registrazioni</div>
<div class='menu' onclick="mostra('guida',this)"><svg viewBox='0 0 24 24'><path d='M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z'/></svg> Guida TV</div>
</aside>

<main>
<div class='top'><b>Windows <span>Media Center</span></b> <small>Windows 11 Edition</small></div>

<div id='tv' class='sezione attiva'>
<div class='titolo'><h1>TV</h1><h2>6 di 12</h2></div>
<div class='player' id='playerTV' style='display:none'>
<div id='tvButtons'>
<button class='tvbtn' onclick="playTV('{RAI1}')">Rai 1</button>
<button class='tvbtn' onclick="playTV('{RAI2}')">Rai 2</button>
<button class='tvbtn' onclick="playTV('{RAI3}')">Rai 3</button>
<button class='tvbtn' onclick="playTV('{RAI_NEWS}')">Rai News 24</button>
</div>
<video id='tvVideo' controls autoplay playsinline></video>
<div id='tvStato' class='errore'>Clicca un canale qui sopra e aspetta 5-10 secondi</div>
</div>
<div class='grid'>
<div class='card' onclick="mostra('video',document.querySelectorAll('.menu')[4])"><div class='card-icon'><svg viewBox='0 0 24 24'><path d='M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z'/></svg></div><b>Registrazioni</b></div>
<div class='card' onclick="mostra('guida',document.querySelectorAll('.menu')[5])"><div class='card-icon'><svg viewBox='0 0 24 24'><path d='M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z'/></svg></div><b>Guida TV</b></div>
<div class='card' onclick="playTV('{RAI1}')"><div class='card-icon'><svg viewBox='0 0 24 24'><path d='M21 3H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h5v2h8v-2h5c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 14H3V5h18v12z'/></svg></div><b>In diretta</b></div>
<div class='card' onclick="mostra('cerca',null)"><div class='card-icon'><div class='cerchio'><svg viewBox='0 0 24 24'><path d='M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/></svg></div></div><b>Cerca</b></div>
</div>
</div>

<div id='video' class='sezione'><div class='titolo'><h1>Filmati</h1></div><div class='player' id='playerVideo'>Scegli un filmato</div>{video_html}</div>
<div id='musica' class='sezione'><div class='titolo'><h1>Musica</h1></div><div class='player' id='playerMusica'>Scegli una canzone</div>{musica_html}</div>
<div id='foto' class='sezione'><div class='titolo'><h1>Immagini + Video</h1></div><div class='player' id='playerFoto'>Scegli una foto</div>{foto_html}</div>
<div id='guida' class='sezione'><div class='titolo'><h1>Guida TV</h1></div><div class='grid'>
<div class='card' onclick="playTV('{RAI1}')"><div class='card-icon'><b style='font-size:30px'>1</b></div><b>Rai 1 - 21:00 Film</b></div>
<div class='card' onclick="playTV('{RAI2}')"><div class='card-icon'><b style='font-size:30px'>2</b></div><b>Rai 2 - 21:00 Serie</b></div>
<div class='card' onclick="playTV('{RAI3}')"><div class='card-icon'><b style='font-size:30px'>3</b></div><b>Rai 3 - 21:00 News</b></div>
<div class='card' onclick="playTV('{RAI_NEWS}')"><div class='card-icon'><b style='font-size:20px'>NEWS</b></div><b>Rai News 24</b></div>
</div></div>
<div id='cerca' class='sezione'><div class='titolo'><h1>Cerca</h1></div><input placeholder='Scrivi Rai 1, Musica, Foto...' onkeyup="if(event.key==='Enter'){{playTV('{RAI1}');mostra('tv',document.querySelectorAll('.menu')[3])}}"><p style='margin-left:25px'>Scrivi e premi Invio per vedere Rai 1</p></div>

</main>
<script>
let hls = null;
function mostra(id,el){{document.querySelectorAll('.sezione').forEach(s=>s.classList.remove('attiva'));document.getElementById(id).classList.add('attiva');if(el){{document.querySelectorAll('.menu').forEach(m=>m.classList.remove('attivo'));el.classList.add('attivo')}}}}
function playTV(u){{
  mostra('tv', document.querySelectorAll('.menu')[3]);
  document.getElementById('playerTV').style.display='block';
  document.getElementById('tvStato').innerText='Caricamento in corso... aspetta 5-10 secondi';
  var v=document.getElementById('tvVideo');
  if(hls){{hls.destroy(); hls=null;}}
  if(Hls.isSupported()){{
    hls=new Hls(); hls.loadSource(u); hls.attachMedia(v);
    hls.on(Hls.Events.MANIFEST_PARSED,function(){{v.play(); document.getElementById('tvStato').innerText='In onda ora';}});
    hls.on(Hls.Events.ERROR,function(e,d){{document.getElementById('tvStato').innerText='Errore di caricamento, prova un altro canale';}});
  }} else if(v.canPlayType('application/vnd.apple.mpegurl')) {{ v.src=u; v.play(); }}
  else {{ v.src=u; v.play(); }}
}}
function apri(url,nome){{
 if(nome.toLowerCase().match(/\\.(mp3|wav|m4a)$/)){{document.getElementById('playerMusica').innerHTML="<b>"+nome+"</b><audio controls autoplay src='"+url+"'></audio>";mostra('musica',document.querySelectorAll('.menu')[1])}}
 else if(nome.toLowerCase().match(/\\.(jpg|jpeg|png|webp)$/)){{document.getElementById('playerFoto').innerHTML="<b>"+nome+"</b><br><img src='"+url+"'>";mostra('foto',document.querySelectorAll('.menu')[0])}}
 else{{document.getElementById('playerVideo').innerHTML="<b>"+nome+"</b><video controls autoplay src='"+url+"'></video>";mostra('video',document.querySelectorAll('.menu')[2])}}
}}
</script></body></html>
"""

webview.create_window("Windows Media Center", html=HTML, width=1250, height=800)
webview.start()