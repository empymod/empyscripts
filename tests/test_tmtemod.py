import numpy as np
from numpy.testing import assert_allclose
from scipy.constants import mu_0, epsilon_0

from empyscripts import tmtemod
from empymod import kernel, filters, dipole

# We only check that the summed return values in the functions in tmtemod agree
# with the corresponding functions from empyod. Nothing more. The examples are
# based on the examples in empymod/tests/create_data.

# Simple model, three frequencies, 6 layers
freq = np.array([0.003, 2.5, 1e6])
res = np.array([3, .3, 10, 4, 3, 1])
aniso = np.array([1, .5, 3, 1, 2, 1])
eperm = np.array([80, 100, 3, 8, 1, 1])
mperm = np.array([.5, 100, 30, 1, 30, 1])
etaH = 1/res + np.outer(2j*np.pi*freq, eperm*epsilon_0)
etaV = 1/(res*aniso*aniso) + np.outer(2j*np.pi*freq, eperm*epsilon_0)
zeta = np.outer(2j*np.pi*freq, mperm*mu_0)
filt = filters.key_201_2012()
lambd = filt.base/np.array([0.001, 1, 100, 10000])[:, None]
depth = np.array([-np.infty, 0, 150, 300, 500, 600])
depth2 = np.r_[depth, 800]


# test_dipole switched off, not working yet
def tst_dipole():
    for lay in [0, 1, 5]:  # Src/rec in first, second, and last layer
        for f in freq:
            src = [0, 0, depth2[lay+1]-50]
            rec = [[0.001, 1, 100, 10000], [0, 0, 0, 0], depth2[lay+1]-10]
            inp = {'src': src, 'rec': rec, 'depth': depth[1:], 'res': res,
                   'freqtime': f, 'aniso': aniso, 'verb': 0}

            # empymod-version
            out1 = dipole(epermH=eperm, epermV=eperm, mpermH=mperm,
                          mpermV=mperm, xdirect=False, **inp)

            # empyscripts-version
            out2a, out2b = tmtemod.dipole(eperm=eperm, mperm=mperm, **inp)
            out2a = out2a[0] + out2a[1] + out2a[2] + out2a[3] + out2a[4]
            out2b = out2b[0] + out2b[1] + out2b[2] + out2b[3] + out2b[4]

            # Check
            assert_allclose(out1, out2a + out2b, atol=1e-100)

    # Check the 3 warnings

def test_greenfct():
    for lay in [0, 1, 5]:  # Src/rec in first, second, and last layer
        inp = {'depth': depth, 'lambd': lambd,
               'etaH': etaH, 'etaV': etaV,
               'zetaH': zeta, 'zetaV': zeta,
               'lrec': np.array(lay), 'lsrc': np.array(lay),
               'zsrc': depth2[lay+1]-50, 'zrec': depth2[lay+1]-10}

        # empymod-version
        out1a, out1b = kernel.greenfct(ab=11, xdirect=False, msrc=False,
                                    mrec=False, use_ne_eval=False, **inp)

        # empyscripts-version
        out2a, out2b = tmtemod.greenfct(**inp)
        out2a = out2a[0] + out2a[1] + out2a[2] + out2a[3] + out2a[4]
        out2b = out2b[0] + out2b[1] + out2b[2] + out2b[3] + out2b[4]

        # Check
        assert_allclose(out1a, out2a, atol=1e-100)
        assert_allclose(out1b, out2b)


def test_fields():
    Gam = np.sqrt((etaH/etaV)[:, None, :, None] *
                    (lambd**2)[None, :, None, :] + (zeta**2)[:, None, :, None])

    for lay in [0, 1, 5]:  # Src/rec in first, second, and last layer

        inp1 = {'depth': depth, 'e_zH': etaH, 'Gam': Gam,
                'lrec': np.array(lay), 'lsrc': np.array(lay),
                'use_ne_eval': False}
        Rp1, Rm1 = kernel.reflections(**inp1)

        inp2 = {'depth': depth, 'Gam': Gam, 'Rp': Rp1, 'Rm': Rm1,
                'lrec': np.array(lay), 'lsrc': np.array(lay),
                'zsrc': depth2[lay+1]-50}

        for TM in [True, False]:
            inp2['TM'] = TM

            # empymod-version
            out1 = kernel.fields(ab=11, use_ne_eval=False, **inp2)

            # empyscripts-version
            out2 = tmtemod.fields(**inp2)

            # Check
            assert_allclose(out1[0], out2[0] + out2[1])
            assert_allclose(out1[1], out2[2] + out2[3])
