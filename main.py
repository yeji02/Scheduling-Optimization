from scheduler import run_ga
from simulator import simulate_schedule

import random
from scheduler import run_ga, ROUTINGS, PROCESS_TIMES
from simulator import simulate_schedule

if __name__ == "__main__":
    print("=== 생산 스케줄링 + DES 시뮬레이션 통합 최적화 ===")

    # -----------------------------
    # 1. 초기 랜덤 스케줄 평가
    # -----------------------------
    random_schedule = random.sample(range(len(ROUTINGS)), len(ROUTINGS))
    kpi_before = simulate_schedule(random_schedule, ROUTINGS, PROCESS_TIMES)
    print("\n[초기 랜덤 스케줄 KPI]")
    for k, v in kpi_before.items():
        print(f"{k}: {v:.2f}")

    # -----------------------------
    # 2. GA 기반 최적화 실행
    # -----------------------------
    best_schedule = run_ga(
        simulator_func=simulate_schedule,
        n_gen=80,        # 세대 수 증가
        pop_size=60      # population 증가
    )

    kpi_after = simulate_schedule(best_schedule, ROUTINGS, PROCESS_TIMES)

    print("\n[GA 최적 스케줄 순서]")
    print(best_schedule)

    print("\n[GA 최적화 후 KPI]")
    for k, v in kpi_after.items():
        print(f"{k}: {v:.2f}")

    # -----------------------------
    # 3. 결과 비교
    # -----------------------------
    print("\n=== 전후 비교 결과 ===")
    print(f"Makespan: {kpi_before['makespan']:.2f} → {kpi_after['makespan']:.2f}")
    print(f"Throughput: {kpi_before['throughput']:.3f} → {kpi_after['throughput']:.3f}")