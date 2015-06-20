import csv
import gausscoefficients

def custom(gaussfile):
    with open(gaussfile, 'rb') as csvfile:
        gaussreader = csv.reader(csvfile, delimiter=' ',skipinitialspace=True)
        gauss_iter=iter(gaussreader)
        
        gausscoefficients.gcoeff[("Custom","a")]=.572

        for row in gauss_iter:
            if (row[1]=='0'):
                gausscoefficients.gcoeff[("Custom","g",int(row[0]),int(row[1]))]=float(row[2])
                # print 'g',row[0],row[1],row[2]
            else:
                gausscoefficients.gcoeff[("Custom","g",int(row[0]),int(row[1]))]=float(row[2])
                # print 'g',row[0],row[1],row[2]
                row = next(gauss_iter)
                gausscoefficients.gcoeff[("Custom","h",int(row[0]),int(row[1]))]=float(row[2])
                # print 'h',row[0],row[1],row[2]