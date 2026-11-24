from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_expanded=0, nodes_generated=1,
                                max_frontier_size=1, depth=initial.cost)

        frontier = deque([initial])
        visited = {initial.tiles}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            current = frontier.popleft()
            expanded += 1
            for child in current.neighbors():
                if child.tiles in visited:
                    continue
                generated += 1
                # Na BFS o teste de objetivo na geração já garante a solução ótima.
                if child.is_goal:
                    return SearchResult(solution=child, nodes_expanded=expanded,
                                        nodes_generated=generated,
                                        max_frontier_size=max_frontier, depth=child.cost)
                visited.add(child.tiles)
                frontier.append(child)
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(solution=None, nodes_expanded=expanded,
                            nodes_generated=generated, max_frontier_size=max_frontier)
