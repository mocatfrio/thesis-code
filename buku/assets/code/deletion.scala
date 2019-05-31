def Deletion(node: Node, objectId: Int, MBR: Rect2d) {
  val object = node.objects.find(_.id == objectId).get

  object.points.foreach { p => node.swtree.remove(p) }

  val overlappedObjects = getPDRObject(node, MBR)
  val updateObjects = overlappedObjects.map { q =>
    case q@Object(_, _, _, true, _, _, _, _) => q
    case q@Object =>
      val skyProb = computeSkylineProb(node.swtree, q.id)
      q.updateSkyProb(skyProb)
  }
  node.removeObject(objectId)
    .updateObjects(updateObjects)
}
