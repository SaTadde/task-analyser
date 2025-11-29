def detect_cycle(tasks):
    # Build adjacency list
    graph = {t["title"]: t.get("dependencies", []) for t in tasks}

    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:
            return True  # cycle exists
        
        if node in visited:
            return False

        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        recursion_stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            return True

    return False
