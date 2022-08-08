file1 = open("myfile.txt","r+") 
  
print "Output of Read function is "
print file1.read()
print
  
# seek(n) takes the file handle to the nth
# bite from the beginning.
file1.seek(0) 