# go2web: Command-Line Web Fetching and Search Tool

## Overview
`go2web` is a powerful command-line tool for making HTTP requests, searching the web, and fetching web content with advanced features like caching and content negotiation — all built from scratch using raw socket programming in Python.

---

## Installation
Clone the repository and give execution permissions:

```bash
git clone https://github.com/sweet293/go2web.git
cd go2web
chmod +x go2web
```
---

## Features
- HTTP requests to specified URLs using `-u <URL>`
- Web search using DuckDuckGo with `-s <search-term>`
- Content negotiation (accept JSON or HTML responses)
- HTTP caching mechanism for faster repeated requests
- Redirect handling for 3xx responses
- Clean, human-readable output (HTML tags removed)
---

## How it works:
- Uses socket for raw TCP communication with web servers
- Parses HTTP responses manually
- Handles redirects (3xx codes)
- Strips HTML tags for clean terminal output
- Caches responses using file-based storage

## 📌 Usage

### 🔎 Web Search

```bash
./go2web -s "python programming"
```
Displays the top 10 search results with titles and URLs.

### Fetch URL Content
```bash
"What do you want to access?: 2"
```
Opens and displays the 2nd result from the previous search.

### Help
```bash
./go2web -h
```
Shows available options and usage instructions.

### Advanced Options
```bash
--json       Prefer JSON content (if available)
--html       Force HTML content (default)
--no-cache   Disable HTTP response caching
```

## Demo
![Demo] (go2web2025.gif)