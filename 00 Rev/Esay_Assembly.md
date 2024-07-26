# Esay Assembly
- 난이도 : 1
  
## 풀이
```c
// positive sp value has been detected, the output may be wrong!
void __noreturn start()
{
  _BYTE *v0; // ecx
  int v1; // eax
  int v2; // [esp-Ch] [ebp-Ch]

  if ( v2 == 1 )
  {
    print();
    print();
  }
  else
  {
    len = strlen();
    check_password(len, 0, enc_flag, v0);
  }
  print();
  v1 = sys_exit(0);
}

int __usercall check_password@<eax>(int a1@<eax>, int a2@<ecx>, _BYTE *a3@<edi>, _BYTE *a4@<esi>)
{
  do
  {
    a2 |= (unsigned __int8)(*a3++ ^ len ^ *a4++);
    --a1;
  }
  while ( a1 );
  return a2;
}
```
check_password 로직 확인 결과, len은 문자열의 길이이고 enc_flag는 전역 변수로 선언되어 있다. <br> 
a2 |= (~~~~)에서 |=은 a2의 값을 왼쪽으로 미는 것과 같다. a1은 len, a2는 0, a3는 enc_flag, a4는 v0이다.<br>
즉 한 글자씩 돌면서 전체 길이만큼 계속 xor 하는 로직이라고 볼 수 있다.

```c
.data:0804A000 enc_flag        db 74h, 78h, 4Bh, 65h, 77h, 48h, 5Ch, 69h, 68h, 7Eh, 5Ch
.data:0804A000                                         ; DATA XREF: LOAD:0804807C↑o
.data:0804A000                                         ; _start+35↑o
.data:0804A000                 db 79h, 77h, 62h, 46h, 79h, 77h, 5, 46h, 54h, 73h, 72h
.data:0804A000                 db 59h, 69h, 68h, 7Eh, 5Ch, 7Eh, 5Ah, 61h, 57h, 6Ah, 77h
.data:0804A000                 db 66h, 5Ah, 52h, 2, 62h, 5Ch, 79h, 77h, 5Ch, 0, 7Ch, 57h
.data:0804A000                 db 2 dup(0Dh), 4Dh, 0
```
여기 보면 enc_flag에 대한 값이 있는데, 파이썬 리스트로 바꿔보면 다음과 같다.
```py
enc_flag_hex = [
    0x74, 0x78, 0x4B, 0x65, 0x77, 0x48, 0x5C, 0x69, 0x68, 0x7E, 0x5C,
    0x79, 0x77, 0x62, 0x46, 0x79, 0x77, 0x05, 0x46, 0x54, 0x73, 0x72,
    0x59, 0x69, 0x68, 0x7E, 0x5C, 0x7E, 0x5A, 0x61, 0x57, 0x6A, 0x77,
    0x66, 0x5A, 0x52, 0x02, 0x62, 0x5C, 0x79, 0x77, 0x5C, 0x00, 0x7C, 0x57,
    0x0D, 0x0D, 0x4D
]
```

## 최종 코드
```py
# 암호화된 16진수 값들
enc_flag_hex = [
    0x74, 0x78, 0x4B, 0x65, 0x77, 0x48, 0x5C, 0x69, 0x68, 0x7E, 0x5C,
    0x79, 0x77, 0x62, 0x46, 0x79, 0x77, 0x05, 0x46, 0x54, 0x73, 0x72,
    0x59, 0x69, 0x68, 0x7E, 0x5C, 0x7E, 0x5A, 0x61, 0x57, 0x6A, 0x77,
    0x66, 0x5A, 0x52, 0x02, 0x62, 0x5C, 0x79, 0x77, 0x5C, 0x00, 0x7C, 0x57,
    0x0D, 0x0D, 0x4D
]

ans = []

enc_len = len(enc_flag_hex)


for i in range(enc_len):
    decrypted_char = chr(enc_flag_hex[i] ^ enc_len)
    ans.append(decrypted_char)

decrypted_message = ''.join(ans)
print(decrypted_message)

```

## flag : `DH{UGxlYXNlIGRvIG5vdCBiYXNlNjQgZGVjb2RlIGl0Lg==}`