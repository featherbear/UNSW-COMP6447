#include <stdio.h>
#include <stdlib.h>

int main() {}

struct person {
    int age;
    char *name;
};

struct person *sub_8049196() {
    struct person *p = malloc(8);
    
    if (p == NULL) {
        return NULL;
    }

    p->name = malloc(0x40);

    printf("What's your age mate? ");
    // assuming 0x804a023 is "%d"
    scanf("%d", &p->age);

    printf("And what should I call ya? ");
    // assuming 0x804a042 is "%s"
    scanf("%s", p->name);

    printf("nice to meet you %s\n", p->name);

    return p;
}