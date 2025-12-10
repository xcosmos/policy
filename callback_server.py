from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/callback":
            query_params = parse_qs(parsed_path.query)
            code = query_params.get('code', [None])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if code:
                html_content = f"""
                <html>
                <head><title>OAuth Success</title></head>
                <body>
                    <h1>Authorization Successful!</h1>
                    <p>We received the authorization code:</p>
                    <code style="background: #f0f0f0; padding: 10px; display: block; word-break: break-all;">{code}</code>
                    <p>You can close this window now.</p>
                </body>
                </html>
                """
                self.wfile.write(html_content.encode('utf-8'))
                print(f"Received Auth Code: {code}")
            else:
                self.wfile.write(b"<h1>Error: No code received</h1>")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == '__main__':
    # Changed port to 8088 to avoid conflict with Obsidian
    server_address = ('', 8088)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    print("Starting callback server on port 8088...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
