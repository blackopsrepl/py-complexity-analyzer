import time
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import argparse
import importlib

############################################################
### COMMON COMPLEXITY FUNCTIONS (used for curve fitting) ###
############################################################
def constant(n, a): return a  # O(1) complexity: constant time, independent of input size
def logarithmic(n, a): return a * np.log2(n)  # O(log n): logarithmic time, grows with the logarithm of the input size
def linear(n, a): return a * n  # O(n): linear time, grows directly with the input size
def linearithmic(n, a): return a * n * np.log2(n)  # O(n log n): linearithmic time, common in algorithms like merge sort
def quadratic(n, a): return a * n**2  # O(n^2): quadratic time, grows with the square of the input size (e.g., nested loops)
def cubic(n, a): return a * n**3  # O(n^3): cubic time, grows with the cube of the input size (e.g., triple nested loops)
# def exponential(n, a): return a * 2**n  # O(2^n): exponential time, grows very rapidly (e.g., recursive solutions)
def exponential(n, a): a * np.exp(n * np.log(2))

# Map complexity function names to their implementations
complexities = {
    "O(1)": constant,
    "O(log n)": logarithmic,
    "O(n)": linear,
    "O(n log n)": linearithmic,
    "O(n^2)": quadratic,
    "O(n^3)": cubic,
    "O(2^n)": exponential
}

def estimate_time_complexity(func, inputs):
    """
    Estimates the time complexity of a given function.
    
    Parameters:
    - func: The function whose complexity is to be estimated.
    - inputs: A list of input datasets of different sizes to test the function with.

    Returns:
    - The estimated complexity (string), input sizes (n_values), and measured execution times.
    """
    times = []  # List to store the execution times for each input size

    # Measure execution time for each input size
    for input_data in inputs:
        start_time = time.time()  # Start the timer
        func(input_data)  # Call the function with the current input data
        end_time = time.time()  # Stop the timer
        times.append(end_time - start_time)  # Calculate and store the elapsed time

    # Prepare the input sizes (n_values) for curve fitting
    n_values = np.array([len(inp) for inp in inputs])  # Get the size of each input dataset
    times = np.array(times)  # Convert measured times to a NumPy array for numerical operations

    best_fit = None  # Variable to store the name of the best-fit complexity function
    best_error = float('inf')  # Initialize the error to a large number (to be minimized)

    # Try fitting the measured times to each known complexity function
    for complexity_name, complexity_func in complexities.items():
        try:
            # Attempt to fit the current complexity function to the measured data
            params, _ = curve_fit(complexity_func, n_values, times)
            estimated_times = complexity_func(n_values, *params)  # Calculate estimated times using the fitted parameters
            error = np.mean((times - estimated_times) ** 2)  # Calculate mean squared error between measured and estimated times
            # Update best fit if the current fit has a lower error
            if error < best_error:
                best_fit = complexity_name
                best_error = error
        except Exception:
            # If curve fitting fails (e.g., due to numerical issues), skip this complexity function
            continue

    # Return the best-fitting complexity, the input sizes, and the measured execution times
    return best_fit, n_values, times

def plot_comparison(results):
    """
    Plots a comparison graph of execution times for multiple functions.
    
    Parameters:
    - results: A list of tuples, each containing the function name, input sizes, times, and estimated complexity.
    """
    plt.figure(figsize=(10, 6))  # Create a new plot with specified size
    # Plot the execution times for each function
    for result in results:
        function_name, n_values, times, complexity = result
        plt.plot(n_values, times, label=f"{function_name} ({complexity})", marker='o')  # Plot with markers and label
    # Set labels, title, and legend
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Time Complexity Comparison')
    plt.legend()
    # Add grid for easier reading
    plt.grid(True)
    # Display the plot
    plt.show()

def main(funcs, input_sizes):
    """
    Main function to estimate and compare the time complexity of multiple functions.
    
    Parameters:
    - funcs: A dictionary of function names to function objects.
    - input_sizes: A list of input sizes to use for testing each function.
    """
    inputs = [list(range(n)) for n in input_sizes]  # Create input datasets based on the specified sizes
    results = []  # List to store results for each function
    # Estimate complexity for each function
    for func_name, func in funcs.items():
        complexity, n_values, times = estimate_time_complexity(func, inputs)
        results.append((func_name, n_values, times, complexity))  # Store the results
        print(f"Estimated complexity for {func_name}: {complexity}")
    # Plot comparison if --plot was specified
    if args.plot:
        plot_comparison(results)

if __name__ == "__main__":
    ##############################
    ### COMMAND LINE INTERFACE ###
    ##############################
    parser = argparse.ArgumentParser(description='Estimate the time complexity of Python functions.')
    parser.add_argument('module', type=str, help='The module name containing the functions to analyze')
    # TODO: strip '.py' if present
    parser.add_argument('function_names', nargs='+', help='The function names to analyze')
    parser.add_argument('--sizes', nargs='+', type=int, help='List of input sizes to test', default=[10, 100, 500, 1000, 2000])
    # TODO: check for input sizes sorting if not default
    parser.add_argument('--plot', action='store_true', help='Plot comparison graph')
    # Parse arguments
    args = parser.parse_args()
    # Clear import cache and load module
    importlib.invalidate_caches()
    module = importlib.import_module(args.module)
    # Retrieve each function by name
    funcs = {name: getattr(module, name) for name in args.function_names}
    # Run the complexity estimation for the specified functions and input sizes
    input_sizes = args.sizes
    main(funcs, input_sizes)