Andrew Wong z5206677

# 1

Type Mismatch + Integer Underflow.

If `len < -8`, then `header_size + len` will become a negative value. This will cause `read` function to read a large number of bytes due to an (unsigned) integer underflow. This will cause a buffer overflow `storage`, allowing control of the return address, etc of `main`

# 2

Type Mismatch

```
logged_in_user->auth = find_permission_level(arg);
```

A type mismatch between `(char) user->auth` and `(int) find_permission_level` may cause unexpected privilege escalation. For example a permission level of `(int) -1` will translate to `(char) 255`, a permission level of `(int) 257` will be `(char) 1`. This can lead to execution of commands by an unauthorised user

# 3

Use After Free

The `len--` statement in `print_it` makes the program vulnerable to a Use After Free exploit. By controlling the value of `len` outside of the allocate and freeing functions, we can allocate a memory space that is already in use - causing heap instability that can allow us to control the memory

# 4