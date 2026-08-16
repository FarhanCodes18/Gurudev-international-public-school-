import urllib.request
import json

api_key = "AIzaSyD778gbyVVrez8R__xnvVNRMAZjAqEhVgQ"
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"

data = {
    "email": "admin@gurudev.com",
    "password": "adminpassword123",
    "returnSecureToken": True
}

req = urllib.request.Request(url, method="POST")
req.add_header('Content-Type', 'application/json')
data_bytes = json.dumps(data).encode('utf-8')

try:
    response = urllib.request.urlopen(req, data_bytes)
    print("Admin Auth Account created successfully:", response.read().decode('utf-8'))
except Exception as e:
    print("Error creating auth account (Might already exist):", str(e))
