#include <stdio.h>

float diff(float *a, float *b, int len) {
  float diff = 0;
  int i = 0;
  while (i < len) {
    diff += (*a - *b);

    a++;
    b++;
    i++;
  }

  return diff;
}

int main() {
  float a[] = {1.0, 2.0};
  float b[] = {0.5, 2.0};

  printf("%f", diff(a, b, 2));
}
