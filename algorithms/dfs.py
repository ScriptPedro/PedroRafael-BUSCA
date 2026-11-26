from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        stack = [initial]
        # Menor custo com que cada estado já foi alcançado; permite revisitar
        # um estado apenas se ele surgir por um caminho mais curto.
        best_cost = {initial.tiles: 0}
        expanded = 0
        generated = 1
        max_frontier = 1

        while stack:
            current = stack.pop()
            if current.is_goal:
                return SearchResult(solution=current, nodes_expanded=expanded,
                                    nodes_generated=generated,
                                    max_frontier_size=max_frontier, depth=current.cost)
            if current.cost >= self.depth_limit:
                continue
            expanded += 1
            # reversed() para explorar os filhos na ordem em que neighbors() os gera.
            for child in reversed(current.neighbors()):
                known = best_cost.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_cost[child.tiles] = child.cost
                generated += 1
                stack.append(child)
            max_frontier = max(max_frontier, len(stack))

        return SearchResult(solution=None, nodes_expanded=expanded,
                            nodes_generated=generated, max_frontier_size=max_frontier)
