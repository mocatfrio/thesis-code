def determineLandmark(nodeS: Node, edge: Edge, 
  nodeE: Node) = Set[Landmark] {
  val spNodeS = nodeS.getSP()
  val spNodeE = nodeE.getSP()
  val sEdge = edge.objects

  val Q = mutable.Queue[Landmark]()

  val landmarkEdge = findLandmarkEdge(sEdge, edge)
  landmarkEdge.foreach { l =>
    Q.enqueue(l)
  }

  val landmarkNodeS = findLandmarkNodeS(sEdge, edge)
  landmarkNodeS.foreach { l =>
    Q.enqueue(l)
  }

  val landmarkNodeE = findLandmarkNodeE(sEdge, edge)
  landmarkNodeE.foreach { l =>
    Q.enqueue(l)
  }

  val landmarkMid = findLandmarkMid(spNodeS, spNodeE,
    sEdge, edge, Q)
  landmarkMid.foreach { l =>
    Q.enqueue(l)
  }

  Q.toSet
}
