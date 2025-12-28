import os
import sys
import subprocess
import requests  # Remote Update සඳහා අවශ්‍ය වේ
import customtkinter as ctk
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Gemini API Setup
genai.configure(api_key="ඔබේ_GEMINI_API_KEY_එක_මෙතැනට") # ඔබ සතු Key එක ඇතුළත් කරන්න

class HackerConsole(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TASC SYSTEM - ADVANCED VERSION V18")
        self.geometry("1000x700")
        self.configure(fg_color="#0a0a0a")

        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR ----------------
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0f0f0f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="SYSTEM CORE", font=("Courier", 20, "bold"), text_color="#00FF00").pack(pady=20)

        # පැරණි සහ අලුත් සියලුම බොත්තම්
        self.add_menu_button("🤖 ASK AI", self.clear_display, "cyan")
        self.add_menu_button("🔍 IP SCANNER", self.network_scanner, "yellow")
        self.add_menu_button("🧹 SYS CLEANER", self.system_cleaner, "orange")
        self.add_menu_button("🌐 REMOTE UPDATE", self.remote_update, "#00FF7F")

        # ---------------- DISPLAY AREA ----------------
        self.display_top = ctk.CTkTextbox(self, fg_color="#050505", text_color="#00FF00", font=("Courier", 14))
        self.display_top.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="nsew")

        # ---------------- INPUT AREA ----------------
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Command or Question...", fg_color="#101010", text_color="white", font=("Courier", 14))
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.send_btn = ctk.CTkButton(self.input_frame, text="RUN", width=100, command=self.process_ai)
        self.send_btn.pack(side="right")

    def add_menu_button(self, text, command, color):
        ctk.CTkButton(self.sidebar, text=text, fg_color="#1a1a1a", text_color=color, hover_color="#333333", command=command).pack(pady=5, padx=10, fill="x")

    def log_activity(self, message):
        self.display_top.insert("end", f"\n[SYSTEM] {message}\n")
        self.display_top.see("end")

    def clear_display(self):
        self.display_top.delete("1.0", "end")
        self.log_activity("AI CONSOLE READY...")

    # --- 1. NETWORK SCANNER (PROGRAM 02) ---
    def network_scanner(self):
        self.log_activity("SCANNING LOCAL NETWORK...")
        try:
            # Note: sudo apt install nmap තිබිය යුතුය
            cmd = "nmap -sn 192.168.1.0/24" 
            output = subprocess.check_output(cmd.split()).decode()
            self.display_top.delete("1.0", "end")
            self.display_top.insert("end", f"--- NETWORK SCAN RESULTS ---\n\n{output}")
        except Exception as e:
            self.log_activity("ERROR: Install nmap (sudo apt install nmap)")

    # --- 2. SYSTEM CLEANER (PROGRAM 03) ---
    def system_cleaner(self):
        self.log_activity("STARTING SYSTEM CLEANUP...")
        commands = ["rm -rf ~/.cache/*", "rm -rf /tmp/*", "sudo apt-get autoremove -y"]
        for c in commands:
            os.system(c)
        self.display_top.delete("1.0", "end")
        self.display_top.insert("end", "✅ SYSTEM CLEANUP COMPLETED!\nCache and Temp files cleared.")

    # --- 3. REMOTE UPDATE FUNCTION ---
    def remote_update(self):
        self.log_activity("FETCHING UPDATES FROM GITHUB...")
        # ඔබගේ සෘජු RAW URL එක මෙන්න
        raw_url = "https://raw.githubusercontent.com/saradiyel-hub/TASC_System/main/main.py"
        try:
            response = requests.get(raw_url, timeout=15)
            if response.status_code == 200:
                with open("main.py", "w") as f:
                    f.write(response.text)
                self.log_activity("UPDATE DOWNLOADED! RESTARTING...")
                os.execv(sys.executable, ['python3'] + sys.argv)
            else:
                self.log_activity(f"UPDATE FAILED (Status: {response.status_code})")
        except Exception as e:
            self.log_activity(f"REMOTE ERROR: {e}")

    # --- 4. AI PROCESSING ---
    def process_ai(self):
        prompt = self.user_input.get()
        if not prompt: return
        self.log_activity(f"YOU: {prompt}")
        self.user_input.delete(0, "end")
        try:
            model = GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            self.log_activity(f"AI: {response.text}")
        except Exception as e:
            self.log_activity(f"AI ERROR: {e}")

if __name__ == "__main__":
    app = HackerConsole()
    app.mainloop()
