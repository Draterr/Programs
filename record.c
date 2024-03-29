#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define LOWER 1024
#define UPPER 65536

void add(FILE *file){
	//to do malloc new_text
	char *new_text = malloc(LOWER);
	int len;
	printf("Text to add: ");
	scanf("%s%n",new_text,&len);
	new_text = realloc(new_text,len);
	strcat(new_text,"\n");
	fputs(new_text,file);
	printf("added line: %s",new_text);
}
void delete(FILE *file){
	int c;
	int current_line = 1;
	char *removed = malloc(LOWER);
	int line_del;
	printf("Line to delete: ");
	scanf("%d",&line_del);
	FILE *newfile = fopen("new.txt","w+");
	int index = 0;
	rewind(file);
	do{
		c = fgetc(file);
		int convert_ascii = '0' + current_line;
		if(line_del != current_line){
			putc(c,newfile);
		}
		else if(line_del == current_line){ //print the line that is being deleted
			//removed[index] = c;
			*removed = c;
			removed++;
			index++;
			}
		if(c == '\n'){
			current_line++;
		}
	}
	while(c != EOF);
	removed[index-1] = '\0';
	removed = realloc(removed-=index,index);
	printf("Removed line %d\nText: %s",line_del,removed);
}
void modify(FILE *file){
	//find studentid and select one attribute to change (name,studntno,class)

}
int main(int argc, char *argv[]){
	char *file_name = argv[1];
	char *operation = argv[2];
	FILE *fptr = fopen(file_name,"r+");
	size_t increase = LOWER;
	size_t allocated = increase;
	char *string = malloc(allocated);
	size_t index = 0;
	char *search_str = malloc(LOWER);
	char *searchptr;
	int search_len;
	
	if (argc < 2){
		printf("invalid number of arugments!\n");
		return 1;
	}
	else if(fptr == NULL){
		printf("File does not exist.\n");
		return 1;
	}
	else if(ferror(fptr)) {
		printf("Error Opening file!\n");
		return 1;
	}
	
	while(!feof(fptr) && !ferror(fptr)){
		if(index >= allocated){
			if(index >= UPPER){
				increase  = UPPER;
			}
			allocated += increase;
			string = realloc(string, allocated);
			increase *= 2;
			//printf("%ld",allocated);
		}
		string[index] = fgetc(fptr);
		index++;
		}
	string[index-1] = '\0';
	if(strcmp(operation, "add") == 0){
		add(fptr);
	}
	else if(strcmp(operation, "delete") == 0){
		delete(fptr);
	}
	else if(strcmp(operation, "modify") == 0){
	}
	else if(strcmp(operation, "search") == 0){
		printf("Text to search: ");
		scanf("%s%n",search_str,&search_len);
		search_str = realloc(search_str,search_len);
			searchptr = strstr(string,search_str);
			if(searchptr == NULL){
				printf("Can't find string");
			}
			else{
				char *final_search = malloc(allocated);
				int i = 0;
				while(searchptr[i] != '\n'){
					final_search[i] = searchptr[i];
					i++;
					}
				final_search = realloc(final_search,i);
				printf("%s\n",final_search);
			}
	}
	else{
		printf("Operator not Found!");
	}
	free(string);
	fclose(fptr);
	return 0;
}

