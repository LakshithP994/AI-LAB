import itertools

def cost(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def neighbors(state):
    n = len(state)
    result = []
    for i, j in itertools.combinations(range(n), 2):
        new_state = state.copy()
        new_state[i], new_state[j] = new_state[j], new_state[i]
        result.append(((i, j), new_state))
    return result

def hill_climb(initial_state):
    current = initial_state
    step = 0
    print(f"Step {step}: {current}, Cost = {cost(current)}")
    while True:
        step += 1
        neighs = neighbors(current)
        costs = [(swap, s, cost(s)) for swap, s in neighs]
        min_cost = min(c[2] for c in costs)
        best_neighbors = [c for c in costs if c[2] == min_cost]
        best_neighbors.sort(key=lambda x: (x[0][0], x[0][1]))
        best_swap, best_state, best_cost = best_neighbors[0]
        print(f"  Neighbors and costs:")
        for swap, s, c in costs:
            print(f"    Swap {swap}: {s}, Cost = {c}")
        if best_cost < cost(current):
            print(f"--> Swap {best_swap} -> {best_state}, Cost = {best_cost}")
            current = best_state
        else:
            print(f"No better neighbor found. Terminated at {current} with Cost = {cost(current)}")
            break
    print("\nGoal State:", current)
    return current

initial = [3, 1, 2, 0]
hill_climb(initial)
