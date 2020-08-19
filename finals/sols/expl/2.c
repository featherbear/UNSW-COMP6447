#include <stdio.h>

char banner[] = "________________________\n"
                "|.----------------------.|\n"
                "||                      ||\n"
                "||                      ||\n"
                "||     .-\"````\"-.       ||\n"
                "||    /  _.._    `\\     ||\n"
                "||   / /`    `-.   ; . .||\n"
                "||   | |__  __  \\   |   ||\n"
                "||.-.| | e`/e`  |   |   ||\n"
                "||   | |  |     |   |'--||\n"
                "||   | |  '-    |   |   ||\n"
                "||   |  \\ --'  /|   |   ||\n"
                "||   |   `;---'\\|   |   ||\n"
                "||   |    |     |   |   ||\n"
                "||   |  .-'     |   |   ||\n"
                "||'--|/`        |   |--.||\n"
                "||   ;    .     ;  _.\\  ||\n"
                "||    `-.;_    /.-'     ||\n"
                "||         ````         ||\n"
                "||______________________||\n"
                "'------------------------'\n";

void functions_go_brrrr() {
  char buffer[23];
  puts(banner);
  printf("Do you remember how to roproprop... exec /bin/sh");
  puts("");
  fgets(buffer, 800, stdin);
}

int main(void) {
  setbuf(stdout, NULL);
  printf("want a leak: %p\n", functions_go_brrrr);
  functions_go_brrrr();
}

void _() {
  __asm__("int3;"
          "ret;"

          "mov eax, 0;"
          "mov edx, 0;"
          "ret;"

          "xor ecx, ecx;"
          "ret;"

          "pop ebx;"
          "ret;"

          "int 0x80;"
          "ret;"

          "add eax, 1;"
          "ret;");
}
