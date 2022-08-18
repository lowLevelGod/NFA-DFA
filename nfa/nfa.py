import queue
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from dbus import ValidationException

from automaton.automaton import Automaton

class NFA(Automaton):
    def __init__(self, config_file):
        super().__init__(config_file)
    
    def validate(self):
        return super().validate()
    
    def nfatodfa(self):
        nfa = self.data
        dfa = {}
        dfa['Transitions'] = {}
        dfa['States'] = []
        q = queue.SimpleQueue()
        q.put(tuple([nfa['sstates'][0],]))
        dfa['States'].append(tuple([nfa['sstates'][0],]))
        dfa['States'].append(tuple([None,]))
        current_state = None
        count = 0
        while q.empty() == False:
            current_state = q.get()
            dfa['Transitions'][current_state] = {}
            for word in nfa['Sigma']:
                transition_tuple = []
                for state in current_state:
                    if state in nfa['Transitions'] and word in nfa['Transitions'][state]:
                        transition_tuple += nfa['Transitions'][state][word]
                transition_tuple = tuple(set(transition_tuple))
                if len(transition_tuple) == 0:
                    transition_tuple = tuple([None,])
                else:
                    if transition_tuple not in dfa['Transitions']:
                        dfa['States'].append(transition_tuple)
                        q.put(transition_tuple)
                dfa['Transitions'][current_state][word] = transition_tuple
        dfa['Transitions'][(None, )] = dict((word, (None, )) for word in nfa['Sigma'])
        dfa['fstates'] = []
        for f in nfa['fstates']:
            for state in dfa['States']:
                if f in state:
                    dfa['fstates'].append(state)
        dfa['sstates'] = tuple(nfa['sstates'])
        dfa['Sigma'] = nfa['Sigma']
        self.data = dfa

    def accepts_input(self, input_str):
        self.nfatodfa()
        #self.printdfa()
        current_state = self.data['sstates'][0] if isinstance(self.data['sstates'], list) else self.data['sstates']
        for c in input_str:
            if c not in self.data['Sigma']:
                #raise ValidationException(f"{c} not in Sigma !")
                return False
            else:
                #print(current_state)
                if c not in self.data['Transitions'][current_state]:
                    #raise ValidationException(f"No valid transition from {current_state} with {c} !")
                    return False
                current_state = self.data['Transitions'][current_state][c][0] if isinstance(self.data['Transitions'][current_state][c], list) else self.data['Transitions'][current_state][c]
        if current_state in self.data['fstates']:
            #return "Input Valid !"
            return True
        #return "Input did not reach final state !"
        #return "I don't know what inputs to accept... yet!"
        return False

    def bkt(self, inp):
        nfa = self.data
        q = queue.SimpleQueue()
        q.put(nfa['sstates'][0])
        for c in inp:
            newq = queue.SimpleQueue()
            while q.empty() == False:
                current = q.get()
                if c in nfa['Transitions'][current]:
                    for state in nfa['Transitions'][current][c]:
                        newq.put(state)
            q = newq
        while q.empty() == False:
            if q.get() in nfa['fstates']:
                return True
        return False

    def printdfa(self):
        dfa = self.data
        for k1 in dfa['Transitions'].keys():
            for k2 in dfa['Transitions'][k1].keys():
                k3 = dfa['Transitions'][k1][k2]
                if None not in k1 and None not in k3:
                    print("\t" + "".join([x if x is not None else "None" for x in k1]) if k1 is not None else "None", k2, "".join([x if x is not None else "None" for x in k3]) if k3 is not None else "None", sep=", ")
        print("States :")          
        for state in set(dfa['States']):
            if None not in state:
                print("\t" + "".join([x if x is not None else "None" for x in state] if state is not None else "None") + (", S" if state == dfa['sstates'] else "") + (", F" if state in dfa['fstates'] else ""))
            

nfa = NFA(sys.argv[1])
#print(nfa.data)
sys.argv[len(sys.argv) - 1] = sys.argv[len(sys.argv) - 1].split()
res = False   
if (len(sys.argv) < 5) or (sys.argv[2] == 'convert'):
    res = nfa.accepts_input(sys.argv[len(sys.argv) - 1])
elif sys.argv[2] == 'bkt':
    res = nfa.bkt(sys.argv[len(sys.argv) - 1])
if res:
    print("accept")
else:
    print("reject")
    
    





            
