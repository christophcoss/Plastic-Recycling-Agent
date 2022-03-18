import datetime as d
import matplotlib.pyplot as plt
import inspect, os.path

import seaborn as sns

from RecyclingModel import *

#run model and generate graph results (not much for now)
def my_filename(dir, date, name):
    return "{}/{}_{}".format(dir,date.strftime("%m%d%H%M%S"),name)

if __name__ == '__main__':
    now = d.datetime.now()
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    homeDir = os.path.dirname(os.path.abspath(filename))
    outputDir = homeDir[:-11]+"output"

    model = RecyclingModel(nMunicipality = 1,nRecComp = 10,nHouseholds =1000)
    for i in range(241):
        model.step()
    #print(d.datetime.now())
    model_data = model.datacollector.get_model_vars_dataframe()
    sns.lineplot(data=model_data,x='step',y = 'rateRecycling')
    plt.title('Rate of plastic recycling', fontweight="bold", fontsize=14,y= -0.22)
    plt.xlabel("Step")
    plt.ylabel("Rate")
    plt.savefig(my_filename(outputDir, now, 'rate.png'), bbox_inches='tight')

    plt.figure()

    sns.lineplot(data=model_data,x='step',y = 'collectedWaste')
    plt.title('waste Collected', fontweight="bold", fontsize=14,y= -0.22)
    plt.xlabel("Step")
    plt.ylabel("Waste")
    plt.savefig(my_filename(outputDir, now, 'waste.png'), bbox_inches='tight')

    plt.figure()

    sns.lineplot(data=model_data,x='step',y = 'collectedPlastic')
    plt.title('Plastic Collected', fontweight="bold", fontsize=14,y= -0.22)
    plt.xlabel("Step")
    plt.ylabel("Plastic")
    plt.savefig(my_filename(outputDir, now, 'plastic.png'), bbox_inches='tight')

    plt.figure()

    sns.lineplot(data=model_data,x='step',y = 'availableMoney')
    plt.title('Money Available', fontweight="bold", fontsize=14,y= -0.22)
    plt.xlabel("Step")
    plt.ylabel("Money")
    plt.savefig(my_filename(outputDir, now, 'money.png'), bbox_inches='tight')

    plt.figure()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
