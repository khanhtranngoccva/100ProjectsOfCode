import json

import requests
from urllib import parse, request

api_provider = "https://api.ipgeolocation.io/ipgeo?apiKey=691f8717d7ce4457b412b65e3eb15d7b"

ip_address = "25.72.138.51"


output_url = f'{api_provider}&ip={ip_address}'
# print(output_url)

header = {
    "User-agent": "Mozilla/5.0"
}

a = requests.get(output_url, headers=header)

results = json.loads(a.text)

cname = results.get("country_name", None)

print(f"Country name is: {cname}")