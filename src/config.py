#PUT ADAPTERS HERE FOR OTHER MODULES 

class Reports:
    processed_field = 'Total read pairs processed'
    r1_trim_field = '  Read 1 with adapter'
    r2_trim_field = '  Read 2 with adapter'
    #trim_field = 'Reads with adapters:'
    dimer_field = 'Overview of removed sequences'
    file_dir = '/scratch/tmp/hiseq_4000_run_2/160923_K00356_0013_AHCNKWBBXX'
    # FIXME
    barcode_len = 20
    
class Adapters:
    lab0 = "AATGATACGGCGACCACCGAGATCTACACXXXXXXXXACACTCTTTCCCTACACGACGCTCTTCCGATCT"
    rev0 = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTGXXXXXXXXTGTAGATCTCGGTGGTCGCCGTATCATT"

    lab1 = "GATCGGAAGAGCACACGTCTGAACTCCAGTCACXXXXXXXXATCTCGTATGCCGTCTTCTGCTTG"
    rev1 = "AATGATACGGCGACCACCGAGATCTACACXXXXXXXXACACTCTTTCCCTACACGACGCTCTTCCGATCT"

    insert_re = '([ATCG]{5,8})'
    replace = "XXXXXXXX"

class Constants:
    test_file = "./data/"
