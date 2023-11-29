import os
import argparse
import subprocess
import time;
ts = time.time()


parser = argparse.ArgumentParser(description="Script for running CLD fullsim on Condor")
parser.add_argument("-Nevts_tot", help="Number of events in the hepmc file", required=True)
parser.add_argument("-Nevts_per_job", help="Number of events per condor job", required=True)
parser.add_argument("-Sample", help="Name of the sample", required=True)
parser.add_argument("-output_edm4hep", help="Output file path", required=True)
parser.add_argument("-inputFiles", help="input file path ", required=True)


args = parser.parse_args()

DetectorModelList_ = ["FCCee_o1_v04"]
SteeringFile = "/afs/cern.ch/user/g/gasadows/CLDConfig/CLDConfig/CLDReconstruction_dect.py"
Config_Value_Path = "/afs/cern.ch/user/g/gasadows/CLDConfig/CLDConfig/"
os.system("mkdir "+args.output_edm4hep+"_"+args.Sample+"_RECO_EDM4Hep/")
#setup = "/cvmfs/sw.hsf.org/key4hep/setup.sh"
setup = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

N_jobs = int( int(args.Nevts_tot)/int(args.Nevts_per_job)) +1

print( N_jobs)

directory_sample = "ProdJobs_"+args.Sample+"_RECO_EDM4Hep"
os.system("mkdir "+directory_sample)
   
    # Create the content for config_values.py
            config_content = f'''
DetectorModel = "{DetectorModelPath}"
    '''
            print(config_content)

            # Write the content to config_values.py and overwrite the file if it already exists
            with open(f"{Config_Value_Path}config_values.py", "w") as file:
                file.write(config_content)   

skip_events = 0
for ijob in range(N_jobs-1):

   directory_job = directory_sample+"/Jobs_"+str(ijob)
   os.system("mkdir "+directory_job)
   print("creating job "+str(ijob)+ " in directory " +directory_job)
   bash_file = directory_job + "/bash_script.sh"
   with open(bash_file, "w") as file:
      file.write("#!/bin/bash \n")
      file.write("source " + setup + "\n")
      file.write("git clone https://github.com/key4hep/CLDConfig.git"+"\n")
      file.write("cd CLDConfig/CLDConfig/"+"\n")
      outputfileName = "HNL_50_"+str(ijob)+"_REC_EDM4Hep.root"
      arguments = " --inputFiles " + args.inputFiles +"/"+args.Sample+"/"+args.Sample+"_"+str(ijob)+"_evts_edm4hep.root --filename.PodioOutput  " + outputfileName+ " -n " + args.Nevts_per_job
      command = f"k4run {SteeringFile} " + arguments
      file.write(command+"\n")
      file.write("cp "+ outputfileName + "  " + args.output_edm4hep+"_"+args.Sample+"_RECO_edm4hep"+"/."+"\n")
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





