## Main function
def clear_read_and_plot(file):
    ## Подключение библиотек
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    import matplotlib.gridspec as gridspec
    import warnings
    import os
    ## Настройки для графиков
    plt.rcParams['figure.figsize'] = (8,6)
    plt.rcParams['lines.markersize'] = 3
    plt.rcParams['lines.markeredgewidth'] = 1
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['grid.alpha'] = 0.7
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['font.size'] = 14


    # clear initial data text file from blank lines and extra symbols with awk linux utilite
    #!awk -f clear_data.awk $file > "clear_"$file
    command = 'awk -f clear_data.awk ' + file + ' > clear_' + file
    os.system(command)
   

    # read clear data file to pandas dataframe
    filename = './clear_' + file
    datum = pd.read_csv(filename, index_col=False, sep='\s+', skiprows=10)
    #print(datum.head(2))


    # plot parameters
    params = ["T[C]", "U+_SiPM[V]", "U-_SiPM[V]", "t[s]", "I0_SiPM[uA]"]
    figs = len(params)
    fig, axn = plt.subplots(figs, 1, sharex=False,  figsize=(10, 2*figs))
    axn[0].set_title(filename[8:-4])
    for i, param in enumerate(params):
        axn[i].plot(datum[param], "*", label=param)
        axn[i].grid()
        axn[i].legend()
    plt.savefig(filename[8:-4]+"_params.png", dpi=300,  bbox_inches='tight')


    ## plot horizontal angle distributions
    fig, axn = plt.subplots(figsize=(10, 8))
    grads = sorted([x[0] for x in datum["Vert.angl[grad]."].value_counts().items()])
    for grad in grads:
        data = datum[datum["Vert.angl[grad]."] == grad] 
        ax = "Hor.angl[grad]"
        ## вычитаем пьедестал по току
        yy = data["I_SiPM[uA]"] - data ["I0_SiPM[uA]"]
        plt.plot(data[ax], yy, '*', label=str(grad)+'$^\circ$')
    # Легенда, оси, заголовок
    plt.legend(loc="center right", bbox_to_anchor=(1.25,0.5),
                title="Vertical angle")
    plt.xlabel("Horizontal angle [grad]")
    plt.ylabel("I_SiPM [uA]")
    plt.title(filename[8:-4])
    # сетка
    plt.minorticks_on()
    plt.grid()
    # Внешний вид линий вспомогательной сетки:
    plt.grid(which='minor', color = 'k', linestyle = ':')
    # Сохраняем график в файл
    plt.savefig(filename[8:-3]+"png", dpi=300,  bbox_inches='tight')


    ## fit with polynom all the data
    fig, axn = plt.subplots(figsize=(10, 8))
    y = datum["I_SiPM[uA]"] - datum ["I0_SiPM[uA]"]
    x = datum["Hor.angl[grad]"]
    plt.plot(x, y, '.', label="experim")
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.RankWarning)
        for deg in range(6, 20, 4):
            polynom = np.polyfit(x, y, deg)
            # напечатать коэффициенты фитирующего полинома
            print("Polynomial coefficients: ", polynom)
            p30 = np.poly1d(np.polyfit(x, y, deg))
            xp = np.linspace(0, 180, 720)
            plt.plot(xp, p30(xp), '--', label='fit ' + str(deg))
    plt.legend()
    # сетка
    plt.minorticks_on()
    plt.grid(which='minor', color = 'k', linestyle = ':')
    plt.grid()

