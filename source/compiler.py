#import cbedata
import sys
debug = False
dieonerror = False

fileread = sys.argv[1]
fileout = sys.argv[2]


#OFFLINE PORTION
print('CardCard CL Compiler')
print('CBEDATA v1.4.4 (Modified)')


# # # CBEDATA # # # 
#offline interpreter, get-info
def get_offline(st, path, ty):
    global debug
    pathlist = path.split('-')
    
    st = st.replace('^>', '{special}1')
    st = st.replace('^;', '{special}2')
    st = st.replace('^==', '{special}3')
    st = st.replace('^[', '{special}4')
    st = st.replace('^]', '{special}5')
    
    
    contents = st


    #print('CBD Info: contents var ',contents)
    
    
    offset = 0
    c = 0
    offsets = []
    ok = 1
    
    while c < len(pathlist) - 1:
        i = pathlist[0]
        str(i)
        wtf = 'class['+i
        offset = contents.find(wtf, int(offset), len(contents))
        #print(offset)
    
        pathlist.pop(0)
        #print(pathlist)


    #if the path is invalid, an error will be thrown

    lineafter = contents.find(']',int(offset),len(contents))
    subclass = contents[int(offset):int(lineafter):1]
    
    if debug:
        print('CBD Info: Subclass ',subclass)

    subclass_index_st = subclass.find(str(pathlist[0])+'==')
    subclass_index_et = subclass.find(';',subclass_index_st,len(subclass))
    variable_0 = subclass[int(subclass_index_st):int(subclass_index_et):1]

    var1 = variable_0.split('==')
                                      
    if ty == 'cls':
        return(subclass.replace('{special}1','>').replace('{special}2',';').replace('{special}3','==').replace('{special}4','[').replace('{special}5',']'))

    if ty == 'var':
        norep = str(var1[0])+'=='+str(var1[1])
        return norep.replace('{special}1','>').replace('{special}2',';').replace('{special}3','==').replace('{special}4','[').replace('{special}5',']')

    if ty == 'val':
        if debug:
            print('CBD Info: Return Value',var1[1].replace('{special}1','>').replace('{special}2',';').replace('{special}3','==').replace('{special}4','[').replace('{special}5',']'))
        return(var1[1].replace('{special}1','>').replace('{special}2',';').replace('{special}3','==').replace('{special}4','[').replace('{special}5',']'))

    if ty == 'raw':
        return(contents.replace('{special}1','>').replace('{special}2',';').replace('{special}3','==').replace('{special}4','[').replace('{special}5',']'))

# # # CBEDATA # # # 








def fileio(name, mode, contents = ""):
    f = open(name, mode)
    if mode == 'r':
        try:
            tr = f.read()
        except:
            input('compiler fatal error: could not load a file, <enter> to exit')
            exit()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    f.close()
    return tr
    
def printf(s):
    global debug
    if debug:
        print(s)
    else:
        pass
    
contents = fileio(fileread, 'r').split('\n')
output = ''

if debug:
    print('compiler info debugmode: VERBOSE')
if not debug:
    print('compiler info debugmode: SILENT')


if '-' in fileio(fileread, 'r'):
    if dieonerror:
        input('compiler fatal error: illegal char - in precompiled')
        exit()
    else:
        c = fileio(fileread, 'r')
        c = c.replace('-', '[dash_escape]')
        fileio(fileread, 'w', c)
    
for i in contents:
    i = str(i)
    printf('Contents of this line: '+i)
    if len(i) == 0:
        i = '#BLANK'
    if i[0] != '/' and i[0] != '#':
        printf('compiler info: This line will be ignored by the compiler.\n')
        output = output + i +'\n'
    if i[0] == '#':
        printf('compiler info: This line is a comment.\n')
    if i[0] == '/':
        #/textbar, bgd #420690, fgd #ABCDEF, fontsize 69, text About Me
        conditions = i.split(', ')
        realcone = {}
        #print('\n')
        if len(conditions) >= 2:
            #print(conditions)
            for j in conditions:
                #print(j)
                if j[0] != '/':
                    twoparts = j.split(' ',1)
                    #print('Twoparts',twoparts)
                    realcone[twoparts[0]] = twoparts[1]
            printf(realcone)
            #printf('')

            firstop = i.find(' ')
            printf(firstop)
            printf(i[1:firstop-1])
            printf('main-'+i[1:firstop-1]+'-htmltext')
            try:
                con = get_offline( fileio('compilerlink.cbedata', 'r'), 'main-'+i[1:firstop-1]+'-htmltext', 'val')
            except IndexError:
                con = 'compiler nonfatal error: non variable in compilerlink.cbedata'
                if dieonerror:
                    input('compiler fatal error: non variable in compilerlink.cbedata, <enter> to exit')
                    exit()
            
            printf('Template Text '+con)

            for i in realcone:
                con = con.replace('$'+i, realcone[i])
            printf(con)
            output = output + con + '\n'
            
        else:
            firstop = i.find(' ')
            printf('compiler info: One condition command, will not perform space splice')
            ssi = get_offline( fileio('compilerlink.cbedata', 'r'), 'main-'+i[1:firstop-1]+'-htmltext', 'val')
            output = output + ssi + '\n'

        
        printf('')

output = '<!--this HTML file was compiled using the CardCard Command Line Utility-->\n' + output
output = output.replace('[dash_escape]', '-')


printf('Writing to output file: non.html')
fileio(fileout,'w',output)

print('Show output file?')
s = input('[Y/N] ')

if s == 'y' or s == 'Y':
    print(output)
        
