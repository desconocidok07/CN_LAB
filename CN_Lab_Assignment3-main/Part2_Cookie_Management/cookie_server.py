#!/usr/bin/env python3
"""
CN Lab Assignment 3 - Part 2: Cookie Management with Raw Sockets
This server implements session management using cookies at the raw socket level.
"""

import socket
import threading
import time
import random
from datetime import datetime, timedelta

# Server configuration
HOST = '127.0.0.1'
PORT = 8081
BUFFER_SIZE = 4096

class CookieHTTPServer:
    """HTTP Server with cookie-based session management using raw sockets"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.client_counter = 0
        
    def start(self):
        """Start the server and listen for connections"""
        # Create TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind and listen
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        
        print(f"\n{'='*60}")
        print(f"  Cookie Management Server - CN Lab Assignment 3 Part 2")
        print(f"{'='*60}")
        print(f"Server listening on http://{self.host}:{self.port}")
        print(f"Using raw sockets for HTTP communication")
        print(f"\nFeatures:")
        print(f"  ✓ Cookie-based session management")
        print(f"  ✓ User identification and tracking")
        print(f"  ✓ Personalized responses")
        print(f"\nPress Ctrl+C to stop the server")
        print(f"{'='*60}\n")
        
        try:
            while True:
                # Accept client connection
                client_socket, client_address = self.socket.accept()
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Connection from {client_address}")
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n\nServer stopped by user")
            print(f"{'='*60}\n")
        finally:
            self.socket.close()
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Receive HTTP request
            request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            
            if not request:
                return
            
            # Parse HTTP request
            headers = self.parse_http_request(request)
            
            # Extract cookie if present
            cookie_value = self.extract_cookie(headers)
            
            # Generate response based on cookie presence
            if cookie_value:
                # Returning visitor
                print(f"  → Returning visitor identified: {cookie_value}")
                response = self.create_returning_visitor_response(cookie_value)
            else:
                # First-time visitor
                self.client_counter += 1
                new_user_id = f"User{random.randint(100, 999)}_{self.client_counter}"
                print(f"  → New visitor - assigning ID: {new_user_id}")
                response = self.create_new_visitor_response(new_user_id)
            
            # Send response
            client_socket.sendall(response.encode('utf-8'))
            print(f"  → Response sent ({len(response)} bytes)")
            
        except Exception as e:
            print(f"  ✗ Error handling client: {e}")
        finally:
            client_socket.close()
    
    def parse_http_request(self, request):
        """Parse HTTP request and extract headers"""
        lines = request.split('\r\n')
        headers = {}
        
        # Skip the request line (GET / HTTP/1.1)
        for line in lines[1:]:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.lower()] = value
        
        return headers
    
    def extract_cookie(self, headers):
        """Extract user cookie from headers"""
        cookie_header = headers.get('cookie', '')
        
        # Parse cookie string (format: "user_id=User123; other_cookie=value")
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split('; '):
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name] = value
        
        return cookies.get('user_id')
    
    def create_new_visitor_response(self, user_id):
        """Create HTTP response for first-time visitor with Set-Cookie header"""
        
        # Calculate cookie expiry (1 hour from now)
        expires = datetime.utcnow() + timedelta(hours=1)
        expires_str = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # HTML content for new visitor
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome New User!</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        .welcome-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        .user-id {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            font-weight: bold;
            margin: 20px 0;
        }}
        .info {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }}
        .cookie-info {{
            font-family: monospace;
            background: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="welcome-icon">🎉</div>
        <h1>Welcome, New Visitor!</h1>
        <p>This is your first visit to our server.</p>
        <div class="user-id">Your ID: {user_id}</div>
        
        <div class="info">
            <h3>🍪 Cookie Set Successfully!</h3>
            <p>We've set a cookie to remember you for your next visit.</p>
            <div class="cookie-info">
                <strong>Cookie Name:</strong> user_id<br>
                <strong>Cookie Value:</strong> {user_id}<br>
                <strong>Expires:</strong> {expires_str}
            </div>
        </div>
        
        <p style="margin-top: 30px; color: #666;">
            <strong>Try refreshing the page</strong> to see the personalized welcome message!
        </p>
    </div>
</body>
</html>"""
        
        # Build HTTP response with Set-Cookie header
        response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(html_content)}\r
Set-Cookie: user_id={user_id}; Expires={expires_str}; Path=/; HttpOnly\r
Connection: close\r
\r
{html_content}"""
        
        return response
    
    def create_returning_visitor_response(self, user_id):
        """Create HTTP response for returning visitor"""
        
        # HTML content for returning visitor
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome Back!</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{
            color: #28a745;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        .welcome-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        .user-id {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            font-weight: bold;
            margin: 20px 0;
        }}
        .info {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }}
        .visit-time {{
            font-size: 1.2em;
            color: #666;
            margin-top: 20px;
        }}
        .cookie-status {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 10px;
            margin-top: 15px;
            color: #155724;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="welcome-icon">👋</div>
        <h1>Welcome Back!</h1>
        <p>Great to see you again!</p>
        <div class="user-id">Your ID: {user_id}</div>
        
        <div class="info">
            <h3>✅ Session Recognized</h3>
            <p>Your cookie was successfully read from the request.</p>
            <div class="cookie-status">
                <strong>🍪 Cookie Status:</strong> Active<br>
                <strong>Session ID:</strong> {user_id}<br>
                <strong>Recognition:</strong> Successful
            </div>
        </div>
        
        <div class="visit-time">
            Current visit time: {datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')}
        </div>
        
        <p style="margin-top: 30px; color: #666;">
            <em>Clear your cookies or use incognito mode to see the new visitor page again.</em>
        </p>
    </div>
</body>
</html>"""
        
        # Build HTTP response (no Set-Cookie needed for returning visitor)
        response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(html_content)}\r
Connection: close\r
\r
{html_content}"""
        
        return response

def main():
    """Main function to start the cookie server"""
    server = CookieHTTPServer(HOST, PORT)
    try:
        server.start()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()