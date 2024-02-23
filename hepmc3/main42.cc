#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"

using namespace Pythia8;

int main(int argc, char* argv[]) 
{

  // Check number of command-line arguments.
  if (argc != 4) {
    cerr << " Unexpected number of command-line arguments. \n"
         << " Please specify:\n"
         << "   1) command file cmnd\n"
         << "   2) event file path lhe\n"
         << "   3) output file hepmc3\n"
         << " \n E.g. run \n"
         << "   ./main280 main280.cmnd w+_production_lhc_ output.hepmc\n"
         << " \n Program stopped! " << endl;
    return 1;
  }

  string cmnd_name   = argv[1];
  string input_name  = argv[2];
  string output_name = argv[3];

  // Check that the provided input name corresponds to an existing file.
  ifstream is(cmnd_name.c_str());
  if (!is) {
    cerr << " Command-line file " << cmnd_name << " was not found. \n"
         << " Program stopped! " << endl;
    return 1;
  }

  // Confirm that external files will be used for input and output.
  cout << "\n >>> PYTHIA settings will be read from file " << cmnd_name
       << " <<< \n >>> LHE events will be read from file "
       << input_name << " <<< \n"
       << " <<< \n >>> HepMC events will be written to file "
       << output_name << " <<< \n" << endl;

  // Interface for conversion from Pythia8::Event to HepMC event.
  // Specify file where HepMC events will be stored.
  Pythia8ToHepMC toHepMC(output_name);

  // Generator.
  Pythia pythia;

  // Read in commands from external file.
  pythia.readFile(cmnd_name);

  // Extract settings to be used in the main program.
  int    nEvent    = pythia.mode("Main:numberOfEvents");
  int    nAbort    = pythia.mode("Main:timesAllowErrors");

  int showerModel    = pythia.mode("PartonShowers:Model");
  bool hadronisation = pythia.flag("HadronLevel:all");

  // Initialization.
  pythia.settings.mode("Beams:frameType", 4);
  pythia.settings.word("Beams:LHEF", input_name);
  pythia.init();

  // Begin event loop.
  int iAbort = 0;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) 
  {
    cout << "Event:" << iEvent << endl;
    // Generate event.
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) {
        cout << " Aborted since reached end of Les Houches Event File\n";
        break;
      }

      // First few failures write off as "acceptable" errors, then quit.
      if (++iAbort < nAbort) continue;
      cout << " Event generation aborted prematurely, owing to error!\n";
      break;
    }

    // Construct new empty HepMC event, fill it and write it out.
    toHepMC.writeNextEvent( pythia );

  // End of event loop. Statistics.
  }
  pythia.stat();

  // Done.
  return 0;
}