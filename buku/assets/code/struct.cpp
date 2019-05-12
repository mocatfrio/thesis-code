struct Node {
  Node *left, *right;
  int size;
  char value; 
  Node(char v) {
    left = right = 0;
    size = 1;
    value = v;
  }

  Node* update() {
    size = 1;
    if ( left ) size += left->size;
    if ( right ) size += right->size;
    return this;
  }
};