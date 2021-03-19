def naive_z_algorithm(chars):
    n = len(chars)

    # Create empty z values array
    z_values = [None for _ in chars]

    # z_values[0] is length of string, as it will match the entire string
    z_values[0] = len(chars)

    for i in range(1, n):
        z_values[i] = explicit_comparison_from_i(chars, i)
    
    return z_values


def z_algorithm(chars):
    n = len(chars)

    # Create empty z values array
    z_values = [None for _ in chars]

    # Keep track of left and right bounds of right-most z-box
    l = 0
    r = 0

    # z_values[0] is length of string, as it will match the entire string
    z_values[0] = len(chars)

    # Iterate over remaining characters, and calculate the z values
    for i in range(1, n):
        if explicit_required(i, r):
            # Case 1
            z_values[i] = explicit_comparison_from_i(chars, i)

        elif z_within_z_box(z_values, i, r, l):
            # Case 2a
            z_values[i] = z_value_of_z_box(z_values, i, l)

        elif z_on_edge_of_z_box(z_values, i, r, l):
            # Case 2b
            known_char_count = r - i + 1
            z_values[i] = explicit_comparison_from_i(chars, i, skip=known_char_count)

        else:
            # Optimisation discussed in tutorial
            z_values[i] = r - i + 1

        l, r = update_l_r(z_values, i, r, l)
    
    return z_values


def update_l_r(z_values, i, r, l):
    # Don't change for these cases
    if z_values[i] == 0: return (l, r)
    if i + z_values[i] <= r: return (l, r)

    # Update l and r to right-most z box
    new_l = i
    new_r = i + z_values[i] - 1

    return (new_l, new_r)


def explicit_comparison_from_i(chars, i, skip = 0):
    n = len(chars)

    # If skipping comparisons we know are correct, 
    # set z_value to the number of chars we skipped
    z_value = skip

    # Loop until i characters away from end of chars to avoid 
    for j in range(skip, n - i):
        # If mismatch from prefix, stop loop
        if chars[j] != chars[i + j]: break

        # Increment z value if char matches char in prefix
        z_value += 1

    return z_value


def explicit_required(i, r):
    return i > r


def z_value_of_z_box(z_values, i, l):
    return z_values[i - l]


def z_within_z_box(z_values, i, r, l):
    return z_value_of_z_box(z_values, i, l) < r - i + 1


def z_on_edge_of_z_box(z_values, i, r, l):
    return z_value_of_z_box(z_values, i, l) == r - i + 1
