import ROOT

ROOT.gROOT.SetBatch(True)

def style_histogram(hist, color, style):
    hist.SetLineColor(color)
    hist.SetLineStyle(style)
    hist.SetLineWidth(3)
    #lumi = 150000000    # 150 /ab
    #Xs = 6.637*10**(-10)
    #norm = Xs*lumi
    #hist.Scale( norm / hist.Integral())
    hist.Scale(1.0 / hist.Integral())
    hist.SetStats(0)

def draw_histograms(canvas, histograms, hist_title, x_axis_title, y_axis_title, log_scale=False, y_range=None):
    # Clear the canvas before drawing new histograms
    canvas.Clear()

    # Create a legend
    legend = ROOT.TLegend(0.37, 0.73, 1.6, 0.60)
    legend.SetTextFont(62)
    legend.SetTextSize(0.035)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetMargin(0.1)

    # Draw histograms with proper scaling and axis settings
    for i, hist in enumerate(histograms):
        style_histogram(hist, colors[i], styles[i])

        # Set personalized Y-axis scale for the first histogram in each set
        if i == 0 and y_range:
            hist.GetYaxis().SetRangeUser(y_range[0], y_range[1])

        if i == 0:
            hist.Draw("HIST")
        else:
            hist.Draw("HIST same")

        legend.AddEntry(hist, legend_titles[i], "l")

    legend.Draw()

    # Set X-axis title
    histograms[0].GetXaxis().SetTitle(x_axis_title)
    histograms[0].GetXaxis().SetTitleSize(0.05)

    # Set Y-axis title (assuming the y-axis title is the same for all histograms)
    histograms[0].GetYaxis().SetTitle(y_axis_title)
    histograms[0].GetYaxis().SetTitleSize(0.04)

    # Set Y-axis to logarithmic scale
    if log_scale:
        canvas.SetLogy(True)
    else:
        canvas.SetLogy(False)

    # Get the current pad
    pad = canvas.GetPad(0)
    #pad.SetFrameLineWidth(2)
    ROOT.gStyle.SetLineWidth(2)
    # Set the position of the right and top axes
    pad.SetTickx(1)
    pad.SetTicky(1)
    # Set canvas margins
    canvas.SetBottomMargin(0.12)
    canvas.SetLeftMargin(0.12)

    # Add text on the top left above the graph
    text_left_x = 0.12
    text_left_y = 0.91
    latex_left = ROOT.TLatex()
    latex_left.SetNDC()
    latex_left.SetTextFont(72)
    latex_left.SetTextSize(0.04)
    latex_left.DrawLatexNDC(text_left_x, text_left_y, "FCC-ee CLD Full Simulation")

    # Add text as title header
    text_legend_x = 0.365
    text_legend_y = 0.73
    latex_legend = ROOT.TLatex()
    latex_legend.SetNDC()
    latex_legend.SetTextFont(42)
    latex_legend.SetTextSize(0.025)
    latex_legend.DrawLatexNDC(text_legend_x, text_legend_y, "No selection")

    # Add text on center1
    text_center1_x = 0.365
    text_center1_y = 0.82
    latex_center1 = ROOT.TLatex()
    latex_center1.SetNDC()
    latex_center1.SetTextFont(42)
    latex_center1.SetTextSize(0.035)
    latex_center1.DrawLatexNDC(text_center1_x, text_center1_y, "#sqrt{s} = 91 GeV")

    # Add text on center2
    text_center2_x = 0.365
    text_center2_y = 0.77
    latex_center2 = ROOT.TLatex()
    latex_center2.SetNDC()
    latex_center2.SetTextFont(42)
    latex_center2.SetTextSize(0.035)
    latex_center2.DrawLatexNDC(text_center2_x, text_center2_y, "e^{+}e^{-} #rightarrow N #nu, N #rightarrow ee#nu")

    canvas.Write(f"{hist_title}")
    canvas.Print(f"{output_file_name}.pdf", "pdf")
    #___________________________________________________________________________________________
# Open the input ROOT files
input_files = [
    ROOT.TFile("/afs/cern.ch/user/g/gasadows/HNL/analysis/REC_HNL_Majorana_eenu_30GeV_1p41e-6Ve.root", "READ"),
    ROOT.TFile("/afs/cern.ch/user/g/gasadows/HNL/analysis/REC_HNL_Majorana_eenu_50GeV_1p41e-6Ve.root", "READ"),
    ROOT.TFile("/afs/cern.ch/user/g/gasadows/HNL/analysis/REC_HNL_Majorana_eenu_70GeV_1p41e-6Ve.root", "READ"),
    ROOT.TFile("/afs/cern.ch/user/g/gasadows/HNL/analysis/REC_HNL_Majorana_eenu_90GeV_1p41e-6Ve.root", "READ"),
]

# Get the histograms for each variable
hist_pt = [file.Get("MC_electrons_pt") for file in input_files]
hist_theta = [file.Get("MC_electrons_theta") for file in input_files]
hist_GenVertex = [file.Get("gen_Vertex_Lxyz_distrib_fromHNL") for file in input_files]
hist_invmass = [file.Get("electrons_invmass") for file in input_files]
hist_d0 = [file.Get("track_d0") for file in input_files]
hist_RecVertex = [file.Get("Vertex_dist") for file in input_files]
hist_MC_HNL_p = [file.Get("MC_HNL_p") for file in input_files]
hist_MC_HNL_mass = [file.Get("MC_HNL_mass") for file in input_files]
hist_MC_HNL_theta = [file.Get("MC_HNL_theta") for file in input_files]
hist_MC_invmass = [file.Get("FSGen_ee_invMass") for file in input_files]
hist_CutFlow = [file.Get("cutFlow") for file in input_files]
hist_MissingET = [file.Get("missingEnergy_pt") for file in input_files]
hist_vertex_pull_x = [file.Get("Vertex_diff_x") for file in input_files]

# Create output file root and pdf
output_file_name = "combined_all_HNL"
output_file_root = ROOT.TFile(f"{output_file_name}.root", "RECREATE")
output_file_pdf = ROOT.TCanvas("canvas", "Superimposed Histograms", 800, 800)
output_file_pdf.Print(f"{output_file_name}.pdf[")

# Define colors, styles, and legend titles for histograms
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen + 1 ,ROOT.kBlue]
styles = [1, 9, 10, 6]
legend_titles = ["m_{N} = 30 GeV, V_{e} = 1.41e-6", "m_{N} = 50 GeV, V_{e} = 1.41e-6", "m_{N} = 70 GeV, V_{e} = 1.41e-6", "m_{N} = 90 GeV, V_{e} = 1.41e-6"]
hist_RecVertex
# Superimpose and save histograms with legends for each variable
draw_histograms(output_file_pdf, hist_MC_HNL_mass, "Gen_N_mass", "Gen N mass [GeV]", "Events / 1.0 GeV", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_MC_HNL_p, "Gen_N_p", "Gen N p [GeV]", "Events / 0.5 GeV", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_MC_HNL_theta, "Gen_N_theta", "Gen N #theta [rad]", "Events per bin (0.05 width)", log_scale=False, y_range=(0.001, 0.091))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_pt, "Gen_electrons_pt", "Gen e p_{T} [GeV]", "Events / 0.5 GeV", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_theta, "Gen_electrons_theta", "Gen e #theta [rad]", "Events per bin (0.05 width)", log_scale=False, y_range=(0.001, 0.091))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_MC_invmass, "MCelectrons_InvMass", "Gen m_{ee}", "Events / 1.0 GeV", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_invmass, "electrons_InvMass", "Reco m_{ee} [GeV]", "Events / 1.0 GeV", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_MissingET, "Missing ET", "Reco Missing ET p_{T} [GeV]", "Events / 0.6 GeV", log_scale=True, y_range=(0.001, 1.05))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_GenVertex, "Gen_vertex_displacement", "Gen N L_{xyz} [mm]", "Events / 10 mm", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_RecVertex, "Rec_vertex_displacement", "Reco N L_{xyz} [mm]", "Events / 10 mm", log_scale=True, y_range=(0.001, 2900))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_d0, "track_d0", "d0 [mm]", "Events / 5 mm", log_scale=False, y_range=(0.001, 0.85))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_CutFlow, "cutFlow", "#cut", "#Events", log_scale=False, y_range=(0.001, 1.05))
output_file_pdf.Clear()
draw_histograms(output_file_pdf, hist_vertex_pull_x, "vertex_pull_x", "vertex pull x [mm]", "Events / 2.10^{-3} mm", log_scale=False, y_range=(0.001, 0.305))
output_file_pdf.Clear()

# Close files
for file in input_files:
    file.Close()
output_file_root.Close()

# Print the pdf file
output_file_pdf.Print(f"{output_file_name}.pdf]")
