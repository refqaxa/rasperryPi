import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer

# GPIO Setup
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# HTML-pagina
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Control</title>
</head>
<body>
    <h1>LED Control</h1>
    <button onclick="toggleLED('on')">LED Aan</button>
    <button onclick="toggleLED('off')">LED Uit</button>
    <script>
        function toggleLED(action) {
            fetch('/led/' + action, { method: 'GET' })
                .then(response => response.text())
                .then(alert)
                .catch(console.error);
        }
    </script>
</body>
</html>
"""

# HTTP Server Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.respond(HTML)
        elif self.path == "/led/on":
            GPIO.output(LED_PIN, GPIO.HIGH)
            self.respond("LED is aan")
        elif self.path == "/led/off":
            GPIO.output(LED_PIN, GPIO.LOW)
            self.respond("LED is uit")
        else:
            self.respond("Onbekende route", 404)

    def respond(self, message, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))

# Start HTTP Server
def run():
    server_address = ('', 8000)  # Luister op poort 8000
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server gestart op poort 8000 (http://<RaspberryPi-IP>:8000)")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestopt")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    run()
