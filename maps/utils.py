import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
from datetime import datetime
import pandas as pd
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components

# Code derived from https://www.youtube.com/watch?v=jrT6NiM46jk
def get_graph():
  buffer = BytesIO()
  plt.savefig(buffer, format='png') #Saves the file
  buffer.seek(0) #Sets cursor to beginning of the stream
  image_png = buffer.getvalue()
  graph = base64.b64encode(image_png) #Takes in bytes object
  graph = graph.decode('utf-8')
  buffer.close() #Free memory of buffer
  return graph

def get_plot():
  #Switch the backend as per documentation https://matplotlib.org/2.0.2/faq/usage_faq.html
  plt.switch_backend('AGG')
  plt.figure(figsize=(10,5))
  plt.title('')
  graph = get_graph()
  return graph

def get_yahoo_shareprices(sharename, period="2y"):

  import yfinance as yf
  import pandas as pd
    
  """
  yfinance.history arguments:-

  period: data period to download (Either Use period parameter or use start and end) Valid periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
  interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
  start/end: If not using period - Download date string (YYYY-MM-DD) or datetime.
  prepost: Include Pre and Post market data in results? (Default is False)
  auto_adjust: Adjust all OHLC automatically? (Default is True)
  actions: Download share dividends and share splits events? (Default is True)
  """
  yfdata = yf.Ticker(sharename[1])
  df_shareprices = pd.DataFrame(yfdata.history(period))
  df_shareprices = df_shareprices.dropna()
  df_shareprices = df_shareprices[df_shareprices['Close'] !=0]

  #The index has to be reset and the datatypes converted to float for Plotly
  df_shareprices = df_shareprices.reset_index()
  for i in ['Open', 'High', 'Close', 'Low']: 
        df_shareprices[i]  =  df_shareprices[i].astype('float64')

  return(df_shareprices)

def matplotlib_shareprices(sharenames, period="2y"):

  import matplotlib.pyplot as plt
  from matplotlib.gridspec import GridSpec
  import pandas as pd

  plt.switch_backend('AGG')
  #Switch the backend as per documentation https://matplotlib.org/2.0.2/faq/usage_faq.html
  

#Looping functionality not working for less than 2 companies. For 2 companies "Exception Thrown: too many indices for array: array is 1-dimensional, but 2 were indexed". Appears to be because for a 2x1 axes plot the shape of the axes array is a tuple of (2,) whereas for a 2x2 plot the tuple is (2,2). For 1 company, there is no tuple/shape at all. Countered in the call below by additional if statements for the different scenarios.
#Full screen toggle reminder ctrl-f or crtl-w to close window

  #Work out how to arrange the axes on the matplotlib subplot
  shareno = len(sharenames)
  if shareno == 1:
    pltver = 1
    plthor = 1
  elif shareno == 2:
    pltver = 1
    plthor = 2
  elif shareno < 5:
    pltver = 2
    plthor = 2
  elif shareno < 7:
    pltver = 2
    plthor = 3
  elif shareno < 9:
    pltver = 2
    plthor = 4
  else:
    raise Exception('Maximum of 8 shares. {} provided'.format(shareno))
  
  fig, axes = plt.subplots(nrows=pltver, ncols=plthor)

  nextver = 1
  nexthor = 1
    
  for sharename in enumerate(sharenames):

    #print(sharename, period)
    df_shareprices = get_yahoo_shareprices(sharename, period)
 
    #Line Plot using Matplotlib - for a multiplot
    xax = nexthor - 1
    yax = nextver - 1
    if shareno > 2:
      axes[yax, xax].plot(df_shareprices['Date'], df_shareprices['Close'], linewidth=2)
      axes[yax, xax].set_title(sharename[1], fontsize=12)
      axes[yax, xax].tick_params(axis='both', labelsize=5)
      #axes[yax, xax].set_ylim(ymin=0)
    elif shareno == 2:
      axes[xax].plot(df_shareprices['Date'], df_shareprices['Close'], linewidth=2)
      axes[xax].set_title(sharename[1], fontsize=18)
      axes.set_ylabel("Price GB Pence", fontsize=12)
      axes[xax].tick_params(axis='both', labelsize=10)
      axes[xax].set_ylim(ymin=0)
    else:
      axes.plot(df_shareprices['Date'], df_shareprices['Close'], linewidth=2)
      axes.set_title(sharename[1], fontsize=24)
      axes.tick_params(axis='both', labelsize=15)
      axes.set_ylabel("Price GB Pence", fontsize=14)
      axes.set_ylim(ymin=0)
 
    if nexthor < plthor:
      nexthor += 1
    else:
      nexthor = 1
      nextver += 1

  #plt.get_current_fig_manager().full_screen_toggle()
  #plt.figure(figsize=(10,5))

  plt.suptitle("Share Prices over {} period".format(period), fontsize=20)
  graph = get_graph()
  return graph

def mattest():

  import matplotlib
  import matplotlib.pyplot as plt
  import numpy as np

  plt.switch_backend('AGG')

  N = 5
  menMeans = (20, 35, 30, 35, -27)
  womenMeans = (25, 32, 34, 20, -25)
  menStd = (2, 3, 4, 1, 2)
  womenStd = (3, 5, 2, 3, 3)
  ind = np.arange(N)    # the x locations for the groups
  width = 0.35       # the width of the bars: can also be len(x) sequence

  fig, ax = plt.subplots()

  p1 = ax.bar(ind, menMeans, width, yerr=menStd, label='Men')
  p2 = ax.bar(ind, womenMeans, width,
              bottom=menMeans, yerr=womenStd, label='Women')

  ax.axhline(0, color='grey', linewidth=0.8)
  ax.set_ylabel('Scores')
  ax.set_title('Scores by group and gender')
  ax.set_xticks(ind)
  ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
  ax.legend()

  graph = get_graph()
  return graph

def bokeh_chart():

    DF=pd.DataFrame(columns=['Item','Start','End','Color'])
    Items=[
        ['Contract Review & Award','2015-7-22','2015-8-7','red'],
        ['Submit SOW','2015-8-10','2015-8-14','gray'],
        ['Initial Field Study','2015-8-17','2015-8-21','gray'],
        ['Topographic Procesing','2015-9-1','2016-6-1','gray'],
        ['Init. Hydrodynamic Modeling','2016-1-2','2016-3-15','gray'],
        ['Prepare Suitability Curves','2016-2-1','2016-3-1','gray'],
        ['Improvement Conceptual Designs','2016-5-1','2016-6-1','gray'],
        ['Retrieve Water Level Data','2016-8-15','2016-9-15','gray'],
        ['Finalize Hydrodynamic Models','2016-9-15','2016-10-15','gray'],
        ['Determine Passability','2016-9-15','2016-10-1','gray'],
        ['Finalize Improvement Concepts','2016-10-1','2016-10-31','gray'],
        ['Stakeholder Meeting','2016-10-20','2016-10-21','blue'],
        ['Completion of Project','2016-11-1','2016-11-30','red']
        ] #first items on bottom

    for i,Dat in enumerate(Items[::-1]): #[::-1] reverses the order of the list
        DF.loc[i]=Dat

    DF['Start_dt']=pd.to_datetime(DF.Start)
    DF['End_dt']=pd.to_datetime(DF.End)

    G=figure(title='Project Schedule',x_axis_type='datetime',width=800,height=400,y_range=DF.Item.tolist(),
            x_range=Range1d(DF.Start_dt.min(),DF.End_dt.max()), tools='save')

    hover=HoverTool(tooltips="Task: @Item<br>\
    Start: @Start<br>\
    End: @End")
    G.add_tools(hover)

    DF['ID']=DF.index+0.8
    DF['ID1']=DF.index+1.2
    CDS=ColumnDataSource(DF)
    G.quad(left='Start_dt', right='End_dt', bottom='ID', top='ID1',source=CDS,color="Color")
    script, div = components(G, CDN)
    return(script, div)

def shapefile_info(shapefile):
    print("\n",f"\n{shapefile.info()=}\n")
    print("\n",f"\n{shapefile.head()=}\n")
    print("\n",f"\n{shapefile.shape=}\n")
    print("\n",f"\n{shapefile.crs=}\n")
    print("\n",f"\n{shapefile.total_bounds=}\n")