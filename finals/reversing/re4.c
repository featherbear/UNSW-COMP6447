void md5(arg1)
{
    char thing3[] = {
        0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
        0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10}; //"\x01\x23\x45\x67\x89\xab\xcd\xef"
    int var3c = 0;
    int var18 = 0;

    while (var18 < var3c) {
        var_1c_1 = var8
        var_20_1 = varc
        var_24_1 = var10
        var_28_1 = var14
        var_2c_1 = 0

        if (var_2c_1 < 0x3f) {
            var8 += var_1c_1
            varc += var_20_1
            var10 += var_24_1
            var14 += var_28_1
            var18 += 0x40;
            break;
        }

        if (var_2c_1 > 0xf) {
            
            var_30_1 = (~var_20_1 & var_28_1) | (var_20_1 & var_24_1);
            var_34_1 = var_2c_1;
        } else if (var_2c_1 <= 0x1f) {
                var_30_1 = (~var_28_1 & var_24_1) | (var_28_1 & var_20_1 )
                var_34_1 = (var_2c_1 << 2 + var_2c_1 + 1) & 0xf
        } else if (var_2c_1 <= 0x2f) {
            var_30_1 = var_20_1 ^ var_24_1 ^ var_28_1
            var_34_1 = (3*var_2c_1 + 0x5) & 0xf
        } else {
            var_30_1 = (~var_28_1 | var_20_1) ^ var_24_1
            var_34_1 = (var_2c_1 << 3 - var_2c_1) & 0xf
        }


        var_40_1 = var_28_1
        var_28_1 = var_24_1
        var_24_1 = var_20_1
        
        edx = var_1c_1
        eax = var_30_1

        edx=var_1c_1 + var_30_1

        edx  + array[var_2c_1]

        eax = var_34_1
        eax = ebp-0x7c


    }

    free(var38);

    tobytes(var4, arg1);
    tobytes(var8, arg1 + 4)
    tobytes(varc, arg1 + 8)
    tobytes(var10, arg1 + c)


}

int main() {

}