#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>

int check_element(int i, char j) {
	int k = i + 0x15;
	int l = k ^ 2;
	int m = l - 30;
	if ((char)m == (char)j) {
		return 0;
	}
	return 1;
}

void waste_time() {
	int j = 0;
	int i = 0;
	for (i; i < 1000; i++) {
		j = (i % 2);
	}
	return;
}

int main() {
	char key_arr[] = {113, 115, 104, 114, 134, 114, 55, 55, 107, 106, 123, 111, 56, 121, 114, 60, 106, 113, 55, 125, 106, 130, 59, 56, 123, 112, 121, 114, 132};
	int arr_len = sizeof(key_arr) / sizeof(key_arr[0]);
	char inp_key[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	int i = 0;
	puts("Give the key, if you think you are worthy.\n");
	fgets(inp_key, 40, stdin);
	for (i = 0; i < arr_len; i++) {
		waste_time();
		if (check_element((int)key_arr[i], (int)inp_key[i])) {
			exit(1);
		}
	}
	puts("Good job!");
	return 0;
}
