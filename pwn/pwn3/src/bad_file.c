#include <stdio.h>
#include <unistd.h>

void temp_name(unsigned char* location) {
	gets(location);
	printf("Hello, %s (for now)\n", location);
	free(location);
	return;
}

void perm_name(unsigned char* location) {
	gets(location);
	printf("Hello, %s!\n");
	return;
}

void hidden_alleyway() {
	system("cat flag.txt");
}

int main() {
	FILE *new_file;
	FILE *other_file;
	unsigned char *name = malloc(0x250);
	char void_bytes[0x20];
	char option[2];
	setbuf(stdout, NULL);
	puts("Would you like a (1) temporary name or a (2) permanent name?");
	read(0, option, 2);
	if (option[0] == '1') {
		temp_name(name);
	}
	else {
		perm_name(name);
	}
	new_file = fopen("/dev/null", "rw");
	puts("I created a void for you, and this can let you practice some sorcery");
	puts("You're in danger, you'll need a new name.");
	read(0, name, 0x160);
	puts("Now let's send some magic to the void!!");
	fread(void_bytes, 1, 0x8, new_file);
	printf("%s\n", void_bytes);
	puts("I hope the spell worked!");
	exit(0);
}
