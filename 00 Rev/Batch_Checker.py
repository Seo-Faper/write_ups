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
