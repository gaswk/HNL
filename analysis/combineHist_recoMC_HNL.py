import ROOT

ROOT.gROOT.SetBatch(True) 

def combine_Hist(canvas, blue_hist, red_hist, input_file, legend_title, x_axis_title):
    blue_hist.SetLineColor(ROOT.kBlue)
    red_hist.SetLineColor(ROOT.kRed)
    blue_hist.Draw()
    blue_hist.SetStats(0)  # Disable statistics box 
    red_hist.Draw("same")
    red_hist.SetStats(0)  # Disable statistics box 

    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    legend.SetTextFont(62)
    legend.SetTextSize(0.03)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetMargin(0.1)    # distance between marker and text
    legend.SetHeader(legend_title)
    legend.AddEntry(blue_hist, "MC", "l")
    legend.AddEntry(red_hist, "Reco", "l")
    legend.Draw()

    blue_hist.GetXaxis().SetTitle(x_axis_title)

    canvas.Write(f"Combined_{legend_title}")    
    canvas.Print(f"{output_file_name}.pdf", "pdf")

    canvas.Clear()

def combine_Hist_normalised(canvas, blue_hist, red_hist, input_file, legend_title, x_axis_title):
    blue_hist.SetLineColor(ROOT.kBlue)
    red_hist.SetLineColor(ROOT.kRed)
    blue_hist.DrawNormalized()
    blue_hist.SetStats(0)  # Disable statistics box 
    red_hist.DrawNormalized("same")
    red_hist.SetStats(0)  # Disable statistics box 

    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    legend.SetTextFont(62)
    legend.SetTextSize(0.03)
    legend.SetMargin(0.1)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetHeader(legend_title)
    legend.SetHeader(f"{legend_title} Normalised")
    legend.AddEntry(blue_hist, "MC", "l")
    legend.AddEntry(red_hist, "Reco", "l")
    legend.Draw()

    blue_hist.GetXaxis().SetTitle(x_axis_title)

    canvas.Write(f"Combined_{legend_title}_Normalised")
    canvas.Print(f"{output_file_name}.pdf", "pdf")

    canvas.Clear()

#_____________________________________________________________________________
# Open the input ROOT file
input_file = ROOT.TFile("/afs/cern.ch/user/g/gasadows/FCCAnalyses/tutorial/HNL_50_merged_REC_EDM4Hep.root", "READ")

# Get the histograms you want to superimpose
hist1_blue = input_file.Get("MC_electrons_pt")
hist1_red = input_file.Get("electrons_pt_cut0")

hist2_blue = input_file.Get("MC_electrons_theta")
hist2_red = input_file.Get("electrons_theta_cut0")

hist3_blue = input_file.Get("gen_Vertex_Lxyz_distrib_fromHNL")
hist3_red = input_file.Get("Vertex_dist")

# Create a canvas to draw the histograms
canvas = ROOT.TCanvas("canvas", "Superimposed Histograms", 800, 800)

# Create output file root and pdf
output_file_name = "combined_reco_MC_HNL"
output_file_root = ROOT.TFile(f"{output_file_name}.root", "RECREATE")
output_file_pdf = canvas
output_file_pdf.Print(f"{output_file_name}.pdf[")

# Superimpose and save histograms with legends
combine_Hist(canvas, hist1_blue, hist1_red, input_file, "electrons p_{T}", "p_{T} [GeV]")
combine_Hist(canvas, hist2_blue, hist2_red, input_file, "electrons theta", "#theta [rad]")
combine_Hist(canvas, hist3_blue, hist3_red, input_file, "Vertex displacement", "Displacement [cm]")

# Superimpose and save histograms with legends Normalised
combine_Hist_normalised(canvas, hist1_blue, hist1_red, input_file, "electrons p_{T}", "p_{T} [GeV]")
combine_Hist_normalised(canvas, hist2_blue, hist2_red, input_file, "electrons theta", "#theta [rad]")
combine_Hist_normalised(canvas, hist3_blue, hist3_red, input_file, "Vertex displacement", "Displacement [cm]")

# Close files
input_file.Close()
output_file_root.Close()

# Print the pdf file
output_file_pdf.Print(f"{output_file_name}.pdf]")