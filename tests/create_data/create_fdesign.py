"""Create data for test_fdesign."""
import numpy as np
from copy import deepcopy as dc
from empyscripts import fdesign

# Cannot pickle/shelve this; could dill it. For the moment, we just provide
# it separately here and in the tests.
fI = (fdesign.j0_1(5), fdesign.j1_1(5))

# Define main model
inp1 = {'spacing': (0.04, 0.1, 10),
        'shift': (-3, -0.5, 10),
        'n': 201,
        'cvar': 'amp',
        'save': False,
        'finish': True,
        'full_output': True,
        }
inp2 = dc(inp1)
inp2['r'] = np.logspace(0, 3, 10)
inp2['r_def'] = (1, 1, 2)
inp2['name'] = 'test'
inp2['finish'] = None

# 1. General case with various spacing and shifts
filt1, out1 = fdesign.design(verb=0, plot=0, fI=fI, **inp2)
case1 = (inp2, filt1, out1)

# 2. Specific model with only one spacing/shift
inp3 = dc(inp2)
inp3['spacing'] = 0.0641
inp3['shift'] = -1.2847
filt2, out2 = fdesign.design(verb=0, plot=0, fI=fI, **inp3)
case2 = (inp3, filt2, out2)

# 2.b Same, with only one transform
filt2b, out2b = fdesign.design(verb=0, plot=0, fI=fI[0], **inp3)
case2b = (inp3, filt2b, out2b)

# 3. Maximize r
inp4 = dc(inp3)
inp4['cvar'] = 'r'
filt3, out3 = fdesign.design(verb=0, plot=0, fI=fI, **inp4)
case3 = (inp4, filt3, out3)

# 4. Less defaults
filt4, out4 = fdesign.design(verb=0, plot=0, fI=fI, **inp1)
case4 = (inp1, filt4, out4)

# 5. One shift, several spacings
inp5 = dc(inp2)
inp5['spacing'] = (0.06, 0.07, 10)
inp5['shift'] = -1.2847
filt5, out5 = fdesign.design(verb=0, plot=0, fI=fI, **inp5)
case5 = (inp5, filt5, out5)

# 6. Several shifts, one spacings; r
inp6 = dc(inp2)
inp6['spacing'] = 0.0641
inp6['shift'] = (-1.5, 0, 10)
inp6['cvar'] = 'r'
filt6, out6 = fdesign.design(verb=0, plot=0, fI=fI, **inp6)
case6 = (inp6, filt6, out6)

# # Store data # #
np.savez_compressed('../data/fdesign.npz',
                    case1=case1, case2=case2, case2b=case2b, case3=case3,
                    case4=case4, case5=case5, case6=case6)
