import requests
import json

response = requests.get(url='https://api.github.com/users/le0lik/repos').json()

with open('file.json', 'w') as out_file:
    json.dump(response, out_file)

for i in response:
    print(i['name'])

