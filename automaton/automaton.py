from dbus import ValidationException


class Automaton():
    
    def __init__(self, config_file):
        self.config_file = config_file
        file = open(self.config_file)
        d = {}
        current_set = None
        for line in file.readlines():
            line = line.strip().rstrip()
            if line.startswith("#") == False and len(line) > 0:
                if line.lower() != "End".lower():
                    if ':' in line and len(line.split()) > 1 and ',' not in line:
                        #print(line)
                        current_set = line.split(":")[0].rstrip()
                        if current_set == 'Transitions':
                            d[current_set] = {}
                        else:
                            d[current_set] = []
                    else:
                        line = tuple([x.strip().rstrip() for x in line.split(",")])
                        #print(line)
                        if current_set == 'Transitions':
                            #print(line)
                            if line[0] in d[current_set]:
                                if line[1] in d[current_set][line[0]]:
                                    if line[2] not in d[current_set][line[0]][line[1]]:
                                        d[current_set][line[0]][line[1]].append(line[2])
                                else:
                                    d[current_set][line[0]][line[1]] = [line[2], ]
                            else:
                                d[current_set][line[0]] = {line[1] : [line[2], ]}
                        else:
                            d[current_set].append(line)
        d['fstates'] = []
        d['sstates'] = []
        for state in d['States']:
            for s in state[1:]:
                if s == 'F':
                    d["fstates"].append(state[0])
                elif s == 'S':
                    d["sstates"].append(state[0])
        d['Sigma'] = [x[0] for x in d['Sigma']]
        d['States'] = [x[0] for x in d['States']]
        file.close()
        self.data = d
        if self.validate() == False:
            print("invalid")
            exit()
        #print("Hi, I'm an automaton!")

    def validate(self):
        d = self.data
        if len(d['sstates']) > 1:
            #raise ValidationException("Only one starting state allowed !")
            return False
        for t in d['Transitions'].keys():
            if t not in d['States']:
                #raise ValidationException("Invalid transition - > first state")
                return False
            for w in d['Transitions'][t]:
                if w not in d['Sigma']:
                    #raise ValidationException("Invalid transition - > word")
                    return False
                for t2 in d['Transitions'][t][w]:
                    if t2 not in d['States']:
                        #print(t, w, t2)
                        #raise ValidationException("Invalid transition - > second state")
                        return False

        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass

    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        pass

#nfa = Automaton('input.txt')
#print(nfa.data)

