#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void print_flag()
{
    system("cat flag.txt");
}

void hole_in_one()
{
	write(1, "below par!\n", 11);
}

int main()
{
	void** array_of_func_pntrs = malloc(0x60); // !!!
	int pnt_count = 0;
	write(1, "enter -1 to exit, -2 to free everything\n", 40);
	int al;
	void (*hio)() = &hole_in_one;
	array_of_func_pntrs[pnt_count] = hio; //, sizeof(void*));
	char data[10];

	while(1)
	{
		write(1, "Amount to alloc: ", 17);
		read(0, data, 4);
		al = atoi(data);
		if(al == -1)
		{
			void (*hio)() = array_of_func_pntrs[pnt_count];
			(*hio)();
			break;
		} 
		else if( al == -2)
		{
			for(int i = 0; i < pnt_count; i++)
			{
				free(array_of_func_pntrs[i]);
			}
			array_of_func_pntrs[0] = array_of_func_pntrs[pnt_count];
			pnt_count = 0;
		} 
		else 
		{
			array_of_func_pntrs[pnt_count+1] = array_of_func_pntrs[pnt_count];
			void* n_m = malloc(al);
			write(1, "Data: ", 6);
			read(0, n_m, al-1);
			array_of_func_pntrs[pnt_count] = n_m;
			pnt_count++;
		}
		
	}
	return 0;
}
