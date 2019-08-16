# Metaheuristic-Cuckoo_Search
Cuckoo Search to Minimize Functions with Continuous Variables. The function returns: 1) An array containing the used value(s) for the target function and the output of the target function f(x). For example, if the function f(x1, x2) is used, then the array would be [x1, x2, f(x1, x2)].  

* birds = The population size. The Default Value is 3.

* alpha_value = Levy Flight step size. The Default Value is 0.01.

* lambda_value = Levy Flight distribution. The Default Value is 1.5.

* discovery_rate = Percentage of discovered cuckoo's eggs. The Default Value is 0.25.

* min_values = The minimum value that the variable(s) from a list can have. The default value is -5.

* max_values = The maximum value that the variable(s) from a list can have. The default value is  5.

* iterations = The total number of iterations. The Default Value is 50.

* target_function = Function to be minimized. 
