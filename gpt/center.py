import os


file_path = "input.txt"

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()


print(text[0:100])