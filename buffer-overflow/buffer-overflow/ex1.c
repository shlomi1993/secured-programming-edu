#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv)
{
	setuid(0);
	char buffer[500];
	strcpy(buffer, argv[1]);

	return 0;
}
