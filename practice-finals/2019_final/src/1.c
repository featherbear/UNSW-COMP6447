#include <stdio.h>
int main() {
    char storage[32] = {0};

    int len = 0;
    puts("How many chars would you like to store?");
    scanf("%d", &len);

    if (len >= 32) {
        printf("no");
        return 1;
    }

    int i = 0;
    int *elem = storage;
    for(; i < len; i++, elem++) {
        printf("Enter character %d: ", i);
        scanf("%d", elem);
    }
}
