import copy

original_list = [[1, 2], [3, 4]]
shallow_copy = copy.copy(original_list)

shallow_copy[0][0] = 99  # Modifies the nested list in both original and shallow_copy
print(original_list)    # Output: [[99, 2], [3, 4]]
print(shallow_copy)     # Output: [[99, 2], [3, 4]]