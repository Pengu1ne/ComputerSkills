'''
An addition to the POD2L method where the value is collected and saved into
a file.

-wilhelmiina / pengu1ne
'''
###   Import packages
import pandas as pd
import numpy as np

### Create a data frame
foo = []

### Indexes
distance = [3.5,4.0,4.5,5.0,'beta']
dimers = ['ete','ace','cpr','cbd','cpd','fur','pyr','thp','imi','ben','phe']

iterables = [dimers,distance]
#systems = pd.MultiIndex.from_product(iterables, names=['dim','dist'])
systems = pd.MultiIndex.from_product(iterables)
print(systems)

### Columns
#funct = ['pbe','pbe0','lrc-wpbeh','hse06','blyp','b3lyp','b97',
#         'b97-1','wb97x','ot-rsh']
#funct = ['pbe','pbe0','lrc-wpbeh','hse06','blyp','b3lyp','b97',
#         'b97-1','wb97x','ot-rsh','pbe-ln','pbe0-ln','lrc-wpbeh-ln',
#         'hse06-ln','blyp-ln','b3lyp-ln','b97-ln','b97-1-ln','wb97x-ln',
#         'ot-rsh-ln']
funct_ln = ['pbe_ln','pbe0_ln','lrc-wpbeh_ln','hse06_ln','blyp_ln','b3lyp_ln',
            'b97_ln','b97-1_ln','wb97x_ln','ot-rsh_ln']

####   TEST TEST TEST   ###
print('''No values''')
df = pd.DataFrame(data=foo, index=systems, columns=[funct_ln])
print(df)
print('-------------------------------------------------------------------')
print('''New values''')
#df.at['blyp',('ace',4.0)] = 2.0
df.loc[('fur',4.5), 'hse06'] = 2.0
print(df)
df.to_excel('hab11-ln.xlsx',sheet_name='hab11-pod2l-ln')
