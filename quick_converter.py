import csv
with open("seeds_dataset.txt", 'r') as src_file:
    with open("seeds.csv", 'w',newline ='') as dst_file:
        writer = csv.writer(dst_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in src_file:
            line =  line.split()
            writer.writerow(line)
        dst_file.close()
    src_file.close()