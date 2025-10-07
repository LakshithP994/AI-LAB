import random, math

def cost(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def random_neighbor(state):
    n = len(state)
    i, j = random.sample(range(n), 2)
    new_state = state[:]
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def simulated_annealing(n=8, start_temp=100, stop_temp=0.1, alpha=0.99):
    current = [random.randint(0, n - 1) for _ in range(n)]
    current_cost = cost(current)
    T = start_temp
    step = 0
    while T > stop_temp and current_cost != 0:
        step += 1
        neighbor = random_neighbor(current)
        neighbor_cost = cost(neighbor)
        delta = neighbor_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current, current_cost = neighbor, neighbor_cost
        T *= alpha
        print(f"Step {step}: {current}, Cost = {current_cost}, Temp = {T:.3f}")
    print("\nFinal State:", current)
    print("Final Cost:", current_cost)
    return current

simulated_annealing()
