import schemdraw
from schemdraw import logic
import schemdraw.elements as elm
from schemdraw.parsing import logicparse
from schemdraw import flow
from enum import Enum
from itertools import product

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

class S(Enum): # wire names enumerated for router
    BLACK = 0
    RED = 1
    GREEN = 2

class IO:
    def __init__(self, in_out, bus,config, xy):
        self.name = f'{in_out}->{bus.name}_{xy}'
        self.in_out_inout = in_out
        self.tristate = False
        self.xy = xy
        self.pad_val = 2
        self.io_out_val = 2
        self.tri_in = 2
        self.last_direction = None
        self.attacted_to_bus = bus
        self.router = None

        if in_out == "IN":
           self.router = IO2BUS(self,bus)
           self.router.config = config

    def set_val_pad_in(self,val):
           if self.tristate == False:
              self.last_direction = "IN"
              self.pad_val = val
           else:
              if self.tri_in == 1:
                  self.last_direction = "IN"
                  self.pad_val = val
              else:
                 self.last_direction = None
                 self.pad_val = 2
                 
        
    def set_val_pin_to_fpga(self,val):
           if self.tristate == False:
              self.last_direction = "OUT"
              self.io_out_val = val
           else:
              if self.tri_in == 1:
                  self.last_direction = "OUT"
                  self.io_out_val = val
              else:
                 self.last_direction = None
                 self.io_out_val = 2

    def run(self):
           if self.in_out_inout == None:
              print(f"Error IO: {self.name} is not set to IN, OUT or INOUT")
           else:
              if self.in_out_inout == "OUT":
                    self.pad_val = self.io_out_val
              if self.in_out_inout == "IN":
                    self.io_out_val = self.pad_val


class Bus6:
    def __init__(self, name, xy = (0,0)):
        self.name = name
        self.a = 2
        self.b = 2
        self.c = 2
        self.d = 2
        self.e = 2
        self.f = 2
        self.xy = xy

    def input(self, a,b,c,d,e,f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def out(self):
        return [self.a, self.b, self.c, self.d, self.e, self.f]
    
class IO2BUS:
  def __init__(self,IO_i,BUS_i):
    self.name = f"{IO_i.name}->{BUS_i.name}"
    self.input = IO_i
    self.output = BUS_i
    self.config = None
  def run(self):
     if self.config == 0:
        self.output.a = self.input.io_out_val
     if self.config == 1:
        self.output.b = self.input.io_out_val
     if self.config == 2:
        self.output.c = self.input.io_out_val
     if self.config == 3:
        self.output.d = self.input.io_out_val
     if self.config == 4:
        self.output.e = self.input.io_out_val
     if self.config == 5:
        self.output.f = self.input.io_out_val
   
class SOP2BUS:
  def __init__(self,SOP_i,BUS_i):
    self.name = f"{SOP_i.name}->{BUS_i.name}"
    self.input = SOP_i
    self.output = BUS_i
    self.config = None
  def run(self):
     if self.config == 0:
        self.output.a = self.input.postFF
     if self.config == 1:
        self.output.b = self.input.postFF
     if self.config == 2:
        self.output.c = self.input.postFF
     if self.config == 3:
        self.output.d = self.input.postFF
     if self.config == 4:
        self.output.e = self.input.postFF
     if self.config == 5:
        self.output.f = self.input.postFF

class BUS2SOP:
  def __init__(self,BUS_i,SOP_i):
    self.name = f"{BUS_i.name}->{SOP_i.name}"
    self.input = BUS_i
    self.output = SOP_i
    self.config = [None,None],[None,None],[None,None],[None,None],[None,None],[None,None] # bus signal, lut input
  def run(self):
     bus_value = self.input.out()
     for config in self.config:
        self.output.input[config[1]] = bus_value[config[0]]

   

class SOP_lut:
    def __init__(self, name,bus_in,bus_out,config_in, config_out, xy):
        self.name = name
        self.config = None
        self.input = [2,2,2,2,2,2]  # 6 inputs in a list
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.preFF = 2
        self.postFF = 2
        self.syncro = False
        self.xy = xy
        self.route_in = BUS2SOP(bus_in,self)
        self.route_out = SOP2BUS(self,bus_out)

        self.route_in.config = config_in
        self.route_out.config = config_out


    def run(self):
        self.a, self.b, self.c, self.d, self.e, self.f = self.input + [None] * (6 - len(self.input))
        output = SOP_tile(self.a, self.b, self.c, self.d, self.e, self.f, self.config)
        if self.syncro == False:
           self.preFF = output[2]
           self.postFF = output[2] # for now just return the full SOP
        else:
           self.preFF = output[2]

    def TT(self,a,b,c,d,e,f):
        output = SOP_tile(a, b, c, d, e, f, self.config)
        return output[2]

    def clock(self):
       self.postFF = self.preFF


# Rest of your code...


def and4_gate(a,b,c,d):
    result = a and b and c and d
    return result

def or3_gate(a,b,c):
    result = a or b or c
    return result

def mux2_1(a,b,sw):
    if sw == 0:
      return a
    else:
      return b


def router(a,b,c,d,e,f,swither): # swither= config = [out1,out2,out3,out4] *4 + e/f mux config + flip flop
    ef_mux = swither[4]
    if ef_mux == False:
      #           0      1    2     3     4   5       6   7       8   9   10  11
      selector = [a,  not a,  b,  not b,  c, not c,   d, not d    ,None,None,True,False] #true and false only for simulation, in actual design double up logic
    else:
      #           0      1    2     3     4   5    6   7       8   9   10  11
      selector = [a,  not a,  b,  not b,  c, e,   d, f   ,None,None,True,False]
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
    if len(swither) == 4:
       swither.append(False)
    sop_input = router(a,b,c,d,e,f,swither)
    sop_output = SOP(sop_input[0], sop_input[1], sop_input[2], sop_input[3])

    result = sop_output

    return result

### MAKE CONFIG FUNCTIONS

# def make_and()

def make_mux2(in1, in2,sw, en=False, ): #generates config for a single 2:1 mux using , if en is a value tha tpin becomes the enable pin otherwise it is alway enabled
    if sw in [8,9,10,11]:
      return "Error: sw is invalid must be a,b,c,d and not constant"
    else:
      if en == False:
        return [[in1, sw+1, 10, 10], [in2, sw, 10, 10],[7,7,7,7],[7,7,7,7],True]
      else:
        return [[in1, sw+1, 10, en], [in2, sw, 10, en],[7,7,7,7],[7,7,7,7],True]
    
def make_mux4(in1, in2,in3,in4,sw0,sw1, en=False): #generates config for a single 4:1 mux using 
    if sw0 in [8,9,10,11] or sw1 in [8,9,10,11] :
      return "Error: sw0 and sw1 are invalid must be a or b and not constant"
    else:
      if en == False:
        return [[in1.value, sw0.value+1, sw1.value+1, 10], [in2.value, sw0.value+1, sw1.value, 10],[in3.value, sw0.value+1, sw1.value+1, 10], [in4.value, sw0.value, sw1.value, 10],True]
      else:
        return [[in1.value, sw0.value+1, sw1.value+1, en], [in2.value, sw0.value+1, sw1.value, en],[in3.value, sw0.value+1, sw1.value+1, en], [in4.value, sw0.value, sw1.value, en],True]

def show_sop_state(sop0):
  with schemdraw.Drawing() as d:
      d.config(unit=0.5)
      XP = elm.Ic(pins=[
                  elm.IcPin(name='A', side='left',color=S(sop0.input[0]).name),
                  elm.IcPin(name='B',  side='left',color=S(sop0.input[1]).name),
                  elm.IcPin(name='C',  side='left',color=S(sop0.input[2]).name),
                  elm.IcPin(name='D',  side='left',color=S(sop0.input[3]).name),
                  elm.IcPin(name='E',  side='left',color=S(sop0.input[4]).name),
                  elm.IcPin(name='F',  side='left',color=S(sop0.input[5]).name),

                  # elm.IcPin(name='SOP_0', side='right',color=S(sop0.run()[0]).name),
                  # elm.IcPin(name='SOP_1', side='right',color=S(sop0.run()[1]).name),
                  elm.IcPin(name='sOP_2', side='right',color=S(sop0.postFF).name),

                        ],
                    edgepadW = -3.1,  # Make it a bit wider
                    pinspacing=0.6).label('Sop_tile_0', 'bottom', fontsize=12)
      
  d.draw()

# Show SOP TILE CONFIGURATION
def show_sop(sop0):
  g1 = f'({w(sop0.config[0][0]).name} and {w(sop0.config[0][1]).name} and {w(sop0.config[0][2]).name} and {w(sop0.config[0][3]).name})'
  g2 = f'({w(sop0.config[1][0]).name} and {w(sop0.config[1][1]).name} and {w(sop0.config[1][2]).name} and {w(sop0.config[1][3]).name})'
  g3 = f'({w(sop0.config[2][0]).name} and {w(sop0.config[2][1]).name} and {w(sop0.config[2][2]).name} and {w(sop0.config[2][3]).name})'
  g4 = f'({w(sop0.config[3][0]).name} and {w(sop0.config[3][1]).name} and {w(sop0.config[3][2]).name} and {w(sop0.config[3][3]).name})'
  g5 = f'({g1} or {g2} )'
  g6 = f'({g3} or {g4} )'
  g7 = f'({g5} or {g6} )'
  d = logicparse(g7, outlabel='$SOP$')
  elements = d.elements

  d.draw()

def make_sop_element(sop0):
   nc = ""
   if sop0.config == None:
      nc = "(nc)"
   return elm.Ic(pins=[
                      elm.IcPin(name=f'A{nc}', side='left',color=S(sop0.input[0]).name),
                      elm.IcPin(name=f'B{nc}',  side='left',color=S(sop0.input[1]).name),
                      elm.IcPin(name=f'C{nc}',  side='left',color=S(sop0.input[2]).name),
                      elm.IcPin(name=f'D{nc}',  side='left',color=S(sop0.input[3]).name),
                      elm.IcPin(name=f'E{nc}',  side='left',color=S(sop0.input[4]).name),
                      elm.IcPin(name=f'F{nc}',  side='left',color=S(sop0.input[5]).name),

                    #   elm.IcPin(name='SOP_0', side='right',color=S(sop0.run()[0]).name),
                    #   elm.IcPin(name='SOP_1', side='right',color=S(sop0.run()[1]).name),
                      elm.IcPin(name='sOP_2', side='right',color=S(sop0.postFF).name),

                            ],
                        edgepadW = -3.1,  # Make it a bit wider
                        pinspacing=0.6).label(sop0.name, 'bottom', fontsize=12)
   

def make_bus_element(bus0,d):
    buslength = d.unit*16
    offset = 0.0
    spacing = 0.1
    logic.Line().down(buslength).label(f'{bus0.name}', 'left').color(S(bus0.a).name)
    d.move( dx=spacing, dy = buslength - offset)  
    logic.Line().down(buslength).color(S(bus0.b).name)  
    d.move( dx=spacing, dy = buslength- offset)  
    logic.Line().down(buslength).color(S(bus0.c).name)  
    d.move( dx=spacing, dy = buslength - offset)    
    logic.Line().down(buslength).color(S(bus0.d).name)   
    d.move( dx=spacing, dy = buslength - offset)  
    logic.Line().down(buslength).color(S(bus0.e).name)   
    d.move( dx=spacing, dy = buslength - offset)  
    logic.Line().down(buslength).color(S(bus0.f).name)   
    d.move( dx=spacing, dy = buslength - offset)  
   

def show_fpga_state(SOP0,SOP1,SOP2,SOP3, bus0,bus1,bus2):

  with schemdraw.Drawing() as d:
    d.config(unit=0.5)

    make_sop_element(SOP0)
    d.move( dx=6) 
    make_sop_element(SOP1)
    d.move(dy=-6, dx=-6) 
    make_sop_element(SOP2)
    d.move( dx=6) 
    make_sop_element(SOP3)

    d.move( dx=-9, dy = 10)
    make_bus_element(bus0,d)
    d.move( dx=6, dy = 0)
    make_bus_element(bus1,d)
    d.move( dx=6, dy = 0)
    make_bus_element(bus2,d)

    




  d.draw()

def print_SOP_def(sop0):
   print(f"Logic Type SOP")
   print(f"Name: {sop0.name}")
   print(f"Config: {sop0.config}")
   print(f"Input: {sop0.input}")
   print(f"Syncronus: {sop0.syncro}")

def print_SOP_state(sop0):
   print(sop0)


def print_SOP_TT_nbit(sop, num_bits, endidness = False, reverse_order=False):
    input_variables = [chr(ord('a') + i) for i in range(num_bits)]
    input_str = ''.join(input_variables)

    if reverse_order:
        input_str = input_str[::-1]

    print(f"{input_str} => out")

    for values in product(range(2), repeat=num_bits):
        if reverse_order:
            values = values[::-1]
        input_values = ''.join(map(str, values))
        result = sop.TT(*values, *[0] * (6 - num_bits))
        print(f"{input_values} => {result}")

def run_fpga_async(fpga_in):
    IO = fpga_in[0]
    tiles = fpga_in[1]
    for element in IO:
       element.run()
       element.router.run()  
    for element in tiles:
       element.route_in.run()
       element.run()
       element.route_out.run()
    for element in IO:
       element.router.run()
       element.run()
   



    # SOP0.input = B0.out() # update the SOP input
    # SOP1.input = B1.out() # update the SOP input

    # SOP0.run() # get the SOP output
    # SOP1.run() # get the SOP output
    # B1.a=SOP0.postFF
    # B2.a=SOP1.postFF

    # SOP0.input = B0.out() # update the SOP input
    # SOP1.input = B1.out() # update the SOP input

### canmake mux 8 from 2 mux 1,4 or'd together
      # https://www.electronicshub.org/multiplexerandmultiplexing/

## need to make templates for :: and, or, nand,nor,invert, encoder,decoder, and sop generator from terms, look at old pythong logic maker program

#Build a 2x2 FPGA with 3 busses running vericly
B0 = Bus6("BO",(0,0))

B1 = Bus6("B1",(2,0))

B2 = Bus6("B2",(4,0))

rout_bus2sop_0 = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
rout_bus2sop_1 = [[0,0],[1,1],[3,2],[0,0],[0,0],[0,0]]


SOP0 = SOP_lut("SOP_0_0",B0,B1,rout_bus2sop_0,0,(1,0))
SOP1 = SOP_lut("SOP_0_1",B1,B2,rout_bus2sop_0,0,(3,0))
SOP2 = SOP_lut("SOP_1_0",B0,B1,rout_bus2sop_1,1,(1,1))
SOP3 = SOP_lut("SOP_1_1",B1,B2,rout_bus2sop_0,1,(3,1)) 


# route_config = [[0, 5, 10, 10], [2, 4, 10, 10], [11, 11, 11, 11], [11, 11, 11, 11]]

# sop0 = SOP_lut("SOP_0_0") # make a SOP tile
# sop0.config = make_mux4(w.A, w.B,w.E,w.F,w.C,w.D, en=False) # config it to be a 4:1 mux with c and d as the sw
SOP0.config = [[1, 3, 10, 10], [0, 5, 10, 10], [0, 4, 10, 10], [11, 11, 11, 11]] # a'b' + ac' + ac
SOP1.config = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]] # inverter of a
SOP2.config = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]] # inverter of a
SOP3.config = make_mux2(0, 2,4) # mux2 this is not working
IN1 = IO("IN",B0,0,(0,0)) # create input pin connected to bus 0 via a router connected to wire a on bus 0


# route_0 = IO2BUS(IN1,B0)
# route_0.config = 0
fpga_one = [IN1],[SOP0,SOP1,SOP2,SOP3]

IN1.set_val_pad_in(1)

B0.b = 1
B0.d = 1

show_fpga_state(SOP0,SOP1,SOP2,SOP3, B0,B1,B2)

run_fpga_async(fpga_one)

show_fpga_state(SOP0,SOP1,SOP2,SOP3, B0,B1,B2)

IN1.set_val_pad_in(0)

run_fpga_async(fpga_one)

##############################


show_fpga_state(SOP0,SOP1,SOP2,SOP3, B0,B1,B2)

print("")





def show_sop_full(sop0):

  with schemdraw.Drawing() as d:
      d.config(unit=0.5)
#place and gates and not gates 
      a0 = logic.And(inputs=4)
      d.move_from(a0.in1, dy=-2.5)
      a1 = logic.And(inputs=4)
      d.move_from(a1.in1, dy=-2.5)
      a2 = logic.And(inputs=4)
      d.move_from(a2.in1, dy=-2.5)
      a3 = logic.And(inputs=4)

      logic.Line().left(d.unit).at(a0.in1).label('A3_0', 'left')
      logic.Line().left(d.unit).at(a0.in2).label('A3_1', 'left')
      logic.Line().left(d.unit).at(a0.in3).label('A3_2', 'left')
      logic.Line().left(d.unit).at(a0.in4).label('A3_3', 'left')

      logic.Line().left(d.unit).at(a1.in1).label('A2_0', 'left')
      logic.Line().left(d.unit).at(a1.in2).label('A2_1', 'left')
      logic.Line().left(d.unit).at(a1.in3).label('A2_2', 'left')
      logic.Line().left(d.unit).at(a1.in4).label('A2_3', 'left')

      logic.Line().left(d.unit).at(a2.in1).label('A1_0', 'left')
      logic.Line().left(d.unit).at(a2.in2).label('A1_1', 'left')
      logic.Line().left(d.unit).at(a2.in3).label('A1_2', 'left')
      logic.Line().left(d.unit).at(a2.in4).label('A1_3', 'left')

      logic.Line().left(d.unit).at(a3.in1).label('A0_0', 'left')
      logic.Line().left(d.unit).at(a3.in2).label('A0_1', 'left')
      logic.Line().left(d.unit).at(a3.in3).label('A0_2', 'left')
      logic.Line().left(d.unit).at(a3.in4).label('A0_3', 'left')

#place or gates
      d.move_from(a3.in1, dy=0.5, dx= 2.5)
      o0 = logic.Or(inputs=2).right()
      d.move_from(o0.in1, dy=3.5)
      o1 = logic.Or(inputs=2)
      d.move_from(o0.in1, dy=1.5,dx=2.5)
      o2 = logic.Or(inputs=2).label('SOP_2', 'right')

      logic.Wire('-|').at(o1.in1).to(a0.out)
      logic.Wire('-|').at(o1.in2).to(a1.out)
      logic.Wire('-|').at(o0.in1).to(a2.out)
      logic.Wire('-|').at(o0.in2).to(a3.out)
      logic.Wire('-|').at(o2.in1).to(o1.out)
      logic.Wire('-|').at(o2.in2).to(o0.out)
      logic.Line().at(o1.out).tox(o2.out).label('SOP_0', 'right')
      logic.Line().at(o0.out).tox(o2.out).label('SOP_1', 'right')

      d.move_from(o0.in1, dy=-2,dx=-7)


      XP = elm.Ic(pins=[
              elm.IcPin(name='A', side='left'),
              elm.IcPin(name=r'$\overline{A}$', side='left'),
              elm.IcPin(name='B',  side='left'),
              elm.IcPin(name=r'$\overline{B}$',  side='left'),
              elm.IcPin(name='C',  side='left'),
              elm.IcPin(name=r'$\overline{C}$',  side='left'),
              elm.IcPin(name='D',  side='left'),
              elm.IcPin(name=r'$\overline{D}$', side='left'),
              elm.IcPin(name='E',  side='left'),
              elm.IcPin(name='F',  side='left'),

              elm.IcPin(name='A_0', side='right'),


              elm.IcPin(name='A_1', side='right'),


              elm.IcPin(name='A_2', side='right'),


              elm.IcPin(name='A_3', side='right'),


                    ],
                edgepadW = -3.1,  # Make it a bit wider
                pinspacing=0.6).label('Xpoint', 'bottom', fontsize=12)
      
      d.move_from(XP.inL2, dx=-4)
      n0 = logic.Not()
      n4 = logic.Not().length(2)
      d.move_from(XP.inL4, dx=-4)
      n1 = logic.Not()
      n5 = logic.Not().length(3)
      d.move_from(XP.inL6, dx=-4)
      n2 = logic.Not()
      n6 = logic.Not().length(2)
      d.move_from(XP.inL8, dx=-4)
      n3 = logic.Not()
      n7 = logic.Not().length(3)
      #logic labels for not input gates
      A = logic.Line().left(d.unit*2).at(n0.in1).label('A', 'left')
      B = logic.Line().left(d.unit*2).at(n1.in1).label('B', 'left')
      C = logic.Line().left(d.unit*2).at(n2.in1).label('C', 'left')
      D = logic.Line().left(d.unit*2).at(n3.in1).label('D', 'left')




      logic.Wire('-|').at(XP.A).to(n0.out)
      logic.Wire('-|').at(XP.B).to(n1.out)
      logic.Wire('-|').at(XP.C).to(n2.out)
      logic.Wire('-|').at(XP.D).to(n3.out)

      logic.Wire('-|').at(XP.inL2).to(n4.out)
      logic.Wire('-|').at(XP.inL4).to(n5.out)
      logic.Wire('-|').at(XP.inL6).to(n6.out)
      logic.Wire('-|').at(XP.inL8).to(n7.out)

      E = logic.Line().left(d.unit*10).at(XP.inL9).label('E', 'left')
      F = logic.Line().left(d.unit*10).at(XP.inL10).label('F', 'left')

      
  elements = d.elements
  d.draw()
      
show_sop_full(sop0)



print("done")
