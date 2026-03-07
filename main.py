import asyncio
from src.scanner import run_scanner
import customtkinter as ctk
from threading import Thread
from PIL import Image
import os
from datetime import datetime
from tkinter import filedialog

class PortScannerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Port Scanner Pro")
        self.geometry("355x700")
        self.resizable(False, False)
        self.is_scanning = False

        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # --- BACKGROUND IMAGE ---
        #self.bg_image = ctk.CTkImage(
        #    light_image=Image.open("assets/base_bg.png"), 
        #    dark_image=Image.open("assets/base_bg.png"), 
        #    size=(500, 700)
        #) 

        #self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        #self.bg_label.place(x=352, y=0)  #Not used for the main version

        # --- LEFT CONTROL PANEL ---
        #  Container to keep everything on the left side (inputs, buttons, progress bar)
        self.left_frame = ctk.CTkFrame(self, width=350, height=700, fg_color="transparent")
        self.left_frame.place(x=0, y=0)

        # App title
        self.main_label = ctk.CTkLabel(self.left_frame, text="PORT SCANNER PRO", font=("Fixedsys", 24, "bold"), text_color="cyan")
        self.main_label.pack(pady=(30, 20), padx=20)

        # Input zone for IP address
        self.ip_label = ctk.CTkLabel(self.left_frame, text="Target IP Address:", font=("Arial", 12, "bold"))
        self.ip_label.pack(pady=(10, 0), padx=30, anchor="w")
        self.ip_entry = ctk.CTkEntry(self.left_frame, width=300, placeholder_text="e.g. 127.0.0.1")
        self.ip_entry.pack(pady=5, padx=30)

        # Input zone for port range
        self.port_label = ctk.CTkLabel(self.left_frame, text="Port Range (from 0 to 65535):", font=("Arial", 12, "bold"))
        self.port_label.pack(pady=(10, 0), padx=30, anchor="w")
        self.port_entry = ctk.CTkEntry(self.left_frame, width=300, placeholder_text="e.g. 20-80 or 0")
        self.port_entry.pack(pady=5, padx=30)

        # Scan Btn
        self.btn_scan = ctk.CTkButton(self.left_frame, width=300, height=40, text="START SCAN", 
                                      font=("Arial", 13, "bold"), command=self.launch_scan)
        self.btn_scan.pack(pady=25, padx=30)

        # --- TERMINAL ---
        self.console_label = ctk.CTkLabel(self, text="LIVE TERMINAL LOG", font=("Courier", 14, "bold"), text_color="white")
        self.console_label.place(x=30, y=390)

        self.console = ctk.CTkTextbox(self, width=300, height=220, 
                                     fg_color="#272727", text_color="#00FF00", 
                                     font=("Courrier New", 11), border_width=4, border_color="#333333",)
        self.console.place(x=30, y = 430)
        self.console.configure(state="disabled")

        # Barre de progression
        self.progress_label = ctk.CTkLabel(self.left_frame, text="Progress: 0%", font=("Arial", 11))
        self.progress_label.pack(padx=30, anchor="w")
        self.progress = ctk.CTkProgressBar(self.left_frame, width=300)
        self.progress.set(0)
        self.progress.pack(pady=5, padx=30)

        # Tags de couleur
        self.console.tag_config("open", foreground="#00FF00") # Vert vif
        self.console.tag_config("closed", foreground="#FFA500") # Orange
        self.console.tag_config("error", foreground="#FF4444") # Rouge
        self.console.tag_config("info", foreground="#00CCFF")  # Cyan

        # Separator lines
        #self.separator = ctk.CTkFrame(self, width=5, height=700, fg_color="#191919")
        #self.separator.place(x=365, y=0)

        # Save logs button
        self.save_btn = ctk.CTkButton(self.left_frame, width=70, height=30, text="SAVE LOGS",
                                        font=("Arial", 8, "bold"), command=self.save_logs, 
                                        border_width=2, border_color="#3B8ED0")
        self.save_btn.pack(pady=22, padx=30, anchor="e")

        # Clear logs button
        self.clear_btn = ctk.CTkButton(self.left_frame, width=70, height=30, text="CLEAR LOGS",
                                        font=("Arial", 8, "bold"), command=self.clear_logs, 
                                        border_width=2, border_color="#3B8ED0")
        #self.clear_btn.pack(pady=22, padx=60, anchor="w")
        self.clear_btn.place(x=180, y=390)

    def clear_logs(self):
        self.log("Logs cleared.", status="info")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")


    def save_logs(self):
        log_content = self.console.get("0.1", "end").strip()

        if not log_content:
            self.log("No logs to save.", status="error")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scan_logs_{timestamp}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=filename,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )   
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(f"Port Scanner Pro Logs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n")
                    f.write(f"{30*'-'}\n")
                    f.write(log_content)
                self.log(f"Logs successfully saved to {os.path.basename(file_path)}", status="info")
            except Exception as e:
                self.log(f"Error saving logs: {str(e)}", status="error")


    def update_progress(self):
        if not self.is_scanning:
            return

        self.scanned_ports += 1
        percent = self.scanned_ports / self.total_ports
        self.after(0, self._set_progress, percent)

    def _set_progress(self, percent):
        self.progress.set(percent)
        self.progress_label.configure(text=f"Progress: {int(percent * 100)}%")

    def log(self, message, status = None): # Ajoute un message dans la console interne
        self.after(0, self._safe_log, message, status)

    def _safe_log(self, message, status):
        self.console.configure(state="normal") # Deverrouille la console pour pouvoir y ecrire
        
        if status == "open":
            self.console.insert("end", message + "\n", "open")
        elif status == "closed":
            self.console.insert("end", message + "\n", "closed")
        elif status == "error":
            self.console.insert("end", message + "\n", "error")
        else:
            self.console.insert("end", message + "\n", "info")

        self.console.see("end") # Scroll auto vers le bas
        self.console.configure(state="disabled") # Reverrouille la console pour eviter les ecritures accidentelles

    def stop_scan(self):
        global stopped
        # On signale au scanner qu'il doit s'arrêter
        self.is_scanning = False 
        self.btn_scan.configure(fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#2E5575", "#1F6AA5"], text="START SCAN", command=self.launch_scan)
        self.log("[ :(  ] Scan stopping...", status="error")
        stopped = True
        return stopped


    def launch_scan(self):
        global port_input, stopped
        self.is_scanning = True

        port_input = self.port_entry.get()
        target = self.ip_entry.get()

        self.btn_scan.configure(fg_color="red",hover_color="red", text="STOP", command=self.stop_scan)

        if not target or len(target.split('.')) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in target.split('.')):
            self.log("Invalid IP address. Please enter a valid IP address", status="error")
            self.stop_scan()
            return

        if port_input:
            try:
                start_p, end_p = map(int, port_input.split('-'))
                if start_p < 0 or end_p > 65535 or start_p > end_p:
                    self.log("Invalid port range. Please enter a valid range (e.g., 20-80).", status="error")
                    return
                target_port = range(start_p, end_p + 1)
            except:
                self.log("Format error, please make sure it's either 0 or e.g., 20-80", status="error")
                self.stop_scan()
                return
        else:
            target_port = range(0, 1025) #1024 ports by default if no input

        self.total_ports = len(target_port)
        self.scanned_ports = 0
        self.progress.set(0)

        Thread(target=self.run_logic, args=(target, target_port), daemon=True).start()

    def run_logic(self, target, port_range):
        global stopped
        stopped = False
        self.log(f"[ :P ] Starting scan on {target}...", status="info")

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Fonction de callback pour que scanner.py ecrive directement dans la console de l'interface
            found = loop.run_until_complete(run_scanner(target, port_range, self.log, self.update_progress, lambda : self.is_scanning))
            if stopped == True:
                self.log(f"\n[ :x ] Scan aborted. Open ports: {', '.join(map(str, found)) if found else 'None'}", status="info")
            else:
                self.log(f"\n[ :D ] Scan completed. Open ports: {', '.join(map(str, found)) if found else 'None'}", status="info")
        except Exception as e:
            self.stop_scan()
            self.log(f"An error occurred: {str(e)}", status="error")
        finally:   
            stopped = False
            loop.close()
            self.after(0, lambda: self.btn_scan.configure(
                fg_color=["#3B8ED0", "#1F6AA5"], 
                hover_color=["#2E5575", "#1F6AA5"], 
                text="START SCAN", 
                command=self.launch_scan
            ))
            
if __name__ == "__main__":
    app = PortScannerGUI()
    app.mainloop()