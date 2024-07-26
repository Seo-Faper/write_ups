# Batch_Checker
- 난이도 : 1
- site : https://dreamhack.io/wargame/challenges/1072
## 풀이
```
SET "vFKIqCfPYoAmeeWzfdvyZYfpahOFHCVyQUtAkTijwIPopWBKOMfruHFORhPjfwYyYKCEqxVzFWNMyyobMWMSiubUIryEWWNrCSRc=ulZiZYfKDHzPwKTOGzSxCQgAqLsLrlZgbVwLZOGrhfXGldhCPdOqLQNphEoyTNANLqJxIeMbOLbSksFJKIydnFKWZJqenBoJNWtVH"
SET "UVeVvzSzLQEcxjDZnrFCsuchulInGHnmANMmdAcpDxNXQWJYholJwnXMYMxyZtauzxbgDhInaTdlgaYsyxWnIlwrYCQQJWsXYRsD=zoicwbfhakobovodszjrrxdeqvebafhaqifmanmwkufv_xxafsqaewqujcuydhyiueqxjznojjjymdxzbkjwmjxhwgsmxwwxeowjx"
SET 
...
@%tWtDFxVVNdburePMrddbWpadDxfqxyLEjneybCnXSlHVWZjUhwlTHOXLlZtcHCjhVRUvpAHmeCzcAIFrWxXQDHKpBZNKqyhCubwM:~53,
1%%yEBnwgURQEtxNyJTQpBBOflLAlqjTJjNlGNQOInMnhmSxetZWSHstdrmhNWJdKqFvDmmAAxbJmHZdKvRUuGtVtqwLrYuvKdhFrwC:~26,
1%%fyjBZrnDUsfRpiZKIgBBSuGBhWjMZJSVhJqTIIqDIBSKQuACSZdfNevFMRVVCtIoWsEHvOwfWhSZxemPcWRzdZJdjxzcdAfvDKVI:~20,1%%
```
SET으로 변수를 설정하고, %variable:~start,length% 형식으로 문자열 슬라이싱을 구현하고 있다. 
정규표현식으로 PoC를 짤 수 있다.
```py
import re


with open('.prob.bat', 'r') as file:
    bat_content = file.read()

variables = {}
set_pattern = re.compile(r'SET\s+"([^=]+)=([^"]+)"')
for match in set_pattern.findall(bat_content):
    var_name, value = match
    variables[var_name] = value

substring_pattern = re.compile(r'%([^%:]+):~(\d+),(\d+)%')
results = []
for match in substring_pattern.findall(bat_content):
    var_name, start, length = match
    start, length = int(start), int(length)
    if var_name in variables:
        variable_value = variables[var_name]
        result = variable_value[start:start + length]
        results.append(result)

print(''.join(results))

```
그럼 다음과 같은 출력이 나온다.<br>
`echooffifFLAG==BA7cH_cAN_hiDe_u5iNg_textechocorrectelseechowrongpause`<br>
띄워쓰기가 짤리긴 했는데 읽는데 큰 지장은 없다.<br>
`echo off if FLAG == BA7cH_cAN_hiDe_u5iNg_text echo correct else echo wrong pause`

## flag : DH{BA7cH_cAN_hiDe_u5iNg_text}