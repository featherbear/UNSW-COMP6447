#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int value = atoi(argv[1]);

    switch (value) {
    case 0:
        puts("Thanks for that");
        break;

    case 1:
        puts("Thanks for that v2.");
        break;

    default:
        printf("Not sure what %d means\n", value);
        return 1;
    }

    return 0;
}
