/*

    run_command_in_sandbox() takes in a user and command, and runs the command in a sandboxed environment. This is a safe function.
    find_permission_level returns an integer for the permission of the uid supplied.

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>

struct user {
  char *name;
  char auth;
};

extern void run_command_in_sandbox(struct user *user, char *cmd);
extern int find_permission_level(char *username);

struct user *logged_in_user = NULL;

int logged_in() {
  if (logged_in_user == NULL) {
    puts("Not logged in.");
    return 0;
  } else {
    return 1;
  }
}

void menu() {
  puts("Available commands:");
  puts("\tuser - shows current logged_in_user info");
  puts("\tlogin logged_in_user - Login to logged_in_user");
  puts("\trun command - Run command as logged_in_user");
}

void logged_in_user_info() {
  if (logged_in()) {
    printf("Logged in %s [%u]\n", logged_in_user->name, logged_in_user->auth);
  }
}

void login(char *buf) {
  if (logged_in_user != NULL) {
    puts("Already logged in. logout first");
    return;
  }

  // Find newline.
  char *arg = strtok(buf + 6, "\n");
  if (arg == NULL) {
    puts("Invalid command");
    return;
  }

  logged_in_user = (struct user *)malloc(sizeof(struct user));
  if (logged_in_user == NULL) {
    puts("Malloc failed");
    exit(-1);
  }

  logged_in_user->name = strdup(arg);
  logged_in_user->auth = find_permission_level(arg);
  printf("Logged in as \"%s\"\n", arg);
}

void run_command(char *buf) {
  if (!logged_in()) {
    return;
  }

  // Find newline.
  char *arg = strtok(buf + 5, "\n");
  if (arg == NULL) {
    puts("Invalid command");
    return;
  }

  run_command_in_sandbox(logged_in_user, strdup(arg));
  syslog(LOG_INFO, strdup(arg));
}

void logout() {
  if (!logged_in()) {
    return;
  }

  free(logged_in_user->name);
  free(logged_in_user);
  logged_in_user = NULL;

  puts("Logged out");
}

int main(int argc, char *argv[], char *envp[]) {
  setbuf(stdout, NULL);

  menu();

  while (1) {
    char buf[512];

    puts("Enter cmd: ");
    putchar('>');
    putchar(' ');

    if (fgets(buf, 512, stdin) == NULL)
      break;

    if (!strncmp(buf, "user", 4)) {
      logged_in_user_info();
    } else if (!strncmp(buf, "login", 5)) {
      login(buf);
    } else if (!strncmp(buf, "run", 4)) {
      run_command(buf);
    } else {
      puts("What?");
      return 0;
    }
  }
}
