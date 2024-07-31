// gcc -o pwn hello_pwn.c -fcf-protection=none -fno-pic -no-pie
// socat TCP-LISTEN:7773,fork,reuseaddr SYSTEM:"env REMOTE_ADDR=\$SOCAT_PEERADDR /home/hello_pwn/hello_pwn"
#include <stdio.h>
#include <stdlib.h>

int main() {
    setbuf(stdin ,NULL);
    setbuf(stdout ,NULL);

    char *ip_addr = getenv("REMOTE_ADDR");
    char ip_buf[0x30];
    memset(ip_buf, 0x00, 0x30);
    memcpy(ip_buf, ip_addr, strlen(ip_addr));
    
    char pw_buf[0x20];    
    memset(pw_buf, 0x00, 0x20);
    printf("Enter password : ");
    gets(pw_buf);
    
    if(!strcmp("PaS5w03d", pw_buf)){
        if(!strcmp(ip_buf, "127.0.0.1")){
            puts("Hello, admin!");
            system("/bin/sh");
        }else{
            puts("Accessible only in localhost");
        }
    }else{
        puts("Wrong password!");
    }
}