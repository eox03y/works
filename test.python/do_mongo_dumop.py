def conv_csvheader_to(inf, outf):
    """
    report.devtype.csv . ..... mongodb collection. ..... ....
    .... ... ...
    ./mongoexport -f _id,phone,tablet,null,Nil --dbpath /iosp/search.data/logAnalysis -d qclog2013 -c devtype  -o devtype.dump.json

    """
    fp = open(inf, 'rb')
    line = fp.readline()
    fp.close()

    outp = open(outf, 'wb')
    flds = line.split(',')
    flds = set(flds)
    flds = list(flds)
    flds.sort()	
    outp.write('_id\n')
    for fld in flds:
        if fld=='date': continue
        outp.write(fld+'\n')
    outp.close()

def mongo_dump():
    colls = ['devtype', 'dm', 'dos', 'im', 'info', 'osshop', 'shop']
    for coll in colls:
        inf = "report.%s.csv" % (coll)
        outf = "report.%s.flds" % (coll)
        conv_csvheader_to(inf, outf)

    import os
    for coll in colls:
        cmd = """/home/query/handol/mongodb-linux-x86_64-2.2.3/bin/mongoexport \
                 --fieldFile report.%s.flds --dbpath /iosp/search.data/logAnalysis \
                 -d qclog2013 -c %s  -o dump.%s.json """ % (coll, coll, coll)
        print cmd
        os.popen(cmd)


        cmd = """/home/query/handol/mongodb-linux-x86_64-2.2.3/bin/mongoexport \
                 --fieldFile report.%s.flds --dbpath /iosp/search.data/logAnalysis \
                 -d qclog2013 -c %s --csv -o dump.%s.csv """ % (coll, coll, coll)
        print cmd
        os.popen(cmd)


mongo_dump()
