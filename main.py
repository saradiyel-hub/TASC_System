import customtkinter as ctk
import psutil
import datetime
import os
import google.generativeai as genai
from tkintermapview import TkinterMapView
from tkinter import messagebox
import pygame
import subprocess
import sys  # පද්ධතියෙන් ආරක්ෂිතව පිටවීමට

# --- Sound System ---
pygame.mixer.init()

def play_sound(sound_type):
    try:
        if sound_type == "login":
            os.system('spd-say "Access Granted. Welcome to TASC System" &')
        elif sound_type == "btn":
            os.system('spd-say "Task Initialized" &')
    except:
        pass

# --- Gemini AI Configuration ---
try:
    genai.configure(api_key="AIzaSyDyhnqD9FW6dr17GCFjdiYplnt8Hpk3wgs")
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    print(f"AI Config Error: {e}")

# --- 1. LOGIN WINDOW ---
class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("SECURITY CHECK"); self.geometry("400x500"); self.configure(fg_color="black")
        self.attributes("-topmost", True)
        
        ctk.CTkLabel(self, text="ACCESS RESTRICTED", font=("Impact", 28), text_color="red").pack(pady=50)
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)
        
        self.bind("<Return>", lambda e: self.check_login())
        ctk.CTkButton(self, text="AUTHENTICATE", fg_color="red", command=self.check_login).pack(pady=30)

    def check_login(self):
        if self.user_entry.get() == "irajhashini" and self.pass_entry.get() == "Irajhashini1993":
            play_sound("login")
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("DENIED", "Invalid Credentials!")

# --- 2. SELECTION PAGE ---
class SelectionPage(ctk.CTk):
    def __init__(self, start_console, open_settings):
        super().__init__()
        self.title("SYSTEM SELECTION"); self.geometry("500x400"); self.configure(fg_color="black")
        ctk.CTkLabel(self, text="CHOOSE OPERATIONAL MODE", font=("Courier", 20, "bold"), text_color="yellow").pack(pady=40)
        ctk.CTkButton(self, text="START MAIN PROGRAM", fg_color="green", text_color="black", height=60, command=lambda: [self.destroy(), start_console()]).pack(pady=10, padx=50, fill="x")
        ctk.CTkButton(self, text="SYSTEM SETTINGS (CODE)", fg_color="red", height=60, command=lambda: [self.destroy(), open_settings()]).pack(pady=10, padx=50, fill="x")

# --- 3. MAIN CONSOLE ---
class HackerConsole(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TASC_SYSTEM_V16")
        self.attributes('-fullscreen', True); self.configure(fg_color="black")
        
        # Layout Columns
        self.grid_columnconfigure(0, weight=0); self.grid_columnconfigure(1, weight=1); self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Left) ---
        self.sidebar = ctk.CTkFrame(self, width=180, fg_color="#080808", border_width=2, border_color="yellow")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        ctk.CTkButton(self.sidebar, text="🤖 GEMINI AI", fg_color="#4B0082", command=self.open_ai_assist).pack(pady=15, padx=10, fill="x")
        
        # EXIT බොත්තම නිවැරදි කර ඇත
        ctk.CTkButton(self.sidebar, text="❌ EXIT SYSTEM", fg_color="#333", command=self.quit_app).pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.sidebar, text="📡 WIFI SCANNER", fg_color="#1a1a1a", text_color="#00FF00", command=self.scan_wifi).pack(pady=10, padx=10, fill="x")
        
        for i in range(2, 14):
            ctk.CTkButton(self.sidebar, text=f"PROGRAM {i:02}", fg_color="#1a1a1a", text_color="#00FF00", command=lambda x=i: self.log_activity(f"PRG_{x} INIT")).pack(pady=2, padx=10, fill="x")

        # --- Center Display Area ---
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=2, border_color="yellow")
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.display_top = ctk.CTkTextbox(self.center_frame, fg_color="#050505", text_color="#00FF00", font=("Courier New", 14), border_width=1, border_color="yellow")
        self.display_top.pack(expand=True, fill="both", pady=2, padx=2)
        
        self.display_bottom = ctk.CTkTextbox(self.center_frame, fg_color="#050505", text_color="cyan", font=("Courier New", 14), border_width=1, border_color="yellow")
        self.display_bottom.pack(expand=True, fill="both", pady=2, padx=2)

        # --- Right Panel ---
        self.right_panel = ctk.CTkFrame(self, width=300, fg_color="#080808", border_width=2, border_color="yellow")
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        
        self.map_view = TkinterMapView(self.right_panel, height=200, corner_radius=10); self.map_view.pack(fill="x", padx=10, pady=10)
        
        self.vpn_sw = ctk.CTkSwitch(self.right_panel, text="VPN ENCRYPTION", text_color="white", command=self.toggle_vpn)
        self.vpn_sw.pack(pady=15)

        # CPU & RAM Stats
        self.stats_frame = ctk.CTkFrame(self.right_panel, fg_color="#111", border_width=1, border_color="yellow")
        self.stats_frame.pack(fill="x", padx=10, pady=10)
        self.stats_lbl = ctk.CTkLabel(self.stats_frame, text="INITIALIZING STATS...", font=("Courier", 13, "bold"), text_color="white")
        self.stats_lbl.pack(pady=10)
        
        self.clock_lbl = ctk.CTkLabel(self.right_panel, text="00:00:00", font=("Courier", 28, "bold"), text_color="yellow")
        self.clock_lbl.pack(pady=20)

        # Shutdown Buttons
        self.panic_btn = ctk.CTkButton(self.right_panel, text="UNLOCK SHUTDOWN", height=60, fg_color="green", text_color="black", font=("Impact", 16), command=self.unlock_shutdown)
        self.panic_btn.pack(pady=10, padx=10, fill="x")
        
        self.shutdown_btn = ctk.CTkButton(self.right_panel, text="EMERGENCY SHUTDOWN", height=60, fg_color="#444", text_color="white", state="disabled", command=lambda: os.system("poweroff"))
        self.shutdown_btn.pack(pady=10, padx=10, fill="x")

        self.update_loop()

    # --- Safe Exit Function ---
    def quit_app(self):
        try:
            play_sound("btn")
            self.destroy() # UI එක වසයි
            sys.exit() # Python Process එක සම්පූර්ණයෙන්ම නතර කරයි
        except:
            os._exit(0) # කිසිම හේතුවක් නිසා stuck වුවහොත් බලහත්කාරයෙන් වසයි

    def update_loop(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.stats_lbl.configure(text=f"CPU LOAD: {cpu}%\nRAM USAGE: {ram}%")
            self.clock_lbl.configure(text=datetime.datetime.now().strftime("%H:%M:%S"))
            self.after(1000, self.update_loop)
        except:
            pass

    def log_activity(self, msg):
        play_sound("btn")
        self.display_bottom.insert("end", f">>> {msg} at {datetime.datetime.now().strftime('%H:%M:%S')}\n")
        self.display_bottom.see("end")

    def unlock_shutdown(self):
        play_sound("btn")
        self.shutdown_btn.configure(state="normal", fg_color="red")
        self.display_top.insert("end", "[!] ALERT: EMERGENCY SHUTDOWN SEQUENCE UNLOCKED.\n")

    def scan_wifi(self):
        self.log_activity("SCANNING NEARBY NETWORKS...")
        try:
            output = subprocess.check_output(["nmcli", "-f", "SSID,BARS,SECURITY", "dev", "wifi"]).decode()
            self.display_top.delete("1.0", "end")
            self.display_top.insert("end", "--- SURROUNDING WIFI NETWORKS ---\n\n" + output)
        except:
            self.display_top.insert("end", "ERROR: WiFi hardware not responding.\n")

    def toggle_vpn(self):
        play_sound("btn")
        state = "ACTIVATED" if self.vpn_sw.get() else "DEACTIVATED"
        self.log_activity(f"VPN {state}")

    def open_ai_assist(self):
        ai_win = ctk.CTkToplevel(self); ai_win.title("GEMINI AI CORE"); ai_win.geometry("450x600"); ai_win.attributes("-topmost", True)
        txt = ctk.CTkTextbox(ai_win, fg_color="black", text_color="white", font=("Courier", 12))
        txt.pack(expand=True, fill="both", padx=10, pady=10)
        ent = ctk.CTkEntry(ai_win, placeholder_text="Ask Gemini..."); ent.pack(fill="x", padx=10, pady=5)
        def send(e=None):
            msg = ent.get(); txt.insert("end", f"USER: {msg}\n")
            try:
                res = model.generate_content(msg); txt.insert("end", f"AI: {res.text}\n")
            except Exception as err: txt.insert("end", f"ERROR: {err}\n")
            ent.delete(0, 'end'); txt.see("end")
        ent.bind("<Return>", send)

if __name__ == "__main__":
    def start(): HackerConsole().mainloop()
    LoginWindow(on_success=lambda: SelectionPage(start_console=start, open_settings=lambda: os.system("lxterminal -e nano main.py")).mainloop()).mainloop()
