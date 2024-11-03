import requests
import time

address = input('Input server address please:')

for i in range(10):
    port = 8080 + i
    server = f'http://{address}:{port}'

    try:
            response = requests.get(server, timeout=5)
            if response.status_code == 200:
                print(f'{i} Server {server} is avalable\nAnswer: {response.status_code}')
            else:
                print(f'{i} Server {server} not avalable\nAnswer: {response.status_code}')
    except requests.exceptions.RequestException as e:
            print(f'{i} Cannot connect to server {server}\nError: {e}')

