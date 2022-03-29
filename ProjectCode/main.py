import datetime as d
import matplotlib.pyplot as plt
import inspect, os.path
from pandas.plotting import table

import seaborn as sns

from RecyclingModel import *

#run model and generate graph results (not much for now)
def my_filename(dir, date, name):
    return "{}/{}_{}".format(dir,date.strftime("%m%d%H%M%S"),name)

if __name__ == '__main__':
    for scenario in os.scandir('Scenarios'):
        if scenario.is_file():
            now = d.datetime.now()
            filename = inspect.getframeinfo(inspect.currentframe()).filename
            homeDir = os.path.dirname(os.path.abspath(filename))
            outputDir = homeDir[:-11]+"output"

            model = RecyclingModel(nMunicipality = 1, scenario = scenario.path)
            for i in range(241):
                model.step()
            #print(d.datetime.now())
            model_data = model.datacollector.get_model_vars_dataframe()
            sns.lineplot(data=model_data,x='step',y = 'rateRecycling')
            plt.title('Rate of plastic recycling ' + scenario.name[:-13], fontweight="bold", fontsize=14,y= -0.22)
            plt.xlabel("Step")
            plt.ylabel("Rate")
            plt.savefig(my_filename(outputDir, now, scenario.name[:-13] + ' rate.png'), bbox_inches='tight')

            plt.figure()

            sns.lineplot(data=model_data,x='step',y = 'collectedWaste')
            plt.title('waste Collected ' + scenario.name[:-13], fontweight="bold", fontsize=14,y= -0.22)
            plt.xlabel("Step")
            plt.ylabel("Waste")
            plt.savefig(my_filename(outputDir, now, scenario.name[:-13] + ' waste.png'), bbox_inches='tight')

            plt.figure()

            sns.lineplot(data=model_data,x='step',y = 'collectedPlastic')
            plt.title('Plastic Collected ' + scenario.name[:-13], fontweight="bold", fontsize=14,y= -0.22)
            plt.xlabel("Step")
            plt.ylabel("Plastic")
            plt.savefig(my_filename(outputDir, now, scenario.name[:-13] + ' plastic.png'), bbox_inches='tight')

            plt.figure()

            sns.lineplot(data=model_data,x='step',y = 'availableMoney')
            plt.title('Money Available ' + scenario.name[:-13], fontweight="bold", fontsize=14,y= -0.22)
            plt.xlabel("Step")
            plt.ylabel("Money")
            plt.savefig(my_filename(outputDir, now, scenario.name[:-13] + ' money.png'), bbox_inches='tight')

            plt.figure()

            result = model_data.loc[model_data['activityBought']!='None'][["step", "activityBought", "activityTargeted", "targetedGroup"]].set_index('step')

            ax = plt.subplot(111, frame_on=False)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            ax.set_title('Activities Bought ' + scenario.name[:-13], fontweight="bold", fontsize=14, y = 0 , pad = -38)

            tat = table(ax, result, loc='center', cellLoc='center')
            w, h = tat[0,0].get_width(), tat[0,0].get_height()
            tat.add_cell(0,-1, w, h, text='Step', loc='center')
            tat.add_cell(0, 0, w, h, text='Activity Bought', loc='center')
            tat.set_fontsize(11)
            tat.scale(1, 1.2)
            tat.auto_set_column_width(col=list(range(len(result.columns))))
            plt.savefig(my_filename(outputDir, now, scenario.name[:-13] + ' activities.png'), bbox_inches='tight')

            plt.figure()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
