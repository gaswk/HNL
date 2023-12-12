# list of processes (mandatory)
processList = {
    #'REC_HNL_Majorana_eenu_90GeV_1e-5Ve' : {'fraction':1, 'crossSection': 2.29*10**(-8)}, # m_HNL 50 GeV, V_eN 1 × 10−5
    'REC_HNL_Majorana_eenu_30GeV_1p41e-6Ve' : {'fraction':1, 'crossSection': 6.637*10**(-10)},  # m_HNL 30 GeV, V_eN 1.41 × 10−6
    'REC_HNL_Majorana_eenu_50GeV_1p41e-6Ve' : {'fraction':1, 'crossSection': 4.535*10**(-10)},  # m_HNL 50 GeV, V_eN 1.41 × 10−6
    'REC_HNL_Majorana_eenu_70GeV_1p41e-6Ve' : {'fraction':1, 'crossSection': 1.968*10**(-10)},  # m_HNL 70 GeV, V_eN 1.41 × 10−6
    'REC_HNL_Majorana_eenu_90GeV_1p41e-6Ve' : {'fraction':1, 'crossSection': 1.749*10**(-12)},  # m_HNL 90 GeV, V_eN 1.41 × 10−6
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

procDictAdd={
    "REC_HNL_Majorana_eenu_30GeV_1p41e-6Ve":{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 6.637*10**(-10), "kfactor": 1.0, "matchingEfficiency": 1.0},
    "REC_HNL_Majorana_eenu_50GeV_1p41e-6Ve":{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.535*10**(-10), "kfactor": 1.0, "matchingEfficiency": 1.0},
    "REC_HNL_Majorana_eenu_70GeV_1p41e-6Ve":{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.968*10**(-10), "kfactor": 1.0, "matchingEfficiency": 1.0},
    "REC_HNL_Majorana_eenu_90GeV_1p41e-6Ve":{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.749*10**(-12), "kfactor": 1.0, "matchingEfficiency": 1.0},
    }


includePaths = ["functions_HNL.h"]


# additional/custom C++ functions, defined in header files (optional)
#includePaths = ["functions.h"]

# Define the input dir (optional)
#inputDir = "/eos/user/g/gasadows/Output/HNL/"
inputDir = "/eos/experiment/fcc/ee/analyses_storage/BSM/HNL_ee/"

#Optional: output directory, default is local running directory
outputDir   = "."


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 150000000 # 150 /ab



# define some binning for various histograms
#bins_theta_el = (100, -90, 90) 

bin_mcpdg = (101, -50, 50)
bin_genStatus = (50, 0, 50)

bins_theta_el = (62, 0, 3.1415)
bins_p_el     = (100, 0, 50) # 100 MeV bins
bins_pt_el    = (100, 0, 50) # 100 MeV bins
bin_delatR = (500, 0, 20)
bins_iso = (500, 0, 0.4)
bins_count = (10, -0.5, 9.5)
bins_invmass= (100, 0, 100)
bins_missingPT= (100, 0, 60)
bins_vertex_r= (100, 0, 100)
bins_vertex_z= (100, 0, 100)
bins_vertex_dist= (100, 0, 1000)
bins_track_d0= (80, -20, 20)

bins_vertex_x_all= (100, 0, 70)
bins_vertex_Lxyz_all= (100, 0, 1000)

bins_2D = (100, 0, 100, 100, 0, 100)

bins_pull_r = (100, 0, 0.3)
bins_pull = (100, -0.1, 0.1)

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):
    
    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    # define some aliases to be used later on
    
    #Pandora PF particles
    df = df.Alias("ReconstructedParticles", "PandoraPFOs")
    #MC particles particles
    df = df.Alias("GenParticles", "MCParticles")
    
    df = df.Define("MC_pdgs", "MCParticle::get_pdg(MCParticles)")

    results.append(df.Histo1D(("MC_pdgs_distrib",     "", *bin_mcpdg),     "MC_pdgs"    ))

    df = df.Define("MC_electrons", "FCCAnalyses::MCParticle::sel_pdgID(11, true) (MCParticles)")
    df = df.Define("MC_electrons_status1", "FCCAnalyses::MCParticle::sel_genStatus(1) (MC_electrons)") #gen status==1 means final state particle (FS)

    df = df.Define("MC_electron_genStatus", "MCParticle::get_genStatus(MC_electrons)")
    results.append(df.Histo1D(("MC_electron_genStatus_distrib",     "", *bin_genStatus),     "MC_electron_genStatus"    ))

    df = df.Define("MC_electrons_p",     "FCCAnalyses::MCParticle::get_p(MC_electrons_status1)")
    df = df.Define("MC_electrons_pt",    "FCCAnalyses::MCParticle::get_pt(MC_electrons_status1)")
    df = df.Define("MC_electrons_theta", "FCCAnalyses::MCParticle::get_theta(MC_electrons_status1)")

    results.append(df.Histo1D(("MC_electrons_p",     "", *bins_p_el),     "MC_electrons_p"    ))
    results.append(df.Histo1D(("MC_electrons_pt",    "", *bins_pt_el),    "MC_electrons_pt"   ))
    results.append(df.Histo1D(("MC_electrons_theta", "", *bins_theta_el), "MC_electrons_theta"))

    # ee invariant mass
    df = df.Define("MC_electrons_n",    "FCCAnalyses::MCParticle::get_n(MC_electrons_status1)")
    df = df.Define("MC_electrons_e", "FCCAnalyses::MCParticle::get_e(MC_electrons_status1)")
    df = df.Define("MC_electrons_px", "FCCAnalyses::MCParticle::get_px(MC_electrons_status1)")
    df = df.Define("MC_electrons_py", "FCCAnalyses::MCParticle::get_py(MC_electrons_status1)")
    df = df.Define("MC_electrons_pz", "FCCAnalyses::MCParticle::get_pz(MC_electrons_status1)")
    df = df.Define("FSGen_ee_energy", "if (MC_electrons_n>1) return (MC_electrons_e.at(0) + MC_electrons_e.at(1)); else return float(-1.);")
    df = df.Define("FSGen_ee_px", "if (MC_electrons_n>1) return (MC_electrons_px.at(0) + MC_electrons_px.at(1)); else return float(-1.);")
    df = df.Define("FSGen_ee_py", "if (MC_electrons_n>1) return (MC_electrons_py.at(0) + MC_electrons_py.at(1)); else return float(-1.);")
    df = df.Define("FSGen_ee_pz", "if (MC_electrons_n>1) return (MC_electrons_pz.at(0) + MC_electrons_pz.at(1)); else return float(-1.);")
    df = df.Define("FSGen_ee_invMass", "if (MC_electrons_n>1) return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz ); else return float(-1.);")
    results.append(df.Histo1D(("FSGen_ee_invMass", "",    *bins_invmass),    "FSGen_ee_invMass"))

    ## test of particule vertex position (initial for electrons)
    df = df.Define("gen_Vertex_x_distrib_all", "FCCAnalyses::MCParticle::get_vertex_x(MCParticles)")
    results.append(df.Histo1D(("gen_Vertex_x_distrib_all", "",    *bins_vertex_x_all),    "gen_Vertex_x_distrib_all")) 
    #df = df.Define("gen_Vertex_x_distrib_electrons_status3", "FCCAnalyses::MCParticle::get_vertex_x(MC_electrons_status1)")
    df = df.Define("MC_electrons_status23", "FCCAnalyses::MCParticle::sel_genStatus(23) (MC_electrons)")
    df = df.Define("gen_Vertex_x_distrib_electrons_status23", "FCCAnalyses::MCParticle::get_vertex_x(MC_electrons_status23)")
    results.append(df.Histo1D(("gen_Vertex_x_distrib_fromHNL", "",    *bins_vertex_x_all),    "gen_Vertex_x_distrib_electrons_status23")) 

    df = df.Define("gen_vertex_Lxyz", "FCCAnalyses::HNLfunctions::gen_vertex_Lxyz(MC_electrons_status23)")
    results.append(df.Histo1D(("gen_Vertex_Lxyz_distrib_fromHNL", "",    *bins_vertex_Lxyz_all),    "gen_vertex_Lxyz")) 

    
    #df = df.Define("MCParents_Ind", "_MCParticles_parents")
    #df = df.Define("MCElectrons_from_HNL", "FCCAnalyses::HNLfunctions::MCElectrons_from_HNL(MCParticles, MCParents_Ind)")
    #df = df.Define("gen_Vertex_x_distrib_fromHNL", "FCCAnalyses::MCParticle::get_vertex_x(MCElectrons_from_HNL)")
    
    #results.append(df.Histo1D(("gen_Vertex_x_distrib_fromHNL", "",    *bins_vertex_x_all),    "gen_Vertex_x_distrib_fromHNL")) 



    ## look at HNL particles
    df = df.Define("MC_HNL", "FCCAnalyses::MCParticle::sel_pdgID(9900012, true) (MCParticles)")

    df = df.Define("MC_HNL_p",     "FCCAnalyses::MCParticle::get_p(MC_HNL)")
    df = df.Define("MC_HNL_pt",    "FCCAnalyses::MCParticle::get_pt(MC_HNL)")
    df = df.Define("MC_HNL_theta", "FCCAnalyses::MCParticle::get_theta(MC_HNL)")
    df = df.Define("MC_HNL_mass", "FCCAnalyses::MCParticle::get_mass(MC_HNL)")

    results.append(df.Histo1D(("MC_HNL_p",     "", *bins_p_el),     "MC_HNL_p"    ))
    results.append(df.Histo1D(("MC_HNL_pt",    "", *bins_pt_el),    "MC_HNL_pt"   ))
    results.append(df.Histo1D(("MC_HNL_theta", "", *bins_theta_el), "MC_HNL_theta"))
    results.append(df.Histo1D(("MC_HNL_mass", "", *bins_invmass), "MC_HNL_mass"))
    
    df = df.Define("MC_HNL_vertex_r", "FCCAnalyses::HNLfunctions::gen_vertex_r (MC_electrons_status1)")
    results.append(df.Histo1D(("gen_Vertex_r_distrib", "",    *bins_vertex_r),    "MC_HNL_vertex_r")) 


    df = df.Define("MC_HNL_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x(MC_electrons_status1)")
    results.append(df.Histo1D(("gen_Vertex_x_distrib", "",    *bins_vertex_r),    "MC_HNL_vertex_x")) 



    ##look aat reco objects
    df = df.Define("electrons_all",    "ReconstructedParticle::sel_absType(11) ( ReconstructedParticles )")
    #df = df.Define("electrons_all", "ReconstructedParticle::sel_electrons(0) ( ReconstructedParticles )")
  
    # select leptons with momentum > 20 GeV
    #df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")
    
     # select leptons with momentum > 5 GeV
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(5)(electrons_all)")

    # compute the electron isolation and store electrons with an isolation cut of 0.25 in a separate column electrons_sel_iso
    df = df.Define("electrons_iso",     "FCCAnalyses::HNLfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
    df = df.Define("electrons_sel_iso", "FCCAnalyses::HNLfunctions::sel_iso(0.25)(electrons, electrons_iso)")

    df = df.Define("electrons_p",     "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_pt",    "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("electrons_no",    "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
    df = df.Define("electrons_q",     "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        
    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("electrons_p_cut0",     "", *bins_p_el),     "electrons_p"    ))
    results.append(df.Histo1D(("electrons_pt_cut0",    "", *bins_pt_el),    "electrons_pt"   ))
    results.append(df.Histo1D(("electrons_theta_cut0", "", *bins_theta_el), "electrons_theta"))
    results.append(df.Histo1D(("electrons_iso_cut0",   "", *bins_iso),      "electrons_iso"))
    results.append(df.Histo1D(("electrons_no_cut0",    "", *bins_count),    "electrons_no"))


    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: at least 1 electron with at least one isolated one
    #########
    df = df.Filter("electrons_no >= 1 && electrons_iso.size() > 0")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2 :at least 2 opposite-sign (OS) isolated leptons
    #########
    df = df.Filter("electrons_no == 2 && electrons_iso.size() == 2 && abs(Sum(electrons_q)) < electrons_q.size()")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))
    
    df = df.Define("dilepton_system_build", "FCCAnalyses::HNLfunctions::dilepton_sys()(electrons)")
    
    df = df.Define("electrons_invmass", "FCCAnalyses::ReconstructedParticle::get_mass(dilepton_system_build)[0]") # recoil mass


    results.append(df.Histo1D(("electrons_invmass",    "", *bins_invmass),    "electrons_invmass"))



    #########
    ### CUT 3: Z mass window
    #########  
    df = df.Filter("electrons_invmass < 86 || electrons_invmass > 96")
    df = df.Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))


    df = df.Define("missingEnergy",       "FCCAnalyses::HNLfunctions::missingEnergy(91., ReconstructedParticles)")
    df = df.Define("missingEnergy_pt",    "FCCAnalyses::ReconstructedParticle::get_pt(missingEnergy)")

    #results.append(df.Histo1D(("missingEnergy_pt", "", *bins_missingPT), "missingEnergy_pt")) # plot it before the cut
    results.append(df.Histo1D(("missingEnergy_pt", "", *bins_missingPT), "missingEnergy_pt")) # plot it before the cut



    #########
    ### CUT 4: missing Et Cuts
    #########  
    #df = df.Filter("missingEnergy_pt > 86")
    #df = df.Define("cut4", "4")
    #results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    #df = df.Alias("ReconstructedTracks", "SiTracks_Refitted_trackStates")
    df = df.Alias("ReconstructedTracksStates", "_SiTracks_Refitted_trackStates")
    df = df.Alias("ReconstructedTracksData", "SiTracks")
    df = df.Define("TracksAtIP", "FCCAnalyses::ReconstructedTrack::TrackStates_at_IP(ReconstructedTracksData, ReconstructedTracksStates)")
    #df = df.Define("TracksAtFistHit", "FCCAnalyses::ReconstructedTrack::TrackStates_at_FirstHit(ReconstructedTracksData, ReconstructedTracksStates)")
    df = df.Define("trackStates_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK(electrons, TracksAtIP)")
    #df = df.Define("trackStates_electrons", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK(electrons, TracksAtFistHit)")
    ##df = df.Define("trackStates_electrons2", "FCCAnalyses::Track::selPDG(11, true) (MCTruthSiTracksLink)")
    df = df.Define("track_d0",    "FCCAnalyses::HNLfunctions::getD0(trackStates_electrons)")
    ##df = df.Define("D0_o", "trackStates_electrons.D0")
    results.append(df.Histo1D(("track_d0", "", *bins_track_d0), "track_d0"))  

    #vertex reconstruction, first attempts...
    df = df.Define("VertexObject_DiElectrons",  "FCCAnalyses::VertexFitterSimple::VertexFitter ( 1, electrons, trackStates_electrons) ")
    df = df.Define("Vertex",   "VertexingUtils::get_VertexData( VertexObject_DiElectrons )")   # primary vertex, in mm


    #df = df.Define("Vertex_r",      "FCCAnalyses::HNLfunctions::vertex_r(Vertex)")   # primary vertex, in mm
    #df = df.Define("Vertex_z",      "FCCAnalyses::HNLfunctions::vertex_z(Vertex)")   # primary vertex, in mm
    df = df.Define("Vertex_dist",   "FCCAnalyses::HNLfunctions::vertex_dist(Vertex)")   # primary vertex, in mm

    #results.append(df.Histo1D(("Vertex_r", "",    *bins_vertex_r),    "Vertex_r")) 
    #results.append(df.Histo1D(("Vertex_z", "",    *bins_vertex_z),    "Vertex_z")) 
    results.append(df.Histo1D(("Vertex_dist", "", *bins_vertex_dist), "Vertex_dist")) 

    results.append(df.Histo2D(("2D_gen_vs_rec_Lxyz", "", *bins_2D), "gen_vertex_Lxyz", "Vertex_dist"))

    df = df.Define("Vertex_diff_Lxyz", "FCCAnalyses::HNLfunctions::Vertex_diff_Lxyz(MC_electrons_status23, Vertex)")
    df = df.Define("Vertex_diff_r", "FCCAnalyses::HNLfunctions::Vertex_diff_r(MC_electrons_status23, Vertex)")
    df = df.Define("Vertex_diff_x", "FCCAnalyses::HNLfunctions::Vertex_diff_x(MC_electrons_status23, Vertex)")
    df = df.Define("Vertex_diff_y", "FCCAnalyses::HNLfunctions::Vertex_diff_y(MC_electrons_status23, Vertex)")
    df = df.Define("Vertex_diff_z", "FCCAnalyses::HNLfunctions::Vertex_diff_z(MC_electrons_status23, Vertex)")


    results.append(df.Histo1D(("Vertex_diff_Lxyz", "", *bins_pull_r), "Vertex_diff_Lxyz")) 
    results.append(df.Histo1D(("Vertex_diff_r", "", *bins_pull_r), "Vertex_diff_r")) 
    results.append(df.Histo1D(("Vertex_diff_x", "", *bins_pull), "Vertex_diff_x")) 
    results.append(df.Histo1D(("Vertex_diff_y", "", *bins_pull), "Vertex_diff_y")) 
    results.append(df.Histo1D(("Vertex_diff_z", "", *bins_pull), "Vertex_diff_z")) 
    

    #test primary vertex reconstruction with no constrains.
    
    #df = df.Alias("UnconstrainedVertex", "PrimaryVertices_res")

    #df = df.Define("Vertex_reco_Lxyz",      "FCCAnalyses::HNLfunctions::reco_vertex_Lxyz (UnconstrainedVertex)")   # primary vertex, in mm

    #results.append(df.Histo1D(("RecoVertex_Lyxz", "", *bins_vertex_Lxyz_all), "Vertex_reco_Lxyz")) 

    return results, weightsum