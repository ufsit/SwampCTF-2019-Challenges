#include <stdlib.h>
#include <unistd.h>

void win_func()
{
    system("cat flag.txt");
}

int main()
{
	void* array_of_pntrs[50];
	int pnt_count = 0;
	void * target = malloc(0x20);
	write(0, "target green provisioned.\n", 26);
	array_of_pntrs[pnt_count] = target;
	pnt_count++;
	int al;
	char data[5];
	write(0, "enter -1 to exit simulation, -2 to free course.\n", 48);
	while(1)
	{
		
		write(0, "Size of green to provision: ", 28);
		read(1, data, 4);
		al = atoi(data);
		if(al == -1)
		{
			break;
		}
		else if(al == -2)
		{
			for(int i = 0; i < pnt_count; i++)
			{
				free(array_of_pntrs[i]);
			}
			array_of_pntrs[0] = malloc(0x20);
			write(0, "target green provisioned.\n", 26);
			pnt_count = 1;
		}
		else {
			void * new_m = malloc(al);
			*(int*)(new_m) = pnt_count;
			array_of_pntrs[pnt_count] = new_m;
			pnt_count++;
			if(pnt_count == 48)
			{
				write(0, "You're too far under par.", 25);
				break;
			}
		}
		if (*(int*)(target) == 4) 
		{
			win_func();	
		}
	}
	return 0;
}
