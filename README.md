# 🏭 생산 스케줄링 + 이산사건 시뮬레이션 통합 최적화

## 📌 프로젝트 개요
본 프로젝트는 **유전 알고리즘(Genetic Algorithm)** 기반의 스케줄링 엔진과  
SimPy 기반 이산사건 시뮬레이션(Discrete Event Simulation)을 결합하여,  
생산 계획을 자동으로 생성하고 → 시뮬레이션으로 실행 → KPI를 평가 → 스케줄을 개선하는  
**스케줄링–시뮬레이션 통합 최적화 구조**를 구현하는 것을 목표로 합니다.

이는 실제 제조 현장에서 자주 수행되는 “스케줄 → 시뮬레이션 → 검증” PoC 구조를 모사한 것으로,  
단순 계산 기반 스케줄링에 비해 **공정 병목·대기 시간·자원 활용도를 현실적으로 반영한 스케줄**을 도출할 수 있습니다.

---

## 🧠 문제 정의

| 항목 | 값 |
|------|-----|
| Job 수 | 20개 |
| Machine 수 | 5개 |
| Routing | Job마다 Machine 순서 다름 (Job Shop) |
| 처리 시간 | 2~10 사이 정수 랜덤 |
| 목표 | Makespan 최소화, Throughput 향상 |
| 제약 | 공정 대기, Idle Time, 병목 발생 가능 |

각 Job은 서로 다른 공정 순서(Routing)와 처리시간을 가지고 있으며, GA는 Job 실행 순서를 최적화합니다.  
SimPy 시뮬레이터는 해당 순서를 받아 Job-Shop 이벤트를 실행하고, makespan과 throughput을 계산해 GA의 fitness로 활용합니다.

---

## ⚙️ 기술 스택

- Python 3.x  
- **SimPy** — 이산사건 시뮬레이션 엔진  
- **DEAP** — Genetic Algorithm 라이브러리  
- Numpy / Pandas — 데이터 처리 및 KPI 계산

---

## 🏗 시스템 구성

```text
┌───────────────────────────┐
│ GA Scheduling Engine      │
│  - Job 순서 최적화       │
│  - Crossover & Mutation   │
└───────────────┬───────────┘
                │
                ▼
┌───────────────────────────┐
│ SimPy DES Simulator       │
│  - Routing & Processing   │
│  - Resource 모델링       │
│  - Event 기반 실행      │
└───────────────┬───────────┘
                │
                ▼
┌───────────────────────────┐
│ KPI Calculation          │
│  - Makespan              │
│  - Throughput            │
└───────────────┬───────────┘
                │
                ▼
┌───────────────────────────┐
│ GA Fitness Update        │
└───────────────────────────┘
'''

---

## 📂 파일 설명

| 파일명 | 설명 |
|--------|------|
| **scheduler.py** | GA 기반 Job-Shop 스케줄 생성 알고리즘. Job 순서를 개체로 표현하고 crossover·mutation으로 진화 수행. |
| **simulator.py** | SimPy 기반 생산 라인 DES 시뮬레이터. Job 순서와 Routing 정보를 받아 이벤트 시뮬레이션을 수행하고 KPI 계산. |
| **main.py** | 전체 파이프라인 실행. 초기 랜덤 스케줄과 GA 최적 스케줄을 비교하여 전후 KPI를 출력. |

---

## 🧪 실험 결과

30세대 GA 최적화 수행 결과, **초기 랜덤 스케줄 대비 Makespan이 단축되고 Throughput이 증가**했습니다.

### 📈 전후 성능 비교

| 항목 | 초기 랜덤 스케줄 | GA 최적화 스케줄 | 개선 |
|------|-----------------|-------------------|------|
| Makespan | 122.00 | 118.00 | ↓ 4.00 |
| Throughput | 0.165 | 0.170 | ↑ 약 3% |

유전 알고리즘 기반 스케줄링 엔진이 단순 랜덤 스케줄에 비해 **생산 일정을 더 효율적으로 재배치**하여,  
Makespan을 단축하고 Throughput을 향상시켰습니다.  
이는 DES 시뮬레이션으로 병목 및 대기 시간을 현실적으로 반영했기 때문에 가능한 결과입니다.

---

## 📝 요약

| 항목 | 내용 |
|------|------|
| 최적화 대상 | Job 순서 (Job-Shop Scheduling) |
| 알고리즘 | Genetic Algorithm (DEAP) |
| 시뮬레이션 | SimPy 기반 DES |
| 목표 | Makespan 최소화, Throughput 향상 |
| 성능 개선 | Makespan 4 감소, Throughput 약 3% 증가 |

---

## 💡 확장 아이디어

- Multi-objective GA(NSGA-II)로 Makespan과 WIP 동시 최적화  
- Setup time, Blocking/Starvation 추가하여 현실적 Job-Shop 모델 구성  
- PPO/DQN 기반 Dispatching Rule 학습으로 GA 대체  
- Plant Simulation + Python 연동으로 실제 Digital Twin 수준으로 확장

---

## 📚 참고
- [SimPy Documentation](https://simpy.readthedocs.io/en/latest/)  
- [DEAP: Distributed Evolutionary Algorithms in Python](https://deap.readthedocs.io/en/master/)  
- 제조 스케줄링 × 시뮬레이션 통합 최적화 관련 연구: Pinedo (2016), *Scheduling: Theory, Algorithms, and Systems*

