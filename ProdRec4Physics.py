import os
import sys
import argparse
import subprocess
import time
import ROOT  
ts = time.time()


parser = argparse.ArgumentParser(description="Script for running CLD fullsim on Condor")
parser.add_argument("-Nevts_tot", help="Number of events in the hepmc file", required=True)
parser.add_argument("-Nevts_per_job", help="Number of events per condor job", required=True)
parser.add_argument("-Sample", help="Name of the sample", required=True)
parser.add_argument("-output_rec", help="Output file path", required=True)
parser.add_argument("-inputFiles", help="input file path ", required=True)


args = parser.parse_args()

# ==========================
# Parameters Initialisation
# ==========================
DetectorModelList_ = ["FCCee_o1_v04"]
# setup = "/cvmfs/sw.hsf.org/key4hep/setup.sh"
setup = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

# ===========================
# Directory Setup and Checks
# ===========================
output_dir = args.output_rec+"_"+args.Sample
output_dir_aida = args.output_rec+"_"+args.Sample+"/aida_outputs"
directory_sample = "ProdJobs_"+args.Sample+"_REC"

JobFlavour = "tomorrow"
# Job flavours:
#   espresso     = 20 minutes
#   microcentury = 1 hour
#   longlunch    = 2 hours
#   workday      = 8 hours
#   tomorrow     = 1 day
#   testmatch    = 3 days
#   nextweek     = 1 week

N_jobs = int(int(args.Nevts_tot) / int(args.Nevts_per_job))
print("N_jobs = ", N_jobs)

# Check if the directory exists and exit if it does
if os.path.exists(directory_sample):
    print(f"Error: Directory '{directory_sample}' already exists and should not be overwritten.")
    sys.exit(1)

# Create output directories if they don't exist
[os.makedirs(directory, exist_ok=True) for directory in [directory_sample, output_dir, output_dir_aida]]

# =======================
# Reconstruction Job Creation 
# =======================
for ijob in range(N_jobs):
   outputfileName = args.Sample +"_"+str(ijob)+"_REC"

   # Check if the input file exists
   inputFile = args.inputFiles + "/" + args.Sample + "/" + args.Sample + "_" + str(ijob) + "_evts_edm4hep.root"
   #inputFile = args.inputFiles + "/" + args.Sample + "/" + args.Sample + "_" + str(ijob) + "_evts.slcio"
   if not os.path.exists(inputFile):
     print(f"Error: Input file {inputFile} does not exist. Skipping job.")
     continue 

   # Check if the output file already exists and has correct Nb of events
   output_file = output_dir +"/"+ outputfileName + "_edm4hep.root"
   if os.path.exists(output_file):
      root_file = ROOT.TFile(output_file, "READ")
      events_tree = root_file.Get("events")
      if events_tree:
          if events_tree.GetEntries() == int(args.Nevts_per_job):
              root_file.Close()
              continue
      root_file.Close()

   bash_file = directory_sample + f"/bash_script_{ijob}.sh"
   with open(bash_file, "w") as file:
      file.write("#!/bin/bash \n")
      file.write("source " + setup + "\n")
      file.write("git clone https://github.com/key4hep/CLDConfig.git"+"\n")
      file.write("cd CLDConfig/CLDConfig/"+"\n")
      arguments = f" --GeoSvc.detectors=$K4GEO/FCCee/CLD/compact/{DetectorModelList_[0]}/{DetectorModelList_[0]}.xml --inputFiles " + inputFile + " --outputBasename  " + outputfileName+ " -n " + args.Nevts_per_job
      command = "k4run CLDReconstruction.py " + arguments + " > /dev/null"
      file.write(command+"\n")
      file.write(f"xrdcp {outputfileName}_edm4hep.root  root://eosuser.cern.ch/{output_dir} \n")
      file.write(f"xrdcp {outputfileName}_aida.root  root://eosuser.cern.ch/{output_dir_aida} \n")
      file.close()
	
# ============================
# Condor Submission Script
# ============================
# Write the condor submission script
condor_script = (
    "executable = $(filename) \n"
    "arguments = $(ClusterId) $(ProcId) \n"
    "output = output.$(ClusterId).$(ProcId).out \n"
    "error = error.$(ClusterId).$(ProcId).err \n"
    "log = log.$(ClusterId).log \n"
    f"+JobFlavour = \"{JobFlavour}\" \n"  
    "queue filename matching files *.sh \n"
)
condor_file = directory_sample + "/condor_script.sub"
with open(condor_file, "w") as file2:
    file2.write(condor_script)
    file2.close()

# ====================
# Submit Job to Condor
# ====================
os.system("cd "+ directory_sample + "; condor_submit condor_script.sub")





