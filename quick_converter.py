import csv
with open("covtype.data", 'r') as src_file:
    with open("covtype.csv", 'w',newline ='') as dst_file:
        writer = csv.writer(dst_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in src_file:
            line =  line.split()
            writer.writerow(line)
        dst_file.close()
    src_file.close()