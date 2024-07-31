from pwn import *
p = remote('fsi.zzado.kr',7772)
p.recvuntil(b"============= Game Start =============\n")
for i in range(20):
    stage = p.recvline()
    if b"MATH Stage" in stage:
        recv_data = str(p.recv().strip()).split(' ')
        payload = bytes(str(eval(''.join([recv_data[0][2:]]+recv_data[1:3]))),encoding='utf-8')
        p.sendline(payload)
        print("MATH")
    elif b"ECHO Stage" in stage:
        q = p.recvline()
        q = q.replace(b'Msg : ', b'').strip()
        p.sendline(q)
        print("ECHO")
p.interactive()