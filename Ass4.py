from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from copy import deepcopy
import matplotlib.pyplot as pyplot
import plotly.plotly as plot
from tkFileDialog import askopenfilename

class Model:
  # Condiser to put a consructor
    def preprocess(self):
        # need to accept path from GUI
        df=pd.read_excel("data.xlsx")
        #name of the columns
        names=list(df)
        names.remove('country')
        names.remove('year')
        # complete missing numeric values with the mean value of the attribute
        for c_name in names:
        # we don't want to change the original object so inplace must be false
            df[c_name]=df[c_name].fillna(df[c_name].mean(), inplace=False)
        #Standardization
        df[names] = df[names].apply(lambda v : (v-v.mean())/v.std(),axis=0)
        # group by country over the years
        self.agg_df=deepcopy(df)
        del self.agg_df['year']
        self.agg_df=self.agg_df.groupby('country').agg(np.mean)
    def cluster (self):
        # need to accept from GUI
        k=3
        i=4
        cluster=KMeans(n_clusters=k,init="random",n_init=i)
        self.agg_df['cluster']=cluster.fit_predict(self.agg_df)
        print(self.agg_df)
    def scatter(self):
        pyplot.scatter(self.agg_df['Generosity'],self.agg_df['Social support'],c=self.agg_df['cluster'])
        pyplot.title('Output for K-Means clustering')
        pyplot.colorbar()
        pyplot.xlabel('Generosity')
        pyplot.ylabel('social_support')
        pyplot.show()

    def worldMap(self):
        plot.sign_in(username='yosefmel',api_key='uWFhsUv98ZXLTPWalwqQ')
        df=self.agg_df
        data = [ dict(
            type = 'choropleth',
            locations = df['country'],
            z = df['cluster'],
            text = df['COUNTRY'],
            colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                         [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.5
                ) ),
            colorbar = dict(
                autotick = False,
                tickprefix = '$',
                title = 'GDP<br>Billions US$'),
        ) ]

        layout = dict(
            title = '2014 Global GDP<br>Source:',
            geo = dict(
                showframe = False,
                showcoastlines = False,
                projection = dict(
                    type = 'Mercator'
                )
            )
        )   
        fig = dict( data=data, layout=layout )
        plot.iplot( fig, validate=False, filename='d3-world-map' )
       
class Clustering:

    def __init__(self, master):
        self.master = master
        master.title("Cluster")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.label = Label(master, text="File:")
        self.entry = Entry(master,bd=2)
        vcmd = master.register(self.validate) # we have to wrap the command
        self.choose_button = Button(master, text="Browse", command=lambda: self.browse())
        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.choose_button.grid(row=2, column=0)


    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False


    def browse(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
        self.entry.insert(0,filename)
model=Model()
model.preprocess()
model.cluster()
model.scatter()
model.worldMap()
root = Tk()
my_gui = Clustering(root)
root.mainloop()

