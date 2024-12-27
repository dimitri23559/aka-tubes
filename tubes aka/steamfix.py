import pandas as pd
import time
import matplotlib.pyplot as plt

# [Previous merge_sort_recursive and merge_sort_iterative functions remain the same]

def linear_search(data, skin_name):
    for item in data:
        if item['Skin Name'].lower() == skin_name.lower():
            return item
    return None

def analyze_performance(file_paths):
    recursive_times = []
    iterative_times = []
    search_times = []
    data_sizes = []

    for file_path in file_paths:
        try:
            data = pd.read_csv(file_path)
            if not {'Skin Name', 'Quantity'}.issubset(data.columns):
                print(f"Error: Required columns missing in {file_path}")
                continue

            data_list = data.to_dict(orient='records')
            data_size = len(data)
            data_sizes.append(data_size)

            # Measure sorts
            start_time = time.time()
            merge_sort_recursive(data_list.copy(), 'Quantity')
            recursive_times.append(time.time() - start_time)

            start_time = time.time()
            merge_sort_iterative(data_list.copy(), 'Quantity')
            iterative_times.append(time.time() - start_time)

            # Search
            search_name = input(f"Enter skin name to search in {file_path}: ")
            start_time = time.time()
            result = linear_search(data_list, search_name)
            search_time = time.time() - start_time
            search_times.append(search_time)

            print(f"Search result: {'Found' if result else 'Not found'}")
            if result:
                print(result)
            print(f"Search time: {search_time:.4f}s")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    # Plot performance
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(data_sizes, recursive_times, 'bo-', label='Recursive')
    plt.plot(data_sizes, iterative_times, 'ro-', label='Iterative')
    plt.xlabel('Data Size')
    plt.ylabel('Runtime (seconds)')
    plt.title('Sorting Runtime Comparison')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(data_sizes, search_times, 'go-', label='Search')
    plt.xlabel('Data Size')
    plt.ylabel('Runtime (seconds)')
    plt.title('Search Runtime')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Example usage
file_paths = [
    '200.csv',
    '150.csv',
    'sample_5000_ak47.csv'
]

analyze_performance(file_paths)