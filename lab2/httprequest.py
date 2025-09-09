import requests

# Test API (jsonplaceholder is a free fake API for testing)
GET_URL = "https://jsonplaceholder.typicode.com/posts/1"
POST_URL = "https://jsonplaceholder.typicode.com/posts"

try:
    # 1. Send a GET request
    print("=== GET Request ===")
    response = requests.get(GET_URL)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text, "\n")

    # 2. Send a POST request
    print("=== POST Request ===")
    data = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(POST_URL, json=data)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text, "\n")

except requests.exceptions.RequestException as e:
    # 3. Log errors if request fails
    print("❌ Request failed:", e)
