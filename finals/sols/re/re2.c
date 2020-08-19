#include <stdio.h>
#include <stdlib.h>

struct person {
  int age;
  char *name;
};

struct person *create_person() {
  struct person *person = malloc(sizeof(struct person));
  if (person == NULL) {
    return NULL;
  }

  person->name = malloc(sizeof(char) * 64);

  printf("What's your age mate? ");
  scanf("%d", &person->age);

  printf("And what should I call ya? ");
  scanf("%s", person->name);

  printf("nice to meet you %s\n", person->name);

  return person;
}

int main(int argc, char *argv[], char *envp[]) { create_person(); }
