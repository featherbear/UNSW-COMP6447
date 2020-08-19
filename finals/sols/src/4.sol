Buffer of size 512 (structs) is allocated and zero'd out.
  assert(totalLen >= 0);
  assert(totalLen <= 512);
  struct xml_string **buffer =
      (struct xml_string **)calloc(sizeof(struct xml_string *), 512);

If you enter 512 structs, this array is *not* Null terminated. So this function has an information leak, and will print out the whole stack if you enter 512 xml nodes.
  for (struct xml_string **start = find_all_htmls(root); *start != NULL;
       start++) {
    struct xml_node *curr = *start;
    printf("%s\n", curr);
  }
