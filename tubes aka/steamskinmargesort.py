import pandas as pd
import time
import matplotlib.pyplot as plt

# Recursive Merge Sort
def merge_sort_recursive(data, column):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        merge_sort_recursive(left_half, column)
        merge_sort_recursive(right_half, column)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i][column] < right_half[j][column]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1

# Iterative Merge Sort
def merge_sort_iterative(data, column):
    width = 1
    n = len(data)

    while width < n:
        for i in range(0, n, 2 * width):
            left = data[i:i + width]
            right = data[i + width:i + 2 * width]
            
            merged = []
            l_idx = r_idx = 0
            while l_idx < len(left) and r_idx < len(right):
                if left[l_idx][column] < right[r_idx][column]:
                    merged.append(left[l_idx])
                    l_idx += 1
                else:
                    merged.append(right[r_idx])
                    r_idx += 1
            merged.extend(left[l_idx:] + right[r_idx:])

            data[i:i + 2 * width] = merged

        width *= 2

# Load and process multiple CSV files
file_paths = [
    '200.csv',
    '150.csv',
    'sample_5000_ak47.csv'
]

recursive_times = []
iterative_times = []
data_sizes = []

for file_path in file_paths:
    try:
        print(f"Processing file: {file_path}")
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist. Skipping.")
        continue

    if 'Skin Name' not in data.columns or 'Quantity' not in data.columns:
        print(f"Error: Required columns 'Skin Name' or 'Quantity' are missing in the file '{file_path}'. Skipping.")
        continue

    data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce').fillna(0)

    if data.empty:
        print(f"Warning: The file '{file_path}' is empty after preprocessing. Skipping.")
        continue

    data_list_recursive = data.to_dict(orient='records')
    data_list_iterative = data.to_dict(orient='records')

    print(f"Data size: {len(data)} rows")

    # Measure Recursive Merge Sort Time
    start_time_recursive = time.time()
    try:
        merge_sort_recursive(data_list_recursive, 'Quantity')
    except Exception as e:
        print(f"Error during recursive merge sort: {e}")
        continue
    time_recursive = time.time() - start_time_recursive
    recursive_times.append(time_recursive)

    # Measure Iterative Merge Sort Time
    start_time_iterative = time.time()
    try:
        merge_sort_iterative(data_list_iterative, 'Quantity')
    except Exception as e:
        print(f"Error during iterative merge sort: {e}")
        continue
    time_iterative = time.time() - start_time_iterative
    iterative_times.append(time_iterative)

    data_sizes.append(len(data))

# Plot time comparison
if data_sizes:
    plt.figure(figsize=(10, 6))
    plt.plot(data_sizes, recursive_times, label="Recursive Merge Sort", marker="o")
    plt.plot(data_sizes, iterative_times, label="Iterative Merge Sort", marker="o")

    plt.title("Perbandingan Waktu Eksekusi Merge Sort Rekursif dan Iteratif")
    plt.xlabel("Jumlah Data")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("No valid data to plot.")
