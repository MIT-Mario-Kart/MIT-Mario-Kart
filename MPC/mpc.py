from collections import namedtuple
import math 
import ipyopt

State = namedtuple('State', ['x', 'y', 'psi', 'v']) # phi -> orientation angle, v velocity

Actuation_Signal = namedtuple('Actuation_Signal', ['a', 'delta']) # a -> throttle, delta -> steering angle
Weight = namedtuple('Weight', ['w_cte', 'w_epsi', 'w_roc_a', 'w_roc_delta'])
Cost_Info = namedtuple('Cost_Info', ['cte', 'epsi', 's_dif_velocity'])
# TODO add a way to check that values are valid (within  the correct ranges when defining the tuples)

dt = 1 # TODO to be determined through testing
N = 1 # TODO to be determined through testing
Lf = 2.67 # TODO corresponds to the radius of the circle formed with constant steering angle and velocity on a flat terrain

ref = State(0, 0, 0, 1) # TODO add reference positions
roc_a = 0 # TODO to be determined through testing
roc_delta = 0 # TODO to be determined through testing
weights = Weight(0, 0, 0, 0) # TODO to be determined through testing

def update_state(cur: State, act: Actuation_Signal): # act represents 
    dx = cur.x + cur.v * math.cos(cur.psi) * dt
    dy = cur.y + cur.v * math.sin(cur.psi) * dt
    dv = cur.v + act.a * dt
    dpsi = cur.psi + (cur.v/Lf) * act.delta * dt
    cte = math.pow(cur.x-ref.x, 2) + math.pow(cur.y-ref.y, 2)
    epsi = math.pow(math.abs(cur.psi - ref.psi), 2)
    s_dif_velocity = math.pow(cur.v - ref.v, 2)
    return State(cur.x + dx, cur.y + dy, cur.psi + dpsi, cur.v + dv), Cost_Info(cte, epsi, s_dif_velocity)

def cost_function(act: Actuation_Signal, cost_info: Cost_Info):
    cost = weights.w_cte * cost_info.cte +  weights.w_epsi * cost_info.epsi + cost_info.s_dif_velocity + math.pow(act.a, 2) + math.pow(act.delta, 2) + weights.w_roc_a * roc_a + weights.w_roc_delta * roc_delta
    return cost

x_start = 0
y_start = x_start + N
psi_start = y_start + N
v_start = psi_start + N
cte_start = v_start + N
epsi_start = cte_start + N
delta_start = epsi_start + N
a_start = delta_start + N - 1
    
