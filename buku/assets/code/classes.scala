case class NewObject(
  id: Int,
  edgeId: Int,
  points: List[Rect2d]
)

case class Object(
  id: Int,
  edgeId: Int,
  skyProb: Double,
  isImpossible: Boolean,
  nodeId: Int,
  rect: Rect2d,
  distance: Double,
  position: Double
)

case class Node(
  id: Int,
  x: Double,
  y: Double,
  swtree: RTree[Point2d],
  objects: Set[Object]
)

case class Edge(
  id: Int,
  i: Int,
  j: Int,
  length: Double,
  objects: Set[Object]
)

class Grid {
  var edges: Set[Edges] = Set()
  var nodes: Set[Nodes] = Set()
  var newObjects: Set[NewObject] = Set()
}

class Gr {
  var graph: Graph[Int, WLkUnDiEdge] = Graph()
  var nodes: mutable.Map[Int, Node] = mutable.Map()
  var edges: mutable.Map[Int, Edge] = mutable.Map()
}

case class TurningPoint(dStart: Double, 
  dEnd: Double, SP: Set[Object])

trait Landmark {
  val objectId: Int,
  val distance: Double
}


