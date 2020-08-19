  header_size + len > 32 -> Vulnerable to int overflow, len can be massive and pass this.
