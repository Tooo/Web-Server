# Web Server
Simple web server that handles one HTTP request at a time.
Handles the messages for 200, 304, 400, 404, and 408.
A multi-threaded web server is also avaliable to handle multiple requests simultaneously

## Installation - Single Thread Web-Server
1. Download and install [Python 3.9.](https://www.python.org/downloads/release/python-392/)
2. In [webserver.py](https://github.com/Tooo/web-server/blob/main/webserver.py), 
   fill in your server's host and port
```python
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
```
3. Run webserver.py
```bash
python3 webserver.py
```
4. Open the URL on your browser with your server's host and port
```bash
<SERVER_HOST>:<SERVER_PORT>
```

## Installation - Multi-Threaded
1. Run multi_webserver.py
```bash
python3 multi_webserver.py
```

## Testing Multi-Thread Web-Server
1. Run multi_webserver.py
```bash
python3 multi_webserver.py
```
2. Run test_multithreaded.py located in the tests directory
```bash
python3 test_multithreaded.py
```


## Supported HTTP Response Status Codes
| Code | Message |
| ---- | --------|
| 200 | OK |
| 304 | Not Modified |
| 400 | Bad Request |
| 404 | Not Found |
| 408 | Request Timed Out |
