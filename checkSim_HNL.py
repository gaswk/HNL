import os
import sys
import ROOT

# ANSI escape codes for text formatting
class Colors:
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'     # Red
    ENDC = '\033[0m'      # End formatting

def check_events(root_file, expected_num_events):
    tree = root_file.Get("events")

    if not tree:
        print(f"Error: Unable to find TTree named 'events' in {root_file.GetName()}")
        return

    # Get the number of events
    num_events = tree.GetEntries()

    if num_events != expected_num_events:
        print(f"File: {root_file.GetName()}\n  {Colors.FAIL} -> /!\ Actual events: {num_events}, Expected events: {expected_num_events}{Colors.ENDC}")
        warnings_or_fail = True

    if warnings_or_fail:
        print()  # Add a new line before the next file

def check_files_in_directory(directory, expected_num_files, expected_num_events):
    file_list = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.root')]

    if len(file_list) != expected_num_files:
        print(f"Directory: {directory}\n  {Colors.FAIL} -> /!\ Actual number of files: {len(file_list)}, Expected number of files: {expected_num_files}{Colors.ENDC}")

    for file_path in file_list:
        root_file = ROOT.TFile.Open(file_path)
        if not root_file or root_file.IsZombie():
            print(f"Error: Unable to open file {file_path}")
            continue

        check_events(root_file, expected_num_events)
        root_file.Close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory> <expected_num_files> <expected_num_events>")
        sys.exit(1)

    # Get parameters from the command-line argument
    directory = sys.argv[1]
    expected_num_files = int(sys.argv[2])
    expected_num_events = int(sys.argv[3])

    # Check all files in the directory
    check_files_in_directory(directory, expected_num_files, expected_num_events)
