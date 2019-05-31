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

case class NewObject(
  id: Int,
  edgeId: Int,
  points: List[Rect2d]
)

case class ObjectToInsert(
  id: Int,
  edgeId: Int,
  skyProb: Double,
  isImpossible: Boolean,
  nodeId: Int,
  rect: Rect2d,
  distance: Double,
  position: Double
)

trait Landmark {
  val objectId: Int,
  val distance: Double
}

class LandmarkLeft(d: Double, e: Option[Int], oId: Int)
  extends Landmark {
    override val distance: Double = d
    override val edgeId: Option[Int] = e
    override val objId: Int = oId
  }

class LandmarkRight(d: Double, e: Option[Int], oId: Int)
  extends Landmark {
    override val distance: Double = d
    override val edgeId: Option[Int] = e
    override val objId: Int = oId
  }

class LandmarkLeftMid(d: Double, e: Option[Int], oId: Int, odId: Int)
  extends Landmark {
    override val distance: Double = d
    override val edgeId: Option[Int] = e
    override val objId: Int = oId
    val objDominatedId: Int = odId
  }

class LandmarkRightMid(d: Double, e: Option[Int], oId: Int, odId: Int)
  extends Landmark {
    override val distance: Double = d
    override val edgeId: Option[Int] = e
    override val objId: Int = oId
    val objDominatedId: Int = odId
  }

case Grid {
  var edges: Set[Edges] = Set()
  var nodes: Set[Nodes] = Set()
  var newObjects: Set[NewObject] = Set()
}

case Gr {
  var graph: Graph[Int, WLkUnDiEdge] = Graph()
  var nodes: mutable.Map[Int, Node] = mutable.Map()
  var edges: mutable.Map[Int, Edge] = mutable.Map()
}
