#httpreq.py
import socket
import ssl
import re
def make_request(url, accept="html"):
    # Extract host from URL
    if '://' in url:
        url = url.split('://', 1)[1]

    parts = url.split('/', 1)
    host = parts[0]
    path = '/' + parts[1] if len(parts) > 1 else '/'

    # Connect to host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    # Choose correct Accept header
    accept_header = "application/json" if accept == "json" else "text/html"

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Accept: {accept_header}\r\n"
        f"Connection: close\r\n\r\n"
    )
    s.send(request.encode())

    # Receive response
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data

    s.close()

    response_text = response.decode('utf-8', errors='replace')

    # Check for redirect
    if '301 Moved Permanently' in response_text or '302 Found' in response_text:
        # Find the redirect location
        match = re.search(r'Location: (.+?)\r\n', response_text)
        if match:
            new_url = match.group(1).strip()
            print(f"Redirecting to: {new_url}")

            # Handle HTTPS redirect
            if new_url.startswith('https://'):
                new_host = new_url.split('://', 1)[1].split('/', 1)[0]
                new_path = '/' + new_url.split('://', 1)[1].split('/', 1)[1] if '/' in new_url.split('://', 1)[
                    1] else '/'

                # Create secure socket
                context = ssl.create_default_context()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ss = context.wrap_socket(s, server_hostname=new_host)
                ss.connect((new_host, 443))

                # Send HTTPS GET request
                accept_header = "application/json" if accept == "json" else "text/html"
                request = (
                    f"GET {new_path} HTTP/1.1\r\n"
                    f"Host: {new_host}\r\n"
                    f"Accept: {accept_header}\r\n"
                    f"Connection: close\r\n\r\n"
                )
                ss.send(request.encode())

                # Receive response
                https_response = b""
                while True:
                    data = ss.recv(4096)
                    if not data:
                        break
                    https_response += data

                ss.close()
                response_text = https_response.decode('utf-8', errors='replace')
                if '\r\n\r\n' in response_text:
                    response_text = response_text.split('\r\n\r\n', 1)[1]

    def clean_html(html):
        html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
        html = re.sub(r'<[^>]+>', '', html)  # scoate tag-urile
        html = re.sub(r'[ \t]+', ' ', html)  # spatii/tabs multiple -> 1 spatiu
        html = re.sub(r'\s*\n\s*', '\n', html)  # spatii inainte/dupa newline -> sterge
        html = re.sub(r'\n+', '\n', html)  # newlines multiple -> unul singur
        return html.strip()

    return clean_html(response_text)