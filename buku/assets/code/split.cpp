pair<Node*, Node*> split(Node* r, int pos) {
  Node *R1 = 0, *R2 = 0;
  if ( !r ) return make_pair(R1, R2);
  int idx = getSize(r->left);
  if ( idx < pos ) {
    pair<Node*, Node*> temp =\
     split(r->right, pos - idx - 1);
    r->right = temp.first;
    R2 = temp.second;
    R1 = r;
  } else {
    pair<Node*, Node*> temp = split(r->left, pos);
    R1 = temp.first;
    r->left = temp.second;
    R2 = r;
  }
  r->update();
  return make_pair(R1, R2);
}