#include <Windows.h>
#include <stdio.h>
#include <string.h>


char g_buffer[1000];

void a1()
{
    __asm {
        pop eax
        ret
        pop ecx
        ret
        mov [eax], ecx
        ret
    }
}

void unhexlify(char* dst, const char* src, size_t length)
{
    char hexBuffer[3] = { 0 };
    for (size_t i = 0; i < length / 2; ++i) {
        memcpy(hexBuffer, src + 2 * i, 2);
        sscanf_s(hexBuffer, "%02hhX", dst + i);
    }
}

int main(int argc, char** argv)
{
    char lBuffer[10];
    if (argc < 2) {
        printf("Please provide an hex string\n");
        return 1;
    }

    size_t length = strlen(argv[1]);
    unhexlify(lBuffer, argv[1], length);

    return 0;
}
