# Code snippet copied from http://www.sanfoundry.com/python-program-count-lines-text-file/
fname = input("Enter file name: ")
open_bracket_char = '['
close_brackt_char = ']'
num_lines = 0
with open(fname, 'r') as f:
    for line in f:
        num_lines += 1
print("Number of lines: " + str(num_lines))
error_count = 0
for line in range(0,num_lines):
    with open(fname, 'r') as f:
        for line_content in f:
            open_bracket=line_content.count(open_bracket_char)
            close_bracket=line_content.count(close_brackt_char)
            if(int(open_bracket) != int(close_bracket)):
                error_count+=1

if(error_count>0):
    print('File contains errors related to ( and )')
else:
    print('File ' + str(fname) + ' is fine.')
