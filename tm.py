import sys

from tkinter import END, IntVar


class TM:
    def __init__(self, response, continue_button):
        self.response = response
        self.continue_button = continue_button
        self.var = IntVar()

    def mprint(self, s):
        self.response.insert(END, s + "\n")

    def load_turing_machine(self, file_name):
        if self.check_file_exists(file_name):
            return True
        else:
            return False

    def execute(self, description, entry, lt, rt, s):
        arq = open('machines/' + description + '.tm', 'r')
        lines = arq.readlines()
        del (lines[0])  # delete the Comment
        tm = {}
        for l in lines:
            x = l.split()
            tm[(x[0], x[1])] = (x[2], x[3], x[4])
        m = {'L': -1, 'S': 0, 'R': 1}
        inftyL = int(lt) * "0"
        inftyR = int(rt) * "0"
        h = len(inftyL) - 1
        inp = entry
        tape = inftyL + inp + inftyR
        q = lines[0].split()[0]  # supposed to be the initial state
        headdisplay = h * ' ' + '^' + q + ((len(inftyR) + len(inp)) * ' ')
        self.mprint(tape)
        self.mprint(headdisplay)
        steps = 0
        symbwritten = 0
        sBs = int(s)
        while (q, tape[h]) in tm.keys():
            steps += 1
            ntape = tape[:h] + (tm[(q, tape[h])])[1] + tape[h + 1:]
            nq = tm[(q, tape[h])][0]
            nh = h + m[tm[(q, tape[h])][2]]
            q, h, tape = nq, nh, ntape
            if sBs != 0:
                if sBs == 1:
                    self.continue_button.wait_variable(self.var)
                self.mprint(tape)
                headdisplay = h * ' ' + '^' + q + (len(tape) - (h + 1)) * ' '
                self.mprint(headdisplay)

        if sBs == 1:
            self.continue_button.configure(state="disabled")
        if not sBs:
            self.mprint(tape)
            headdisplay = h * ' ' + '^' + q + (len(tape) - (h + 1)) * ' '
            self.mprint(headdisplay)

    @staticmethod
    def check_file_exists(file_name):
        try:
            open('machines/' + file_name + '.tm', 'r')
            return True
        except:
            return False
