Node* newnode(char c, Node* left, Node* right) {
  Node* r = new Node(c);
  r->left = left;
  r->right = right;
  r->update();
  return r;
}