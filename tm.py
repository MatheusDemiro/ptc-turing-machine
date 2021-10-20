import sys


class TM:
    def __init__(self, response, description="amt", entry="00", lt="10", rt="10", s="2"):
        self.description = description
        self.entry = entry
        self.lt = lt
        self.rt = rt
        self.s = s
        self.response = response

    def mprint(self, s):
        self.response['text'] += s + '\n'

    def load_turing_machine(self, file_name):
        if self.check_file_exists(file_name):
            self.description = file_name
            return True
        else:
            return False

    def main(self):
        arq = open(self.description + '.tm', 'r')
        lines = arq.readlines()
        del (lines[0])  # delete the Comment
        tm = {}
        for l in lines:
            x = l.split()
            tm[(x[0], x[1])] = (x[2], x[3], x[4])
        m = {'L': -1, 'S': 0, 'R': 1}
        inftyL = int(self.lt) * "0"
        inftyR = int(self.rt) * "0"
        h = len(inftyL) - 1
        inp = self.entry
        tape = inftyL + inp + inftyR
        q = lines[0].split()[0]  # supposed to be the initial state
        headdisplay = h * ' ' + '^' + q + ((len(inftyR) + len(inp)) * ' ')
        self.mprint(tape)
        self.mprint(headdisplay)
        steps = 0
        symbwritten = 0
        sBs = int(self.s)
        while (q, tape[h]) in tm.keys():
            steps += 1
            ntape = tape[:h] + (tm[(q, tape[h])])[1] + tape[h + 1:]
            nq = tm[(q, tape[h])][0]
            nh = h + m[tm[(q, tape[h])][2]]
            q, h, tape = nq, nh, ntape
            if sBs != 0:
                if sBs == 1:
                    input()
                self.mprint(tape)
                headdisplay = h * ' ' + '^' + q + (len(tape) - (h + 1)) * ' '
                self.mprint(headdisplay)

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
