int main() {
  char st[N];
  scanf("%s", st);
  Node* root = 0;
  int Q, type;
  root = insert(root, st);
  scanf("%d", &Q);
  while ( Q-- ) {
    int x, y;
    scanf("%d", &type);
    if (type == 3) {
      scanf("%d", &y);
      printf("%c\n", print(root, y));
    } else {
      scanf("%d%d", &x, &y);
      if(type == 1) {
        root = mutable_begin(root, x, y - x + 1);
      } else {
        root = mutable_end(root, x, y - x + 1);
      }
    }
  }
  return 0;
}