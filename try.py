newfile = ""
filename = "C:/Users/DHAIRYA/Downloads/DetailedStatement.psv"
for i in filename:
    if (i == '/'):
        newfile += '\\\\'
    else:
        newfile += i
print(newfile)
