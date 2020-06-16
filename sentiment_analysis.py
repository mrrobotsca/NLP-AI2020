# We'll start by reading in the corpus, which preserves word order
import pandas as pd
import re
import string

data = pd.read_pickle('corpus.pkl')

# Create quick lambda functions to find the polarity and subjectivity of each routine
# Terminal / Anaconda Navigator: conda install -c conda-forge textblob
from textblob import TextBlob

pol = lambda x: TextBlob(x).sentiment.polarity
sub = lambda x: TextBlob(x).sentiment.subjectivity

data['polarity'] = data['fakenews'].apply(pol)
data['subjectivity'] = data['fakenews'].apply(sub)

# Let's plot the results
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [10, 8]

full_names = list(range(0,150))
xx=[]
yy=[]

for i,j in enumerate(data.index):
    x = data.polarity.loc[j]
    xx.append(x)
    y = data.subjectivity.loc[j]
    yy.append(y)
    plt.scatter(x, y, color='blue')
    # plt.xlim(-.5, .99)

plt.title('Sentiment Analysis', fontsize=20)
plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)

plt.savefig("sentiment_analyse.svg")
plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
#
# # Generate some test data
#


import plotly.graph_objects as go


fig = go.Figure(data=go.Heatmap(
                   z=[[0, 6, 3, 0], [0,13,13,0], [0,4,10,2],[0,1,4,2],[1,2,2,0]],
                   x=['-0.75', '-0.25', '0.25', '0.75'],
                   y=['0.1', '0.3', '0.5','0.7','0.9'],
                   hoverongaps = False))
fig.write_image("heatmap_sa.svg")
fig.show()