import http.server
import ssl
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

server = http.server.HTTPServer(('0.0.0.0', 8443), http.server.SimpleHTTPRequestHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    '../backend/cert.pem',
    '../backend/key.pem'
)
server.socket = context.wrap_socket(server.socket, server_side=True)
print("HTTPS Frontend running on https://192.168.0.110:8443")
server.serve_forever()