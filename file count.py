import statistics

def calculate_population_standard_deviation(data):
    """
    Calculate the population standard deviation of a given array.

    Parameters:
    - data (list): List of numerical values.

    Returns:
    - float: Population standard deviation of the input data.
    """
    try:
        population_std_deviation = statistics.pstdev(data)
        return population_std_deviation
    except statistics.StatisticsError as e:
        print(f"Error calculating population standard deviation: {e}")
        return None

# Example usage:
data_array = [15]
result = calculate_population_standard_deviation(data_array)

if result is not None:
    print(f"The population standard deviation is: {result}")
