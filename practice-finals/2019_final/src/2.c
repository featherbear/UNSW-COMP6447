struct hdr {
    unsigned int l;
    unsigned int type;
};

char *read_packet(int sockfd) {
    int n;
    unsigned int l;
    struct hdr smp_hdr;
    static char buf[1024];

    if(read_all(sockfd, (void *)&smp_hdr, sizeof(smp_hdr)) <= 0) {
        error("Error 0: %m");
        return NULL;
    }

    l = ntohl(smp_hdr.l);
    if(l > (1024 + sizeof (struct hdr) - 1)) {
        error("Error 1.\n");
        return NULL;
    }

    if(read_all(sockfd, buf, l - sizeof(struct hdr)) <= 0) {
        error("Error 2: %m");
        return NULL;
    }

    buf[sizeof(buf)-1] = '\0';
    return strdup(buf);
}

