#include "mem.h"                      
extern BLOCK_HEADER* first_header;

// return a pointer to the payload
// if a large enough free block isn't available, return NULL
void* Mem_Alloc(int size){
    // find a free block that's big enough

    // return NULL if we didn't find a block

    // allocate the block

    // split if necessary (if padding size is greater than or equal to 16 split the block)
	BLOCK_HEADER* current = first_header;
	int payload = size;
	size += 8; // header
	while (size%16) size++; // size now holds the block size
	while (!(current->size_alloc & 1 && current->payload == 0)) {
		if (!(current->size_alloc & 1) && current->size_alloc >= size) {
			if (current->size_alloc >= size+16) { // able to split
				BLOCK_HEADER* next = (BLOCK_HEADER*)((unsigned long)current + size);
				next->size_alloc = current->size_alloc - size;
				next->payload = current->payload - size;
				current->size_alloc = size;
			}
			current->size_alloc += 1;
			current->payload = payload;
			return (void*)((unsigned long)current + 8);
		}
		if (!(current->size_alloc & 1)) current = (BLOCK_HEADER*)((unsigned long)current + current->size_alloc);
		else current = (BLOCK_HEADER*)((unsigned long)current + current->size_alloc - 1);
	}

    return NULL;
}


// return 0 on success
// return -1 if the input ptr was invalid
int Mem_Free(void *ptr){
    // traverse the list and check all pointers to find the correct block 
    // if you reach the end of the list without finding it return -1
    
    // free the block 

    // coalesce adjacent free blocks
	
	BLOCK_HEADER* prev = first_header;
	BLOCK_HEADER* current = NULL;
	BLOCK_HEADER* next = NULL;
	if (!(prev->size_alloc & 1)) current = (BLOCK_HEADER*)((unsigned long)prev + prev->size_alloc);
	else current = (BLOCK_HEADER*)((unsigned long)prev + prev->size_alloc - 1);

	if (ptr == (BLOCK_HEADER*)((unsigned long)prev + 8)) {
		if (!(prev->size_alloc & 1)) return -1;
		prev->size_alloc -= 1;
		prev->payload = prev->size_alloc - 8;
		if (!(current->size_alloc & 1)) {
			prev->size_alloc += current->size_alloc;
			prev->payload += current->size_alloc;
		}
		return 0;
	}

	while (!(current->size_alloc & 1 && current->payload == 0)) {
		if (ptr == (BLOCK_HEADER*)((unsigned long)current + 8)) {
			if (!(current->size_alloc & 1)) return -1;
    		next = (BLOCK_HEADER*)((unsigned long)current + current->size_alloc - 1);

			current->size_alloc -= 1;
			current->payload = current->size_alloc - 8;

			if (!(next->size_alloc & 1)) {
				current->size_alloc += next->size_alloc;
				current->payload += next->size_alloc;
			}
			if (!(prev->size_alloc & 1)) {
				prev->size_alloc += current->size_alloc;
				prev->payload += current->size_alloc;
			}
			return 0;
		}
		
		prev = current;
		if (!(current->size_alloc & 1)) current = (BLOCK_HEADER*)((unsigned long)current + current->size_alloc);
        else current = (BLOCK_HEADER*)((unsigned long)current + current->size_alloc - 1);
	}

    return -1;
}

