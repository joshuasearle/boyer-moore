
def lowercase_to_index(char):
    return ord(char) - ord('a')


def print_matrix(matrix):
    for row in matrix:
        print(row)


def find_extended_bad_character_shift(
    extended_bad_character_table, 
    mismatch_index, 
    mismatch_character, 
    char_to_index=lowercase_to_index
):
    char_index = char_to_index(mismatch_character)
    righmost_mismatch_char_left_of_mismatch = extended_bad_character_table[mismatch_index][char_index]
    return max(mismatch_index - righmost_mismatch_char_left_of_mismatch, 1)


def get_extended_bad_character_table(pat, alphabet_size=26, char_to_index=lowercase_to_index):
    '''
    We want a table that when we query the index of the mismtach, 
    then query the character that was the mismatch, 
    the rightmost occurance of the mismatched character to 
    the left of the mismatch index in the pattern is returned.
    '''
    m = len(pat)
    # -1 signifies that the next occurance of the mismatched character is not in the pattern
    r = [[-1 for _ in range(alphabet_size)] for _ in range(m)]
    i = 0
    for char in pat:
        if i >= m - 1: break
        r[i + 1] = [x for x in r[i]]
        r[i + 1][char_to_index(char)] = i
        i += 1
    return r