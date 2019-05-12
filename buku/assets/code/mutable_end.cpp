Node* mutable_end(Node* r, int x, int len) {
  pair<Node*, Node*> fir = split(r, x);
  pair<Node*, Node*> sec = split(fir.second, len);
  return concate(concate(fir.first, sec.second),\
   sec.first);
}