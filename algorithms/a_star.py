import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

       def heuristic(self, state: State) -> int:
        # Distância de Manhattan de cada peça à sua posição final (ignora o vazio).
        # É admissível: cada movimento desloca uma peça em apenas uma casa.
        total = 0
        for index, value in enumerate(state.tiles):
            if value == 0:
                continue
            goal_index = value - 1
            total += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        counter = 0  # desempate estável na heap (evita comparar State com State)
        frontier = [(self.heuristic(initial), counter, initial)]
        best_cost = {initial.tiles: 0}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)
            # Entrada obsoleta: já existe um caminho melhor para este estado.
            if current.cost > best_cost.get(current.tiles, current.cost):
                continue
            if current.is_goal:
                return SearchResult(solution=current, nodes_expanded=expanded,
                                    nodes_generated=generated,
                                    max_frontier_size=max_frontier, depth=current.cost)
            expanded += 1
            for child in current.neighbors():
                known = best_cost.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_cost[child.tiles] = child.cost
                counter += 1
                generated += 1
                heapq.heappush(frontier, (child.cost + self.heuristic(child), counter, child))
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(solution=None, nodes_expanded=expanded,
                            nodes_generated=generated, max_frontier_size=max_frontier)
