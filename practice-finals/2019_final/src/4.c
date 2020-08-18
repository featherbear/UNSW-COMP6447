#define HEIGHT 1000
#include <stdio.h>
#include <stdlib.h>

typedef struct node {
   int array[HEIGHT];
   int top;
} * Staque;

Staque create(void) {
   Staque st;
   st = malloc(sizeof(struct node));
   if (st == NULL) {
      fprintf (stderr, "create: no memory, aborting\n");
      exit(1);
   }
   st->top = -1;
   return st;
}

int isEmpty(Staque st) {
   int empty = 0;
   if (st == NULL) {
      fprintf(stderr, "isEmpty: staque not initialised\n");
   }
   else {
      empty = st->top < 0;
   }
   return empty;
}


void push(int data, Staque st) {
   if (st == NULL) {
      fprintf(stderr, "push: staque not initialised\n");
      return;
   }
   if (st->top == HEIGHT) {
      fprintf(stderr, "push: staque overflow\n");
      return;
   }
   ++st->top;
   st->array[st->top] = data;
   return;
}

int pop(Staque st) {
   if (st == NULL) {
      fprintf(stderr, "pop: staque not initialised\n");
      return 0;
   }
   if (isEmpty(st)) {
      fprintf(stderr, "pop: staque underflow\n");
      return 0;
   }
   int topdata = st->array[st->top];
   --st->top;
   return topdata;
}

void makeEmpty(Staque st) {
   if (st == NULL) {
      fprintf(stderr, "makeEmpty: staque not initialised\n");
      return;
   }
   if (st->top < 0) {
      fprintf(stderr, "makeEmpty: staque not initialised");
   }
   else {
      while (!isEmpty(st))
         pop(st);
   }
}

void show(Staque st) {
   if (st == NULL) {
      fprintf(stderr, "show: staque not initialised\n");
      return;
   }
   printf("Staque: ");
   if (st->top < 0) {
      printf("[ ]\n");
   }
   else {
      int i;
      putchar('[');                    // start with a [
      for (i = st->top; i > 0; --i) {
         printf("%d, ", st->array[i]); // print each element
      }
      printf("%d]\n", st->array[0]);   // last element includes a ]
   }
   return;
}

int main(int argc, char *argv[]) {
  Staque S = NULL;

  if (argc >= 2) {
     S = create();
	 int i = 1;
	 while (argv[i]) {
		 push(atoi(argv[i++]), S);
	 }
     while (!isEmpty(S)) {
        printf("%d\n", pop(S));
     }
  }
  return EXIT_SUCCESS;
}


