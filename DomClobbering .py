import re

def waf(input):
    t = input.lower()
    pattern = re.compile(r"script|on|frame|object|embed|data|&#|src|//|'|\"|`|\*")
    match = pattern.search(t)
    if match:
        return f"Filtered due to pattern: {match.group()}"
    else:
        return input

s = input()
print(waf(s))