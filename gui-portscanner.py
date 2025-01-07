import socket
import concurrent.futures
import threading
import customtkinter as ctk
import nmap 

# Variable pour contrôler l'état du scan
scanning = False

# Fonction pour scanner un port
def scan_port(domainip: str, port: int) -> tuple:
    try:
        # Utiliser une connexion socket plus rapide
        s = socket.create_connection((domainip, port), timeout=0.5)
        return (port, "open")
    except Exception:
        return (port, "closed")

# Fonction pour scanner les ports
def scan_ports(ip, start_port, end_port):
    open_ports = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            if not scanning:  # Vérifier si le scan doit être arrêté
                break
            port, status = future.result()
            if status == "open":
                open_ports[port] = status
    return open_ports

# Fonction pour scanner les services sur les ports ouverts
def scan_services(ip, open_ports):
    nm = nmap.PortScanner()
    services = {}
    for port in open_ports:
        nm.scan(ip, str(port))
        if nm[ip].all_state() == 'up':
            service_info = nm[ip]['tcp'][port]
            services[port] = {
                'name': service_info['name'],
                'state': service_info['state'],
                'version': service_info.get('version', 'N/A')
            }
    return services

# Fonction pour lancer le scan dans un thread
def start_scan():
    global scanning
    scanning = True
    ip = ip_entry.get()
    start_port = 1  # Port de début fixe
    try:
        end_port = int(end_port_entry.get())
    except ValueError:
        result_text.insert(ctk.END, "Veuillez entrer un numéro de port valide.\n")
        return

    if end_port < start_port or end_port > 65535:
        result_text.insert(ctk.END, "Veuillez entrer une plage de ports valide (1-65535).\n")
        return

    result_text.delete(1.0, ctk.END)  # Effacer le texte précédent
    result_text.insert(ctk.END, f"Scanning {ip} from port {start_port} to {end_port}...\n")
    
    # Lancer le scan dans un thread
    threading.Thread(target=run_scan, args=(ip, start_port, end_port)).start()

# Fonction pour exécuter le scan et afficher les résultats
def run_scan(ip, start_port, end_port):
    open_ports = scan_ports(ip, start_port, end_port)
    if open_ports:
        result_text.insert(ctk.END, f"Ports ouverts: {', '.join(map(str, open_ports.keys()))}\n")
        # Scanner les services sur les ports ouverts
        services = scan_services(ip, open_ports)
        for port, info in services.items():
            result_text.insert(ctk.END, f"Port {port}: {info['name']} (Version: {info['version']})\n")
    else:
        result_text.insert(ctk.END, "Aucun port ouvert trouvé.\n")
    global scanning
    scanning = False  # Réinitialiser l'état du scan

# Fonction pour arrêter le scan
def stop_scan():
    global scanning
    scanning = False
    result_text.insert(ctk.END, "Scan arrêté.\n")

# Création de l'interface graphique
ctk.set_appearance_mode("dark")  # Mode sombre
ctk.set_default_color_theme("blue")  # Thème bleu

app = ctk.CTk()
app.title("Scanner de Ports")
app.geometry("400x400")

# Champ pour entrer l'IP
ip_label = ctk.CTkLabel(app, text="Entrez l'adresse IP:")
ip_label.pack(pady=10)

ip_entry = ctk.CTkEntry(app)
ip_entry.pack(pady=10)

# Champ pour entrer le port de fin avec valeur par défaut 1024
end_port_label = ctk.CTkLabel(app, text="Port de fin (par défaut 1024):")
end_port_label.pack(pady=10)

end_port_entry = ctk.CTkEntry(app)
end_port_entry.insert(0, "1024")  # Valeur par défaut
end_port_entry.pack(pady=10)

# Bouton pour lancer le scan
scan_button = ctk.CTkButton(app, text="Lancer le scan", command=start_scan)
scan_button.pack(pady=10)

# Bouton pour arrêter le scan
stop_button = ctk.CTkButton(app, text="Arrêter le scan", command=stop_scan)
stop_button.pack(pady=10)

# Zone de texte pour afficher les résultats
result_text = ctk.CTkTextbox(app, width=300, height=150)
result_text.pack(pady=10)

app.mainloop()
