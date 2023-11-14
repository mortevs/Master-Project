import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time
start_time=time.time()
perm1=1e-13 #Permeability constants
perm2=1e-17
perm3=2e-14
mu=1e-3 #Viscosity
poro=0.2 #porosity
c_t=1e-9 #total compressibiliy [1/Pa]
p_r=2e+7 #initial pressure [Mpa]
p_w=1e+7 #Well pressure [Mpa]

    
#calculations 

dx=1 #steplength 
dy=1
dt=1/2 #timelength set to half a second
h=50 #reservoir height [m]
l=200 #reservoir length [m]

#creating the permeability matrix
k=pd.DataFrame(np.zeros((h, l)))  
k[0:20]=perm1 #Adding correct permeability to the layers
k[20:30]=perm2
k[30:50]=perm3

#creating initial pressure distribution matrix [t=0]
def initialize(): 
    p=pd.DataFrame(np.zeros((h, l))) #Pandas dataframe
    p[p.columns[0:200]]=p_r #initial pressure
    p[0][0:20]=p_w #boundary condition
    p[0][30:50]=p_w #boundary condition
    return p
flowlist=[]
#update flow gradient in horizontal direction 
def update_gradient(p):
    #Manipulating matrices
    p2=p[p.columns[1:200]] #p shifted dx
    p2 = p2.T.reset_index(drop=True).T #Resetting index, (needed to transpose since reset index resets rows)
    p2.insert(loc=199, column=199, value=p[199]) #Adding end point value for forward difference

    #Calculating Pressure gradient:
    p_der_x=(p2-p)/dx #Forward finite difference method

    #Calculating flow and manipulating matrices:
    qx=p_der_x*(-k)/mu #Flow in horizontal direction
    update_gradient.variable=qx #Saving flow as variable
    qx2=qx[qx.columns[1:200]] #p shifted dx
    qx2 = qx2.T.reset_index(drop=True).T #Resetting index, 
    df = pd.DataFrame([0 for _ in range(50)]) #A column of zeros
    qx2.insert(loc=199, column=199, value=df) #Inserting zero to end ponint for boundary condition
    qx2 = qx2.T.reset_index(drop=True).T 

    #Calculating flow gradient:
    qx_der_x=(qx2-qx)/dx #Backward finite difference method
    qx_der_x.insert(loc=0, column=-1, value=df) #Inserting 0 for correct backward difference
    qx_der_x = qx_der_x.T.reset_index(drop=True).T
    qx_der_x=qx_der_x[qx_der_x.columns[0:200]] #Shifting the matrix for correct calculation

    Q = -qx[0].sum()
    flowlist.append(Q)
    #update_gradient.variable=flowlist
    return qx_der_x

#update flow gradient in vertical direction
def update_gradient2(p):
    #Manipulating matrices:
    py2=(p[1:50]).reset_index(drop=True)
    py2=py2.append(p[49:50]) #Adding end point value for forward difference

    #Calculating pressure gradient
    p_der_y=(py2-p)/dy #Forward difference method

    #Calculating flow and manipulating matrices:
    qy=p_der_y*-k/mu #Flow in vertical direction
    update_gradient2.variable=qy #saving flow as variable
    qy2=qy[1:50] #qy shifted dy
    qy2=qy2.reset_index(drop=True) 
    df = pd.DataFrame(np.zeros((1, 200)))#Zero matrix
    qy2=qy2.append(df) #Adding zero for boundary condidion
    qy2=qy2.reset_index(drop=True)

    #Calculating flow gradient:
    qx_der_y=(qy2-qy)/dy #Backward difference 
    qx_der_y=df.append(qx_der_y) #Adding zero for boundary condition
    qx_der_y = qx_der_y.reset_index(drop=True)
    qx_der_y=qx_der_y[0:50] #Shifting matrix for correct backward difference
    return qx_der_y

#Calculate pressure distribution matrix at time t [s]
def calculate_pressure(t):
    p=initialize()
    for i in range(1,t+1):
        qx_der_x=update_gradient(p) #Fetching dq/dx
        qx_der_y=update_gradient2(p) #Fetching dq/dy

        p+=-dt/(poro*c_t)*(qx_der_x+qx_der_y) #Main equation
    return p

# def calculate_flow(t):
#     for i in range(1,t+1): 
#         qx = update_gradient.variable
#         #print(qx)
#         Q = -qx.sum(columns(0))
#         #print(Q)
#     return Q 

#plotting the pressure distribution matrix at time t [s]
def plot_pressure(t):

    p=calculate_pressure(t)
    p = p.reindex(index=p.index[::-1]) #need to reverse rows for plotting
    plt.imshow(p, origin="lower", cmap="jet", extent = (0, 200, 50, 0), aspect=3)
    plt.xlabel('Distance from well [m]')
    plt.ylabel('Depth [m]')
    plt.title('Pressure [MPa], Time: '+ str(t/(3600*2)) + ' hour(s)')
    cbar = plt.colorbar()
    #cbar.set_ticks(['10', '11','12','13','14','15','16','17','18','19','20'])

    #For plotting flow arrays
    U=update_gradient.variable #Fetching horizontal flow
    V=update_gradient2.variable #Fetching vertical flow
    U=U.iloc[:, ::20] #Point every ten meters in x-direction
    U=U.iloc[::4, :] #Point every four meters in y-direction
    V=V.iloc[:, ::20]
    V=V.iloc[::4, :]
    x,y = np.meshgrid(np.arange(0,200,20),np.arange(0,50,4)) #Creating grid for vectors 
    plt.quiver(x,y, U, -V, width=0.002, headwidth=4, scale=None) #Plotting vectors and rescaling
    plt.show()

    #Flow into the well
def plot_flow(t):  
    t=np.linspace(0, t*1/2, t)
    Q=np.array(flowlist)
    plt.plot(t, Q)
    plt.yscale('log',base = 10)
    plt.xscale('log',base = 10)
    plt.grid()
    plt.title('Flow into the well ')
    plt.xlabel('Time [s]')
    plt.ylabel('Flow [m3/s]')
    plt.show()

def run(t):
    plot_pressure(t*3600*2)

    #calling on the plot pressure function as a function of the calculated pressure at time t.
    #because dt is 0.5, we need to double the time
    #In this partical case 1 hour is the chosen simulation time
     #calculate_pressure(3600*2*24*4)
     #print(time.time()-start_time) #Prints running time
     #plot_flow(3600*2*24*4) #plotting log-log flow vs time 4 days
      #print(sum(flowlist)) #cumulative produciton 