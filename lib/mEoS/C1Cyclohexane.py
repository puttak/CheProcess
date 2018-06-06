#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2017, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


from lib.meos import MEoS
from lib import unidades


class C1Cyclohexane(MEoS):
    """Multiparameter equation of state for methylcyclohexane"""
    name = "methylcyclohexane"
    CASNumber = "108-87-2"
    formula = "C6H11-CH3"
    synonym = ""
    rhoc = unidades.Density(267.0660832)
    Tc = unidades.Temperature(572.2)
    Pc = unidades.Pressure(3470.0, "kPa")
    M = 98.18606  # g/mol
    Tt = unidades.Temperature(146.7)
    Tb = unidades.Temperature(374.)
    f_acent = 0.23
    momentoDipolar = unidades.DipoleMoment(0.0, "Debye")
    id = 39

    CP1 = {"ao": 2.04122,
           "an": [0.016417, 0.000185315, -3.14826e-7, 1.65567e-10],
           "pow": [1, 2, 3, 4],
           "ao_exp": [],
           "exp": [],
           "ao_hyp": [], "hyp": []}

    lemmon = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for methylcyclohexane "
                    "of Lemmon (2007).",
        "__doi__": {"autor": "Lemmon, E.W.",
                    "title": "",
                    "ref": "unpublished equation, 2007",
                    "doi": ""},

        # Yoneda, Y., Sato, S., Matsumoto, T.
        # Density of Methylcyclohexane at Temperatures up to 600K and Pressures
        # up to 200 MPa
        # Int. J. Thermophys. 38 (2017) 106
        # doi: 10.1007/s10765-017-2241-7
        # As report Yoneda et al., its new (p, ρ, T) data disabling this eq as
        # reference equation

        "R": 8.314472,
        "cp": CP1,
        "ref": "NBP",

        "Tmin": Tt, "Tmax": 600., "Pmax": 500000.0, "rhomax": 9.13,
        "Pmin": 0.0000003, "rhomin": 9.12,

        "nr1": [1.3026, -2.6270, 0.68834, -0.16415, 0.092174, 0.0003842],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.38, 1.2, 2.14, 1.6, 0.3, 0.7],

        "nr2": [-0.29737, -0.078187, -0.049139, -0.30402, -0.074888],
        "d2": [1, 2, 5, 1, 4],
        "t2": [2.7, 3.25, 2.35, 3.7, 4.1],
        "c2": [1, 1, 1, 2, 2],
        "gamma2": [1]*17}

    eq = lemmon,

    _vapor_Pressure = {
        "eq": 5,
        "ao": [-0.65871e1, -0.56553e1, 0.68947e1, -0.41281e1, -0.25444e1],
        "exp": [1.0, 1.5, 1.6, 3.2, 10.]}
    _liquid_Density = {
        "eq": 1,
        "ao": [0.18273e-1, 0.15215e2, -0.21951e2, 0.94466e1, 0.16781],
        "exp": [0.1, 0.64, 0.8, 1.0, 4.5]}
    _vapor_Density = {
        "eq": 3,
        "ao": [-0.52572e1, -0.13417e2, -0.24271e1, -0.54482e2, -0.15791e3],
        "exp": [0.544, 2.3, 2.5, 6.1, 15.0]}

    thermo0 = {"eq": 1,
               "__name__": "Perkins (2008)",
               "__doi__": {"autor": "Perkins, R.A. Hammerschmidt, U. and Huber, M.L.",
                           "title": "Measurement and Correlation of the Thermal Conductivity of Methylcyclohexane and Propylcyclohexane from 300 K to 600 K at Pressures to 60 MPa",
                           "ref": "J. Chem. Eng. Data, 2008, 53 (9), pp 2120–2127",
                           "doi": "10.1021/je800255r"},
               "__test__":
                    """
                    >>> st=C1Cyclohexane(T=300, P=1e5)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    300.00 0.100 763.527638 0.106327779
                    >>> st=C1Cyclohexane(T=450, P=1e5)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    450.00 0.100 2.68445155 0.0276787553
                    >>> st=C1Cyclohexane(T=450, P=5e7)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    450.00 50.000 701.680049 0.0995066894
                    >>> st=C1Cyclohexane(T=600, P=1e5)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    600.00 0.100 1.98434155 0.059060141
                    >>> st=C1Cyclohexane(T=600, P=4.744e6)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    600.00 4.744 267.000153 0.0708547641
                    >>> st=C1Cyclohexane(T=600, P=5e7)
                    >>> print "%0.2f %0.3f %0.9g %0.9g " % ( \
                        st.T, st.P.MPa, st.rho, st.k.WmK)
                    300.00 50.000 610.749122 0.093158965
                    """, # Table 5, pag 2125

               "Tref": 572.2, "kref": 1,
               "no": [0.289968e-2, -0.180666e-1, 0.727576e-1, -0.129778e-1],
               "co": [0, 1, 2, 3],

               "Trefb": 572.2, "rhorefb": 2.72, "krefb": 1.,
               "nb": [0.91914900e-1, -0.79040800e-1, -0.81708800e-1,
                      0.92391100e-1, 0.29644900e-1, -0.42849800e-1,
                      -0.29983400e-2, 0.72786000e-2, 0.0, 0.0],
               "tb": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
               "db": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
               "cb": [0]*10,

               "critical": 3,
               "gnu": 0.63, "gamma": 1.2415, "R0": 1.01,
               "Xio": 0.15e-9, "gam0": 0.052, "qd": 6.24e-10, "Tcref": 858.3}

    _thermal = thermo0,
