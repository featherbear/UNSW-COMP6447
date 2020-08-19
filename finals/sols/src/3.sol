wow.. a lot of vulns here.

easy vuln: Use after free in read/write functions, since theres no check on a free.

hard vuln: allocate() increments len even if it fails, so it will eventually overflow, and continue to let you allocate chunks.
