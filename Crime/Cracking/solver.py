import re
from collections import Counter

reg = input('Input your searchstring here (use . for wildcard characters, e.g. "..l.y" for "silly"): ')
with open(
    r"C:\Users\lospo\Desktop\Stuff\Python code\TornCracking\ignis-100K.txt",
    "r",
    encoding="utf-8",
) as file:
    lines = file.readlines()

    pattern = re.compile(rf"^{reg}$", re.IGNORECASE)
    match_count = 0
    matched_passwords = []

    for i, line in enumerate(lines, 1):
        password = line.strip().lower()

        if pattern.search(password) and not re.search(r"[^a-zA-Z0-9]", password):
            matched_passwords.append(password)
            match_count += 1
            print(f"Line {i}: {password}")

    print(f"Total matching lines: {match_count}")

    if match_count > 1:
        password_length = len(matched_passwords[0])

        position_counts = [Counter() for _ in range(password_length)]

        for password in matched_passwords:
            for idx, char in enumerate(password):
                position_counts[idx][char] += 1

        for idx, counter in enumerate(position_counts):
            if len(counter) > 1:
                total = sum(counter.values())
                print(f"\nPosition {idx + 1}:", end="  ")
                sorted_counts = sorted(
                    counter.items(), key=lambda x: x[1], reverse=True
                )
                for char, count in sorted_counts:
                    percentage = (count / total) * 100
                    print(f"  {char.upper()} ({percentage:.0f}%)", end=" ")
