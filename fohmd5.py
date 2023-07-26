import hashlib
import argparse
import string
import time
import math

UP = "\x1B[3A"
CLR = "\x1B[0K"

"""
Encode password to MD5
"""


def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


"""
Crack MD5 hash using dictionary
"""


def crack_md5_dict(hash_list, dictionary_path):

    print(f"Cracking {hash_list}.....")
    print(f"Using dictionary from {dictionary_path}.....")

    with open(dictionary_path, "r") as dictionary_file:
        
        dictionary_file.seek(0)
        # Iterate through the dictionary file line by line
        for index, line in enumerate(dictionary_file, start=1):
            password = line.strip()
            hashed_pass = md5_hash(password)
            if hashed_pass == hash_list:
                print(f"\n\nHash {hash_list} cracked: {password}\n")
                return
            
    print("\n\nPassword not found. Try another dictionary.\n")


"""
Crack MD5 hash using brute-force
"""


# TODO length, wildcards, time
def crack_md5_brute(hash_list, length, max_length, interval):

    to_go = int(math.factorial(100)/math.factorial((100-int(max_length))))
    print(f"Cracking {hash_list}.....")
    calc = 1
    start_time = time.time()
    start_time2 = time.time()
    for string_length in range(int(length), int(max_length) + 1):
        mystring = ["0"] * string_length

        # Infinite loop until user cancels or pass found
        while True:
            if calc != 1 and (time.time() - start_time2) > float(interval):
                print_progress(calc, ''.join(mystring), start_time, to_go)
                start_time2 = time.time()
            for iteration in range(len(string.printable)):
                char = string.printable[iteration]
                mystring[-1] = char
                
                calc += 1
                c = "".join(mystring)
                hashed_pass = md5_hash(c)
                if str(hashed_pass) == str(hash_list):
                    print(f"\n\nHash cracked: {c}\n")
                    return

            # Increment the digits from right to left
            index = string_length - 1
            while index >= 0:
                if mystring[index] == string.printable[-1]:
                    mystring[index] = string.printable[0]
                    index -= 1
                else:
                    mystring[index] = string.printable[
                        string.printable.index(mystring[index]) + 1
                    ]
                    break
            else:
                break
    print("\n\nCracking unsuccessful.\n")


"""
Print progress of the running process
"""


def print_progress(iteration, mystring, start_time, to_go):
    elapsed_time = round(time.time() - start_time,3)
    progress=round((iteration/to_go)*100,3)
    print(
        f"Testing combination: {mystring}  Iteration: {iteration}/{to_go}   Elapsed time: {elapsed_time}    Progress: {progress}%"
        )


"""
Read hash file contents
"""


def read_hash_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


"""
Main function
"""


def main():
    ascii_art = r"""
:::::::::: ::::::::  :::    ::: ::::    ::::  :::::::::  :::::::::: 
:+:       :+:    :+: :+:    :+: +:+:+: :+:+:+ :+:    :+: :+:    :+: 
+:+       +:+    +:+ +:+    +:+ +:+ +:+:+ +:+ +:+    +:+ +:+        
:#::+::#  +#+    +:+ +#++:++#++ +#+  +:+  +#+ +#+    +:+ +#++:++#+  
+#+       +#+    +#+ +#+    +#+ +#+       +#+ +#+    +#+        +#+ 
#+#       #+#    #+# #+#    #+# #+#       #+# #+#    #+# #+#    #+# 
###        ########  ###    ### ###       ### #########   ########  


                                                          
"""
    print(ascii_art)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("hash", help="Hashed password to crack")
    parser.add_argument(
        "-a",
        "--attack",
        choices=["dict", "brute"],
        default="dict",
        help="Select the attack type: dict or brute (default: dict)",
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        default="passwords.txt",
        help="Specify the dictionary file for the dictionary attack (default: passwords.txt)",
    )
    parser.add_argument(
        "-l",
        "--length",
        default=1,
        help="Specify the length of bruteforced password (default: 1)",
    )
    parser.add_argument(
        "-ml",
        "--maxlength",
        default=100,
        help="Specify the length of bruteforced password (default: 1)",
    )
    parser.add_argument(
        "-i",
        "--interval",
        default=300,
        help="Specify interval of progress update (seconds) (default: 300)",
    )


    args = parser.parse_args()

    # Check if the 'hash' argument contains a path to a file
    if args.hash.endswith(".txt"):
        hash_value = read_hash_from_file(args.hash)
    else:
        hash_value = args.hash

    if args.attack == "dict":
        crack_md5_dict(hash_value, args.attack, args.dictionary)

    if args.attack == "brute":
        crack_md5_brute(hash_value, args.length, args.maxlength, args.interval)


if __name__ == "__main__":
    main()
