import os

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(120, 160):
        print(f"{i}: {lines[i].strip()}")

if __name__ == '__main__':
    main()
