import sys
from cStringIO import StringIO
from cutadapt.scripts import cutadapt
from config import Adapters, Reports
import re
import argparse
#from optparse import OptionParser, OptionGroup, SUPPRESS_HELP

# POTENTIALLY MOVE THESE TO CONFIG OR JSON LATER ON 
class Config:
    TRIM_NAME_IDX = 26
    ADAPTER_FWD = 'AGATCGGAAGAGCACACGTC'
    ADAPTER_REV = 'AGATCGGAAGAGCGTCGTGT'
    SEQ_FIELD = 1
    DIMER_FWD_FIELD = 2
    DIMER_REV_FIELD = 3

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        values = re.sub(r'\s{4,}', ' ', self._stringio.getvalue())
        values = re.split('(?:===).*', values)
        new_vals = [re.split(r'\n\n|\n|:', value) for value in values]

        self.extend(new_vals)
        sys.stdout = self._stdout


def grep_report(report, outfile):
    fields = [Reports.processed_field, Reports.r1_trim_field, Reports.r2_trim_field]
    dimers0 = [ report[Config.DIMER_FWD_FIELD][field] for field in range(report[Config.DIMER_FWD_FIELD].index(Reports.dimer_field), len(report[Config.DIMER_FWD_FIELD]))]
    dimers1 = [ report[Config.DIMER_REV_FIELD][field] for field in range(report[Config.DIMER_REV_FIELD].index(Reports.dimer_field), len(report[Config.DIMER_REV_FIELD]))]
    
    # FIXME: make dry-er and remove hardcoded values 
    with open(outfile, "w") as fh:
        for field in fields:
            print(field)
            fh.write(report[Config.SEQ_FIELD][report[Config.SEQ_FIELD].index(field)].strip() + "\t" + report[1][report[Config.SEQ_FIELD].index(field) + 1].strip() + "\n")
        for field in dimers0: 
            fh.write(field + "\n")
        for field in dimers1:
            fh.write(field + "\n")

def datapath(path):
    return os.path.join(os.path.dirname(__file__), path)

def run(inf1, inf2, out1=None, out2=None, fwd=None, rev=None, stdout_override=True):
    # FIXME: ADD OVERRIDES 
    if not out1: 
        # if the file is a .fastq.gz, normal OS extension tools will not work
        # TODO: fix for different types of file inputs 
        out1 = inf1[:Config.TRIM_NAME_IDX] + '_trimmed' + inf1[Config.TRIM_NAME_IDX:]
    if not out2:
        out2 = inf2[:Config.TRIM_NAME_IDX] + '_trimmed' + inf2[Config.TRIM_NAME_IDX:]
            
    params = ['-a', Config.ADAPTER_FWD, '-A', Config.ADAPTER_REV,
              '-o', out1, '-p', out2,
              inf1, inf2 ]

    if stdout_override:
        with Capturing() as output:
            cutadapt.main(params)
            return output
    else:
        return cutadapt.main(params)

def main():
    parser = argparse.ArgumentParser(description='Process read1 and read2 fastq inputs using cutadapt, write report to TSV')
    parser.add_argument('read1', metavar='read1', nargs='?', help='a fastq(.gz) R1')
    parser.add_argument('read2', metavar='read2', nargs='?', help='a fastq(.gz) R2')  # argparse.FileType('r')

    parser.add_argument('report', metavar='report', type=str, nargs='?', help='the output of cutadapt redirected to a .tsv')

    parser.add_argument('--o','--outfile', nargs='?', help='the fastq(.gz) output file of R1')
    parser.add_argument('--p','--outfile2', nargs='?', help='the fastq(.gz) output file of R2')
    
    parser.add_argument('--a', '--adapter', metavar='fwd-adapter', type=str, nargs='?', help='the forward adapter')
    parser.add_argument('--A', '--adapter2', metavar='rev-adapter', type=str, nargs='?', help='the reverse adapter')

    args = parser.parse_args()

    output = run(args.read1, args.read2, out1=args.o, out2=args.p, fwd=args.a, rev=args.A)
    grep_report(output, args.report)
    

if __name__=='__main__':
    # keep the same file name _filtered 
    main()
    
