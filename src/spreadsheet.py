import csv

f=open("asdf.csv",'wt')

try:
    w = csv.writer(f)
    w.writerow({'Title1','Title2'})
    for i in range(10):
        w.writerow((i+1,chr(ord('a')+i), '08/%02d/07' % (i+1)))
finally:
    f.close()
print(open("asdf.csv",'rt').read())