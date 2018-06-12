from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from copy import deepcopy
import matplotlib.pyplot as pyplot
import plotly.plotly as py
from tkFileDialog import askopenfilename

class Model:
    def __init__(self, master,path, KMeansNumber, run_number):
        self.KMeansNumber=KMeansNumber
        self.run_number= run_number
        self.path=path
  # Condiser to put a consructor
    def preprocess(self):
        # need to accept path from GUI
        df=pd.read_excel(self.path)
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
        self.agg_df=self.agg_df.groupby('country', as_index=False).agg(np.mean)
    def cluster (self):
        # need to accept from GUI
        k=self.KMeansNumber
        i=self.run_number
        cluster=KMeans(n_clusters=k,init="random",n_init=i)
        self.agg_df['cluster']=cluster.fit_predict(self.agg_df[self.agg_df.columns[1:]])
      #  print(self.agg_df)
    def scatter(self):
        pyplot.scatter(self.agg_df['Generosity'],self.agg_df['Social support'],c=self.agg_df['cluster'])
        pyplot.title('Output for K-Means clustering')
        pyplot.colorbar()
        pyplot.xlabel('Generosity')
        pyplot.ylabel('social_support')
        pyplot.show()

    def worldMap(self):
        py.sign_in(username='yosefmel',api_key='uWFhsUv98ZXLTPWalwqQ')
        df=self.agg_df
       # print(df.head(10))
        data = [dict(
            type='choropleth',
            locations=df['country'],
            z=df['cluster'],
            locationmode='country names',
            colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"], \
                        [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                title='cluster'),
        )]
        layout = dict(
            title='K-Means Clustering',
            geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection=dict(
                        type='Mercator'
                    )
                )
        )
        fig = dict(data=data, layout=layout)
        py.iplot(fig, validate=False, filename='World-Map')
        py.image.save_as(fig, filename='worldMap.png')

class Clustering:
    def __init__(self, master):
        self.master = master
        master.title("Cluster")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.labelfile = Label(master, text="File:")
        self.entryfile = Entry(master,bd=2)
        vcmd = master.register(self.validate) # we have to wrap the command
        self.choose_button = Button(master, text="Browse", command=lambda: self.browse())
        self.labelK = Label(master, text="Num of clusters k:")
        self.entryK = Entry(master,bd=2)
        self.labelRun = Label(master, text="Num of runs:")
        self.entryRun = Entry(master,bd=2)
        self.pre_proc = Button(master, text="Pre-process",command=self.pre_proc)
        self.cluster = Button(master, text="Cluster",command=self.clustering)
        # LAYOUT
        self.labelfile.grid(row=0, column=0, sticky=W)
        self.entryfile.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.choose_button.grid(row=1, column=4)
        self.labelK.grid(row=2, column=0, sticky=W)
        self.entryK.grid(row=2, column=1, columnspan=3, sticky=W+E)
        self.labelRun.grid(row=3, column=0, sticky=W)
        self.entryRun.grid(row=3, column=1, columnspan=3, sticky=W+E)
        self.pre_proc.grid(row=4, column=0)
        self.cluster.grid(row=4,column=1)

    def clustering (self): 
        print(1)
        
    def validate(self):
       input1=self.entryK.get("1.0",END)
       input2=self.entryRun.get("1.0",END)
       return input1,input2

    def pre_proc(self):
        print(self.validate())
        # model=Model()
        # model.preprocess()

    def browse(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.entryfile.insert(0,filename)

# model.cluster()
# model.scatter()
# model.worldMap()
root = Tk()
my_gui = Clustering(root)
root.mainloop()

