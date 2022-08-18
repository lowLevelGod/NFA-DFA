
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from dbus import ValidationException

from automaton.automaton import Automaton


class DFA(Automaton):

    def __init__(self, config_file):
        super().__init__(config_file)
        #print("More precisely, a DFA.")

    def validate(self):
        return super().validate()

    def accepts_input(self, input_str):
        current_state = self.data['sstates'][0] if isinstance(self.data['sstates'], list) else self.data['sstates']
        for c in input_str:
            if c not in self.data['Sigma']:
                #raise ValidationException(f"{c} not in Sigma !")
                return False
            else:
                #print(current_state)
                if (current_state not in self.data['Transitions']) or (c not in self.data['Transitions'][current_state]):
                    #raise ValidationException(f"No valid transition from {current_state} with {c} !")
                    return False
                current_state = self.data['Transitions'][current_state][c][0] if isinstance(self.data['Transitions'][current_state][c], list) else self.data['Transitions'][current_state][c]
        if current_state in self.data['fstates']:
            #return "Input Valid !"
            return True
        #return "Input did not reach final state !"
        #return "I don't know what inputs to accept... yet!"
        return False

    def read_input(self, input_str):
        pass


if __name__ == "__main__":
    '''
    num_args = len(sys.argv)
    if num_args > 1:
        print(f"I see you provided {num_args-1} argument{'s' if num_args > 2 else ''} from the console.")
        print("Here's a list with all the system arguments:")
        for i, arg in enumerate(sys.argv):
            print(f"Argument {i}: {arg:>32}")
        print()
    '''
    dfa = DFA(sys.argv[1])    
    #print(dfa.data['States'])
    res = dfa.accepts_input(sys.argv[2].split())
    if res:
        print("accept")
    else:
        print("reject")
