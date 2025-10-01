import random
from deap import base, creator, tools
import numpy as np

# ==========================
# Job-Shop 기본 설정
# ==========================
N_JOBS = 20
N_MACHINES = 5

# 각 Job별 Machine 처리 순서와 처리 시간 랜덤 생성 (예시)
# 실제 환경에서는 공정 라우팅/시간 테이블을 불러와도 됨
ROUTINGS = [np.random.permutation(N_MACHINES).tolist() for _ in range(N_JOBS)]
PROCESS_TIMES = np.random.randint(2, 10, size=(N_JOBS, N_MACHINES))

# ==========================
# GA 초기 설정
# ==========================
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Makespan 최소화
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
# 개체: Job 실행 순서를 나타내는 길이 N_JOBS의 permutation
toolbox.register("indices", random.sample, range(N_JOBS), N_JOBS)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# ==========================
# 평가 함수: Simulator 결과 기반
# ==========================
def evaluate_schedule(individual, simulator_func):
    """
    individual: job 실행 순서
    simulator_func: 스케줄을 받아 DES 시뮬레이션 후 KPI 반환하는 함수
    """
    kpis = simulator_func(individual, ROUTINGS, PROCESS_TIMES)
    return (kpis["makespan"],)   # 최소화 대상

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def run_ga(simulator_func, n_gen=20, pop_size=30):
    toolbox.register("evaluate", evaluate_schedule, simulator_func=simulator_func)
    pop = toolbox.population(n=pop_size)

    for gen in range(n_gen):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Crossover & Mutation
        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.7:
                toolbox.mate(c1, c2)
                del c1.fitness.values
                del c2.fitness.values

        for mut in offspring:
            if random.random() < 0.3:
                toolbox.mutate(mut)
                del mut.fitness.values

        # Evaluate
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid)
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        best = tools.selBest(pop, 1)[0]
        print(f"[Gen {gen}] Best makespan: {best.fitness.values[0]:.2f}")

    return tools.selBest(pop, 1)[0]
