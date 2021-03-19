# Boyer Moore String Pattern Matching Algorithm

This algorithm is a worst case linear time solution to the exact pattern matching problem.
It works by preproccessing the pattern in linear time in a multitude of different ways.

### High Level Explanation

We start at alignment `0` and find the first mismatching character, and give this information to the two rules:
- The extended bad character rule
- The good suffix rule

These rules gives us the longest safe jump to the next alignment.
We then choose the bigger of the two jumps, as they are both safe.
We continue this until we reach the end of the text, keeping note of all the exact matches.

The good suffix rules attempts to match suffixes in the text, the occurances of the suffix in the pattern.
The extended bad character rule attempts to match mismatched characters.