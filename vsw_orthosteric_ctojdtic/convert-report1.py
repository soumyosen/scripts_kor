infile = open('output_report_XP.txt','r')
rl = infile.readlines()
outfile = open('output-report_XP.csv','w')
for i,line in enumerate(rl):
  if i<12:continue
  rll = line.rsplit()
  outfile.write("{},{},{},{},{},{},{}\n".format(rll[0],rll[1],rll[3],rll[6],rll[7],rll[9],rll[10]))
outfile.close()
infile.close()
quit()
