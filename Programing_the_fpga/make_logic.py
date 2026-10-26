import itertools 

class lut:
    def __init__(self, top, bottom = None):
        self.type = "3 In , 2 Out"
        self.top_logic = ''
        self.bot_logic = ''
        #needs a location name from a list, unique
        if bottom == None:
            self.lut_top = top
            self.lut_bottom = 0
        else:
            self.lut_top = top
            self.lut_bottom = bottom

    def __str__(self):
        return f"{self.type} {hex(self.lut_top)}  /  {hex(self.lut_bottom)}"

class lut_config:
    def __init__(self, config):
        self.value = config
    def __str__(self):
        a = self.value and 1
        b = self.value and 2
        c = self.value and 4
        d = self.value and 8
        e = self.value and 16
        f = self.value and 32
        g = self.value and 64
        h = self.value and 128
        return f"Value {bin(self.value)} \n O0 clk = {a} \n O1 clk = {b} \n O2 clk = {c} \n O3 clk = {d} \n O0->a clk = {e} \n O1->a2 clk = {f} \n O3->a2 clk = {g} \n O3->a clk = {h} \n"

        
class clb:    
    def __init__(self, atype, btype, config):
        
        self.a_type = atype
        self.a_val = make(atype)
        self.b_type = btype
        self.b_val = make(btype)   

        self.config = lut_config(config)

    def info(self):
        return f" LutA {self.a_type} = {hex(self.a_val)} \n LutB {self.b_type} = {hex(self.b_val)} \n Config {self.config} \n"
        
        
    def bit(self):
        #return int(self.a_val,2) + (int(self.b_val,2) << 7) + (int(self.config,2) << 15)
        return self.a_val + (self.b_val << 7) + (self.config.value << 15)

    # def set_config(self):

        
    #     self.config.value or 

# Logic functions: take and return iterators of truth values
    
def make(result):
    data = create(num=3)
    Shift_reg8 = ''
    Shift_reg8B = ''
    tup = 0
    for row, result_cell in zip(data, result):
        if type(result_cell) is tuple:
            Shift_reg8 = Shift_reg8 + ({True: '1', False:'0'}[result_cell[0]])
            Shift_reg8B = Shift_reg8B + ({True: '1', False:'0'}[result_cell[1]])
            tup =1
        else:
            Shift_reg8 = Shift_reg8 + ({True: '1', False:'0'}[result_cell])
            tup = 0
    if tup == 1 :
        return int(Shift_reg8,2) + (int(Shift_reg8B,2) << 7)
    else:
        return int(Shift_reg8,2)

def AND(a, b, c = None):
    if c == None:
        for p, q in zip(a, b):
            yield p and q
    else:
        ab = []
        for p, q in zip(a, b):
            ab.append(p and q)
        for p, q in zip(ab, c):
            yield p and q

def OR(a, b, c = None):
    if c == None:
        for p, q in zip(a, b):
            yield p or q
    else:
        ab = []
        for p, q in zip(a, b):
            ab.append(p or q)
        for p, q in zip(ab, c):
            yield p or q

def NOT( a):
    for p in a:
        yield not p

def BUF(a):
    for p in a:
        yield p

def NAND( a, b, c = None):
    if c == None:
        result = AND( a, b)
        for p in result:
            yield not p
    else:
        result = AND( a, b, c)
        for p in result:
            yield not p

def NOR( a, b, c = None):
    if c == None:
        result = OR( a, b)
        for p in result:
            yield not p
    else:
        result =OR( a, b, c)
        for p in result:
            yield not p

def XOR( a, b, c = None):
    if c == None:
        for p, q in zip(a, b):
            yield p ^ q
    else:
        ab = []
        for p, q in zip(a, b):
            ab.append(p ^ q)
        for p, q in zip(ab, c):
            yield p ^ q

def XNOR( a, b, c = None):
    if c == None:
        for p, q in zip(a, b):
            yield ~(p ^ q)
    else:
        ab = []
        for p, q in zip(a, b):
            ab.append(~(p ^ q))
        for p, q in zip(ab, c):
            yield ~(p ^ q)


def ADD( a, b, c = None):
    if c == None:  # half adder no carry in
        sum = XOR(a, b)
        carry = AND(a, b)
        for p, q in zip(sum, carry):
            yield p , q
    else: # full adder with
        carry = [1,1,1,0,1,0,0,0]
        sum = [1,0,0,1,0,1,1,0]
        for p, q in zip(sum, carry):
            yield p , q

def SUB( a, b, c = None): # need to check it works
    if c == None:  # half sub no borrow in
        diff = XOR(a, b)
        borrow = AND(NOT(a), b)
        for p, q in zip(diff, borrow):
            yield p , q
    else: # full sub with
        borrow = [1,0,0,0,1,1,1,0]
        diff = [1,0,0,1,0,1,1,0]
        for p, q in zip(diff, borrow):
            yield p , q

def ENC( a, b, c): # need to check it works 3:2 encoder
    Aout = [1,1,1,1,1,1,1,0]
    Bout = [1,1,1,1,0,0,0,0]
    for p, q in zip(Aout, Bout):
        yield p , q

def DEC( a, b, c): # need to check it works 2:2 binary to dec decoder
    Aout = [0,0,0,0,0,0,1,0]
    Bout = [0,0,0,0,0,1,0,0]
    for p, q in zip(Aout, Bout):
        yield p , q

def MUX2( a, b, c): # need to check it works 2:1 mux with c as the switch
    muxout = [1,1,0,0,1,0,1,0]
    
    for p in muxout:
        yield p

    #make function to pass inputs to output 1 or 2 that caN BE SUPER IMPOSED ON A FUNCTION
    #SO YOU CAN USE THE SECOND HALF OF A LUT TO DRIVE THE SECODN LUT USING THE INTERNAL SWITCHING








def create(num=2):
    ''' Returns a list of all of the possible combinations of truth for the given number of variables.
    ex. [(T, T), (T, F), (F, T), (F, F)] for two variables '''
    return list(itertools.product([True, False], repeat=num))

def unpack(data):
    ''' Regroups the list returned by create() by variable, making it suitable for use in the logic functions.
    ex. [(T, T, F, F), (T, F, T, F)] for two variables '''
    return [[elem[i] for elem in lst] for i, lst in enumerate(itertools.tee(data, len(data[0])))]

def print_result(data, result):
    ''' Prints the combinations returned by create() and the results returned by the logic functions in a nice format. '''
    n = len(data[0])
    headers = 'CBA'[:n]
    print (headers + "|RESULT")
    print ('-' * len(headers) + '+------')
    for row, result_cell in zip(data, result):
        if type(result_cell) is tuple:
            print (''.join({True: '1', False:'0'}[cell] for cell in row) + '|' + '  ' + {True: '1', False:'0'}[result_cell[0]]+''+{True: '1', False:'0'}[result_cell[1]])
        else:
            print (''.join({True: '1', False:'0'}[cell] for cell in row) + '|' + '  ' + {True: '1', False:'0'}[result_cell])



def getSRData(data, result):
    Shift_reg8 = ''
    Shift_reg8B = ''
    tup = 0
    for row, result_cell in zip(data, result):
        if type(result_cell) is tuple:
            Shift_reg8 = Shift_reg8 + ({True: '1', False:'0'}[result_cell[0]])
            Shift_reg8B = Shift_reg8B + ({True: '1', False:'0'}[result_cell[1]])
            tup =1
        else:
            Shift_reg8 = Shift_reg8 + ({True: '1', False:'0'}[result_cell])
            tup = 0
    if tup == 1 :
        return int(Shift_reg8,2) + (int(Shift_reg8B,2) << 7)
    else:
        return int(Shift_reg8,2)
   


if __name__ == '__main__':
   
    
    data = create(num=3)
    C, B, A = unpack(data)
    # result = IMPLIES(A, OR(B, C))
    # result = L.ADD(A,B,C)
    # print_result(data,result)

    andAB = AND(A,B)
    sub = SUB(A,B,C)
    clb1 = clb(andAB, sub, 0)  
    print(clb1.info())
    print(clb1.bit())

    result = OR(A,B)
    # print_result(data,result)
    # result = OR(A,B)
    # SR1 = getSRData(data,result)
    # print('bin: ' + str(bin(SR1)) + ' hex: '+ str(hex(SR1)) + ' dec: ' + str((SR1)))


    # lut1 = lut(make(AND(A,B)),make(OR(A,B)))
    # print(lut1)