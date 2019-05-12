char print(Node* r, int pos) {
  int idx = getSize(r->left);
  if ( idx == pos ) return r->value;
  if ( pos <= idx ) return print(r->left, pos);
  else return print(r->right, pos - idx - 1);
}