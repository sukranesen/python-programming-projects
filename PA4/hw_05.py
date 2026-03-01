import os

# Custom pseudorandom number generator with a random initial seed
class PRNG:
    def __init__(self, seed=None):
        # Use a truly random seed if no seed is provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), 'big')  # Generate a random 32-bit integer
        self.state = seed

    def randint(self, low, high):
        # Simple linear congruential generator (LCG)
        self.state = (1103515245 * self.state + 12345) % (2 ** 31)
        return low + (self.state % (high - low + 1))


# Generate logistics dataset
def generate_logistics_dataset(num_warehouses=100, max_packages=1000, seed=None):
    """Generates a logistics dataset with a random or specified seed."""
    prng = PRNG(seed)  # Initialize PRNG with the seed or a random one
    data = []
    for i in range(1, num_warehouses + 1):
        warehouse_id = f"WH-{str(i).zfill(3)}"
        priority_level = prng.randint(1, 5)
        package_count = prng.randint(0, max_packages)
        data.append([warehouse_id, priority_level, package_count])
    return data


# Save dataset to a CSV file
def save_to_csv(data, file_name):
    """Saves the dataset to a CSV file."""
    with open(file_name, "w") as file:
        # Write the header
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")
        # Write each row
        for row in data:
            file.write(",".join(map(str, row)) + "\n")


# Error Handling for Sorting Functions
def validate_input(array):
    if not array:
        raise ValueError("Input array is empty.")
    if not all(isinstance(item, list) and len(item) == 3 for item in array):
        raise ValueError("Each item in the array must be a list with three elements.")
    if not all(isinstance(item[1], int) and isinstance(item[2], int) for item in array):
        raise ValueError("Priority level and package count must be integers.")


def bubble_sort(array):
    global counter
    counter = 0
    validate_input(array)
    n = len(array)

    for i in range(n):
        for j in range(0, n - i - 1):
            counter += 1
            if array[j][1] > array[j + 1][1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            elif array[j][1] == array[j + 1][1]:
                if array[j][2] > array[j + 1][2]:
                    array[j], array[j + 1] = array[j + 1], array[j]

    return array


def merge_sort(array):

    global counter
    counter = 0
    validate_input(array)

    def merge_sort_helper(array):
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left = merge_sort_helper(array[:mid])
        right = merge_sort_helper(array[mid:])
        return merge(left, right)

    def merge(left, right):
        global counter
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            counter += 1
            if left[i][1] < right[j][1] or (
                    left[i][1] == right[j][1] and left[i][2] <= right[j][2]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1

        while j < len(right):
            merged.append(right[j])
            j += 1

        return merged

    return merge_sort_helper(array)



def quick_sort(array):
    global counter
    counter = 0
    validate_input(array)

    def _quick_sort(arr):
        global counter
        if len(arr) <= 1:
            return arr

        pivot = arr[0]
        less = []
        equal = []
        greater = []

        for item in arr:
            counter += 1
            if item[1] < pivot[1] or (
                    item[1] == pivot[1] and item[2] < pivot[2]
            ):
                less.append(item)
            elif item[1] == pivot[1] and item[2] == pivot[2]:
                equal.append(item)
            else:
                greater.append(item)

        sorted_less = _quick_sort(less)
        sorted_greater = _quick_sort(greater)

        return sorted_less + equal + sorted_greater

    return _quick_sort(array)


def two_level_sorting(sort_func, dataset):
    global counter

    validate_input(dataset)

    counter = 0
    sorted_by_pl = sort_func(dataset)
    sort_pl_counter = counter

    counter = 0
    sorted_by_pc = sort_func(sorted_by_pl)
    sort_pc_counter = counter

    return sorted_by_pc, sort_pl_counter, sort_pc_counter


def write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
):
    """Write sorted results and comparisons to the output file."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("=== Bubble Sorted Results ===\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("-" * 40 + "\n")
        for row in bubble_sorted:
            file.write(f"{row[0]:<12}  {row[1]:<14}  {row[2]:<13}\n")
        file.write("\n")
        file.write("=== Comparison Results ===\n")
        if merge_check:
            file.write("Merge and Bubble sorts are identical.\n")
        else:
            file.write("Merge and Bubble sorts differ.\n")

        if quick_check:
            file.write("Quick and Bubble sorts are identical.\n")
        else:
            file.write("Quick and Bubble sorts differ.\n")

        file.write("\n=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_sort_pl_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_sort_pl_counter}\n")
        file.write(f"Quick priority sort recursive step count: {quick_sort_pl_counter}\n\n")

        file.write(f"Bubble package count sort iteration count: {bubble_sort_pc_iterations}\n")
        file.write(f"Merge package count n_of right array is smaller than left: {merge_sort_pc_counter}\n")
        file.write(f"Quick package count sort recursive step count: {quick_sort_pc_counter}\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    # File paths and dataset size
    # Specify paths for input and output files
    INPUT_FILE = "hw05_input.csv"  # Path where the generated dataset will be saved
    OUTPUT_FILE = "hw05_output.txt"  # Path where the sorted results and metrics will be saved
    SIZE = 10  # Number of warehouses in the dataset

    # Generate the dataset
    dataset = generate_logistics_dataset(SIZE,
                                         max_packages=100)  # Generate a dataset with SIZE warehouses and max_packages packages

    # Save the generated dataset to the input file
    save_to_csv(dataset, INPUT_FILE)

    ###############################################################################################################
    # Perform sorting and counting operations
    # Sort using Bubble Sort and count iterations for Priority Level (_pl_) and Package Count (_pc_)
    bubble_sorted, bubble_sort_pl_iterations, bubble_sort_pc_iterations = two_level_sorting(bubble_sort, dataset)

    # Sort using Merge Sort and count recursive steps for Priority Level and Package Count
    merge_sorted, merge_sort_pl_counter, merge_sort_pc_counter = two_level_sorting(merge_sort, dataset)

    # Sort using Quick Sort and count recursive steps for Priority Level and Package Count
    quick_sorted, quick_sort_pl_counter, quick_sort_pc_counter = two_level_sorting(quick_sort, dataset)
    ###############################################################################################################

    # Comparisons
    # Check if Merge Sort results match Bubble Sort results
    merge_check = merge_sorted == bubble_sorted

    # Check if Quick Sort results match Bubble Sort results
    quick_check = quick_sorted == bubble_sorted

    # Write results and metrics to the output file
    write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
    )