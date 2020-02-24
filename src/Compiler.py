#!/usr/bin/env python
# coding: utf-8

# In[184]:


import sys


# In[185]:


def generatelist(code):
    a=[]
    if('"' in code):
        j=code.find('"')
        a=code[:j].split()
        if('"' in code[j+1:]):
            k=code[j+1:].find('"')
            a=a+[code[j:j+k+2]]+generatelist(code[j+k+2:])
        else:
            assert(1==2),"error Invalid String type"
    else:
        a=code.split()
    return a


# In[186]:


def tokenisation(contents):
    contents_1=[]
    for i in range(len(contents)):
        contents_1.append([i+1,contents[i]])
    for i in range(len(contents_1)):
        while('\n' in contents_1[i][1]):
            j=contents_1[i][1].find('\n')
            contents_1[i][1]=contents_1[i][1][:j]+contents_1[i][1][j+1:]
        while('\t' in contents_1[i][1]):
            j=contents_1[i][1].find('\t')
            contents_1[i][1]=contents_1[i][1][:j]+contents_1[i][1][j+1:]
    b=True 
    i=0
    while(i<len(contents_1)):
        if(b):
            if('/*' in contents_1[i][1]):
                j=contents_1[i][1].find('/*')
                if('*/' in contents_1[i][1][j+2:]):
                    k=contents_1[i][1][j+2:].find('*/')
                    contents_1[i][1]=contents_1[i][1][:j]+contents_1[i][1][j+k+4:]
                    i=i-1
                else:
                    contents_1[i][1]=contents_1[i][1][:j]
                    b=False
        else:
            if('*/' in contents_1[i][1]):
                p=contents_1[i][1].find('*/')
                contents_1[i][1]=contents_1[i][1][p+2:]
                b=True
                i=i-1
            else:
                contents_1[i][1]=''
        i=i+1
    for i in range(len(contents_1)):
        if('//' in contents_1[i][1]):
            j=contents_1[i][1].find('//')
            contents_1[i][1]=contents_1[i][1][:j]
    contents=[]
    for i in contents_1:
        if(i[1]!=''):
            contents.append(i)
    keywords=['class','constructor','method','function','int','boolean','char','void','var','static','field','let','do','if']
    keywords+=['else','while','return','true','false','null','this']
    symbols=['(',')','[',']','{','}',',',';','=','.','+','-','*','/','&','|','~','<','>']
    for i in range(len(contents)):
        if('"'not in contents[i][1]):
            contents[i][1]=contents[i][1].split()
        else:
            contents[i][1]=generatelist(contents[i][1])
    for i in range(len(contents)):
        a=[]
        for j in contents[i][1]:
            if(j[0]=='"'):
                a=a+['<stringConstant>'+' '+j[1:-1]+' '+'</stringConstant>']
            else:
                p=''
                for k in j:
                    if('_'==k):
                        p+=k
                    elif(k.isalpha()):
                         if(len(p)>0 and p[0].isnumeric()):
                            assert(1==2),"Invalid StringConstant"
                         else:
                             p+=k
                    elif(k.isnumeric()):
                        p+=k
                    else:
                        if(len(p)>0):
                            if(p.isnumeric()):
                                a=a+['<integerConstant>'+' '+p+' '+'</integerConstant>']
                            elif(p in keywords):
                                a=a+['<keyword>'+' '+p+' '+'</keyword>']
                            else:
                                a=a+['<identifier>'+' '+p+' '+'</identifier>']
                            p=''
                        if(k=='<'):
                            k='&lt;'
                        if(k=='>'):
                            k='&gt;'
                        if(k=='&'):
                            k='&amp;'
                        a=a+['<symbol>'+' '+k+' '+'</symbol>']
                if(b):
                     if(len(p)>0):
                            if(p.isnumeric()):
                                a=a+['<integerConstant>'+' '+p+' '+'</integerConstant>']
                            elif(p in keywords):
                                a=a+['<keyword>'+' '+p+' '+'</keyword>']
                            else:
                                a=a+['<identifier>'+' '+p+' '+'</identifier>']
        contents[i][1]=a
    final=['<tokens>']
    for i in contents:
        final+=i[1]
    final+=['</tokens>'] 
    return [final,contents]



# In[187]:


def typeof(a):
    return ('<identifier>' in a)  or ('int' in a) or ('char' in a) or ('boolean' in a)


# In[188]:


def statement(a):
    return ('let' in a) or ('while' in a) or ('if' in a) or ('do' in a) or('return' in a)


# In[189]:


def op(a):
    for i in ['+','-','*','/','&amp;','&gt;','&lt;','|','=']:
        if(i in a):
            if(i=='/'):
                if(a.count(i)==2):
                    return True
            else:
                return True
    return False   


# In[190]:


def KeywordConstant(a):
    for i in ['true','false','null','this']:
        if(i in a):
            return True
    return False


# In[191]:


def unaryOp(a):
    return ('-' in a) or ('~' in a)


# In[192]:


def CompilevarDec(a,p):
    b=[]
    index=0
    b+=[(p+'<varDec>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    if (not typeof(a[index][0])):
        assert(1==2),"Error in Line varDec"+str(a[index][1])+"expected type"
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        if('identifier' not in a[index][0]):
            assert(1==2),"Error in Line varDec"+str(+a[index][1])+"expected identifier"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
        while(',' in a[index][0]):
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            if('identifier' not in a[index][0]):
                assert(1==2),"Error in Line varDec "+str(a[index][1])+"expected identifier"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
        if(';' not in a[index][0]):
                assert(1==2),"Error in Line varDec "+str(a[index][1])+"expected ;"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
    b+=[(p+'</varDec>',-1)]
    return [b,index]


# In[193]:


def CompileexpressionList(a,p):
    b=[]
    b+=[(p+'<expressionList>',-1)]
    index=0
    if(')' not in a[index][0]):
        d=Compileexpression(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        while(',' in a[index][0]):
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            d=Compileexpression(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
    b+=[(p+'</expressionList>',-1)]
    return [b,index]


# In[194]:


def CompilesubroutineCall(a,p):
    b=[]
    index=0
    b+=[(p+a[index][0],a[index][1])]
    index+=1
    if('.' in a[index][0]):
        b+=[(p+a[index][0],a[index][1])]
        index+=1
        a[index]
        assert('identifier'in a[index][0]),"Error in Line:subroutineCall "+str(a[index][1])+"Expecting Identifier"
        b+=[(p+a[index][0],a[index][1])]
        index+=1
    a[index]
    assert('(' in a[index][0]),"Error in Line subroutineCall "+str(a[index][1])+"Expecting Symbol ("
    b+=[(p+a[index][0],a[index][1])]
    index+=1
    d=CompileexpressionList(a[index:],p)
    b+=d[0]
    index+=d[1]
    assert(')'in a[index][0]),"Error in Line subroutineCall "+str(a[index][1])+"Expecting Symbol )"
    b+=[(p+a[index][0],a[index][1])]
    index+=1
    return [b,index]


# In[195]:


def Compileterm(a,p):
    b=[]
    index=0
    b+=[(p+'<term>',-1)]
    if('integerConstant' in a[index][0]):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    elif('stringConstant' in a[index][0]):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    elif(KeywordConstant(a[index][0])):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    elif(unaryOp(a[index][0])):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        d=Compileterm(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
    elif('identifier' in a[index][0]):
        if ('(' in a[index+1][0] or '.' in a[index+1][0]):
            d=CompilesubroutineCall(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
        elif('[' in a[index+1][0]):
            b+=[(p+'  '+a[index][0],a[index][1]),(p+'  '+a[index+1][0],a[index][1])]
            index+=2
            d=Compileexpression(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
            assert(']' in a[index][0]),"Error in Line: term "+str(a[index][1])+"Expected ]"
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1        
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
    elif('(' in a[index][0]):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        d=Compileexpression(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        assert(')' in a[index][0]),"Error in Line: term "+str(a[index][0])+"Expected )"
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    else:
        assert(1==2),"Error in line term "+str(a[index][1])+"Expecting term"
    b+=[(p+'</term>',-1)]
    return [b,index]


# In[196]:


def Compileexpression(a,p):
    b=[]
    index=0
    b+=[(p+'<expression>',-1)]
    d=Compileterm(a[index:],p+'  ')
    b+=d[0]
    index+=d[1]
    while(op(a[index][0])):
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        d=Compileterm(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
    b+=[(p+'</expression>',-1)]
    return [b,index]


# In[197]:


def CompilewhileStatement(a,p):
    b=[]
    index=0
    b+=[(p+'<whileStatement>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    if('(' not in a[index][0]):
        assert(1==2),"Error in Line whileStatement "+str(a[index][1])+"Expecting ("
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        d=Compileexpression(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        if(')' not in a[index][0]):
            assert(1==2),"Error in Line whileStatement "+str(a[index][1])+"Expecting )"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            if('{' not in a[index][0]):
                assert(1==2),"Error in Line whileStatement "+str(a[index][1])+"Expecting {"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                d=Compilestatements(a[index:],p+'  ')
                b+=d[0]
                index+=d[1]
                if ('}' not in a[index][0]):
                    assert(1==2),"Error in Line whileStatement "+str(a[index][1])+"Expecting }"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
                    index+=1
    b+=[(p+'</whileStatement>',-1)]
    return [b,index]


# In[198]:


def CompileReturnStatement(a,p):
    b=[]
    index=0
    b+=[(p+'<returnStatement>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    if (';' not in a[index][0]):
        d=Compileexpression(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        if(';' not in a[index][0]):
            assert(1==2),"Error in Line ReturnStatement"+str(a[index][1])+"Expecting ;"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    b+=[(p+'</returnStatement>',-1)]
    return [b,index]


# In[199]:



def CompiledoStatement(a,p):
    b=[]
    index=0
    b+=[(p+'<doStatement>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    d=CompilesubroutineCall(a[index:],p+'  ')
    b+=d[0]
    index+=d[1]
    if(';' not in a[index][0]):
        assert(1==2),"Error in Line doStatement"+str(a[index][1])+"Expecting ;"
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
    b+=[(p+'</doStatement>',-1)]
    return [b,index]


# In[200]:


def CompileifStatement(a,p):
    b=[]
    index=0
    b+=[(p+'<ifStatement>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    if('(' not in a[index][0]):
        assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected ("
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        d=Compileexpression(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        if(')' not in a[index][0]):
            assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected )"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            if('{' not in a[index][0]):
                assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected  symbol {"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                d=Compilestatements(a[index:],p+'  ')
                b+=d[0]
                index+=d[1]
                if('}' not in a[index][0]):
                    assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected Symbol }"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
                    index+=1
                    if('else' in a[index][0]):
                        b+=[(p+'  '+a[index][0],a[index][1])]
                        index+=1
                        if('{' not in a[index][0]):
                            assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected Symbol {"
                        else:
                            b+=[(p+'  '+a[index][0],a[index][1])]
                            index+=1
                            d=Compilestatements(a[index:],p+'  ')
                            b+=d[0]
                            index+=d[1]
                            if('}' not in a[index][0]):
                                assert(1==2),"Error in Line ifStatement "+str(a[index][1])+"Expected Symbol }"
                            else:
                                b+=[(p+'  '+a[index][0],a[index][1])]
                                index+=1
    b+=[(p+'</ifStatement>',-1)]
    return [b,index]


# In[201]:


def CompileletStatement(a,p):
    b=[]
    index=0
    b+=[(p+'<letStatement>',-1)]
    b+=[(p+'  '+a[index][0],a[index][1])]
    index+=1
    if('identifier' not in a[index][0]):
        assert(1==2),"Error in Line letStatement"+str(a[index][1])+"expected identifier"
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        if('[' in a[index][0]):
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            d=Compileexpression(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
            if(']' not in a[index][0]):
                assert(1==2),"Error in Line letStatement"+str(a[index][1])+"expected identifier"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
        if('=' not in a[index][0]):
            assert(1==2),"Error in Line letStatement"+str(a[index][1])+"expected identifier"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            d=Compileexpression(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
            if (';' not in a[index][0]):
                assert(1==2),"Error in Line letStatement"+str(a[index][1])+"expected ;"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
    b+=[(p+'</letStatement>',-1)]
    return [b,index]


# In[202]:


def Compilestatements(a,p):
    b=[]
    index=0
    b+=[(p+'<statements>',-1)]
    while(statement(a[index][0])):
        if ('let' in a[index][0]):
            d=CompileletStatement(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
        elif('while' in a[index][0]):
            d=CompilewhileStatement(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
        elif ('if' in a[index][0]):
            d=CompileifStatement(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
        elif ('do' in a[index][0]):
            d=CompiledoStatement(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
        else:
            d=CompileReturnStatement(a[index:],p+'  ')
            b+=d[0]
            index+=d[1]
    b+=[(p+'</statements>',-1)]
    return [b,index]
           


# In[203]:


def CompileparameterList(a,p):
    b=[]
    index=0
    b+=[(p+'<parameterList>',-1)]
    if (typeof(a[0][0])):
        b+=[(p+'  '+a[0][0],a[0][1])]
        if('<identifier>' not in a[1][0]):
            assert(1==2),"Error in line parameterList"+str(a[1][1])+"expected identifier"
        else:
            b+=[(p+'  '+a[1][0],a[1][1])]
            index=2
            while(',' in a[index][0]):
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                if(not typeof(a[index][0])):
                      assert(1==2),"Error in line parameterList"+str(a[index][0])+"missing type of Argument"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
                    index+=1
                    if('<identifier>' not in a[index][0]):
                        assert(1==2),"Error in line parameterList"+str(a[index][1])+"expected identifier"
                    else:
                        b+=[(p+'  '+a[index][0],a[index][1])]
                        index+=1
    b+=[(p+'</parameterList>',-1)]
    return [b,index]


# In[204]:


def CompilesubroutineBody(a,p):
    b=[]
    index=0
    b+=[(p+'<subroutineBody>',-1)]
    if('{' not in a[0][0]):
        assert(1==2),"Error in line subroutineBody "+str(a[0][1])+"expected {"
    else:
        b+=[(p+'  '+a[0][0],a[0][1])]
        index=1
        while('var' in a[index][0]):
            d=CompilevarDec(a[index:],p+'  ')
            index+=d[1]
            b+=d[0]
        d=Compilestatements(a[index:],p+'  ')
        b+=d[0]
        index+=d[1]
        if('}' not in a[index][0]):
            assert(1==2),"Error in line"+str(a[index][1])+"expected"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
    b+=[(p+'</subroutineBody>',-1)]
    return [b,index]
        


# In[205]:


def CompilesubroutineDec(a,p):
    b=[]
    index=0
    b+=[(p+'<subroutineDec>',-1)]
    b+=[(p+'  '+a[index][0],a[index][0])]
    index+=1
    if(not typeof(a[index][0]) and ('void' not in a[index][0])):
        print("Error in line subroutineDec",a[index][1],"return type missing for subroutine")
    else:
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        if('<identifier>' not in a[index][0]):
            assert(1==2),"Error in line subroutineDec "+str(a[index][1])+"expected subroutine name"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            if('(' not in a[index][0]):
                assert(1==2),"Error in line subroutineDec "+str(a[index][1])+"expected ("
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                d=CompileparameterList(a[index:],p+'  ')
                index+=d[1]
                b+=d[0]
                if(')' not in a[index][0]):
                    assert(1==2),"Error in line subroutineDec "+str(a[index][1])+"expected )"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
                    index+=1
                    d=CompilesubroutineBody(a[index:],p+'  ')
                    index+=d[1]
                    b+=d[0]
    b+=[(p+'</subroutineDec>',-1)]
    return [b,index]


# In[206]:


def CompileclassVarDec(a,p):
    b=[]
    index=0
    b+=[(p+'<classVarDec>',-1)]
    b+=[(p+'  '+a[0][0],a[0][1])]
    if(not type(a[1][0])):
        assert(1==2),"Error in line classVarDec"+str(a[1][1])+"type missing"
    else:
        b+=[(p+'  '+a[1][0],a[1][1])]
        if('<identifier>' not in a[2][0]):
            assert(1==2),"Error in line classVarDec"+str(a[2][1])+"expected identifier"
        else:
            b+=[(p+'  '+a[2][0],a[2][1])]
            index=3
            while(',' in a[index][0]) :
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                if('<identifier>' not in a[index][0]):
                    assert(1==2),"Error in line classVarDec"+str(a[index][1])+"expected identifier"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
            if(';' not in a[index][0]):
                assert(1==2),"Error in line classVarDec"+a[index][1]+"expected ;"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
            b+=[(p+'</classVarDec>',-1)]
            index+=1
    return [b,index]


# In[207]:


def CompileClass(a):
    p=''
    b=[]
    index=0
    if (a[0][0]!='<keyword> class </keyword>'):
        assert(1==2),"Error in line"+str(a[index][1])+" keyword class missing"
    else:
        b+=[(p+'<class>',-1)]
        b+=[(p+'  '+a[index][0],a[index][1])]
        index+=1
        if('<identifier>' not in a[index][0]):
            assert(1==2),"Error in line"+str(a[1][1])+"Expected identifier"
        else:
            b+=[(p+'  '+a[index][0],a[index][1])]
            index+=1
            if('{' not in a[index][0]):
                assert(1==2),"Error in line"+str(a[index][1])+"Expected Symbol {"
            else:
                b+=[(p+'  '+a[index][0],a[index][1])]
                index+=1
                while('static' in a[index][0] or 'field' in a[index][0]):
                    d=CompileclassVarDec(a[index:],p+'  ')
                    b+=d[0]
                    index+=d[1]
                while('constructor' in a[index][0] or 'method'in a[index][0] or 'function' in a[index][0]):
                    d=CompilesubroutineDec(a[index:],p+'  ')
                    b+=d[0]
                    index+=d[1]
                if('}' not in a[index][0]):
                    assert(1==2),"Error in line"+str(a[index][1])+"Expected Symbol }"
                else:
                    b+=[(p+'  '+a[index][0],a[index][1])]
        b+=[(p+'</class>',-1)]
    return b


# In[208]:


def parser(a):
    contents=[]
    contents=CompileClass(a)
    final=[]
    for i in contents:
        final+=[i[0]]
    return [final,contents]


# In[209]:


def compileTerm(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    i=1
    b=[]
    c=a[i][0].split()
    if(c[0]=='<symbol>'):
        if(c[1]=='('):
            i+=1 # for ( 
            d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
            i+=1 # for )
        else:
            i+=1 # for Unaryop
            d=compileTerm(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
            if(c[1]=='-'):
                b+=['neg']
            else:
                b+=['not']
    elif(c[0]=='<integerConstant>'):
        b+=['push'+' '+'constant'+' '+c[1]]
        i+=1 # for integerConstant
    elif(c[0]=='<keyword>'):
        i+=1 # for keyword
        if(c[1]=='this'):
            b+=['push pointer 0']
        else:
            b+=['push constant 0']
            if(c[1]=='true'):
                b+=['not']
    elif(c[0]=='<identifier>'):
        kind=''
        index=''
        typ=''
        flag=[True,-1]
        if(c[1] in set(subroutineSymboltable.keys())):
                kind=subroutineSymboltable[c[1]][0]
                typ=subroutineSymboltable[c[1]][1]
                index=str(subroutineSymboltable[c[1]][2])
        elif(c[1] in set(classSymboltable.keys())):
            kind=classSymboltable[c[1]][0]
            if(kind=='field'and subroutineKind=='function'):
                flag=[False,i]               #print("Error Not declared ")
            else:
                if(kind=='field'):
                    kind='this'
                typ=classSymboltable[c[1]][1]
                index=str(classSymboltable[c[1]][2])
        else:
             flag=[False,i]                   #print("Error not declared variable")
        i+=1 # for <identifier>
        if(len(a[i][0].split())>1):
            if('['==(a[i][0].split())[1]):
                i+=1 # for '['
                d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
                b+=d[0]
                i+=d[1]
                i+=1 # for ']'
                if(not flag[0]):
                    assert(1==2),"Variable"+str(a[flag[1]][0].split()[1])+"is not declared present in line"+str(a[flag[1]][1])
                else:
                   b+=['push'+' '+kind+' '+index]
                   b+=['add','pop pointer 1','push that 0']
            elif('('==(a[i][0].split())[1]):
                b+=['push pointer 0']
                i+=1 # for (
                d=compileExpressionList(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
                b+=d[0]
                nP=d[1]
                i+=d[2]
                i+=1 # for ) 
                b+=['call'+' '+classname+'.'+c[1]+' '+str(nP+1)]
            elif('.'==(a[i][0].split())[1]):
                i+=1
                id2=(a[i][0].split())[1]
                if(flag[0]):
                    b+=['push'+' '+kind+' '+index]
                i+=1 # for (
                d=compileExpressionList(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
                b+=d[0]
                nP=d[1]
                i+=d[2]
                i+=1 # for ) 
                if(flag[0]):
                    b+=['call'+' '+typ+'.'+id2+' '+str(nP+1)]
                else:
                    b+=['call'+' '+c[1]+'.'+id2+' '+str(nP)]
        else:
            b+=['push'+' '+kind+' '+index]
            if(not flag[0]):
                 assert(1==2),"Variable"+str(a[flag[1]][0].split()[1])+"is not declared present in line"+str(a[flag[1]][1])
    else:
        j=a[i][0].find('<')
        string=a[i][0][j+17:-18]
        print(string)
        length=len(string)
        print(len(string))
        b+=['push'+' '+'constant'+' '+str(length)]
        b+=['call String.new 1']
        for ii in string:
                b+=['push'+' '+'constant'+' '+str(ord(ii))]
                b+=['call String.appendChar 2']
        i+=1 # for <stringConstant>
    i+=1 # for</term>
    return [b,i]


# In[210]:


def call(op):
    if (op=='+'):
        return ['add']
    elif(op=='-'):
        return ['sub']
    elif(op=='&amp;'):
        return ['and']
    elif(op=='|'):
        return ['or']
    elif(op=='&gt;'):
        return ['gt']
    elif(op=='&lt;'):
        return ['lt']
    elif(op=='='):
        return ['eq']
    elif(op=='*'):
        return ['call Math.multiply 2']
    elif(op=='/'):
        return ['call Math.divide 2']


# In[211]:


def compileExpression(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    b=[]
    i=1
    op=''
    while('</expression>'!=(a[i][0].split())[0]):
        if('<term>'==(a[i][0].split())[0]):
            d=compileTerm(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
            if(op!=''):
                print(op=='&lt;',op)
                b+=call(op)
                op=''
        elif('<symbol>'==(a[i][0].split())[0]):
            if('('==(a[i][0].split())[1]):
                i+=1
                d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
                b+=d[0]
                i+=d[1]
                i+=1
                if(op!=''):
                    b+=call(op)
                    op=''
            else:
                op=(a[i][0].split())[1]
                if(op=='&lt;'):
                    print(a[i])
                i+=1
        else:
            i+=1
    i+=1
    return [b,i]


# In[212]:


def compileExpressionList(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    b=[]
    nP=0
    i=1
    while('</expressionList>'!=(a[i][0].split())[0]):
        if((a[i][0].split())[0]=='<expression>'):
            d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
            nP+=1
        else:
            i+=1
    i+=1 # for '</expressionList>'
    return [b,nP,i]


# In[213]:


def compiledoStatement(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    b=[]
    i=2
    id1=(a[i][0].split())[1]
    i+=1
    if('.'!=(a[i][0].split())[1]):
        b+=['push pointer 0']
        i+=1 #  for (
        d=compileExpressionList(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
        b+=d[0]
        nP=d[1]
        i+=d[2]
        b+=['call'+' '+classname+'.'+id1+' '+str(nP+1),'pop temp 0']
        i+=1 # for ) 
    else:
        i+=1 # for '.'
        kind=''
        typ=''
        id2=(a[i][0].split())[1]
        i+=1
        if(id1 in set(subroutineSymboltable.keys())):
            kind=subroutineSymboltable[id1][0]
            typ=subroutineSymboltable[id1][1]
            index=subroutineSymboltable[id1][2]
            b+=['push'+' '+kind+' '+str(index)]
        elif(id1 in set(classSymboltable.keys())):
            kind=classSymboltable[id1][0]
            typ=classSymboltable[id1][1]
            index=classSymboltable[id1][2]
            if(kind=='field'):
                if(subroutineKind=='function'):
                    print("Error can't access field variables")
                else:
                    b+=['push'+' '+'this'+' '+str(index)]
            else:
                b+=['push'+' '+'static'+' '+str(index)]
        i+=1 #  for (
        d=compileExpressionList(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
        b+=d[0]
        nP=d[1]
        i+=d[2]
        i+=1 # for ) 
        if(kind==''):
            b+=['call'+' '+id1+'.'+id2+' '+str(nP)]
        else:
            b+=['call'+' '+typ+'.'+id2+' '+str(nP+1)]
        b+=['pop temp 0']
    i+=2 #for ; </doStatement>
    return [b,i]


# In[214]:


def compilereturnStatement(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    b=[]
    i=2
    if('<expression>'==(a[i][0].split())[0]):
        d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
        b+=d[0]
        i+=d[1]
        b+=['return']
    else:
        b+=['push constant 0']
        b+=['return']
    i+=2 # for ; and </returnStatement>
    return [b,i]


# In[215]:


def compilewhileStatement(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    global labelNum
    g=labelNum
    b=['label'+' '+classname+'.'+str(g)]
    labelNum+=2
    i=3
    d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
    b+=d[0]
    i+=d[1]
    i+=2 # for ) { 
    b+=['not']
    b+=['if-goto'+' '+classname+'.'+str(g+1)]
    d=compilestatements(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
    b+=d[0]
    i+=d[1]
    i+=1  # for }
    b+=['goto'+' '+classname+'.'+str(g)]
    b+=['label'+' '+classname+'.'+str(g+1)]
    i+=1 # for </whileStatement>
    return [b,i]


# In[216]:


def compileifStatement(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    global labelNum
    b=[]
    i=3
    g=labelNum
    labelNum+=2
    d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
    b+=d[0]
    i+=d[1]
    b+=['not']
    b+=['if-goto'+' '+classname+'.'+str(g)]
    i+=2 # for { )
    d=compilestatements(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
    b+=d[0]
    i+=d[1]
    i+=1  # for }
    b+=['goto'+' '+classname+'.'+str(g+1)]
    b+=['label'+' '+classname+'.'+str(g)]
    if(len(a[i][0].split())>1 and 'else'==(a[i][0].split())[1]):
        i+=2 # for else and { 
        d=compilestatements(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
        b+=d[0]
        i+=d[1]
        i+=1 # for } 
    b+=['label'+' '+classname+'.'+str(g+1)]
    i+=1 # for </ifStatement>
    return [b,i]


# In[217]:


def compileletStatement(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    varname=(a[2][0].split())[1]
    kind=''
    index=''
    b=[]
    i=0
    if(varname in set(subroutineSymboltable.keys())):
        kind=subroutineSymboltable[varname][0]
        index=str(subroutineSymboltable[varname][2])
    elif(varname in set(classSymboltable.keys())):
        if(classSymboltable[varname][0]=='static'):
            kind='static'
        else:
            if(subroutineKind=='function'):
                 assert(1==2),"Variable"+varname+"not declared and used in line"+str(a[2][1]) 
            else:
                kind='this'
        index=str(classSymboltable[varname][2])
    else:
         assert(1==2),"Variable"+varname+"not declared and used in line"+str(a[2][1]) 
    i=4
    d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
    b+=d[0]
    i+=d[1]
    i+=1
    if('='==(a[3][0].split())[1]):
        b+=['pop'+' '+kind+' '+index]
    else:
        b+=['push'+' '+kind+' '+index]
        b+=['add']
        i+=1
        d=compileExpression(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
        b+=d[0]
        i+=d[1]
        i+=1
        b+=['pop temp 0','pop pointer 1','push temp 0','pop that 0']
    return [b,i]


# In[218]:


def compilestatements(a,classSymboltable,subroutineSymboltable,subroutineKind,classname):
    i=1
    b=[]
    while('</statements>'!=(a[i][0].split())[0]):
        if('<letStatement>'==(a[i][0].split())[0]):
            d=compileletStatement(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
        elif('<ifStatement>'==(a[i][0].split())[0]):
            d=compileifStatement(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
        elif('<whileStatement>'==(a[i][0].split())[0]):
            d=compilewhileStatement(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
        elif('<returnStatement>'==(a[i][0].split())[0]):
            d=compilereturnStatement(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
        elif('<doStatement>'==(a[i][0].split())[0]):
            d=compiledoStatement(a[i:],classSymboltable,subroutineSymboltable,subroutineKind,classname)
            b+=d[0]
            i+=d[1]
        else:
            i+=1
    i+=1
    return [b,i]    


# In[219]:


def compilevarDec(a,subroutineSymboltable,local_count,total_count):
    Symboltable={}
    i=2
    typeofvar=''
    while('</varDec>'!=(a[i][0].split())[0]):
        if(typeofvar==''):
            typeofvar=(a[i][0].split())[1]
            i+=1
        elif(','==(a[i][0].split())[1]):
            i+=1
        elif(';'==(a[i][0].split())[1]):
            i+=1
        else:
            b=a[i][0].split()
            print(b)
            if(b[1] in set(subroutineSymboltable.keys())):
                assert(1==2),"Error redeclared variable"+b[1]+"in line"+str(a[i][1])
            else:
                Symboltable[b[1]]=['local',typeofvar,local_count]
                local_count+=1
                total_count+=1
                i+=1
    i+=1
    return [Symboltable,local_count,total_count,i]


# In[220]:


def compilesubroutineBody(a,subroutineSymboltable,classSymboltable,f,local_count,total_count):
    i=1
    b=[]
    classname=f[0]
    subroutinename=f[1]
    subroutinekind=f[2]
    field_count=f[3]
    argument_count=f[4]
    while('</subroutineBody>'!=(a[i][0].split())[0]):
        if('<varDec>'==(a[i][0].split())[0]):
            d=compilevarDec(a[i:],subroutineSymboltable,local_count,total_count)
            subroutineSymboltable.update(d[0])
            print(subroutineSymboltable)
            local_count=d[1]
            total_count=d[2]
            i+=d[3]
        elif('<statements>'==(a[i][0].split())[0]):
            b+=['function '+f[0]+'.'+f[1]+' '+str(local_count)]
            if(subroutinekind=='constructor'):
                b+=['push'+' '+'constant'+' '+str(field_count)]
                b+=['call Memory.alloc 1']
                b+=['pop pointer 0']
            elif(subroutinekind=='method'):
                b+=['push argument 0']
                b+=['pop pointer 0']
            d=compilestatements(a[i:],classSymboltable,subroutineSymboltable,subroutinekind,f[0])
            b+=d[0]
            i+=d[1]
        else:
            i+=1
    return [b,i]


# In[221]:


def compileparameterList(a,argument_count,total_count):
    i=1
    Symboltable={}
    while('</parameterList>'!=(a[i][0].split())[0]):
        if(','==((a[i][0]).split())[1]):
            i+=1
        else:
            argtype=(a[i][0].split())[1]
            i+=1
            varname=(a[i][0].split())[1]
            i+=1
            Symboltable[varname]=['argument',argtype,argument_count]
            argument_count+=1
            total_count+=1
    i+=1
    return [Symboltable,argument_count,total_count,i]


# In[222]:


def compilesubroutineDec(a,classSymboltable,classname,field_count):
    subroutineSymboltable={}
    subroutinekind=(a[1][0].split())[1]
    subroutinetype=(a[2][0].split())[1]
    subroutinename=(a[3][0].split())[1]
    argument_count=0
    local_count=0
    total_count=0
    b=[]
    i=5
    if(subroutinekind=='constructor' and subroutinetype!=classname):
          assert(1==2),"Error invalid return type for constructor"
    else:
        if(subroutinekind=='method'):
            subroutineSymboltable['this']=['argument',classname,argument_count]
            argument_count+=1
            total_count+=1
        while('</subroutineDec>'!=(a[i][0].split())[0]):
            if('<parameterList>'==(a[i][0].split())[0]):
                    d=compileparameterList(a[i:],argument_count,total_count)
                    subroutineSymboltable.update(d[0])
                    argument_count=d[1]
                    total_count=d[2]
                    i+=d[3]
            elif('<subroutineBody>'==(a[i][0].split())[0]):
                    f=[classname,subroutinename,subroutinekind,field_count,argument_count]
                    d=compilesubroutineBody(a[i:],subroutineSymboltable,classSymboltable,f,local_count,total_count)
                    b+=d[0]
                    i+=d[1]
            else:
                i+=1
        i+=1
    return [b,i]


# In[223]:


def compileclassVarDec(a,static_count,field_count,total_count,classSymboltable):
    Symboltable={}
    j=len(a)
    i=1
    keywordtype=''
    kind=''
    while('</classVarDec>' != (a[i][0].split())[0]):
        b=a[i][0].split()
        if(kind==''):
            kind=b[1]
        elif(keywordtype==''):
            keywordtype=b[1]
        elif(b[0]=='<identifier>'):
            if(b[1] in set(classSymboltable.keys())):
                assert(1==2),"Error redeclared variable"+b[1]+"in line"+str(a[i][1])
            else:
                if(kind=='static'):
                    Symboltable[b[1]]=[kind,keywordtype,static_count]
                    static_count+=1
                else:
                    Symboltable[b[1]]=[kind,keywordtype,field_count]
                    field_count+=1
                total_count+=1
        i+=1
    i+=1
    return [Symboltable,static_count,field_count,total_count,i]


# In[224]:


def compileClass(a):
    b=[]
    classSymboltable={}
    static_count=0
    field_count=0
    total_count=0
    j=len(a)
    i=1
    classname=(a[2][0].split())[1]
    while(i!=j):
        if('<classVarDec>' == (a[i][0].split())[0]):
            d=compileclassVarDec(a[i:],static_count,field_count,total_count,classSymboltable)
            classSymboltable.update(d[0])
            static_count=d[1]
            field_count=d[2]
            total_count=d[3]
            i+=d[4]
        elif('<subroutineDec>'==(a[i][0].split())[0]):
            d=compilesubroutineDec(a[i:],classSymboltable,classname,field_count)
            b+=d[0]
            i+=d[1]
        else:
            i+=1
    return b


# In[225]:


labelNum=0


# In[226]:


def main():
    count=int(sys.argv[1])
    files=[]
    global labelNum
    for i in range(count):
        files.append(sys.argv[2+i])
    for file in files:
        labelNum=0
        with open(file) as myfile:
            contents=myfile.readlines()
        filename=file[:-5]
        try:
            contents=tokenisation(contents)
        except IndexError:
            with open(filename+'.err',mode='w') as f1:
                f1.write('Program terminated with no class declaration')
            continue
        except AssertionError as e:
            with open(filename+'.err',mode='w') as f2:
                f2.write(str(e))
            continue
        else:
            final=contents[0]
            contents=contents[1]
            with open(filename+'T.xml',mode='w') as myfile:
                 myfile.write('\n'.join(final)+'\n')
            final=[] # important tuple
            for i in contents:
                ii=i[0]
                for j in i[1]:
                    final+=[(j,ii)]
            try:
                contents=parser(final)
            except IndexError:
                    with open(filename+'.err',mode='w') as f1:
                        f1.write('Program terminated with no class declaration')
                    continue
            except AssertionError as e:
                    with open(filename+'.err',mode='w') as f2:
                         f2.write(str(e))
                    continue
            else:
                final=contents[0]
                contents=contents[1]
                with open(filename+'.xml',mode='w') as myfile:
                    myfile.write('\n'.join(final)+'\n')
                try:
                    contents=compileClass(contents)
                except IndexError:
                    with open(filename+'.err',mode='w') as f1:
                        f1.write('Program terminated with no class declaration')
                    continue
                except AssertionError as e:
                     with open(filename+'.err',mode='w') as f2:
                        f2.write(str(e))
                else:
                    with open(filename+'.vm',mode='w') as myfile:
                        myfile.write('\n'.join(contents)+'\n')


            


# In[227]:


if __name__ == "__main__":
    main()


# In[ ]:




