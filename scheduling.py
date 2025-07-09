#20204017 이상혁 운영체제 CPU 스케줄링 코드
import os

# 프로세스 클래스 정의
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=None):
        self.pid = pid  # 프로세스 ID
        self.arrival_time = arrival_time  # 도착 시간
        self.burst_time = burst_time  # 실행 시간
        self.remaining_time = burst_time  # 남은 실행 시간
        self.priority = priority  # 우선순위
        self.waiting_time = 0  # 대기 시간
        self.turnaround_time = 0  # 반환 시간
        self.response_time = -1  # 응답 시간

# FCFS 스케줄링 알고리즘
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # 도착 시간으로 정렬
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    gantt_chart = []

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        gantt_chart.append((current_time, process.pid, process.burst_time))  # 간트 차트에 추가
        process.response_time = current_time - process.arrival_time  # 응답 시간 계산
        process.waiting_time = current_time - process.arrival_time  # 대기 시간 계산
        current_time += process.burst_time  # 현재 시간 업데이트
        process.turnaround_time = current_time - process.arrival_time  # 반환 시간 계산
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
        total_response_time += process.response_time

    avg_waiting_time = total_waiting_time / len(processes)  # 평균 대기 시간 계산
    avg_turnaround_time = total_turnaround_time / len(processes)  # 평균 반환 시간 계산
    avg_response_time = total_response_time / len(processes)  # 평균 응답 시간 계산

    return avg_waiting_time, avg_turnaround_time, avg_response_time, processes, gantt_chart

# SJF 스케줄링 알고리즘
def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))  # 도착 시간과 실행 시간으로 정렬
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []
    gantt_chart = []

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= current_time]  # 도착한 프로세스 선택
        if arrived_processes:
            shortest_process = min(arrived_processes, key=lambda x: x.burst_time)  # 가장 짧은 실행 시간을 가진 프로세스 선택
            processes.remove(shortest_process)
            if current_time < shortest_process.arrival_time:
                current_time = shortest_process.arrival_time
            gantt_chart.append((current_time, shortest_process.pid, shortest_process.burst_time))  # 간트 차트에 추가
            shortest_process.response_time = current_time - shortest_process.arrival_time  # 응답 시간 계산
            shortest_process.waiting_time = current_time - shortest_process.arrival_time  # 대기 시간 계산
            current_time += shortest_process.burst_time  # 현재 시간 업데이트
            shortest_process.turnaround_time = current_time - shortest_process.arrival_time  # 반환 시간 계산
            completed_processes.append(shortest_process)
            total_waiting_time += shortest_process.waiting_time
            total_turnaround_time += shortest_process.turnaround_time
            total_response_time += shortest_process.response_time
        else:
            current_time += 1  # 도착한 프로세스가 없으면 시간 증가

    avg_waiting_time = total_waiting_time / len(completed_processes)  # 평균 대기 시간 계산
    avg_turnaround_time = total_turnaround_time / len(completed_processes)  # 평균 반환 시간 계산
    avg_response_time = total_response_time / len(completed_processes)  # 평균 응답 시간 계산

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# 우선순위 스케줄링 (비선점형) 알고리즘
def priority_scheduling_non_preemptive(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))  # 도착 시간과 우선순위로 정렬
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []
    gantt_chart = []

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= current_time]  # 도착한 프로세스 선택
        if arrived_processes:
            highest_priority_process = min(arrived_processes, key=lambda x: x.priority)  # 가장 높은 우선순위를 가진 프로세스 선택
            processes.remove(highest_priority_process)
            if current_time < highest_priority_process.arrival_time:
                current_time = highest_priority_process.arrival_time
            gantt_chart.append((current_time, highest_priority_process.pid, highest_priority_process.burst_time))  # 간트 차트에 추가
            highest_priority_process.response_time = current_time - highest_priority_process.arrival_time  # 응답 시간 계산
            highest_priority_process.waiting_time = current_time - highest_priority_process.arrival_time  # 대기 시간 계산
            current_time += highest_priority_process.burst_time  # 현재 시간 업데이트
            highest_priority_process.turnaround_time = current_time - highest_priority_process.arrival_time  # 반환 시간 계산
            completed_processes.append(highest_priority_process)
            total_waiting_time += highest_priority_process.waiting_time
            total_turnaround_time += highest_priority_process.turnaround_time
            total_response_time += highest_priority_process.response_time
        else:
            current_time += 1  # 도착한 프로세스가 없으면 시간 증가

    avg_waiting_time = total_waiting_time / len(completed_processes)  # 평균 대기 시간 계산
    avg_turnaround_time = total_turnaround_time / len(completed_processes)  # 평균 반환 시간 계산
    avg_response_time = total_response_time / len(completed_processes)  # 평균 응답 시간 계산

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# 우선순위 스케줄링 (선점형) 알고리즘
def priority_scheduling_preemptive(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))  # 도착 시간과 우선순위로 정렬
    current_time = 0
    ready_queue = []
    gantt_chart = []
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []

    while processes or ready_queue:
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))  # 우선순위와 도착 시간으로 정렬
            current_process = ready_queue.pop(0)
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time  # 첫 응답 시간 계산
            if gantt_chart and gantt_chart[-1][1] == current_process.pid:
                gantt_chart[-1] = (gantt_chart[-1][0], current_process.pid, gantt_chart[-1][2] + 1)  # 간트 차트 업데이트
            else:
                gantt_chart.append((current_time, current_process.pid, 1))  # 간트 차트에 추가
            current_process.remaining_time -= 1  # 남은 실행 시간 감소
            current_time += 1  # 현재 시간 증가
            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time  # 반환 시간 계산
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time  # 대기 시간 계산
                completed_processes.append(current_process)
                total_waiting_time += current_process.waiting_time
                total_turnaround_time += current_process.turnaround_time
                total_response_time += current_process.response_time
            else:
                ready_queue.append(current_process)  # 아직 완료되지 않은 프로세스를 다시 큐에 추가
        else:
            current_time += 1  # 도착한 프로세스가 없으면 시간 증가

    avg_waiting_time = total_waiting_time / len(completed_processes)  # 평균 대기 시간 계산
    avg_turnaround_time = total_turnaround_time / len(completed_processes)  # 평균 반환 시간 계산
    avg_response_time = total_response_time / len(completed_processes)  # 평균 응답 시간 계산

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# 라운드 로빈 스케줄링 알고리즘
def round_robin_scheduling(processes, time_quantum):
    current_time = 0
    ready_queue = []
    gantt_chart = []
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []
    processes_dict = {process.pid: process for process in processes}

    processes.sort(key=lambda x: x.arrival_time)
    ready_queue.append(processes.pop(0))

    while ready_queue or processes:
        if ready_queue:
            current_process = ready_queue.pop(0)
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time

            time_slice = min(current_process.remaining_time, time_quantum)
            gantt_chart.append((current_time, current_process.pid, time_slice))
            current_time += time_slice
            current_process.remaining_time -= time_slice

            while processes and processes[0].arrival_time <= current_time:
                ready_queue.append(processes.pop(0))

            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                total_waiting_time += current_process.waiting_time
                total_turnaround_time += current_process.turnaround_time
                total_response_time += current_process.response_time
                completed_processes.append(current_process)
            else:
                ready_queue.append(current_process)

        elif processes:
            current_time = processes[0].arrival_time
            ready_queue.append(processes.pop(0))

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)
    avg_response_time = total_response_time / len(completed_processes)

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# HRN 스케줄링 알고리즘
def hrn_scheduling(processes):
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []
    gantt_chart = []

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= current_time]
        if arrived_processes:
            for process in arrived_processes:
                process.priority = 1 + (current_time - process.arrival_time) / process.burst_time
            highest_priority_process = max(arrived_processes, key=lambda x: x.priority)
            processes.remove(highest_priority_process)
            if current_time < highest_priority_process.arrival_time:
                current_time = highest_priority_process.arrival_time
            gantt_chart.append((current_time, highest_priority_process.pid, highest_priority_process.burst_time))
            highest_priority_process.response_time = current_time - highest_priority_process.arrival_time
            highest_priority_process.waiting_time = current_time - highest_priority_process.arrival_time
            current_time += highest_priority_process.burst_time
            highest_priority_process.turnaround_time = current_time - highest_priority_process.arrival_time
            completed_processes.append(highest_priority_process)
            total_waiting_time += highest_priority_process.waiting_time
            total_turnaround_time += highest_priority_process.turnaround_time
            total_response_time += highest_priority_process.response_time
        else:
            current_time += 1

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)
    avg_response_time = total_response_time / len(completed_processes)

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# SRT 스케줄링 알고리즘
def srt_scheduling(processes, time_quantum):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    ready_queue = []
    gantt_chart = []
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    completed_processes = []

    while processes or ready_queue:
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
            current_process = ready_queue.pop(0)
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time
            time_slice = min(current_process.remaining_time, time_quantum)
            gantt_chart.append((current_time, current_process.pid, time_slice))
            current_time += time_slice
            current_process.remaining_time -= time_slice
            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed_processes.append(current_process)
                total_waiting_time += current_process.waiting_time
                total_turnaround_time += current_process.turnaround_time
                total_response_time += current_process.response_time
            else:
                ready_queue.append(current_process)
        else:
            current_time += 1

    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)
    avg_response_time = total_response_time / len(completed_processes)

    return avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart

# 간트 차트를 출력하는 함수
def print_gantt_chart(gantt_chart):
    chart_str = "간트 차트:\n"
    for start_time, pid, duration in gantt_chart:
        chart_str += f"| {start_time} P{pid} ({duration}) "
    chart_str += f"| {gantt_chart[-1][0] + gantt_chart[-1][2]}\n"
    print(chart_str)

# 각 프로세스의 대기 시간, 반환 시간, 응답 시간을 출력하는 함수
def print_times(processes, avg_waiting_time, avg_turnaround_time, avg_response_time):
    times_str = "\n각 프로세스별 대기 시간:\n"
    for process in processes:
        times_str += f"P{process.pid}: 대기 시간={process.waiting_time}\n"

    times_str += f"\n평균 대기 시간: {avg_waiting_time:.2f}\n"

    times_str += "\n각 프로세스별 응답 시간:\n"
    for process in processes:
        times_str += f"P{process.pid}: 응답 시간={process.response_time}\n"

    times_str += f"\n평균 응답 시간: {avg_response_time:.2f}\n"

    times_str += "\n각 프로세스별 반환 시간:\n"
    for process in processes:
        times_str += f"P{process.pid}: 반환 시간={process.turnaround_time}\n"

    times_str += f"\n평균 반환 시간: {avg_turnaround_time:.2f}\n"

    print(times_str)

# 선택한 스케줄링 알고리즘을 실행하는 함수
def run_scheduling(algorithm, processes, time_quantum=None):
    if algorithm == "FCFS":
        return fcfs_scheduling(processes)
    elif algorithm == "SJF":
        return sjf_scheduling(processes)
    elif algorithm == "Priority (Non-preemptive)":
        return priority_scheduling_non_preemptive(processes)
    elif algorithm == "Priority (Preemptive)":
        return priority_scheduling_preemptive(processes)
    elif algorithm == "Round Robin":
        return round_robin_scheduling(processes, time_quantum)
    elif algorithm == "HRN":
        return hrn_scheduling(processes)
    elif algorithm == "SRT":
        return srt_scheduling(processes, time_quantum)
    else:
        raise ValueError("Invalid scheduling algorithm")

# 스케줄링을 시작하는 함수
def start_scheduling():
    while True:
        file_path = "c:/Users/Administrator/vs code/.vscode/processes.txt"  # 파일 경로 설정

        if not os.path.exists(file_path):
            print("파일이 존재하지 않습니다. 올바른 경로를 입력해주세요.")
            return

        with open(file_path, 'r') as file:
            lines = file.readlines()

        num_processes = int(lines[0].strip())
        processes = []
        index = 1

        for i in range(num_processes):
            pid, arrival_time, burst_time, priority = map(int, lines[index].strip().split())
            processes.append(Process(pid, arrival_time, burst_time, priority))
            index += 1

        print("\n스케줄링 알고리즘을 선택하세요:")
        print("1. FCFS (First-Come, First-Served)")
        print("2. SJF (Shortest Job First)")
        print("3. Priority (Non-preemptive)")
        print("4. Priority (Preemptive)")
        print("5. Round Robin")
        print("6. HRN (Highest Response Ratio Next)")
        print("7. SRT (Shortest Remaining Time)")

        choice = int(input("선택: "))
        time_quantum = None

        if choice == 5 or choice == 7:
            time_quantum = int(input("타임 퀀텀을 입력하세요: "))

        algorithm_map = {
            1: "FCFS",
            2: "SJF",
            3: "Priority (Non-preemptive)",
            4: "Priority (Preemptive)",
             5: "Round Robin",
            6: "HRN",
            7: "SRT"
        }

        algorithm_name = algorithm_map.get(choice)
        if not algorithm_name:
            print("잘못된 선택입니다.")
            continue

        avg_waiting_time, avg_turnaround_time, avg_response_time, completed_processes, gantt_chart = run_scheduling(algorithm_name, processes, time_quantum)

        print_gantt_chart(gantt_chart)
        print_times(completed_processes, avg_waiting_time, avg_turnaround_time, avg_response_time)

        if algorithm_name == "HRN":
            print("\nHRN 스케줄링에서 각 프로세스의 우선순위:")
            for process in completed_processes:
                print(f"P{process.pid} -> 우선순위: {process.priority:.2f}")

        next_action = input("\n계속하려면 '계속', 그만하려면 '그만'을 입력하세요: ")
        if next_action.lower() == "그만":
            break

if __name__ == "__main__":
    start_scheduling()
