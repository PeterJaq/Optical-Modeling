from TransferMatrix import OpticalModeling
import matplotlib.pyplot as plt
plt.style.use('ggplot')

Device = [
        ("Air", 0),  # layer 0, substrate, thickness doesn't mater                      # layer 1
        ("SiO2", 136.93),  # layer 2
        ("Zn0.16", 26),
        ("SiO2", 41.73),
        ("Cu", 50)
         ]


libname = "Index_Refraction_Zn+SiO2.csv"

Solarfile = "SolarAM15.csv"  # Wavelength vs  mW*cm-2*nm-1

wavelength_range = [250, 1500]  # wavelength range (nm) to model [min, max]

plotWL = [450, 600, 700, 950]

SaveName = "Result"  # prefix of the file names

saveFigE, saveFigAbs, saveFigGen = False, False, False

if __name__ == "__main__":

    max_abs = 0
    best_device = None

    for l1 in range(0, 1000):
        if l1 % 100 == 0:
            print("Step %d " % l1)
        for l2 in range(0, 1500):
            for l3 in range(0, 1000):
                for l4 in range(0, 1000):

                    Device = [
                        ("Air", l1/10.0),  # layer 0, substrate, thickness doesn't mater                      # layer 1
                        ("SiO2", l2/10.0),  # layer 2
                        ("Zn0.16", l3/10.0),
                        ("SiO2", l4/10.0),
                        ("Cu", 200)
                    ]

                    OM = OpticalModeling(Device, libname=libname, WLrange=wavelength_range,
                                         plotWL=plotWL, WLstep=2.0, posstep=1.0)
                    OM.RunSim(plotE=False, plotAbs=True, plotGen=False,
                              saveFigE=False, saveFigAbs=False, saveFigGen=False,
                              figformat='pdf', savename=SaveName)
                    if OM.mean_abs > max_abs:
                        max_abs = OM.mean_abs
                        best_device = Device
                    #summary = OM.JscReport()

                    OM.SaveData(savename=SaveName, saveE=False, saveAbs=False, saveGen=False)
    print(max_abs)
    print(best_device)
    plt.show()