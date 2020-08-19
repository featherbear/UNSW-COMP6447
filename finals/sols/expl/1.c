#include <stdio.h>

void win() { system("/bin/sh"); }

int main() {
  setbuf(stdout, NULL);
  char buf[4];
  printf("Let's see if you can do this. Win functions @ %p\n", win);
  fgets(buf, 400, stdin);
}
