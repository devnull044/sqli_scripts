import request

url = 'https://ac351f881f9b2cd180271ce4000300d1.web-security-academy.net/filter?category=Accessories'

sqli_row = ["'+ORDER+BY",
            "'+UNION+SELECT+"]

try:
    r = requests.get(url=url)
except Exception as e:
    print(e)
    exit()

if r.status_code = 200:
    attack_url = url[:url.rfind("=")-1]
    attack_r = requests.get()
