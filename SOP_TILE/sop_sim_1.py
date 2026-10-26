from enum import Enum
class w(Enum): # wire names enumerated for router
    A = 0
    nA = 1
    B = 2
    nB = 3
    C = 4
    nC = 5
    D = 6
    nD = 7
    E = 8
    F = 9
    LOGIC_1 = 10
    LOGIC_0 = 11

class Bus6:
    def __init__(self, name):
        self.name = name
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0

    def input(self, a,b,c,d,e,f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def out(self):
        return [self.a, self.b, self.c, self.d, self.e, self.f]


class SOP_lut:
    def __init__(self, name):
        self.name = name
        self.config = None
        self.input = None  # 6 inputs in a list
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None

    def run(self):
        self.a, self.b, self.c, self.d, self.e, self.f = self.input + [None] * (6 - len(self.input))
        output = SOP_tile(self.a, self.b, self.c, self.d, self.e, self.f, self.config)
        return output

# Rest of your code...


def and4_gate(a,b,c,d):
    result = a and b and c and d
    return result

def or3_gate(a,b,c):
    result = a or b or c
    return result

def router(a,b,c,d,e,f,swither): # swither = [out1,out2,out3,out4] *4
    #           0      1    2     3     4   5       6   7       8   9   10  11
    selector = [a,  not a,  b,  not b,  c, not c,   d, not d    ,e,f,True,False]
    out1 = [selector[swither[0][0]],selector[swither[0][1]],selector[swither[0][2]],selector[swither[0][3]]   ]
    out2 = [selector[swither[1][0]],selector[swither[1][1]],selector[swither[1][2]],selector[swither[1][3]]   ]
    out3 = [selector[swither[2][0]],selector[swither[2][1]],selector[swither[2][2]],selector[swither[2][3]]   ]
    out4 = [selector[swither[3][0]],selector[swither[3][1]],selector[swither[3][2]],selector[swither[3][3]]   ]

    result = [out1,out2,out3,out4]

    return result

def SOP(and1, and2, and3, and4):
    result = [None,None,None]

    and1_out = and4_gate(and1[0],and1[1],and1[2],and1[3])
    and2_out = and4_gate(and2[0],and2[1],and2[2],and2[3])
    and3_out = and4_gate(and3[0],and3[1],and3[2],and3[3])
    and4_out = and4_gate(and4[0],and4[1],and4[2],and4[3])

    or1_out = or3_gate(and1_out,and2_out,0)
    or2_out = or3_gate(and3_out,and4_out,0)
    or3_out = or3_gate(or1_out,or2_out,0)

    result = [or1_out,or2_out,or3_out]
    return result

def SOP_tile(a,b,c,d,e,f,swither):

    sop_input = router(a,b,c,d,e,f,swither)
    sop_output = SOP(sop_input[0], sop_input[1], sop_input[2], sop_input[3])

    result = sop_output

    return result

### MAKE CONFIG FUNCTIONS

# def make_and()

def make_mux2(in1, in2,sw, en=False): #generates config for a single 2:1 mux using , if en is a value tha tpin becomes the enable pin otherwise it is alway enabled
    if sw in [8,9,10,11]:
      return "Error: sw is invalid must be a,b,c,d and not constant"
    else:
      if en == False:
        return [[in1, sw+1, 10, 10], [in2, sw, 10, 10]]
      else:
        return [[in1, sw+1, 10, en], [in2, sw, 10, en]]
    
def make_mux4(in1, in2,in3,in4,sw0,sw1, en=False): #generates config for a single 4:1 mux using 
    if sw0 in [8,9,10,11] or sw1 in [8,9,10,11] :
      return "Error: sw0 and sw1 are invalid must be a,b,c,d and not constant"
    else:
      if en == False:
        return [[in1.value, sw0.value+1, sw1.value+1, 10], [in2.value, sw0.value+1, sw1.value, 10],[in3.value, sw0.value+1, sw1.value+1, 10], [in4.value, sw0.value, sw1.value, 10]]
      else:
        return [[in1.value, sw0.value+1, sw1.value+1, en], [in2.value, sw0.value+1, sw1.value, en],[in3.value, sw0.value+1, sw1.value+1, en], [in4.value, sw0.value, sw1.value, en]]



### canmake mux 8 from 2 mux 1,4 or'd together
      # https://www.electronicshub.org/multiplexerandmultiplexing/

## need to make templates for :: and, or, nand,nor,invert, encoder,decoder, and sop generator from terms, look at old pythong logic maker program

# a = 1
# b = 0
# c = 0
# d = 0
# e = 0
# f = 0
# route_config = [[0,3,10,10],[0,2,10,10],[0,4,10,10],[11,11,11,11]]
# logic_test = SOP_tile(a,b,c,d,e,f,route_config)


# for f in range(2):
#     for e in range(2):
# #         for d in range(2):
# for a in range(2):
#     for b in range(2):
#         for c in range(2):
#             # for d in range(2):
#             #     for e in range(2):
#             #         for f in range(2):
#                         route_config = [[0, 5, 10, 10], [2, 4, 10, 10], [11, 11, 11, 11], [11, 11, 11, 11]] # mux2,a and b are muxed with c as the select 
#                         # route_config = [[1, 3, 10, 10], [0, 5, 10, 10], [0, 4, 10, 10], [11, 11, 11, 11]] # a'b' + ac' + ac

#                         logic_test = SOP_tile(a, b, c, d, e, f, route_config)
#                         print(f"{a}{b}{c}{d}{e}{f} => {logic_test}")

bus0 = Bus6("Global Bus 0")
bus1 = Bus6("Global Bus 1")
bus0.input(1,0,0,0,0,0)
sw0 = 0
sw1 = 0
# route_config = [[0, 5, 10, 10], [2, 4, 10, 10], [11, 11, 11, 11], [11, 11, 11, 11]]

sop0 = SOP_lut("SOP_0_0")
sop0.config = make_mux4(w.A, w.B,w.E,w.F,w.C,w.D, en=False)

bus0.input(1,0,0,0,0,0)
sop0.input = bus0.out()
output = sop0.run()

bus0.input(0,0,0,0,0,0)
sop0.input = bus0.out()
output = sop0.run()

bus0.input(1,0,1,0,0,0)
sop0.input = bus0.out()
output = sop0.run()

bus0.input(0,1,0,1,0,0)
sop0.input = bus0.out()
output = sop0.run()



# bus1.input(output)

print("done")
