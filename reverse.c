#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MEM 1024
int main(){
	char *arr = malloc(MEM);
	printf("Input string: ");
	fgets(arr,MEM,stdin);
	char *firstptr;
	char *lastptr;
	char tmp;
	int len = strlen(arr);
	char *pmt;
	if(len > MEM){
		pmt = realloc(arr,len);
		if(pmt == NULL){
			printf("realloc failed!");
			return -1;
		}
	}
	for(int i=0;i<(len)/2;i++){
		firstptr = &arr[i];
		lastptr = &arr[len-1-i];
		tmp = *lastptr;
		arr[len-1-i] = *firstptr;
		//printf("%d (%c) is being replaced by: %c\n",len-i,tmp,*firstptr);
		//printf("%d (%c) is being replaced by: %c\n",i,*firstptr,tmp);
		arr[i] = tmp; 
	}
	printf("%s\n",arr);
	return 0;
	free(arr);
}
