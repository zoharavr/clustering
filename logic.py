import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import plotly.plotly as py
import tkMessageBox
from sklearn.cluster import KMeans
from copy import deepcopy


class Model:
#constructor
    def __init__(self,path, KMeansNumber, run_number):
        self.KMeansNumber=KMeansNumber
        self.run_number= run_number
        self.path=path
#checks if we got an empty file OR if the input for clusters is bigger then the amount of observations 
    def preValid(self,df): 
        if  df.empty:
            tkMessageBox.showerror("K Means Clustering","Please enter a valid file")
            return False
        
        if  len(df.index)<int(self.KMeansNumber):
            tkMessageBox.showerror("K Means Clustering","Please enter a valid number of clusters")
            return False  
        return True  

    def preprocess(self):
        df=pd.read_excel(self.path)
        # check for problematic inputs
        if (not self.preValid(df)): 
            return False
        # get name of the columns and remove the ones that are not numeric
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
        tkMessageBox.showinfo("K Means Clustering","Preprocessing completed successfully!")
        return True
#Build a model using K-Means algorithm
    def cluster (self):
        k=int(self.KMeansNumber)
        i=int(self.run_number)
        cluster=KMeans(n_clusters=k,init="random",n_init=i)
        self.agg_df['cluster']=cluster.fit_predict(self.agg_df[self.agg_df.columns[1:]])

#make the scatter chart
    def scatter(self):
        pyplot.scatter(self.agg_df['Generosity'],self.agg_df['Social support'],c=self.agg_df['cluster'])
        pyplot.title('Output for K-Means clustering')
        #show the color of each cluster
        pyplot.colorbar()
        pyplot.xlabel('Generosity')
        pyplot.ylabel('social_support')
        pyplot.savefig('scatter.png')

#Division of countries into clusters
    def worldMap(self):
        py.sign_in(username='yosefmel',api_key='uWFhsUv98ZXLTPWalwqQ')
        df=self.agg_df
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
            title='Division of countries into clusters',
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