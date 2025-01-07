import csv

header=['Scene Number', 'Position','Left Camera', 'Right Camera', 'Depth Image', 'Depth Data', 'Focal length', 'Base Line']



with open('DataOutput/test.csv','w',newline='') as f:
    writer=csv.writer(f)
    
    writer.writerow(header)
    
with open('DataOutput/test.csv','a') as f:
    f.write('Element')
    f.write(',')
    
with open('DataOutput/test.csv','a') as f:
    f.write('Element\n')
    #f.write("\n")
    
with open('DataOutput/test.csv','a') as f:
    f.write('NewLineElement')
    f.write(',')
    
with open('DataOutput/test.csv','a') as f:
    f.write('Element')
    f.write(',')
    
#with open('DataOutput/test.csv','a') as f:
#    f.write(newline='')    
'''    
with open('DataOutput/test.csv','a',newline='') as f:
    #f.writerow('NL,')
    writer=csv.writer(f)
    element=['Afternewline']
    writer.writerow(element)
'''    
  
'''    
pose_x = 'Element' 
pose_y = 2




with open('DataOutput/test.csv', mode='a') as file_:
    file_.write("{},{}".format(pose_x, pose_y))
    file_.write("\n")  # Next line.
    
    '''