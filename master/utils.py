import string
from base64 import b64encode
from random import choice, randint
from os import urandom

ALLOWED_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


# Output: Returns the edit distance between two strings
# source of function - https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings, which is the minimum number of single-character edits (i.e. insertions, deletions or substitutions) required to change one word into the other.

    :s1: The first string to compare
    :s2: The second string to compare
    :return: The Levenshtein distance between `s1` and `s2`
    """
    m, n = len(s1) + 1, len(s2) + 1
    dp = [[0] * n for _ in range(m)]

    for i in range(m):
        dp[i][0] = i
    for j in range(n):
        dp[0][j] = j

    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i - 1][j - 1] + cost,
                dp[i][j - 1] + 1
            )

    return dp[m - 1][n - 1]


def generate_random_strings(count):
    """
    Generate a specified number of random strings.
    Reference from https://stackoverflow.com/questions/48421142/fastest-way-to-generate-a-random-like-unique-string-with-random-length-in-python
    """
    generated = set()

    while len(generated) < count:
        desired_length = randint(12, 20)

        # Generate a random string by encoding random bytes
        urandom_bytes = urandom((desired_length + 1) * 3 // 4)
        candidate = b64encode(urandom_bytes, b'//').upper()[:desired_length]

        # Replace any '/' characters with a random character (now byte encoded)
        while b'/' in candidate:
            candidate = candidate.replace(b'/', choice(ALLOWED_CHARS).encode(), 1)

        # Add the generated string to the set if it's not already there
        if candidate not in generated:
            generated.add(candidate)
            yield candidate.decode()

