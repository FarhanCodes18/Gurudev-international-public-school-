import urllib.request
import json

url = "https://firestore.googleapis.com/v1/projects/gurudev-international/databases/(default)/documents/admins?documentId=admin"

data = {
    "fields": {
        "role": {"stringValue": "admin"},
        "email": {"stringValue": "admin@gurudev.com"},
        "name": {"stringValue": "Super Admin"}
    }
}

req = urllib.request.Request(url, method="POST")
req.add_header('Content-Type', 'application/json')
data_bytes = json.dumps(data).encode('utf-8')

try:
    response = urllib.request.urlopen(req, data_bytes)
    print("Admin seeded successfully:", response.read().decode('utf-8'))
except Exception as e:
    print("Error seeding admin. It might already exist or require auth:", str(e))
