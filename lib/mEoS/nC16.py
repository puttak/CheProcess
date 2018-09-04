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


from unittest import TestCase

from lib.meos import MEoS
from lib import unidades


class nC16(MEoS):
    """Multiparameter equation of state for n-hexadecane"""
    name = "n-hexadecane"
    CASNumber = "544-76-3"
    formula = "C16H34"
    synonym = ""
    _refPropName = ""
    _coolPropName = ""
    rhoc = unidades.Density(226.441)
    Tc = unidades.Temperature(722.1)
    Pc = unidades.Pressure(1.4799, "MPa")
    M = 226.441  # g/mol
    Tt = unidades.Temperature(291.329)
    Tb = unidades.Temperature(560)
    f_acent = 0.744
    momentoDipolar = unidades.DipoleMoment(0.0, "Debye")
    id = 20

    Fi1 = {"ao_log": [1, 22],
           "pow": [0, 1],
           "ao_pow": [45.96, -26.19],
           "ao_exp": [18.9, 76.2],
           "titao": [420/Tc, 1860/Tc]}

    romeo = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for n-hexadecane of Romeo "
                    "(2018).",
        "__doi__": {"autor": "Romeo, R.",
                    "title": "Density measurements in subcooled water at "
                             "presures up to 400 MPa",
                    "ref": "Doctoral thesis, Politecnico di Torino, 2018",
                    "doi": "10.6092_polito_porto_2652785"},

        "R": 8.3144621,
        "cp": Fi1,
        "ref": "OTO",

        "Tmin": 298, "Tmax": 700.0, "Pmax": 200000.0, "rhomax": 10,
        # "Pmin": 0.580, "rhomin": 8.165,

        "nr1": [0.03965879, 1.945813, -3.738575, -0.3428167, 0.3427022],
        "d1": [4, 1, 1, 2, 3],
        "t1": [1, 0.224, 0.91, 0.95, 0.555],

        "nr2": [-2.519592, -0.8948857, 0.10760773, -1.297826, -0.04832312],
        "d2": [1, 3, 2, 2, 7],
        "t2": [2.36, 3.58, 0.5, 1.72, 1.078],
        "c2": [2, 2, 1, 2, 1],
        "gamma2": [1]*5,

        "nr3": [4.245522, -0.31527585, -0.7212941, -0.2680657, -0.7859567],
        "d3": [1, 1, 3, 2, 2],
        "t3": [1.14, 2.43, 1.75, 1.1, 1.08],
        "alfa3": [0.641, 1.008, 1.026, 1.21, 0.93],
        "beta3": [0.516, 0.669, 0.25, 1.33, 2.1],
        "gamma3": [1.335, 1.187, 1.39, 1.23, 0.763],
        "epsilon3": [0.75, 1.616, 0.47, 1.306, 0.46]}

    eq = romeo,

    _vapor_Pressure = {
        "eq": 3,
        "n": [-10.4856, 3.8226, -8.6727, -4.144, 0.8801, -5.7224],
        "t": [1, 1.5, 2.8, 6.7, 8.9, 15.5]}
    _liquid_Density = {
        "eq": 1,
        "n": [3.43, -4.008, 8.4779, -7.894, 3.4824],
        "t": [0.39, 0.84, 1.27, 1.72, 2.26]}

    # The paper has a typo, and the N6 in saturated vapor density is missing
    # TODO: Do a correlation myself
    _vapor_Density = {
        "eq": 2,
        "n": [-5.0096, 0.9061, -61.4138, -143.5222, -369.0229],
        "t": [0.44, 2.32, 1.75, 4.4, 9.97, 20.9]}

    visco0 = {"__name__": "Meng (2018)",
              "__doi__": {
                  "autor": "Meng, X.Y., Sun, Y.K., Cao, F.L., Wu, J.T., "
                           "Vesovic, V.",
                  "title": "Reference Correlation of the Viscosity of "
                           "n-Hexadecane from the Triple Point to 673 K and "
                           "up to 425 MPa",
                  "ref": "J. Phys. Chem. Ref. Data 47(3) (2018) 033102",
                  "doi": "10.1063/1.5039595"},

              "eq": 1, "omega": 3,
              "collision": [-0.6131, 414.4, -39759],

              "sigma": 1,
              "n_chapman": 0.32137/M**0.5,

              "Tref_res": 722.1, "rhoref_res": M,
              "nr": [0.000692129, 0.00645721, -0.000305913, 1.26656e-12,
                     21.851, -30.2533, 21.0853],
              "dr": [9+2/3, 9+2/3, 11+2/3, 24+2/3, 1.6+2/3, 0.6+2/3, 2/3],
              "tr": [-0.5, 0.8, -0.5, 5, -0.5, -1.5, -0.5],

              "special": "_vir"}

    def _vir(self, rho, T, fase):
        # The initial density dependence has a different expresion, without muo
        muB = 0
        if rho:
            for i, n in enumerate([7.4345, -739.4, -2255587]):
                muB += n/T**i
        return muB*rho/self.M

    _viscosity = visco0,

class Test(TestCase):

    def test_meng(self):
        # Table 5, saturation states, include basic test for Romeo EoS
        st = nC16(T=293.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 10), 1.157e-7)
        self.assertEqual(round(st.Gas.rhoM, 11), 4.747e-8)
        self.assertEqual(round(st.Gas.mu.muPas, 2), 3.93)
        self.assertEqual(round(st.Liquido.rhoM, 4), 3.4168)
        self.assertEqual(round(st.Liquido.mu.muPas, 1), 3468.0)

        st = nC16(T=383.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 7), 1.828e-4)
        self.assertEqual(round(st.Gas.rhoM, 8), 5.740e-5)
        self.assertEqual(round(st.Gas.mu.muPas, 2), 5.18)
        self.assertEqual(round(st.Liquido.rhoM, 4), 3.1384)
        self.assertEqual(round(st.Liquido.mu.muPas, 1), 795.7)

        st = nC16(T=473.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 6), 9.779e-3)
        self.assertEqual(round(st.Gas.rhoM, 6), 2.521e-3)
        self.assertEqual(round(st.Gas.mu.muPas, 2), 6.72)
        self.assertEqual(round(st.Liquido.rhoM, 4), 2.8521)
        self.assertEqual(round(st.Liquido.mu.muPas, 1), 351.2)

        st = nC16(T=563.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 4), 1.087e-1)
        self.assertEqual(round(st.Gas.rhoM, 5), 2.528e-2)
        self.assertEqual(round(st.Gas.mu.muPas, 2), 9.03)
        self.assertEqual(round(st.Liquido.rhoM, 4), 2.5309)
        self.assertEqual(round(st.Liquido.mu.muPas, 1), 184.0)

        st = nC16(T=653.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 4), 5.507e-1)
        self.assertEqual(round(st.Gas.rhoM, 4), 1.381e-1)
        self.assertEqual(round(st.Gas.mu.muPas, 2), 12.44)
        self.assertEqual(round(st.Liquido.rhoM, 4), 2.1011)
        self.assertEqual(round(st.Liquido.mu.muPas, 1), 97.4)

        # Table 8, Pag 9
        self.assertEqual(round(nC16(T=300, rhom=0).mu.muPas, 3), 4.016)
        self.assertEqual(round(nC16(T=300, rhom=3.3958).mu.muPas, 3), 2952.344)
        self.assertEqual(round(nC16(T=300, rhom=3.5204).mu.muPas, 3), 5399.826)
        self.assertEqual(round(nC16(T=300, rhom=3.9643).mu.muPas, 2), 64703.41)
        self.assertEqual(round(nC16(T=400, rhom=0).mu.muPas, 3), 5.399)
        self.assertEqual(round(nC16(T=400, rhom=3.0865).mu.muPas, 3), 667.473)
        self.assertEqual(round(nC16(T=400, rhom=3.2773).mu.muPas, 3), 1133.060)
        self.assertEqual(round(nC16(T=400, rhom=3.8145).mu.muPas, 3), 8775.901)
        self.assertEqual(round(nC16(T=600, rhom=0).mu.muPas, 3), 8.135)
        self.assertEqual(round(nC16(T=600, rhom=2.8585).mu.muPas, 3), 325.831)
        self.assertEqual(round(nC16(T=600, rhom=3.578).mu.muPas, 3), 1463.805)
        self.assertEqual(round(nC16(T=700, rhom=0).mu.muPas, 3), 9.418)

        # This point isn't real, it's in two phases region so need force
        # calculation
        st = nC16(T=700, rhom=2.6752)
        mu = st._Viscosity(2.6752*st.M, 700, None)
        self.assertEqual(round(mu.muPas, 3), 223.559)

        self.assertEqual(round(nC16(T=700, rhom=3.4806).mu.muPas, 3), 949.425)

 
