import pandas as pd

def load_intervals_from_csv(file_path):
    """
    Load intervals from a CSV file. Each interval includes a start time, end time, and cost.
    
    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of tuples, each representing an interval (start, end, cost).
    """
    intervals_data = pd.read_csv(file_path)
    intervals_list = []
    for _, row in intervals_data.iterrows():
        intervals_list.append((int(row['Interval_start']), int(row['Interval_end']), int(row['Cost'])))
    return intervals_list

def find_previous_non_overlapping(intervals, current_index):
    """
    Find the index of the last interval that ends before the current interval starts.

    Parameters:
        intervals (list): List of sorted intervals (start, end, cost).
        current_index (int): Index of the current interval.

    Returns:
        int: Index of the last non-overlapping interval, or -1 if none found.
    """
    low, high = 0, current_index - 1
    while low <= high:
        mid = (low + high) // 2
        if intervals[mid][1] < intervals[current_index][0]:
            if intervals[mid + 1][1] < intervals[current_index][0]:
                low = mid + 1
            else:
                return mid
        else:
            high = mid - 1
    return -1

def optimize_intervals(intervals, trade_off=0.5):
    """
    Find the optimal combination of non-overlapping intervals based on a trade-off between count and cost.

    Parameters:
        intervals (list): List of tuples (start, end, cost).
        trade_off (float): Trade-off parameter (0 for cost priority, 1 for count priority).

    Returns:
        tuple: Selected intervals and their total score.
    """
    # Scale trade-off to use integer calculations
    #Figure out this
    scale_factor = 1000
    trade_off_scaled = int(trade_off * scale_factor)

    # Sort intervals by their end times
    intervals.sort(key=lambda interval: interval[1])

    num_intervals = len(intervals)
    # Maximum scores at each step
    max_scores = [0] * (num_intervals + 1)

    # Initialize the tracker
    selected_intervals_tracker = []  
    for _ in range(num_intervals + 1):
        # Append an empty list for each interval
        selected_intervals_tracker.append([])  


    for i in range(1, num_intervals + 1):
        start, end, cost = intervals[i - 1]

        # Option 1: Exclude the current interval
        exclude_current = max_scores[i - 1]

        # Option 2: Include the current interval
        previous_index = find_previous_non_overlapping(intervals, i - 1)
        #Focus entirely on minimizing costs
        if trade_off == 0 and cost == 0:
            include_current = max_scores[previous_index + 1] + 1  
        #Focus entirely on selecting the maximum number of intervals
        elif trade_off == 1:
            include_current = max_scores[previous_index + 1] + 1
        else:
            include_current = (max_scores[previous_index + 1]+ trade_off_scaled * 1 - max(0, (scale_factor - trade_off_scaled) * cost))

        # Choose the better option (current one or previous one)
        if include_current > exclude_current:
            max_scores[i] = include_current
            selected_intervals_tracker[i] = selected_intervals_tracker[previous_index + 1] + [(start, end, cost)]
        else:
            max_scores[i] = exclude_current
            selected_intervals_tracker[i] = selected_intervals_tracker[i - 1]



    if trade_off == 1:
        # Use the count of intervals
        final_score = len(selected_intervals_tracker[num_intervals])  
    else:
        # Scale the score for trade-off
        final_score = max_scores[num_intervals] / scale_factor  


    # Return the final set of selected intervals and the total score
    return selected_intervals_tracker[num_intervals], final_score

if __name__ == "__main__":
    # Path to the input file
    file_path = "2_OptimizingIntervalCombinations_intervals.csv"

    # Load intervals from CSV
    intervals = load_intervals_from_csv(file_path)

    # Get trade-off parameter from user
    trade_off = float(input("Enter the trade-off parameter (0 to 1): "))

    # Optimize and find the best set of intervals
    optimal_intervals, maximum_score = optimize_intervals(intervals, trade_off)

    total_cost = 0

    # Display results
    print("\nOptimal set of intervals:")
    for interval in optimal_intervals:
        total_cost += interval[2]
        print(interval)


    print(f"\nMaximum Score: {maximum_score}")

    print(f"\nTotal Cost Score: {total_cost}")

    print(f"\nCount Intervals: {len(optimal_intervals)}")

