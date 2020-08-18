mov eax, {stackAddress}   # Search from the stack address
mov ebx, 0x11223344       # Check for this signature
loop:
   inc eax                # Increment memory address
   cmp [eax-4], ebx       # Compare value at address to signature
   jne loop               # Loop if no match
   
   push eax               # Prepare jump to address eax
   ret                    # Go go go!