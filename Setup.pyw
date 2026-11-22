import os, shutil, subprocess, tkinter as tk
from tkinter import filedialog, messagebox

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = r"C:\Program Files\Windows Media Center"
pagina = 0
cartella = DEST

root = tk.Tk()
root.title("Windows Media Center Setup")
root.geometry("520x380")
root.resizable(False, False)
root.configure(bg="white")

top = tk.Frame(root, bg="#0f6fce", height=70)
top.pack(fill="x")
tk.Label(top, text="Windows Media Center", font=("Segoe UI", 16, "bold"), bg="#0f6fce", fg="white").place(x=15, y=10)
tk.Label(top, text="Setup Wizard", font=("Segoe UI", 10), bg="#0f6fce", fg="white").place(x=15, y=38)
tk.Label(top, text="◉", font=("Segoe UI", 28, "bold"), bg="#0f6fce", fg="#2ecc71").place(x=450, y=8)

centro = tk.Frame(root, bg="white")
centro.pack(fill="both", expand=True, padx=20, pady=15)
titolo = tk.Label(centro, text="", font=("Segoe UI", 13, "bold"), bg="white", anchor="w", justify="left")
titolo.pack(fill="x")
testo = tk.Label(centro, text="", font=("Segoe UI", 10), bg="white", anchor="nw", justify="left", wraplength=470)
testo.pack(fill="both", expand=True)
entry = tk.Entry(centro, font=("Segoe UI", 10), width=48)
btn_browse = tk.Button(centro, text="Browse...", command=lambda: [entry.delete(0, tk.END), entry.insert(0, filedialog.askdirectory())])

basso = tk.Frame(root, bg="#f0f0f0", height=50)
basso.pack(fill="x", side="bottom")
btn_back = tk.Button(basso, text="< Back", width=12, command=lambda: cambia(-1))
btn_next = tk.Button(basso, text="Next >", width=12, bg="#0f6fce", fg="white", command=lambda: cambia(1))
btn_cancel = tk.Button(basso, text="Cancel", width=12, command=lambda: root.destroy())
btn_back.place(x=180, y=12); btn_next.place(x=290, y=12); btn_cancel.place(x=400, y=12)

def mostra():
    entry.pack_forget(); btn_browse.pack_forget()
    if pagina == 0:
        titolo.config(text="Welcome to the Windows Media\nCenter Setup Wizard")
        testo.config(text="The installer will guide you through the steps required to install Windows Media Center on your computer.\n\nClick Next to continue.")
        btn_back.config(state="disabled"); btn_next.config(text="Next >")
    elif pagina == 1:
        titolo.config(text="Select Installation Folder")
        testo.config(text="The installer will install Windows Media Center in the following folder.\n\nTo install in this folder, click Next. To install to a different folder, enter it below or click Browse.")
        entry.delete(0, tk.END); entry.insert(0, cartella)
        entry.pack(pady=10); btn_browse.pack()
        btn_back.config(state="normal")
    elif pagina == 2:
        titolo.config(text="Confirm Installation")
        testo.config(text="The installer is ready to install Windows Media Center.\n\nClick Next to start the installation.")
    elif pagina == 3:
        titolo.config(text="Installation Complete")
        testo.config(text="Windows Media Center has been successfully installed.\n\nClick Close to exit.")
        btn_next.config(text="Close")

def cambia(d):
    global pagina, cartella
    if pagina == 1:
        cartella = entry.get()
    if pagina == 2 and d == 1:
        try:
            os.makedirs(cartella, exist_ok=True)
            for f in ["MediaCenter.py", "logo.jpg"]:
                src = os.path.join(BASE, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(cartella, f))
            # Crea il file che dice "setup fatto"
            open(os.path.join(cartella, "installato.txt"), "w").write("ok")
            # Collegamento sul Desktop
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            target = os.path.join(cartella, "MediaCenter.py")
            ps = f'$W = New-Object -ComObject WScript.Shell; $S = $W.CreateShortcut("{desktop}\\Windows Media Center.lnk"); $S.TargetPath = "pythonw.exe"; $S.Arguments = "\\"{target}\\""; $S.WorkingDirectory = "{cartella}"; $S.Save()'
            subprocess.run(["powershell", "-Command", ps], creationflags=subprocess.CREATE_NO_WINDOW)
            messagebox.showinfo("Fatto", "Installato!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
    if pagina == 3 and d == 1:
        root.destroy()
        return
    pagina += d
    if pagina < 0: pagina = 0
    if pagina > 3: pagina = 3
    mostra()

mostra()
root.mainloop()