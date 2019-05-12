Node* mutable_begin(Node* r, int x, int len) {
  pair<Node*, Node*> fir = split(r, x);
  pair<Node*, Node*> sec = split(fir.second, len);
  return concate(sec.first, concate(fir.first,\
   sec.second));
}