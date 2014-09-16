import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats

# Build the labels for axes
if type(input_data.columns) == pd.MultiIndex:
    labels = input_input_data.columns.values( input_data.columns.names.index(0) )

else: # pd.Index
    labels = input_data.columns.values



correlations = {}
for n, v in enumerate(config.get('variables')):
    a, b = v
    x = input_data.ix[:, a ] 
    y = input_data.ix[:, b ]  

    fit = np.polyfit(x,y,1)

    do = pd.DataFrame( np.zeros((len(x),2 )) )

    do.ix[:,0] = x.values
    do.ix[:,1] = y.values
    
    do.columns = pd.Index( [labels[a], labels[b]], names='Label' )
    
    # Keep class information for plot (make optional)
    do.index = input_data.index
    
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(x, y)

    correlations["R%d" % (n+1)] = {
        'data': do,
        'fit': fit,
        'label': u'r²=%0.2f, p=%0.2f' % (r_value**2, p_value)
    }
do = None;

# Generate simple result figure (using pathomx libs)
from pathomx.figures import scatterplot

for k,c in correlations.items():
    x_data = np.linspace(np.min(c['data'].ix[:,0]), np.max(c['data'].ix[:,0]), 50)
    lines = [
        (x_data, np.polyval(c['fit'], x_data), c['label'])
    ]

    vars()[k] = scatterplot(c['data'], lines=lines, styles=styles);
