#! /usr/bin/python3.6
import csv
import re
import sys

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    print("Please provide a file name")
    raise SystemExit

output_file = '.'.join(input_file.split('.')[:-1]) + "-converted-test.csv"

def fix_null_callee(callee_class, call):
    # example callee_class: null.CallerPsuedoId: 1987196923
    # example call: public abstract java.util.Optional java.util.stream.Stream.findFirst()
    first_part = callee_class.split('.')[0]
    if first_part == 'null':
        pattern = '([a-zA-Z_$][a-zA-Z\d_$]*\.)+'
        call = call.split('(')[-2]
        call = call.split(' ')[-1]
        call_stripped = re.search(pattern, call)
        call_stripped = call_stripped.group(0).split('.')[:-1]
        fixed = ".".join(call_stripped)
        return fixed
    else:
        return callee_class
    
with open(input_file, 'r') as f:
    reader = csv.DictReader(f, delimiter= ';', 
                            fieldnames=['Timestamp', 'Thread', 'Type', 'Caller', 
                                        'Callee', 'Message'])
    
    with open(output_file, 'w', newline='') as out:
        writer = csv.writer(out, delimiter=';')
        writer.writerow(['Start Time', 'End Time', 'Thread', 'Caller', 'Callee', 'Message'])
        stacks = {}
        
        for row in reader:
            if row['Type'] == 'Entry':
                if row['Thread'] in stacks:
                    stacks[row['Thread']].append(row)
                else:
                    stacks[row['Thread']] = [row]
            elif row['Type'] == 'Exit':
                callee = fix_null_callee(row['Callee'], row['Message'])
                entry = stacks[row['Thread']].pop()
                writer.writerow([entry['Timestamp'], row['Timestamp'], row['Thread'], row['Caller'], 
                                 callee, row['Message']])
            else:
                print(row)
        
        for thread_name, thread in stacks.items():
            if len(thread) > 0:
                print('Incomplete log for thread {}, flushing'.format(thread_name))
                while len(thread) > 0:
                    row = thread.pop()
                    print(row)
                    writer.writerow([row['Timestamp'], '2999-12-31T00:00:00,000', row['Thread'], row['Caller'], row['Callee'], row['Message']])
                