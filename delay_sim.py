#__________________________________________________#
#_____________________logic simulation_____________#
#__________________________________________________#
from gate import GAND
from gate import GOR
from gate import GXOR
from gate import GNOT
from PDF import PDF, PDF_generator, read_sstalib

def delay_sim (nodelist_order):
    
    sstalib = read_sstalib("tech10nm.sstalib")
    for i in nodelist_order:
        if (i.gtype == 'IPT'):
            if i.num in node_num:
                i.value = node_dict[i.num]
                # print(node_dict[i.num], i.value)
        elif (i.gtype == 'BRCH'):
            i.value = i.unodes[0].value
            # print("test",i.num,i.value)
        elif (i.gtype == 'XOR'):
            for j in range(0, i.fin):
                if j == 0:
                    temp_value = i.unodes[j].value
                else:
                    temp_value = GXOR(temp_value, i.unodes[j].value)
            i.value = temp_value
        elif (i.gtype == 'OR'):
            for j in range(0, i.fin):
                if j == 0:
                    temp_value = i.unodes[j].value
                else:
                    temp_value = GOR(temp_value, i.unodes[j].value)
            i.value = temp_value
        elif (i.gtype == 'NOR'):
            for j in range(0, i.fin):
                if j == 0:
                    temp_value = i.unodes[j].value
                else:
                    temp_value = GOR(temp_value, i.unodes[j].value)
            i.value = GNOT(temp_value)
        elif (i.gtype == 'NOT'):
            i.value = GNOT(i.unodes[0].value)
        elif (i.gtype == 'NAND'):
            for j in range(0, i.fin):
                if j == 0:
                    temp_value = i.unodes[j].value
                else:
                    temp_value = GAND(temp_value, i.unodes[j].value)
            i.value = GNOT(temp_value)
        elif (i.gtype == 'AND'):
            for j in range(0, i.fin):
                if j == 0:
                    temp_value = i.unodes[j].value
                else:
                    temp_value = GAND(temp_value, i.unodes[j].value)
            i.value = temp_value   