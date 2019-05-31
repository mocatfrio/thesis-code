def ComputeSkyline(graph: Graph) = Unit {
  graph.edges.foreach { edge => 
    val nodeS = graph.getNodeS(edge)
    val nodeE = graph.getNodeE(edge)

    val landmarks =
      determineLandmark(nodeS, edge, nodeE)
    val turningPoints =
      determineTurningPoints(landmarks, edge)
  }
}