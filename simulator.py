import simpy
import numpy as np

def job_process(env, job_id, routing, process_times, machines, start_event, log):
    """Job 1개에 대한 처리 프로세스"""
    yield start_event  # 모든 Job 동시 시작 (0초부터)
    for stage, machine_id in enumerate(routing):
        machine = machines[machine_id]
        with machine.request() as req:
            yield req
            t_proc = process_times[job_id, machine_id]
            yield env.timeout(t_proc)
            log.append((job_id, machine_id, env.now))

def simulate_schedule(schedule, routings, process_times):
    """
    schedule: job 실행 순서 (GA로 생성됨)
    routings: 각 job의 공정 순서 리스트
    process_times: 처리시간 테이블
    """
    env = simpy.Environment()
    n_machines = process_times.shape[1]
    machines = [simpy.Resource(env, capacity=1) for _ in range(n_machines)]

    log = []
    start_event = env.event()

    # Job 생성 (GA 순서대로 투입)
    for i, job_id in enumerate(schedule):
        routing = routings[job_id]
        env.process(job_process(env, job_id, routing, process_times, machines, start_event, log))

    # 동시에 시작
    env.timeout(0)
    start_event.succeed()

    env.run()

    # KPI 계산
    makespan = max([t for _, _, t in log]) if log else 0
    throughput = len(schedule) / makespan if makespan > 0 else 0
    return {"makespan": makespan, "throughput": throughput, "n_jobs": len(schedule)}
