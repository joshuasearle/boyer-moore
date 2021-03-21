
from z_algorithm import z_algorithm


def get_z_suffix_values(pat):
    '''
    z_suffix_values[i] = the longest substring starting at i, that is also a suffix of the string.
    The character preceeding the substring also must be different than the character preceeding the suffix.
    '''
    l = list(reversed(z_algorithm(pat[::-1])))
    # Last value will always be length of pattern, so remove it to aviod confusion
    l.pop()
    return l


def get_good_suffix_values(pat):
    '''
    good_suffix_values[i] = The endpoint of the rightmost substring that matches the suffix starting at i.
    The character preceeding the substring must be different than the character preceeding the suffix.
    '''
    m = len(pat)
    z_suffix_values = get_z_suffix_values(pat)

    good_suffix_values = [0 for _ in range(m + 1)]
    
    for i in range(m - 1):
        p = z_suffix_values[i]
        j = m - p
        good_suffix_values[j] = i
    
    return good_suffix_values


def get_matched_prefix_values(pat):
    '''
    matched_prefix_values[i] = The longest suffix of the suffix starting at i that is also a prefix
    '''
    m = len(pat)
    z_values = z_algorithm(pat)
    matched_prefix_values = [0 for _ in range(m)]
    # Manually compute value for last index
    matched_prefix_values[-1] = 1 if pat[0] == pat[-1] else 0

    # Loop backwards, skipping last element
    for i in range(m - 2, -1, -1):
        if z_values[i] + i < m:
            max_prefix_length = matched_prefix_values[i + 1]
        else:
            max_prefix_length = max([matched_prefix_values[i + 1], z_values[i]])
        matched_prefix_values[i] = max_prefix_length
    
    return matched_prefix_values


def find_good_suffix_rule_shift(good_suffix_values, matched_prefix_values, k, m):
    
    good_suffix_value = good_suffix_values[k + 1]

    if no_char_matched(k, m):
        return handle_no_char_match(good_suffix_value, k, m)
    
    matched_prefix_value = matched_prefix_values[k + 1]
    
    if full_match(k):
        return handle_full_match(matched_prefix_values, m)
    
    elif good_suffix_exists(good_suffix_values, k):
        return handle_good_suffix_exists(good_suffix_value, k, m)
    
    else:
        return handle_matched_prefix(matched_prefix_value, k, m)


def full_match(k):
    return k == -1


def no_char_matched(k, m):
    return k + 1 >= m


def good_suffix_exists(good_suffix_values, k):
    return good_suffix_values[k + 1] != 0


def handle_full_match(matched_prefix_values, m):
    # We need to shift to match the biggest prefix that is also a suffix, but not the suffix itself
    shift = m - matched_prefix_values[1]
    if matched_prefix_values[1] == 0:
        # If not aligning with any prefix, we know nothing about any mactches,
        # so r = l = -1
        l = -1
        r = -1
        return (shift, l, r)
    else:
        # We know some of the prefix matches
        l = 0
        r = m - shift - 1
        return (shift, l, r)


def handle_no_char_match(good_suffix_value, k, m):
    return handle_good_suffix_exists(good_suffix_value, k, m)


def handle_good_suffix_exists(good_suffix_value, k, m):
    suffix_length = m - k - 1
    shift = m - good_suffix_value - 1
    # min to handle case where suffix length is zero
    l = min(good_suffix_value - suffix_length + 1, good_suffix_value)
    r = good_suffix_value
    return (shift, l, r)


def matched_prefix_value_exists(matched_prefix_value):
    return matched_prefix_value == 0


def handle_matched_prefix(matched_prefix_value, k, m):
    if matched_prefix_value_exists(matched_prefix_value):
        shift = m
        l = -1
        r = -1
        return (shift, l, r)
    else:
        prefix_length = matched_prefix_value
        shift = m - matched_prefix_value
        l = 0
        r = prefix_length - 1
        return (shift, l, r)
