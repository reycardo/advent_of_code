import subprocess
import sys
import os


def download_aoc_input(day, year):
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(
        os.getcwd(), "advent-of-code", "src", str(year), f"Day{day}"
    )
    os.makedirs(output_dir, exist_ok=True)

    # Run the aocd command to download the input and redirect it to a file
    command = f"aocd {day} {year} > {output_dir}\\input.txt"
    subprocess.run(command, shell=True)


def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python my_script.py <day> <year>")
        sys.exit(1)

    # Get day and year from command-line arguments
    day = sys.argv[1]
    year = sys.argv[2]

    # Run the function to download AOC input
    download_aoc_input(day, year)


if __name__ == "__main__":
    main()
