import sys

def main():
    attempt = sys.argv[1]
    if attempt == '1':
        exit(1)
    else:
        print(attempt)
        exit(0)


if __name__ == "__main__":
    main()