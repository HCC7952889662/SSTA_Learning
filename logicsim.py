#__________________________________________________#
#_____________________logic simulation_____________#
#__________________________________________________#
from gate import GAND
from gate import GOR
from gate import GXOR
from gate import GNOT
def logic_sim (nodelist_order):
    f1 = open("input.txt", "r")
    content = f1.readlines()
    node_num = list()
    node_val = list()
    for i in range(len(content)):
        node_num.append(int(content[i].split(',')[0]))
        node_val.append(content[i].split(',')[1].split('\n')[0])
        # print(node_num[i],node_val[i])
    node_dict = dict(zip(node_num, node_val))
    for i in nodelist_order:
        # print(i.gtype)
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