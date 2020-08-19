#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  int var = atoi(argv[1]);

  switch (var) {
  case 0:
    puts("Thanks for that");
    break;
  case 1:
    puts("Thanks for that v2.");
    break;
  default:
    printf("Not sure what %d means\n", var);
    return 1;
  }

  return 0;
}
