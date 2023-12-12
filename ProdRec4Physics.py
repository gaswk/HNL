import os
import argparse
import subprocess
import time
import ROOT  
ts = time.time()


parser = argparse.ArgumentParser(description="Script for running CLD fullsim on Condor")
parser.add_argument("-Nevts_tot", help="Number of events in the hepmc file", required=True)
parser.add_argument("-Nevts_per_job", help="Number of events per condor job", required=True)
parser.add_argument("-Sample", help="Name of the sample", required=True)
parser.add_argument("-output_edm4hep", help="Output file path", required=True)
parser.add_argument("-inputFiles", help="input file path ", required=True)


args = parser.parse_args()

DetectorModelList_ = ["FCCee_o1_v04"]
Config_Value_Path = "/afs/cern.ch/user/g/gasadows/CLDConfig/CLDConfig/"
output_dir = args.output_edm4hep+"_"+args.Sample
output_dir_aida = args.output_edm4hep+"_"+args.Sample+"/aida_outputs"
os.system("mkdir "+output_dir)
os.system("mkdir "+output_dir_aida)
#setup = "/cvmfs/sw.hsf.org/key4hep/setup.sh"
setup = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

N_jobs = int( int(args.Nevts_tot)/int(args.Nevts_per_job)) 

print("N_jobs = ", N_jobs)

directory_sample = "ProdJobs_"+args.Sample+"_REC"
os.system("mkdir "+directory_sample)

skip_events = 0
for ijob in range(N_jobs):
   directory_job = directory_sample+"/Jobs_"+str(ijob)
   os.system("mkdir "+directory_job)
   print("creating job "+str(ijob)+ " in directory " +directory_job)
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
              print(f"Output file {output_file} already exists and has correct Nb of events. Skipping job.")
              root_file.Close()
              continue
      root_file.Close()

   bash_file = directory_job + "/bash_script.sh"
   with open(bash_file, "w") as file:
      file.write("#!/bin/bash \n")
      file.write("source " + setup + "\n")
      file.write("git clone https://github.com/key4hep/CLDConfig.git"+"\n")
      file.write("cd CLDConfig/CLDConfig/"+"\n")
      arguments = f" --GeoSvc.detectors=$K4GEO/FCCee/CLD/compact/{DetectorModelList_[0]}/{DetectorModelList_[0]}.xml --inputFiles " + inputFile + " --outputBasename  " + outputfileName+ " -n " + args.Nevts_per_job
      command = "k4run CLDReconstruction.py " + arguments + " > /dev/null"
      file.write(command+"\n")
      file.write("cp "+ outputfileName + "_edm4hep.root" + "  " + output_dir +"\n")
      file.write("cp "+ outputfileName + "_aida.root" + "  " + output_dir_aida +"\n")
      file.close()
	
   condor_file = directory_job + "/condor_script.sub"
   print(condor_file)
   with open(condor_file, "w") as file2:
        file2.write("executable = bash_script.sh \n")
        file2.write("arguments = $(ClusterId) $(ProcId) \n")
        file2.write("output = output.$(ClusterId).$(ProcId).out \n")
        file2.write("error = error.$(ClusterId).$(ProcId).err \n")
        file2.write("log = log.$(ClusterId).log \n")
        #file2.write("+JobFlavour = \"espresso\" \n")
        #file2.write("+JobFlavour = \"microcentury\" \n")
        file2.write("+JobFlavour = \"workday\" \n")
        file2.write("queue \n")
        file2.close()
   os.system("cd "+ directory_job + "; condor_submit condor_script.sub")





