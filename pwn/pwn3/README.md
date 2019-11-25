# [SwampCTF 2019 Pwn] Bad File

## Flavor Text

Files are cool, so I'll let you play with one! This file I let you use may seem dull, but you should find some magic you can use within! 

* Flag: `flag{plz_n3v3r_f1l3_4ft3r_fr33!}`
* Expected difficulty: medium

## Description

This challenges is a relatively easy introduction to FILE exploitation. A use-after-free bug should be found quickly, but the challenge will be understanding the FILE struct format.
Participants should look into the source code of fread or discover information on FSOP by searching online.
Debugging will be important, as well as sending raw data, so gdb and pwntools will be important.
Additionally, the GOT and recognition of partial RELRO is important.

## Challenge Solution

In this challenge, there is an ability to free the name chunk if you choose to use a temporary name. However, if you do this, the new_file FILE struct is stored on the same section of the heap.
In order to abuse this, you can change the name and therefore the FILE contents before fread is called.
This is a modern version of libc (> 2.23) so it is not easy to overwrite the vtable of the file.
I learned about this idea from Angelboy [translated article](https://gsec.hitb.org/materials/sg2018/D1%20-%20FILE%20Structures%20-%20Another%20Binary%20Exploitation%20Technique%20-%20An-Jie%20Yang.pdf)
However, fread can be used to arbitrarily write to memory if flags and pointers are set properly.
No flags should be set, so the header is 0xfbad0000. 
All of the read ptrs should be null, these would affect the flow of fread.
The location from buf_base to buf_end should be where to write, and these need to be greater than the size passed to fread.
fileno should be set to 0 to match stdin, so you can input the data
The address of the hidden function can be written to the GOT (puts or exit).

The following is the beginning layout of the FILE struct from [Geeks for Geeks](https://www.geeksforgeeks.org/data-type-file-c/)

```
struct _IO_FILE {
  int _flags;       /* High-order word is _IO_MAGIC; rest is flags. */
  #define _IO_file_flags _flags

    /* The following pointers correspond to the C++ streambuf protocol. */
	/* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
    char* _IO_read_ptr;   /* Current read pointer */
	char* _IO_read_end;   /* End of get area. */
	char* _IO_read_base;  /* Start of putback+get area. */
	char* _IO_write_base; /* Start of put area. */
	char* _IO_write_ptr;  /* Current put pointer. */
	char* _IO_write_end;  /* End of put area. */
	char* _IO_buf_base;   /* Start of reserve area. */
	char* _IO_buf_end;    /* End of reserve area. */
	/* The following fields are used to support backing up and undo. */
	char *_IO_save_base; /* Pointer to start of non-current get area. */
	char *_IO_backup_base;  /* Pointer to first valid character of backup area */
	char *_IO_save_end; /* Pointer to end of non-current get area. */

	struct _IO_marker *_markers;

	struct _IO_FILE *_chain;

	int _fileno;
```

The exploit is exp.py, it creates the file payload.
