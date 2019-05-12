Node* build(char* start, char* end) {
  if ( start == end ) return NULL;
  char* mid = start + (end - start)/2;
  return newnode(*mid, build(start, mid),\
   build(mid+1, end));
}