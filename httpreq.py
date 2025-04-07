#httpreq.py
import socket
import ssl
import re
def make_request(url):
    # Extract host from URL
    if '://' in url:
        url = url.split('://', 1)[1]

    host = url.split('/', 1)[0]
    path = '/'

    # Connect to host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    # Send HTTP GET request
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
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
                request = f"GET {new_path} HTTP/1.1\r\nHost: {new_host}\r\nConnection: close\r\n\r\n"
                ss.send(request.encode())

                # Receive response
                https_response = b""
                while True:
                    data = ss.recv(4096)
                    if not data:
                        break
                    https_response += data

                ss.close()
                return https_response.decode('utf-8', errors='replace')

    return response_text