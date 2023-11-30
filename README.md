# HNL

Here is an example of HNL (long lived particle) production for CLD full simulation and reconstruction.
## Generate HNL
 One needs first to generated HNL events in the hepmc3 format (so including hadronisation). HNL lhe files can be produced with madgraph, following same production as for the FCC HNL analysis in [arXiv:2203.05502v4](https://arxiv.org/pdf/2203.05502.pdf). The madgraph parameters can be found at [MG Card](https://github.com/FCC-LLP/FCCAnalyses/blob/master/examples/FCCee/bsm/LLPs/DisplacedHNL/HNL_sample_creation/mg5_proc_card_HNL_Majorana_eenu_50GeV_1p41e-6Ve.dat). 

The madgraph HNL model can be found at the link below. The tgz file has to be unziped within the "models" directory of madgraph. 

[HNL MG5 model](https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/HeavyN/SM_HeavyN_CKM_AllMasses_LO.tgz)
 
Generations can be simply be done with the following command :
 
 ```
bin/mg5_aMC mg5_proc_card_HNL_Majorana_eenu_50GeV_1p41e-6Ve.dat
 ```
 Once the generation is done, the hepmc file is produced in the "events" directory of the process directory. It has to be unzipped in a dedicated directory. 

 Then run pythia standalone to produce HEPMC3 file.The hepmc file has to be reached by condor, so it has to be either on AFS or EOS.

**Simulation of displaced vertex require status code 2 for the HNL, while it is status 22 out of pythia**, [script to change the status in HEPMC3](https://github.com/gaswk/HNL/blob/main/hep_status22_to_2.py), example of usage:
```
python hep_status22_to_2.py input.hepmc output.hepmc
```

## Simulation and Reconstruction with CLD FullSim

Then, move to where (on lxplus) you want to run the scripts and get the CLDConfig repo:
```
git clone https://github.com/key4hep/CLDConfig.git
```

The simulation can be launch from the script:
```
python condorJobs_simHNL.py -Nevts_tot="50000" -Nevts_per_job="1000" \
        -Sample="HNL_Majorana_eenu_50GeV_1p41e-6Ve" \
        -output_sclio="Output/HNL/" \
        -inputFiles="HNL_Majorana_eenu_90GeV_1p41e-6Ve.hepmc"
```
```Nevts_tot``` is the total number of events, ```Nevts_per_job``` is the number of events per job. The number of jobs is determined automatically from ```Nevts_tot``` and ```Nevts_per_job```. ```Sample``` is the sample name, note that it should match the last part of the inputFiles path.

Once the simulation is produced, the reconstruction is done with the script, notes that ```Nevts_tot```, ```Nevts_per_job``` and ```Sample``` **should be the same as for the simulation**
```
python condorJobs_recoHNL.py -Nevts_tot="50000" -Nevts_per_job="1000" \
        -Sample="HNL_Majorana_eenu_50GeV_1p41e-6Ve" \
        -output_edm4hep="/eos/user/g/gasadows/Output/HNL/REC" \
        -inputFiles="/eos/user/g/gasadows/Output/HNL/"
```

Sometimes events or outputs are missing, to check that all events have been simulated and reconstructed run the following checks:
```
python checkSim_HNL.py outputSim_edm4hep.root expected_n_files expected_n_evts
```
```
python checkRec_HNL.py outputSim_edm4hep.root expected_n_files expected_n_evts
```