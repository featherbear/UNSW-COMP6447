float sub_8049196(float *arg1, float *arg2, int arg3){

    float sum = 0;
    int idx = 0;

    while (idx < arg3){
        sum += *arg1 - *arg2;
        arg1++;
        arg2++;
        idx++;
    }

    return sum;
}

int main() {
    
}