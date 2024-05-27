import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FlowSimulation:
    def __init__(self, t, perm1=1e-13, perm2=1e-17, perm3=2e-14, mu=1e-3, poro=0.2, c_t=1e-9, p_r=2e+7, p_w=1e+7):
        self.t = t
        self.perm1 = perm1
        self.perm2 = perm2
        self.perm3 = perm3
        self.mu = mu
        self.poro = poro
        self.c_t = c_t
        self.p_r = p_r
        self.p_w = p_w

        self.dx = 1
        self.dy = 1
        self.dt = 1 / 2
        self.h = 50
        self.l = 200

        self.flowlist = []
        self.k = self.create_permeability_matrix()
        self.p = self.initialize_pressure_matrix()

    def create_permeability_matrix(self):
        k = pd.DataFrame(np.zeros((self.h, self.l)))
        k[0:20] = self.perm1
        k[20:30] = self.perm2
        k[30:50] = self.perm3
        return k

    def initialize_pressure_matrix(self):
        p = pd.DataFrame(np.zeros((self.h, self.l)))
        p[p.columns[0:200]] = self.p_r
        p.iloc[0, 0:20] = self.p_w
        p.iloc[0, 30:50] = self.p_w
        return p

    def update_gradient(self, p):
        p2 = p[p.columns[1:200]].copy()
        p2 = p2.T.reset_index(drop=True).T
        p2.insert(loc=199, column=199, value=p[199])

        p_der_x = (p2 - p) / self.dx

        qx = p_der_x * (-self.k) / self.mu
        qx2 = qx[qx.columns[1:200]].copy()
        qx2 = qx2.T.reset_index(drop=True).T
        df = pd.DataFrame([0 for _ in range(50)])
        qx2.insert(loc=199, column=199, value=df)
        qx2 = qx2.T.reset_index(drop=True).T

        qx_der_x = (qx2 - qx) / self.dx
        qx_der_x.insert(loc=0, column=-1, value=df)
        qx_der_x = qx_der_x.T.reset_index(drop=True).T
        qx_der_x = qx_der_x[qx_der_x.columns[0:200]]

        Q = -qx[0].sum()
        self.flowlist.append(Q)

        return qx_der_x

    def update_gradient2(self, p):
        py2 = pd.concat([p[1:50].reset_index(drop=True), p[49:50].reset_index(drop=True)], ignore_index=True)

        p_der_y = (py2 - p) / self.dy

        qy = p_der_y * -self.k / self.mu
        qy2 = qy[1:50].copy()
        qy2 = qy2.reset_index(drop=True)
        df = pd.DataFrame(np.zeros((1, 200)))
        qy2 = pd.concat([qy2, df], ignore_index=True)

        qx_der_y = (qy2 - qy) / self.dy
        qx_der_y = pd.concat([df, qx_der_y], ignore_index=True)
        qx_der_y = qx_der_y[0:50]

        return qx_der_y

    def calculate_pressure(self):
        p = self.p.copy()
        for _ in range(0, self.t - 1):
            qx_der_x = self.update_gradient(p)
            qx_der_y = self.update_gradient2(p)
            p += -self.dt / (self.poro * self.c_t) * (qx_der_x + qx_der_y)
        return p

    def get_pressure_plot(self):
        p = self.calculate_pressure()
        p = p.reindex(index=p.index[::-1])
        fig, ax = plt.subplots()
        cax = ax.imshow(p, origin="lower", cmap="jet", extent=(0, 200, 50, 0), aspect=3)
        ax.set_xlabel('Distance from well [m]')
        ax.set_ylabel('Depth [m]')
        ax.set_title(f'Pressure [MPa], Time: {self.t / (3600 * 2)} hour(s)')
        fig.colorbar(cax)

        U = self.update_gradient(self.p)
        V = self.update_gradient2(self.p)
        U = U.iloc[:, ::20]
        U = U.iloc[::4, :]
        V = V.iloc[:, ::20]
        V = V.iloc[::4, :]
        x, y = np.meshgrid(np.arange(0, 200, 20), np.arange(0, 50, 4))
        ax.quiver(x, y, U, -V, width=0.002, headwidth=4, scale=None)
        
        return fig

    def get_flow_plot(self):
        t = np.linspace(0, self.t * 1/2, self.t)
        Q = np.array(self.flowlist)
        fig, ax = plt.subplots()
        ax.plot(t, Q)
        ax.set_yscale('log', base=10)
        ax.set_xscale('log', base=10)
        ax.grid()
        ax.set_title('Flow into the well')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Flow [m³/s]')
        
        return fig




