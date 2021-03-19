
from extended_bad_character import get_extended_bad_character_table, find_extended_bad_character_shift, lowercase_to_index
from good_suffix import get_good_suffix_values, get_matched_prefix_values, find_good_suffix_rule_shift, full_match


def naive_pattern_match(txt, pat):
    n = len(txt)
    m = len(pat)
    match_indices = []
    for i in range(n - m + 1):
        for j in range(m):
            if txt[i + j] != pat[j]:
                break
        else:
            match_indices.append(i)
    return match_indices


def boyer_moore(txt, pat, alphabet_size=26, char_to_index=lowercase_to_index):
    n = len(txt)
    m = len(pat)
    
    # Preprocessing
    ebct = get_extended_bad_character_table(pat, alphabet_size, char_to_index)
    gs = get_good_suffix_values(pat)
    mp = get_matched_prefix_values(pat)
    
    # Store the alignments where a full match has occured
    match_indices = []
    
    # Alignment
    j = 0
    
    # Alignment pattern section (Galil's optimisation)
    # -1 represents no characters match
    l = -1
    r = -1
    
    while not alignement_will_overflow(n, m, j):
        k = find_mismatch_index(txt, pat, j, l, r)
        c = txt[j + k]
        
        if full_match(k):
            match_indices.append(j)
        
        ebc_shift = find_extended_bad_character_shift(ebct, k, c, char_to_index)
        gs_shift, new_l, new_r = find_good_suffix_rule_shift(gs, mp, k, m)
        
        if use_good_suffix_shift(gs_shift, ebc_shift):
            j += gs_shift
            l = new_l
            r = new_r
        else:
            j += ebc_shift
            l = -1
            r = -1
    
    return match_indices


def use_good_suffix_shift(good_suffix_shift, extended_bad_character_shift):
    return good_suffix_shift >= extended_bad_character_shift


def alignement_will_overflow(n, m, j):
    return j + m > n

def find_mismatch_index(txt, pat, j, l, r):
    m = len(pat)
    i = m - 1
    while True:
        if i == -1:
            # If the previous char matched, the entire pattern matched, so we break
            break
        elif i == r:
            # If the char we are checking is within the range to know be matched, 
            # set i to the char before the matched section
            # (Galil's optimisation)
            i = l - 1
        elif pat[i] != txt[j + i]:
            # If there is a mismatch between pattern and txt, break
            break
        else:
            # If char matches, not end of pattern, and not in range we know match, try next char
            i -= 1
    
    # Return the index where the mismatch occured
    # If there was a full match, we will return -1
    return i

