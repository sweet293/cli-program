import socket
import ssl
import re
import html
from urllib.parse import quote


def search_request(query):
    host = 'html.duckduckgo.com'
    path = f"/html/?q={quote(query)}"

    context = ssl.create_default_context()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss = context.wrap_socket(s, server_hostname=host)
    ss.connect((host, 443))

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36\r\n"
        "Accept: text/html\r\n"
        "Accept-Language: en-US,en;q=0.9\r\n"
        "Connection: close\r\n\r\n"
    )
    ss.send(request.encode())

    response = b""
    while True:
        data = ss.recv(4096)
        if not data:
            break
        response += data
    ss.close()

    response_text = response.decode('utf-8', errors='replace')

    # Extract titles and links
    matches = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>', response_text, re.DOTALL)

    # Clean titles from leftover tags/entities
    cleaned_results = []
    for link, title in matches[:10]:
        clean_title = re.sub('<.*?>', '', title)
        clean_title = html.unescape(clean_title)
        cleaned_results.append((clean_title.strip(), link))

    print("==== RAW RESPONSE START ====")
    print(response_text[:1000])  # print first 1000 chars
    print("==== RAW RESPONSE END ====")
    return cleaned_results
