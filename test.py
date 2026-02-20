#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some strings.')
    parser.add_argument('strings', metavar='mot', type=str, nargs='+',help='a string to print')
    args = parser.parse_args()

    # Process strings if provided
    if args.strings:
        for string in args.strings:
            print(f'"{string}"', end=' ')
        print()

