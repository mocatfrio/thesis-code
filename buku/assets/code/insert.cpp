Node* insert(Node* r, char s[]) {
  Node* x = build(s, s + strlen(s));
  return concate(r, x);
}