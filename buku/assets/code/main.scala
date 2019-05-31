val nodes = readDatasetNodes()
val edges = readDatasetEdges()

val grid = new Grid()

grid.insertNodes(nodes)
grid.insertEdges(edges)

val streaming = Set(.....)

stream.foreach { object =>
  grid = Processing(grid, object)
}