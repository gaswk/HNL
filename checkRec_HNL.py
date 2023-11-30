import os
import sys
import ROOT

# ANSI escape codes for text formatting
class Colors:
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'     # Red
    ENDC = '\033[0m'      # End formatting

def check_events_electrons_tracks_hits(root_file, expected_num_events, min_electron_percentage, min_track_percentage):
    tree = root_file.Get("events")

    if not tree:
        print(f"Error: Unable to find TTree named 'events' in {root_file.GetName()}")
        return

    # Get the TBranches
    electron_type_branch = tree.GetBranch("PandoraPFOs.type")
    track_branch = tree.GetBranch("SiTracks_Refitted")

    # Get the leaves
    electron_type_leaf = electron_type_branch.GetLeaf("PandoraPFOs.type")

    # Get the number of events
    num_events = tree.GetEntries()

    # Initialize counts
    electron_count = 0
    track_count = track_branch.GetEntries()

    # Loop over events to count electrons
    for event in range(num_events):
        tree.GetEntry(event)

        # Count electrons
        electrons = [electron_type_leaf.GetValue(entry) for entry in range(electron_type_branch.GetEntries())]
        electron_count += any(electron == abs(11) for electron in electrons) and any(electron == -abs(11) for electron in electrons)

        # Count tracks
        track_count += track_branch.GetEntries()

    warnings_or_fail = False  # Flag to track warnings or fails

    if num_events != expected_num_events:
        print(f"File: {root_file.GetName()}\n  {Colors.FAIL} -> /!\ Actual events: {num_events}, Expected events: {expected_num_events}{Colors.ENDC}")
        warnings_or_fail = True

    if electron_count < min_electron_percentage * num_events:
        print(f"File: {root_file.GetName()}\n  {Colors.WARNING} -> Only {electron_count}/{num_events} events have at least two reconstructed electrons of opposite signs{Colors.ENDC}")
        warnings_or_fail = True

    if track_count < min_track_percentage * num_events:
        print(f"File: {root_file.GetName()}\n  {Colors.FAIL} -> /!\ Only {track_count} events have at least two reconstructed tracks{Colors.ENDC}")
        warnings_or_fail = True

    if warnings_or_fail:
        print()  # Add a new line before the next file

def check_files_in_directory(directory, expected_num_files, expected_num_events, min_electron_percentage, min_track_percentage):
    file_list = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.root')]

    if len(file_list) != expected_num_files:
        print(f"Directory: {directory}\n  {Colors.FAIL} -> /!\ Actual number of files: {len(file_list)}, Expected number of files: {expected_num_files}{Colors.ENDC}")

    for file_path in file_list:
        root_file = ROOT.TFile.Open(file_path)
        if not root_file or root_file.IsZombie():
            print(f"Error: Unable to open file {file_path}")
            continue

        check_events_electrons_tracks_hits(root_file, expected_num_events, min_electron_percentage, min_track_percentage)
        root_file.Close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory> <expected_num_files> <expected_num_events>")
        sys.exit(1)

    # Get parameters from the command-line argument
    directory = sys.argv[1]
    expected_num_files = int(sys.argv[2])
    expected_num_events = int(sys.argv[3])

    # Expected values
    #expected_num_events = 5000  # Number expected number of events
    min_electron_percentage = 0.8    # Acceptable pourcentage of event with at least 2 reconstructed electrons of opposite signs
    min_track_percentage = 0.8   # Acceptable pourcentage of event with at least 2 reconstructed tracks

    # Check all files in the directory
    check_files_in_directory(directory, expected_num_files, expected_num_events, min_electron_percentage, min_track_percentage)
