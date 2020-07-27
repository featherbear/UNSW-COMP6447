#include <stdio.h>

int main(int argc) {
    int var_14 = 0;

    while (var_14 <= 9) {
        // Print if odd
        if (var_14 & 1) {
            // Don't know what the print string is
            // But we know it prints out var_14
            printf("%d", var_14);
        }

        var_14++;
    }

    return 1;
}