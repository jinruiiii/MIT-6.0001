# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    # Base case, when there is only 1 char, which means only 1 way of permuting
    if len(sequence) == 1:
        list_char = [sequence]
        return list_char
    else:
        # Calling a recursive function of a smaller magnitude each time
        all_permutations = get_permutations(sequence[1:])
        char = sequence[0]
        # possibilities_unrefined takes in all different orders, even duplicates if there are 2 or more same chars
        possibilities_unrefined = []
        # Slotting in the first char into each permutation of the remaining character
        for element in all_permutations:
            for i in range(len(element) + 1):
                possibilities_unrefined.append(element[:i] + char + element[i:])
        # Initializing a dict to get the frequency of each permutation
        frequency_dict = {}
        for element in possibilities_unrefined:
            if element in frequency_dict:
                frequency_dict[element] += 1
            else:
                frequency_dict[element] = 1
        possibilities_refined = []
        # possibilites_refined ensures that duplicates of the same permutation do not get returned more than once
        for key in frequency_dict:
            possibilities_refined.append(key)
        return possibilities_refined        


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    # Test Cases of sequence length 3 
    print("Input = 'abc' Expected Output = ['abc', 'bac', 'bca', 'acb', 'cab', 'cba']")
    print(f"Actual Output = {get_permutations('abc')}")
    print("")
    print("Input = 'abc' Expected Output = ['aab', 'aba', 'baa']")
    print(f"Actual Output = {get_permutations('aab')}")
    print("")
    print("Input = 'abc' Expected Output = ['aaa']")
    print(f"Actual Output = {get_permutations('aaa')}")

