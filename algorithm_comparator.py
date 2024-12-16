from datetime import datetime


def compare_algorithms(algorithms, algorithm_names, input_data):
    for i in range(len(algorithms)):
        print(f"Wynik algorytmu {algorithm_names[i]}: W TRAKCIE LICZENIA", end="")
        time_start = datetime.now()
        result = algorithms[i](input_data)
        time_end = datetime.now()
        time_result = round((time_end - time_start).total_seconds() * 1000, 2)
        print("\b" * 18, f"{result} (czas: {time_result} ms)", sep="")
