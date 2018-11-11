import sys
import os
import gzip
from multiprocessing import Pool
from functools import partial
from conf import *
from trimmer import *
from composer import *

def fastq_reader(project_dir):
    fastq_list, gz, pairs_list = [], [], {}
    for filename in os.listdir(project_dir):
        if filename == R1_barcodes:
            pass
        elif filename == R2_barcodes:
            pass
        else:
            try:
                fastq_test, pairs_list = file_type.is_fq(project_dir + '/' + filename, pairs_list)
                gz.append(0)
            except UnicodeDecodeError:
                fastq_test, pairs_list = file_type.is_gz(project_dir + '/' + filename, pairs_list)
                gz.append(1)
            if fastq_test is None:
                raise TypeError
            fastq_list.append(project_dir + '/' + filename)
    return fastq_list, gz, pairs_list

def barcode_reader(project_dir, barcodes):
    barcode_list = []
    try:
        with open(project_dir + '/' + barcodes) as f:
            for line in f:
                barcode_list.append(line.rstrip())
            return barcode_list
    except FileNotFoundError:
        sys.exit('''
based on your configuration file your project
directory must contain a newline-separated list
of barcodes named ''' + barcodes
        )

class file_type:
    def is_fq(filename, pairs_list):
        with open(filename) as f:
            for i, line in enumerate(f):
                if i == 1 and line[0] != '@':
                    return
                else:
                    pairs_list = file_type.is_paired(filename, line, pairs_list)
                if i == 3 and line[0] != '+':
                    return
                if i == 5 and line[0] != '@':
                    return
                else:
                    return True, pairs_list

    def is_gz(filename, pairs_list):
        with gzip.open(filename, 'rt') as f:
            for i, line in enumerate(f):
                if i == 1 and line[0] != '@':
                    return
                else:
                    pairs_list = file_type.is_paired(filename, line, pairs_list)
                if i == 3 and line[0] != '+':
                    return
                if i == 5 and line[0] != '@':
                    return
                else:
                    sys.exit('''
sorry, gzipped functionality is not currently supported
                ''')
#                    return True, pairs_list

    def is_paired(filename, line, pairs_list):
        for i, x in enumerate(line):
            if x == ' ':
                space_pos = i
        header = line[:space_pos]
        if header in pairs_list:
            pairs_list[header].append(filename)
        else:
            pairs_list[header] = [filename]
        return pairs_list

def input_sort(paired, pairs_list):
    input1_list, input2_list, ignore = [], [], False
    for values in pairs_list.values():
        if paired == True:
            if len(values) == 2:
                for filename in values:
                    with open(filename) as f:
                        header = f.readline()
                        for i, x in enumerate(header):
                            if x == ' ':
                                space_pos = i
                        end = header[space_pos+1]
                        if int(end) == 1:
                            input1_list.append(os.path.basename(filename))
                        if int(end) == 2:
                            input2_list.append(os.path.basename(filename))
            else:
                sys.exit('''
paired forward and end reads don't match expected number
                    ''')
        if paired == False:
            if len(values) == 1:
                for filename in values:
                    input1_list.append(os.path.basename(filename))
            elif ignore == True:
                for filename in values:
                    input1_list.append(os.path.basename(filename))
            else:
                print('''
unexpected paired libraries found
                    ''')
                answer = input('continue treating all files as single-end libraries?\n')
                ignore = True if answer in ('Y', 'y', 'Yes', 'yes', 'YES') else sys.exit()
                for filename in values:
                    input1_list.append(os.path.basename(filename))
    return input1_list, input2_list

if __name__ == '__main__':
    if os.path.exists(project_dir) == True:
        project_dir = os.path.abspath(project_dir)
    else:
        sys.exit('''
project directory not found
                ''')
    pool = Pool(threads)        
    fastq_list, gz, pairs_list = fastq_reader(project_dir)
    input1_list, input2_list = input_sort(paired, pairs_list)
    if R1_barcodes:
        R1_barcodes = barcode_reader(project_dir, R1_barcodes)
    if R2_barcodes:
        R2_barcodes = barcode_reader(project_dir, R2_barcodes)
    if front_trim > 0:
        trim_part = partial(trimmer, front_trim, back_trim, project_dir)
        pool.map(trim_part, fastq_list)
        pool.close()
        for i, filename in enumerate(input1_list):
            input1_list[i] = project_dir + '/trimmed_' + os.path.basename(filename)
        for i, filename in enumerate(input2_list):
            input2_list[i] = project_dir + '/trimmed_' + os.path.basename(filename)        
    print(input1_list)
    print(input2_list)
        


#    if R1_barcodes:
#        comp_part = partial(compser.trimmer, front_trim, back_trim, project_dir)
#                pool.map(comp_part, fastq_list)
#                pool.close()

#        for x, input1 in enumerate(input1_list):
#            input1 = input1
#            input2 = input2_list[x]
#            pipe_writer_forward1(input1, input2, cutoff, 200000, R1_barcodes, project_dir)
