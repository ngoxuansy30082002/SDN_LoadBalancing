from http.server import HTTPServer, BaseHTTPRequestHandler
import time

HOST_NAME = "10.0.0.2"
PORT_NUMBER = 80
RESPONSE_STRING = "10.0.0.2"
MAX_PACKET_SIZE = 1024


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_length = int(self.headers.get('Content-Length', 0))

        # Xử lý dữ liệu theo từng phần nhỏ
        processed_bytes = 0
        while processed_bytes < content_length:
            chunk_size = min(MAX_PACKET_SIZE, content_length - processed_bytes)
            data = self.rfile.read(chunk_size)
            processed_bytes += len(data)
            # time.sleep(0.01)
            # Ở đây bạn có thể thêm logic xử lý dữ liệu
            # ...

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(RESPONSE_STRING.encode())


if __name__ == "__main__":
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(f"Server started at http://{HOST_NAME}:{PORT_NUMBER}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")
