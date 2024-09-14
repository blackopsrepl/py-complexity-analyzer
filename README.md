### Complexity Estimation and Curve Fitting with Python

#### Overview
This program (`complexity_estimator.py`) measures the time complexity of functions using empirical analysis. It works by measuring execution times for various input sizes and fitting these measured times to a set of predefined mathematical models (complexity functions like `O(n)`, `O(n^2)`, etc.). It then identifies the best-fitting model, helping estimate the time complexity.

#### Core Concepts
1. **Empirical Complexity Estimation**:
   - Empirical analysis involves running a function with different input sizes and measuring the time it takes to execute.
   - The measured times are then compared to known complexity models to estimate the best fit.
   - The approach finds the model (e.g., `O(n)`, `O(n^2)`) that most closely describes the behavior of the function.

2. **Curve Fitting**:
   - This program uses **`scipy.optimize.curve_fit`** to fit the measured execution times to a set of predefined functions (complexity models).
   - **`curve_fit`** employs the **Levenberg-Marquardt algorithm**, which combines gradient descent and Gauss-Newton methods to minimize the error (difference) between observed times and the estimated model's times.
   - The output is the complexity model that provides the smallest error, indicating the best fit to the measured data.

3. **General Function Fitting**:
   - The program is not strictly limited to estimating "Big O" notation. It fits any set of measured execution times to a set of predefined models, finding the local minimum of the difference (mean squared error) between them.
   - This process is a form of **model fitting**, where "models" represent different time complexity functions.

#### Logic
1. **Input**:
   - One or more functions to analyze.
   - A list of input sizes to test (e.g., `[10, 100, 500, 1000]`).
   - The functions can be provided either programmatically or through command-line arguments, using dynamic importing.

2. **Execution**:
   - Measures the execution time of each function for the specified input sizes.
   - Stores the timing data for each input size.

3. **Curve Fitting**:
   - Compares the timing data against a set of predefined models (complexity functions).
   - Uses `curve_fit` to find parameters for each model that minimize the error between the model and the measured data.
   - Selects the model with the lowest error as the estimated complexity.

4. **Plotting**:
   - The program can plot the execution times of multiple functions to visually compare their complexities.
   - Uses `matplotlib` to generate comparison graphs.

#### Key Functions
- **`estimate_time_complexity(func, inputs)`**:
  - Measures execution times of `func` for different input sizes (`inputs`).
  - Fits these times to a set of predefined complexity functions.
  - Returns the best-fit complexity, input sizes, and measured times.
- **`plot_comparison(results)`**:
  - Plots execution times for each function.
  - Displays a graph showing how different functions' execution times grow with input size.

#### Usage
1. **Command-Line Interface**:
   - Specify the module and functions to analyze via command-line arguments.
   - Example: `python3 complexity_estimator.py module_name function_name1 function_name2 --sizes 10 100 1000`
2. **Programmatic Use**:
   - Import `estimate_time_complexity` and `main` functions into another script.
   - Pass functions directly for analysis and plotting.

#### Limitations
- The program estimates complexity based on empirical data and may not always identify the exact theoretical complexity, especially for functions with hidden constants or lower-order terms.
- `curve_fit` tries to minimize local error, which means it might (and will) converge on the nearest model rather than the exact theoretical model.
- Focuses on time complexity (not space complexity).

#### Example
To analyze two functions:
```python
def func1(input_data):
    return sum(i * i for i in input_data)

def func2(input_data):
    total = 0
    for i in range(len(input_data)):
        for j in range(len(input_data)):
            total += i * j
    return total

# Estimate and plot their complexities
input_sizes = [10, 100, 500, 1000, 2000]
functions = {'func1': func1, 'func2': func2}
main(functions, input_sizes)
```
This estimates the time complexity of `func1` and `func2`, then plots a comparison graph.

#### Notes
- **Model Fitting**: The program isn't strictly limited to Big O estimation since it just fits execution time data to a predefined set of models.