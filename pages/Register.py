import requests

# URL endpoint for the API
url = "https://www.screener.in/api/company/3370/chart/?q=Price-DMA50-DMA200-Volume&days=365&consolidated=true"

# Cleaned request headers
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-IE,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": "theme=dark; csrftoken=IJtgqIdAmTmsEtdJ3M8iNjt5ZaKsEH6L; sessionid=9ebpb9akgyq31bfxyqcx9qoua0ssdw6i",
    "pragma": "no-cache",
    "referer": "https://www.screener.in/company/TATAMOTORS/consolidated/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("Data fetched successfully:")
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
