#include <stdlib.h>

struct myStruct {
    char value;
    struct myStruct *next;
};

struct myStruct *doIt() {
    struct myStruct *var_C = NULL;
    int var_8 = 0;

    while (var_8 <= 9) {
        struct myStruct *node = malloc(sizeof(struct myStruct));
        if (node == NULL) {
            exit(1);
        }

        if (var_C == NULL) {
            var_C = node;
        } else {
            node->next = var_C;
            var_C = node;
        }

        node->next = 0; // Well this line is interesting...

        node->value = var_8 + 0x41;
        var_8++;
    }
    return var_C;
}

int main() {}