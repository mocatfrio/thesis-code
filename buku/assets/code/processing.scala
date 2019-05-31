def Processing(grid, object) {
  val Q = Queue[NodeQueue]()
  val Gr = new Graph()
  val visitedNodes = Set[Int]()
  
  val edge = getEdgeEnclosing(object)
  val nodeI = grid.getNode(edge.i)
  val nodeJ = grid.getNode(edge.j)
  
  val gridNodeI = grid.getGridEnclosingNode(nodeI)
  val gridNodeJ = grid.getGridEnclosingNode(nodeJ)
  
  Gr.insertGrid(gridNodeI)
  if (gridNodeI != gridNodeJ) Gr.insertGrid(gridNodeJ)

  val distanceNodeI = grid.getDistance(object, nodeI)
  val distanceNodeJ = grid.getDistance(object, nodeJ)
  
  Q.enqueue(NodeQueue(nodeI.id, distanceNodeI))
  visitedNodes = visitedNodes + nodei.id

  Q.enqueue(NodeQueue(nodeJ.id, distanceNodeJ))
  visitedNodes = visitedNodes + nodej.id

  while (Q.nonEmpty) {
    Q = Q.sortBy(_.distance)
    val NodeQueue(currentNodeId, distance) = Q.dequeue()

    if (distance < D_EPSILON) {
      if (!visitedNodes.contains(node.id)) {
        val dataGrid = 
          grid.getGridEnclosingNode(currentNodeId)
        Gr.insertGrid(dataGrid)
      }

      val currentNode =
        tempGraph.getNode(currentNodeId).get

      val updatedNode = object match {
        case newObject@NewObject=>
          Insertion(currentNode, newObject, distance)
        case ExpiredObject(objectId) =>
          Insertion(currentNode, objectId)
      }

      Gr.updateNode(updatedNode)
      grid.updateNode(updatedNode)

      val neighbors = Gr.getNeighbor(currentNodeId)

      neighbors.keys.foreach { node =>
        val distanceUnvisitedNode = 
          distance + neighborNodesEdges(n)
        Q.enqueue(
          NodeQueue(n.id, distanceUnvisitedNode)
        )

        visitedNodes += n.id
      }
    }
  }

  Gr.edges.filter(e => e.isUpdated)
    .foreach { edge => 
      val nodeS = graph.getNodeS(edge)
      val nodeE = graph.getNodeE(edge)

      val landmarks =
        determineLandmark(nodeS, edge, nodeE)
      val turningPoints =
        determineTurningPoints(landmarks, edge)
  }

  grid
}
