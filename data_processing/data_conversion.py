num2move_unit = [['pillage',[]],['build_city',[]],
                 ['move',['north']],['move',['north-east']],
                 ['move',['east']],['move',['south-east']],
                 ['move',['south']],['move',['south-west']],
                 ['move',['west']],['move',['north-west']]]

num2move_citytile = [['research',[]],['build_cart',[]],['build_worker',[]],
                 ['move',['north']],['move',['north-east']],
                 ['move',['east']],['move',['south-east']],
                 ['move',['south']],['move',['south-west']],
                 ['move',['west']],['move',['north-west']]]

class Function():
    def __init__(self,info):
        self.function = info[0]
        self.args = info[1]
    def run_function(self,obj):
        obj_str = obj
        eval_string = 'obj_str'+'.'+self.function+'('
        args = []
        counter = 0
        for arg in self.args:
            args.append(arg)
            args[counter] = arg
            eval_string += 'self.args['+str(counter)+']'
            counter += 1
            
            if counter != len(self.args):
                eval_string += ','
        eval_string += ')'
        print(eval_string)
        eval(eval_string)
        
def Num2Move(num):
    len_unit = len(num2move_unit)
    
    if num < len_unit:
        action = num2move_unit[num]
    else:
        num -= len_unit
        action = num2move_citytile[num]
    return action
    
        