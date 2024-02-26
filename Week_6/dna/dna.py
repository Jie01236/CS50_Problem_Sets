import csv
import sys


def main():

    #Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    #Read database file into a variable
    Person_STR = []
    filename = sys.argv[1]
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            Person_STR.append(row)

    # TODO: Read DNA sequence file into a variable
    #open DNA sequence, read contents into memory
    filename2 = sys.argv[2]
    with open(filename2) as file:
        dna_sequence = file.read()

    # to confirm a match, check every colunm other than the 1st column
    subsequences = list(Person_STR[0].keys())[1:]

    # save match counts in some data structure
    str_counts = {}

    for each_STR in subsequences: #subseq是从Person_STR列表中提取的每个短串
        # Find longest match of each STR in DNA sequence （调用函数）
        # 函数：对比一个DNA样本和从Person_STR列表中提取的每个短串，得出短串的数量
        match_count = longest_match(dna_sequence, each_STR)
        str_counts[each_STR] = match_count
        # match counts是value，从Person_STR列表中提取的每个短串each_STR是key

    # TODO: Check database for matching profiles
    # if so print the name, else print "no match"
    for person in Person_STR:
        for each_STR in subsequences:
            # 如果某个 STR 计数不匹配
            if str_counts[each_STR] != int(person[each_STR]):
                break
        else:  # 如果 for 循环没有被 break 打断，则所有 STR 都匹配
            print(person['name'])
            return
        
    print("No match")

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
