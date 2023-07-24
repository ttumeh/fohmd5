import hashlib
import argparse
from tqdm.auto import tqdm


"""
Encode password to MD5
"""
def md5_hash(password):
    return (hashlib.md5(password.encode()).hexdigest())


"""
Crack MD5 hash
"""
def crack_hash_parallel(hash_list, hash_type, dictionary_path):

    print(f'Cracking {hash_list}.....')
    print(f'Using dictionary from {dictionary_path}.....')

    with open(dictionary_path, 'r') as dictionary_file:
        num_lines = sum(1 for _ in dictionary_file)
        dictionary_file.seek(0)
                # Initialize tqdm progress bar
        progress_bar = tqdm(total=num_lines, position=0, leave=False)
        # Iterate through the dictionary file line by line
        for index, line in enumerate(dictionary_file, start=1):
            password = line.strip()
            hashed_pass = md5_hash(password)
            if (hashed_pass == hash_list):
                print(f"\n\nHash {hash} cracked: {password}")
                break
            else: 
                print(f'\rCracking Progress: ({index}/{num_lines})', end='', flush=True)
                # Update tqdm progress bar
                progress_bar.update(1)

    print('\n\nPassword not found')


"""
Read hash file contents
"""
def read_hash_from_file(file_path):
    with open(file_path, 'r') as file:
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
    parser.add_argument('hash', help='Hashed password to crack')
    parser.add_argument('-a', '--attack', choices=['dict', 'brute'], default='dict', 
                        help='Select the attack type: dict or brute (default: dict)')
    parser.add_argument('-d', '--dictionary', default='passwords.txt', 
                        help='Specify the dictionary file for the dictionary attack (default: passwords.txt)')
    args = parser.parse_args()

    # Check if the 'hash' argument contains a path to a file
    if args.hash.endswith('.txt'):
        hash_value = read_hash_from_file(args.hash)
    else:
        hash_value = args.hash

    # Call the cracking function with the provided arguments
    crack_hash_parallel(hash_value, args.attack, args.dictionary)

if __name__ == '__main__':
    main()