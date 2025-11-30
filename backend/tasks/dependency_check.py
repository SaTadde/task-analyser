def detect_cycle(tasks):
    graph = {}
    for t in tasks:
        graph[t["title"]] = t.get("dependencies", [])

    visited = set()
    stack = set()
    cycle_path = []

    def dfs(node):
        if node in stack:
            cycle_path.append(node)
            return True

        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dfs(dep):
                cycle_path.append(node)
                return True

        stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            cycle_path.reverse()
            return True, cycle_path

    return False, []
