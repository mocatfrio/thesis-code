def determineTurningPoints(landmarks: Set[Landmark], 
  edge: Edge, nodeS: Edge) = Vector[TurningPoint] {
  val queue = landmarks.toSeq.sortBy(_.distance)

  var currentSP = nodeS.getSP()

  var dStart: Double = 0
  val dEnd: Double = edge.length

  var turningPointList = Vector[TurningPoint]()

  while (queue.nonEmpty) {
    val landmark = queue.dequeue

    landmark match {
      case _: LandmarkLeft =>
        if (!isLandMidDomExists(queue, landmark)) {
          val tp = TurningPoint(dStart,
            landmark.distance, currentSP)
          turningPointList :+= tp

          dStart = landmark.distance
          currentSP += landmark.object
        }
      case _: LandmarkRight =>
        if (isObjectInCurrentSP(SP, landmark.object)) {
          val tp = TurningPoint(dStart, 
            landmark.distance, currentSP)
          turningPointList :-= tp

          dStart = landmark.distance
          currentSP -= landmark.object
        }
      case _: LandmarkLeftMid =>
        if (isObjectInCurrentSP(SP, landmark.objectDom) &
          isObjectInCurrentSP(SP, landmark.object)) {
          val tp = TurningPoint(dStart, 
            landmark.distance, currentSP)
          turningPointList = turningPointList :+ tp

          dStart = landmark.distance
          currentSP -= landmark.objDominated
        }
      case _ =>
        if (isLandMidDomExists(queue, landmark)) {
          val tp = TP(dStart, 
            landmark.distance, currentSP)
          turningPointList :+= tp

          dStart = landmark.distance
          currentSP += landmark.objDominated
        }
    }
  }

  turningPointList
}