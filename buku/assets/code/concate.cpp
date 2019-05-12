Node* concate(Node* R1, Node* R2) {
  if ( !R1 || !R2) return R1 ? R1 : R2;
  if (random(R1->size, R2->size)) {
    R1->right = concate(R1->right, R2);
    return R1->update();
  } else {
    R2->left = concate(R1, R2->left);
    return R2->update();
  }
}