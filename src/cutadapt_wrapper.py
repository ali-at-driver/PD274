import sys
from cStringIO import StringIO
from cutadapt.scripts import cutadapt
from config import Adapters, Reports
import re

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        values = re.sub(r'\s{4,}', ' ', self._stringio.getvalue())
        values = re.split('(?:===).*', values)
        new_vals = [re.split(r'\n\n|\n|:', value) for value in values]#self._stringio.getvalue()))# values.splitlines())

        self.extend(new_vals)
        sys.stdout = self._stdout


def grep_report(report):#, trim_fields=None, dimer_fields=None):
    print(report)
    print(len(report))
    fields = [Reports.processed_field, Reports.r1_trim_field, Reports.r2_trim_field]
    print(report[1].index(fields[0]))
    #dimer_indices0 = [i for i, x in enumerate(report[2]) if x == Reports.dimer_field]
    #print(dimer_indices)
    #dimer_indices1 = [i for i, x in enumerate(report[3]) if x == Reports.dimer_field]

    dimers0 = [ report[2][field] for field in range(report[2].index(Reports.dimer_field), len(report[2]))]
    dimers1 = [ report[3][field] for field in range(report[3].index(Reports.dimer_field), len(report[3]))]
    with open("test.tsv", "w") as fh:
        for field in fields:
            print(field)
            fh.write(report[1][report[1].index(field)].strip() + "\t" + report[1][report[1].index(field) + 1].strip() + "\n")
        for field in dimers0: 
            fh.write(field + "\n")
        for field in dimers1:
            fh.write(field + "\n")
"""
  Total read pairs processed:              1,000
  Read 1 with adapter:                      56 (5.6%)
  Read 2 with adapter:                      56 (5.6%)
"""
def grep_fields(idx, report):
    for i in xrange(idx, len(report)):
        final_report += report[i]
        final_report += "\n"
    return final_report


def write_to_tsv():
    with open("test.tsv", "w") as fh:
        for e in ordered:
            fh.write("\t\t".join(map(str, e[:2])) + "\n")

def datapath(path):
    return os.path.join(os.path.dirname(__file__), path)

def run(inf1, inf2, out1, out2, params=None, lab_adapt_override=None, stdout_override=True):
    #if type(params) is str:
    #   params = params.split()

    params = ['-a', 'AGATCGGAAGAGC', '-A', 'AGATCGGAAGAGC']
    params += ['-o', out1, '-p', out2]
    params += [inf1, inf2]
    if stdout_override:
        with Capturing() as output:
            cutadapt.main(params)
            return output
    else:
        return cutadapt.main(params)


if __name__=='__main__':
    output = run('../data/E144-T1-D1_S15_L004_R1_001.fastq.gz', '../data/E144-T1-D1_S15_L004_R1_001.fastq.gz','out1.fastq.gz', 'out1.fastq.gz', stdout_override=True)

    grep_report(output)
