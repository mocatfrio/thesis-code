#include <stdio.h>
#include <cstdlib>
#include <cstring>
#include <utility>

using namespace std;

const int N = 1e5 + 10;

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

inline int getSize(Node* o) {
  return o ? o->size : 0;
}

inline bool random(int a, int b) {
  return rand() % ( a + b ) < a;
}

void inorder(Node* r) {
  if ( r ) {
    printf("ke kiri\n");
    inorder(r->left);
    printf("%c %d\n", r->value, r->size);
    printf("ke kanan\n");
    inorder(r->right);
  }
  return;
}

inline Node* newnode(char c, Node* left, Node* right) {
  Node* r = new Node(c);
  r->left = left;
  r->right = right;
  r->update();
  return r;
}

inline Node* build(char* start, char* end) {
  if ( start == end ) return NULL;
  char* mid = start + (end - start)/2;
  return newnode(*mid, build(start, mid), build(mid+1, end));
}

inline pair<Node*, Node*> split(Node* r, int pos) {
  Node *R1 = 0, *R2 = 0;
  if ( !r ) return make_pair(R1, R2);
  int idx = getSize(r->left);
  if ( idx < pos ) {
    pair<Node*, Node*> temp = split(r->right, pos - idx - 1);
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

inline Node* concate(Node* R1, Node* R2) {
  if ( !R1 || !R2) return R1 ? R1 : R2;
  if (random(R1->size, R2->size)) {
    R1->right = concate(R1->right, R2);
    return R1->update();
  } else {
    R2->left = concate(R1, R2->left);
    return R2->update();
  }
}

inline Node* insert(Node* r, char s[]) {
  Node* x = build(s, s + strlen(s));
  return concate(r, x);
}

inline char print(Node* r, int pos) {
  int idx = getSize(r->left);
  if ( idx == pos ) return r->value;
  if ( pos <= idx ) return print(r->left, pos);
  else return print(r->right, pos - idx - 1);
}

inline Node* mutable_begin(Node* r, int x, int len) {
  pair<Node*, Node*> fir = split(r, x);
  pair<Node*, Node*> sec = split(fir.second, len);
  return concate(sec.first, concate(fir.first, sec.second));
}

inline Node* mutable_end(Node* r, int x, int len) {
  pair<Node*, Node*> fir = split(r, x);
  pair<Node*, Node*> sec = split(fir.second, len);
  return concate(concate(fir.first, sec.second), sec.first);
}

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