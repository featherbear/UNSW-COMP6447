int main() {
    return re_this(1,2);
}

int re_this(int arg1, int arg2) {
    // ecx = arg1 + arg2
    // EAX = SAR (arithmetic (arg+arg2) >> by 0x1f (31))

    // eax = 6 * [ HI((arg1+arg2) * 0x2aaaaaaab) - (arithmetic (arg+arg2) >> by 0x1f (31)) ]
    // eax = 6 * [ (arg1+arg2) / 6 - (arithmetic (arg+arg2) >> by 0x1f (31)) ]
    // eax = arg1 + arg2 - 6 * [ HI((arg1+arg2) * 0x2aaaaaaab) - (arithmetic (arg+arg2) >> by 0x1f (31)) ]

    // Multiply by 0x2aaaaaab - Divide by 6

    // return (arg1 + arg2) - ((arg1 + arg2) / 6 * 6);   
    // sum/6         => number of times 6 fits in the sum
    // (sum/6) * 6   => quotient * 6 => highest multiple of 6 in the sum
    // sum - sum/6*6 => remainder when dividing by 6
    
    return (arg1 + arg2) % 6;
}