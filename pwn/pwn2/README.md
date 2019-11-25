# [SwampCTF 2019 Pwn] Dream Heaps

## Flavor Text

Due to the new order in this culture, dreams should be logged in a file for organizational purposes. You can change them if you want, but make sure to get rid of these unwanted ideas as soon as possible. Be careful though, don't be tempted to use dreams that you've already deleted! 

* Flag: `flag{d0nt_bE_nu11_b3_dul1}`
* Expected difficulty: medium 

## Description

This challenge involves a null byte overflow in the heap area. There is no use after free or other overflow aloud.
An info leak can be found by changing the previous size and the previous free metadata for a chunk and creating overlapping chunks.
Arbitrary write access comes from corrupting the forward pointer and adding a chosen element into a fastbin.
Additionally, the exploitation will involve overwriting the free hook or malloc hook, because RELRO with be full.
There will also be a limit on the number of chunks that can be allocated, so people will have to plan ahead and organize the heap exploit.

## Challenge Solution

This challenge uses a relatively simple bug, but the exploitation process for this bug occurs in many steps. 
In order to exploit this, the edit function must be used to write a null byte after the entered data.
If the edit function is used this takes place, so any changes without corruption must involve deletion and creation of a new chunk.
First, four chunks will be made, two of which have a size of 0xf8 (which will be shown on the heap as 0x100).
This size matters because the null byte overflow can be used to change the free bit without affecting the size of the chunk.
The first chunk is freed in order to put the arena libc pointers into the heap. 
After this, the second is editted to create a fake previous size and change the clear bit of chunk 2.
When the second chunk is now freed, it will consolidate to the metadata of the first chunk, if the previous size was set to the correct value.
A new chunk should be allocated to push the libc values into the first chunk, and these can be viewed and used as an infoleak.

Now that we have an info leak, we can use this to get code execution! This will involve a fastbin exploit with the overlapping chunks that we have created.
The previously created chunk (4) should be deleted and a new one should be created to add the size for a fastbin chunk. This should be the second chunk we created, so the size should match.
Then we will free this fastbin by freeing chunk 1. This will put it in a fastbin list.
After this we will free the previously created (consolidated) chunk in order to affect the forward pointer of the fastbin chunk.
This pointer should be set to the location we will write in, which must match a bin size. 
As RELRO is full, we will have to overwrite a libc hook. 0x23 bytes before malloc_hook, a fake chunk can be created with a size of 0x7f, or something between 0x70 and 0x80 based on ASLR. 

```
gef➤  p &__malloc_hook
$1 = (void *(**)(size_t, const void *)) 0x7f5aeae6fb10 <__malloc_hook>
gef➤  x/8gx 0x7f5aeae6fb10-0x23
0x7f5aeae6faed <_IO_wide_data_0+301>:   0x5aeae6e260000000      0x000000000000007f
0x7f5aeae6fafd: 0x5aeab30e20000000      0x5aeab30a0000007f
0x7f5aeae6fb0d <__realloc_hook+5>:      0x000000000000007f      0x0000000000000000
0x7f5aeae6fb1d: 0x0100000000000000      0x0000000000000000
```

If you don't have this, go back and make sure that your fastbins go into the 0x70 bin!
The next created chunk in this fastbin size will make this pointer the closest location in the fastbin, so the allocation afterwards will write there!
We will use this allocation to write a one_gadget to the malloc_hook, and we will use the offset of 0xf1147 from libc for this gadget (other's may not work).
A new dream after this will call malloc, which will use the function pointer of malloc_hook, so we will have a shell!

This was a difficult challenge to learn, and it was based partially on a technique I saw in plaidCTF's plaiddb. I also read an article about null byte poisoning that helped me understand the consolidation more [devel0pment](https://devel0pment.de/?p=688)
