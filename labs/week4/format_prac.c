#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
       #include <sys/types.h>
       #include <sys/stat.h>
       #include <fcntl.h>

#define USERNAME "COMP6447_ADMIN"

int target;
int getInput(char *check, char *input);
		
int main(){
	char password[40];
	memset(password,0,40);
	char input[40];
	memset(input,0,40);

	printf("Opening password file...\n");
	int fp = open("password", O_RDONLY);
	if(fp == -1){
		printf("Missing admins file\n");
		strcpy(password,"___PASSWORD___");
	}else{
		int len = read(fp, password, 40);
		if(len==0){
			printf("Password file is empty\n");
			return 1;	
		}	
		password[len] = 0;
	}	

	printf("Enter Username:\n");
	if(getInput(USERNAME,input)){
		printf("Enter Password:\n");
		if(getInput(password,input)){
			printf("Welcome Admin!\n");
			if(target){
				printf("Legendary Hacker!\n");
			}else{
				printf("Nearly there... Can you change the variable as well?\n");
				getInput("",input);
				if(target){
					printf("Legendary Hacker!\n");
				}
			}
		}else{
			printf("Invalid Password\n");
			
		}
	}else{
		printf("Invalid Username\n");
	}
	return 1;
}

int getInput(char *check, char* input){

	fgets(input,40,stdin);
	
	if (strncmp(check,input,strlen(check)-1)) {
		printf(input);
		printf("\n");
		return 0;
	}
	return 1;
}
