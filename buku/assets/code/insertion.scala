def Insertion(node: Node, newObject: NewObject, 
    distance: Double) {
  val newMBR = newObject.getMBR()
  val overlappedObjects = getPDRObjects(node, newMBR)

  newObject.points.foreach(p => node.tree.add(p))

  val updateObjects = overlappedObjects.map { q =>
    val qMBR = q.getMBR()
    
    if (newMBR.contains(qMBR)) {
      q.asImpossible
    } else {
      val prob = computeDominationProb(node.swtree, q.id)
      if (prob > (1 - P_THRESHOLD) {
        q.asImpossible
      } else {
        val skyProb = computeSkylineProb(node.swtree, q)
        q.updateSkyProb(skyProb)
      }
    }
  }

  val skyProb = 
    computeSkylineProb(node.swtree, newObject.id)
  val newObject =
    new Object(newObject, distance, skyProb)
  updatedObjects += newObject
  node.updateObjects(updatedObjects)
}
