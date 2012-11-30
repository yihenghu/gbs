"""" Very important: Without the "index_col=0", to get the row names to act as the index you need to remove the word "locus" (or whatever the column 1 name is) and move it to the second row all on its own. So then the real data starts on row 3. By including the index at import you can take a regular spreadsheet"""
import numpy as np
import pandas as pd
import scipy as sp
#data = pandas.read_csv("play.csv",index_col=0)
# file path if needed: /Users/paulwolf/Documents/Manuscripts_and_Projects/Aspen_GBS/UNEAK_8_Aug _12/aspen_hapmap/
#output_file = open("locus_dist_plot", 'w')
#df=pandas.DataFrame(data)
#not_N = df.values != 'N'
#col_sums = scipy.sum(not_N, axis=0)
#row_sums = scipy.sum(not_N, axis=1)



#for row in df.values:
#    inds_per_locus = 0
#    for ind in locus:
#        if ind != 'N':
#            inds_per_locus += 1
#    new_row = str(row) + "\n"

 #   output_file.write(new_row)
#output_file.close()

#You can see a particular column by indexing its name:
#print df.p8
#print""
#You can see rows by indexing the range. Note that you need to use numpy to view the array. Just the index works but it does not show under a print statement.
#print "Four rows of DataFrame:", df['TP2':'TP5']
#row_set=np.array(df['TP2':'TP5'])
#print""
#print "Now converted to np.array:"
#print row_set
#start=data[:6]
#print start
#df = DataFrame(data)
#print data['TP2', 'TP3']
########################################################################

# hmp = pd.read_csv("hmp_play.txt", index_col = 0, header = 1)
# hmc = pd.read_csv("hmc_play", index_col = 0, header = 1)

hmp = pd.read_table('hmp_play.txt', index_col = 0, header = 0)
hmc = pd.read_table('hmc_play02.txt', index_col = 0, header = 0)
#######

# clean:
# load hmp and hmc, then:

hmp_trimmed = hmp.ix[:30, 'FLFL04':'WWA30'] # later, change the '30'

results = []
for i, col in enumerate(hmp_trimmed.columns):
    base_values = hmp_trimmed[col]
    count_values = hmc[hmc.columns[i]]
    results.append(gbs.filter_single_col(base_values, count_values))

df = pd.DataFrame(zip(*results), index = hmp_trimmed.index[:30], columns=hmp_trimmed.columns, dtype = np.str)

#
data = gbs.sort_loci_pdDF(df)


#######
df.insert(0, 'alleles', hmp.ix[:, 'alleles'])
df2 = hmp.ix[:, 'chrom': 'QCcode'] # maybe do that after the ambig_func
df = df.join(df2)

################################# later...
first_allele = []
second_allele = []
for allele in hmp.ix[:, 'alleles']:
    first_allele.append(allele.split('/')[0])
    second_allele.append(allele.split('/')[1])

hmp = hmp.ix[:, 'FLFL04':'WWA30']
hmp.insert(0, 'allele_1', first_allele)
hmp.insert(1, 'allele_2', second_allele)

#######

#!head -n 10 hmc_play
#######
# not_N = hmp.values != 'N'
# print not_N[i]


#not_N = df.values != 'N'

#####################################################
###################### test w/ single columns
a = hmc.ix[:,1].copy()
b = hmp.ix[:,3].copy()[:30]
a[0] = '5|0'
a[1] = '0|7'
b[0] = 'T'
b[1] = 'C'

############# simplified version (w/ just one series/list) working, now extend the whole thing to the whole pie

single = []
for i, base in enumerate(b):
    count_1, count_2 = a[i].split('|')
    if base == 'N':
        value = 'N'
    else:
        if int(count_1) < 4 and int(count_2) < 4:
            value = 'N'
        elif int(count_1) < 4 and int(count_2) >= 4:
            value = base # note: check allele_1 and allele_2 and ambiguity codes!
        elif int(count_1) >= 4 and int(count_2) < 4:
            value = base
        else:
            value = base # maybe here: check for ambiguity and potential alleles
    single.append(value)

########################################################################
########################################################################
# ambiguity codes
# - if ambiguity code doesn't make sense, flag that position (how?)
# - so compare allele_1 & allele_2 with actual value



iupac = pd.DataFrame([['N', 'G', 'A', 'T', 'C'], ['G', 'G',None,None,None], ['A',None ,'A',None,None], ['T',None ,None,'T',None], ['C',None ,None,None,'C'], ['B', 'G', None, 'T', 'C'], ['D', 'G', 'A', 'T',None], ['H',None ,'A', 'T', 'C'], ['K', 'G',None,'T',None], ['M',None ,'A', None,'C'], ['R', 'G', 'A',None,None], ['S', 'G',None,None,'C'],['V', 'G', 'A',None,'C'], ['W',None ,'A', 'T',None], ['Y',None ,None,'T', 'C']], columns = ('amb_code', 'G', 'A', 'T', 'C'), dtype = np.str)


########################################################################
# ambiguity codes
# - if ambiguity code doesn't make sense, flag that position (how?)
# - so compare allele_1 & allele_2 with actual value
labels = ['PT1', 'PT2', 'PT3', 'PT4', 'PT5', 'PT6', 'PT7', 'PT8', 'PT9', 'PT10', 'PT11', 'PT12', 'PT13', 'PT14', 'PT15']
c = pd.Series(['A', 'T', 'C', 'G', 'W', 'B', 'D', 'H', 'K', 'M', 'N', 'R', 'S', 'V', 'Y'], index = labels)
# d = a[:30]

# al_1 = hmp.allele_1[:15]
# al_2 = hmp.allele_2[:15]
e = hmp.alleles[:30].copy() # old hmp with 'x/y' values in .alleles
###
# c = df.FLFL23[:30].copy()
d = hmc.FLFL23[:30].copy()

# target:             5                       10                        15
['A', 'T', 'C', 'A', 'A', 'N', 'N', 'N', 'A', 'G', 'A', 'G', 'T', 'C', 'T',
 'G', 'T', 'G', 'T', 'A',      'C', 'C', 'A', 'T', 'G', 'N', 'N', 'A', 'G', 'N']
# amb --- c     for testing.... (TP26 and TP28: amb_codes are wrong...)
c = pd.Series(
['M', 'W', 'H', 'D', 'R', 'N', 'N', 'N', 'W', 'R', 'H', 'V', 'K', 'M', 'Y',
 'A', 'G', 'G', 'T', 'A',      'C', 'N', 'W', 'Y', 'Y', 'T', 'S', 'W', 'R', 'N'], index = hmp.index[:30])

e.ix[12] = 'G/T'
e.ix[15] = 'C/G'
e.ix[16] = 'G/T'

d = pd.Series(    #            5                                 10
['5|1', '0|7', '1|6', '4|0', '7|0', '0|3', '2|2', '1|3', '4|2', '0|10',
 '4|1', '0|5', '0|7', '0|9', '3|11', '1|4', '0|7', '1|4', '2|6', '7|0',
 '5|0', '0|8', '7|1', '0|4', '1|12', '0|1', '1|3', '10|2', '0|4', '1|3'], index = hmp.index[:30])
#####################################################
# old version, see debug_ambig.py
ambig = []
for i, base in enumerate(c):
    count_1, count_2 = d[i].split('|')
    allele_1, allele_2 = e[i].split('/')
    for j, ambi in enumerate(iupac.ix[5:, 0]): # starting from the 5th row; we don't need 'N's and single nucleotides.
        if base == 'N':
            value = 'N'
        else:
            if base == ambi and count_1 >= 4 and count_2 < 4: # then check with the allele_1 & 2 and, if
                value = allele_1
            elif base == ambi and count_2 >= 4 and count_1 < 4:
                value = allele_2
            elif base == ambi and count_1 >= 4 and count_2 >= 4:
                value = 'what now?'
            else:
                value = base
    ambig.append(value)

for j, ambi in enumerate(iupac.ix[5:, 0]):
    print ambi

########################################################################
# unused columns have to be cut out in order to just process the real stuff
# probably append again after this is finished (??)
# ----> maybe use df.filter to restrict to columns based on a certain (regex ??) pattern



##############################################
## def my_awesome_gbs_function(hmp., hmc, threshold = 4): # threshold 4 per default

# 1) read in both input files (hmc and hmp)

# 2) a dataFrame similar to hmp (input !!!)
df = pd.DataFrame([[0,1,'a'], [3,4,'b']], index = hmp.index[:30], columns=hmp.columns, dtype = np.str)

# 3) probably extract columns allele_1 and allele_2 into seperate list/series ?

# 4) ...the loop...

# 5) insert N's and bases into new df (in the loop or outside?

## --->> probably at the start, specify the potential bases allele_1 & allele_2

