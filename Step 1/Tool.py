import astpretty
from typed_ast import ast3
import re

import astor
import typed_astunparse
import json
import time
import sys
import os.path

import collections
import copy

from anytree import Node,RenderTree

from typing import (
    Any, TypeVar, List, Tuple, cast, Set, Dict, Union, Optional, Callable, Sequence,
)

import subprocess

from collections import defaultdict



from subprocess import Popen, PIPE

#TODO  

#  -  make it so that the programmer can change the levels.
#  -  How to correlate the lines without deleting the comments or searching the instruction through code

buildInFunctions = {
    
    "all": "High",
    "any": "High",
    "callable":"High",
    "compile":"High",
    "delattr":"High",
    "eval":"High",
    "filter":"High",
    "format":"High",
    "frozenset":"High",
    "getattr":"High",
    "globals":"High",
    "hasattr":"High",
    "id":"High",
    "input":"High",
    "isinstance":"High",
    "issubclass":"High",
    "iter":"High",
    "locals":"High",
    "len":"High",
    "max":"High",
    "min":"High",
    "open":"High",
    "print":"High",
    "range":"High",
    "repr":"High",
    "round":"High",
    "setattr":"High",
    "sum":"High",
    "super":"High",
    "abs":"High",
    "ascii":"High",
    "bin":"High",
    "bool":"High",
    "bytearray":"High",
    "bytes":"High",
    "chr":"High",
    "complex":"High",
    "dict":"High",
    "float":"High",
    "hash":"High",
    "hex":"High",
    "int":"High",
    "pct":"High",
    "ord":"High",
    "pow":"High",

}


class HCLI():
    pass

class HCHI(HCLI):
    pass

class LCLI(HCLI):
    pass

class LCHI(LCLI,HCHI):
    pass
    
with open('todoexample.py') as b:
    todotree = ast3.parse(b.read())

with open('TESTEPARAELIMINAR.py') as b:
    soontodeletetree = ast3.parse(b.read())

with open('finaltest.py') as b:
    finaltree = ast3.parse(b.read())


with open('implicitFlowIf.py') as b:
    implicitIFTree = ast3.parse(b.read())


with open('implicitFlowWhile.py') as b:
    implicitWhileTree = ast3.parse(b.read())


with open('zclassgentest.py') as b:
    ztree = ast3.parse(b.read())

with open('models2.py') as b:
    ModelsTree = ast3.parse(b.read())


with open('views2.py') as b:
    ElectionServerTree = ast3.parse(b.read())


with open('test.py') as b:
    testTree = ast3.parse(b.read())

with open('testAssignTransformer.py') as b:
    testTransformer = ast3.parse(b.read())

with open('outputBeforeChanges.py') as b:
    treeBeforeChanges = ast3.parse(b.read())


with open('testNewClass.py') as b:
    classTree = ast3.parse(b.read())

with open('recognizingClassTest.py') as b:
    classRecognizeTree = ast3.parse(b.read())


with open('implicitflowsFor.py') as b:
    implicitTree = ast3.parse(b.read())

with open('expressionTree.py') as b:
    expressionTree = ast3.parse(b.read())

with open('multipleFor.py') as b:
    multipleForTree = ast3.parse(b.read())


def fileToTree(file):
    with open(file) as b:
        tree = ast3.parse(b.read())
    return tree


def prettyprinting(tree):
    astpretty.pprint(tree)

def prettyprintingString(node):
    return astpretty.pprint(node)



def unparseTypedASt(tree):
    #prettyprinting(tree)
    #print(typed_astunparse.unparse(tree))
    return typed_astunparse.unparse(tree)

def generateClassNodes(className,dependencies):

    defaultClassNode = ast3.ClassDef(
            lineno=0,
            col_offset=0,
            name=className,
            bases=[],
            keywords=[],
            body=[ast3.Pass(lineno=0, col_offset=0)],
            decorator_list=[],
        )

    if dependencies: #If list is not empty
        for dep in dependencies:
            defaultClassNode.bases.append(ast3.Name(lineno=0, col_offset=0, id=dep, ctx=ast3.Load()))

    #prettyprinting(defaultClassNode)
    return defaultClassNode


# input seria qualquer coisa Conf- (L,H) Int- (B,C)(A,B)
# Talvez atraves de 2 listas?[LC,MC,HC][LI,MI,HI]

def inputIntoConfAndIntLists():
    secLevelNumbers = int(input("Enter the number of security levels:"))
    intList = []
    confList = []

    print("Insert Confidentiality levels in a crescent manner:")
    for i in range(0,secLevelNumbers):
        lvlConf = input()
        confList.append(lvlConf)

    print("Insert Integrity levels in a crescent manner:")
    for i in range(0,secLevelNumbers):
        lvlInt = input()
        intList.append(lvlInt)
    
    #print("confLIst",confList)
    #print("intList", intList)

    if len(confList)== len(intList):
        return confList,intList
    else:
        return "Lists must have equal size."

def generateSecurityClasses2(tree,ConfList,IntList):  

    # test out that the middle classes can't be compared, so no relations between them. 


    #1st step: 0,0; 1,0 ; 0,1 ; 2,0; 1,1 ; 0,2; 2,1; 1,2 ; 2,2  #Every pair completed, now the relations:

    # 0,0 -> 0,1 
    # 0,0 -> 1,0

    # 0,1 -> 1,1
    # 0,1 -> 0,2
    
    # 1,0 -> 2,0
    # 1,0 -> 1,1

    # 1,1 -> 1,2
    # 1,1 -> 2,1

    # 2,0 -> 2,1
    # 0,2 -> 1,2

    # 2,1 -> 2,2
    # 1,2 -> 2,2



    # 0,0 -> 0,1
    # 0,0 -> 1,0
    
    # 1,0 -> 1,1
    # 0,1 -> 1,1

    notImportCounter = 0  # Check how many imports to insert the classes after
    for nody in ast3.walk(tree):
        if isinstance(nody,ast3.Import) or isinstance(nody,ast3.ImportFrom):
            notImportCounter+=1


    insertIndex = notImportCounter

    sizeOFConfList = len(ConfList)

    for indexConf in range(len(ConfList)):
        for indexInt in range(len(IntList)):

            if indexConf + 1 == sizeOFConfList and indexInt + 1 == sizeOFConfList:
                node = generateClassNodes(ConfList[indexConf] + IntList[indexInt],[])
                tree.body.insert(insertIndex,node)
                ast3.fix_missing_locations(node)
                continue

            elif indexConf + 1 == sizeOFConfList:
                node = generateClassNodes(ConfList[indexConf] + IntList[indexInt] , [ ConfList[indexConf] + IntList[indexInt + 1 ]])
                tree.body.insert(insertIndex,node)
                ast3.fix_missing_locations(node) 
                continue

            elif indexInt + 1 == sizeOFConfList:
                node = generateClassNodes(ConfList[indexConf] + IntList[indexInt] , [ ConfList[indexConf + 1] +  IntList[indexInt]])
                tree.body.insert(insertIndex,node)
                ast3.fix_missing_locations(node)
                continue 
            else:
                #prettyprinting(tree)
                node = generateClassNodes(ConfList[indexConf] + IntList[indexInt] , [ ConfList[indexConf + 1] +  IntList[indexInt] , ConfList[indexConf] + IntList[indexInt+1 ]]) 
                tree.body.insert(insertIndex,node)
                ast3.fix_missing_locations(node)
                continue
                          
    #prettyprinting(tree)

    #prettyprinting(tree)
    unparseTypedASt(tree)
    return tree



#ConfList = ["LC", "HC"]
#IntList = ["HI","LI"]

# #generateSecurityClasses2(ztree, ConfList, intList)



def generateInsertNode():
    nodeToInsert = ast3.UnaryOp(
                    ast3.USub(),
                    ast3.Num(5, lineno=0, col_offset=0),
                    lineno=0,
                    col_offset=0)

    return nodeToInsert
  
def generateafterNode():
    return ast3.Assign(
            lineno=29,
            col_offset = 0,
            targets=[ast3.Name(lineno=0, col_offset=0 ,id="ds" , ctx=ast3.Store())],
            value= ast3.Name(lineno=31 ,col_offset=4,id='leftside',ctx=ast3.Load()),
            type_comment='None')


# def declassification(var: Tuple[LowIntegrity, HighConfidentiality]):
#     return cast(Tuple[LowIntegrity, LowConfidentiality],var)


def sizeOfNodeInLines(node):
    unparsedLines = unparseTypedASt(node).split("\n")
    return len(unparsedLines)
    
def sizeOfNodeInLinesClass(node):
    unparsedLines = unparseTypedASt(node).split("\n")
    return len(unparsedLines) - 3 # Because this methods adds 1 empty line

def separateCodeThroughLines(node):
    unparsedLines = unparseTypedASt(node).split("\n")
    return unparsedLines



def equalNodes(node1, node2):
    if isinstance(node1, ast3.withitem):
        node1 = node1.context_expr
    if isinstance(node2, ast3.withitem):
        node2 = node2.context_expr


    return prettyprintingString(node1) == prettyprintingString(node2) and node1.lineno == node2.lineno
    #return prettyprintingString(node1) == prettyprintingString(node2) and node1.lineno == node2.lineno and node1.col_offset == node2.col_offset

def equalNodesDifLines(node1,node2):
    prettyprinting(node1)
    prettyprinting(node2)
    return prettyprintingString(node1) == prettyprintingString(node2)



def getFirstStatement(leftsideNumber):
    return ast3.Assign(
            lineno=0,
            col_offset = 0,
            targets=[ast3.Name(lineno=0, col_offset=0,id= "leftside" + str(leftsideNumber), ctx=ast3.Store())],
            value = ast3.Call(
                        lineno=0,
                        col_offset=0,
                        func=ast3.Name(lineno=0, col_offset=0, id='LCHI', ctx=ast3.Load()),
                        args=[],
                        keywords=[]),

            type_comment=None,
            )

def getAssignStatement(leftsideNumber,idBuiltIn):
        return ast3.Assign(
            lineno=0,
            col_offset = 0,
            targets=[ast3.Name(lineno=0, col_offset=0,id= "leftside" + str(leftsideNumber), ctx=ast3.Store())],
            value = ast3.Name(lineno=0, col_offset=0,id=idBuiltIn , ctx=ast3.Load()),
            type_comment=None,
            )


def getAssignStatementForAttrCases(leftsideNumber,obj,arg):
        return ast3.Assign(
                    lineno=0,
                    col_offset=0,
                    targets=[ast3.Name(lineno=0, col_offset=0,id='leftside' + str(leftsideNumber), ctx=ast3.Store())],
                    value=ast3.Attribute(
                        lineno=0,
                        value=ast3.Name(lineno=0, col_offset=0,id=obj, ctx=ast3.Load()),
                        attr=arg,
                        ctx=ast3.Load(),
                        ),
                    type_comment=None
                    )
                
def getAssignStatementForSubscriptCases(leftsideNumber,rightside): # Which means when we have [] in the functions. e.g a dictionary. or a list
        return ast3.Assign(
                    lineno=0,
                    col_offset=0,
                    targets=[ast3.Name(lineno=0, col_offset=0,id='leftside' + str(leftsideNumber), ctx=ast3.Store())],
                    value=rightside,
                    type_comment=None
                    )


def getAssignmentForLoops(leftside,rightside):
    return ast3.Assign(
                    lineno=0,
                    col_offset=0,
                    targets=[ast3.Name(lineno=0, col_offset=0,id = leftside, ctx= ast3.Store())],
                    value= ast3.Name(lineno=0, col_offset=0, id = rightside, ctx= ast3.Load()),
                    type_comment=None
                    )


def getVariablesFromNode(node):
    variableList = []
    for field in ast3.walk(node): # Para cada ParentNode (node)
        if isinstance(field,ast3.Name):
            variableList.append(field.id)

    return variableList


def getAssignmentForExpressions(leftsideNumber,LatticeList):
    leftside = "T" + str(leftsideNumber)
    argsLatticeList = []
    argsLatticeList.append(ast3.Str(lineno=0, col_offset=0, s=leftside, kind=''))
    for seclevel in LatticeList:
        argsLatticeList.append(ast3.Str(lineno=0, col_offset=0, s=seclevel, kind=''))

    return ast3.Assign(
            lineno=0,
            col_offset=0,
            targets=[ast3.Name(lineno=0, col_offset=0, id=leftside, ctx=ast3.Store())],
            value=ast3.Call(
                lineno=1,
                col_offset=4,
                func=ast3.Name(lineno=1, col_offset=4, id='TypeVar', ctx=ast3.Load()),
                args=argsLatticeList,
                keywords=[],
            ),
            type_comment=None
            )




def getFunctionForExpressions(leftsideNumber): #2  leftside will be equal to the number of arguments
    expressionHandler = "expressionHandler" + str(leftsideNumber) # add2(), add3() for 2 and 3 arguments respectively
    argNumber = 0
    argumentList =[] #the nodes in args
    unionList = [] #list that will be used for the "return" value of the function for 2 arguments, it'll have []


    for i in range(0,leftsideNumber): #building the argument of the function.

        unionList.append(ast3.Name(lineno=0, col_offset=0, id='T' + str(i), ctx=ast3.Load()))
        argumentList.append(ast3.arg(
                            lineno=0,
                            col_offset=0,
                            arg='x' + str(i), #x0, x1 etc how many arguments we need
                            annotation=ast3.Subscript(
                                lineno=0,
                                col_offset=0,
                                value=ast3.Name(lineno=0, col_offset=0, id='Tuple', ctx=ast3.Load()),
                                slice=ast3.Index(
                                    value=ast3.ExtSlice([
                                       
                                        ast3.Index(value = ast3.Name(lineno=0, col_offset=0, id='A', ctx=ast3.Load())),
                                        ast3.Index(value = ast3.Name(lineno=0, col_offset=0, id='T' + str(i), ctx=ast3.Load()))
                                        ]),
                                        ctx=ast3.Load(),
                                    ),
                                ctx=ast3.Load()
                                ),
                                #ctx=ast3.Load(),
                                type_comment=None
                                )
                            
                            )

    return ast3.FunctionDef(
        lineno=0,
        col_offset=0,
        name=expressionHandler,
        args=ast3.arguments(
            args=argumentList,
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=[ast3.Return(lineno=0, col_offset=0, value=None)],
        decorator_list=[],
        returns=ast3.Subscript(
            lineno=1,
            col_offset=44,
            value=ast3.Name(lineno=0, col_offset=0, id='Tuple', ctx=ast3.Load()),
            slice=ast3.Index(
                value=ast3.ExtSlice([
                        ast3.Name(lineno=0, col_offset=0, id='A', ctx=ast3.Load()),
                        ast3.Subscript(
                            lineno=1,
                            col_offset=52,
                            value=ast3.Name(lineno=1, col_offset=52, id='Union', ctx=ast3.Load()),
                            slice=ast3.Index(
                                value=ast3.ExtSlice(unionList),
                                ctx=ast3.Load(),
                            ),
                            ctx=ast3.Load(),
                        ),
                    ],
                    ctx=ast3.Load(),
                ),
            ),
            ctx=ast3.Load(),
        ),
        type_comment=None
        )




def lineAfterANode(node):

    #prettyprinting(node)
    size = sizeOfNodeInLines(node)
    #print("Linha depois do no",node.lineno + size - 2 ) # -2 para sairem as linhas vazias
    return node.lineno + size - 2 



def checkIfLastBuiltIn(targetNode,tree): #Check if a certain node is the last builtIn function in a node

    flag = True
    bingo = 0

    for node in ast3.walk(tree):
        for childNode in ast3.iter_child_nodes(node):
            for field, value in ast3.iter_fields(childNode):
                if isinstance(value,list):
                    for i in range(len(value)):
                        if equalNodes(value[i], targetNode):
                            bingo = i
                        elif isinstance(value[i],ast3.Expr): 
                            if (hasattr(value[i].value.func,"id") and (value[i].value.func.id in buildInFunctions) and (i > bingo) and (bingo != 0)):
                                flag = False
            return flag





def checkHowManybuiltIns(node):

    builtinCounter = 0
    astBuiltInTypeTuple = (ast3.NameConstant,ast3.Str,ast3.Num)        
    for childNode in ast3.iter_child_nodes(node): #percorre childs de cada parent.
        #prettyprinting(childNode)
        if(isinstance (childNode,ast3.Expr)): 
            if hasattr(childNode.value.func,"id") and any(isinstance(childNode.value.args[0],x) for x in astBuiltInTypeTuple): # para o caso de se usar uma funçao com um builtIn type e nao variavel ex: print("fd")
                continue 
            elif((hasattr(childNode.value.func,"id") and (childNode.value.func.id in buildInFunctions) ) or ( hasattr(childNode.value.func,"attr") and (childNode.value.func.attr in buildInFunctions) ) ) : # Assim que encontra uma builtin function nos childnodes volta ao parent e encontra a posicao do child dentro do parent.
                #prettyprinting(childNode)
                for var in childNode.value.args:
                    builtinCounter+=1

    
    return builtinCounter



def transformAssignment(node,typeAnnotation):
    node.value=ast3.Name(lineno=0, col_offset=0, id=typeAnnotation, ctx=ast3.Load())
    node.type_comment=None
    return node


def transformAssignmentDictCases(node,variableBeingCast,indexDictType,valueDictType):
    node.value=ast3.Call(
                        lineno=0,
                        col_offset=0,
                        func=ast3.Name(lineno=0, col_offset=8, id='cast', ctx=ast3.Load()),
                        args=[
                            ast3.Subscript(
                                lineno=0,
                                col_offset=0,
                                value=ast3.Name(lineno=0, col_offset=0, id='Dict', ctx=ast3.Load()),
                                slice=ast3.Index(
                                    value=ast3.Tuple(
                                        lineno=0,
                                        col_offset=0,
                                        elts=[
                                            ast3.Name(lineno=0, col_offset=0, id=indexDictType, ctx=ast3.Load()),
                                            ast3.Name(lineno=0, col_offset=0, id=valueDictType, ctx=ast3.Load()),
                                        ],
                                        ctx=ast3.Load(),
                                    ),
                                ),
                                ctx=ast3.Load(),
                            ),
                            variableBeingCast
                            
                        ],
                        keywords=[],
                    )
    node.type_comment=None
    return node



def assignmentTransformer(tree):

    for node in ast3.walk(tree): # Para cada ParentNode (node) 
        for childNode in ast3.iter_child_nodes(node): #percorre childs de cada parent.
            if isinstance (childNode,ast3.Assign) and hasattr(childNode,"type_comment") :
                
                if childNode.type_comment != None:
                    if "Dict" in childNode.type_comment:

                        dictIndextype = re.search("Dict\[(.*),", childNode.type_comment) #Extrai da string que e o type comment o tipo do index.
                        dictValuetype = re.search(",(.*)\]", childNode.type_comment) # Analogo a instrucao anterior.
                  
                        transformAssignmentDictCases(childNode,childNode.targets[0],dictIndextype.group(1),dictValuetype.group(1))


                    else:
                        transformAssignment(childNode,childNode.type_comment)  


    return
                

def addAssignToPrintOptimized3(tree):
    
    numberId = 0 

    addedLineCounter = 0 #its purpose is to have information to track the line that generates the warning in the original, we also need this line.
    

    logDict = defaultdict(list) # Dicionario que vai ter {"linha ficheiro alterado": [linha original, conteudo da linha]}

    astBuiltInTypeTuple = (ast3.NameConstant,ast3.Str,ast3.Num) # Os 3 tipos de builtInTypes para o loop conseguir ignorar o caso print("ola") ou print(10)

    # Para as atribuicoes normais basta ver se quantas linhas foram adicionadas ate la e adicionar ao numero. 

    for node in ast3.walk(tree): # Para cada ParentNode (node) 
        for childNode in ast3.iter_child_nodes(node): #percorre childs de cada parent.
            if (isinstance (childNode,ast3.Expr)):  
                #tive de por o hasattr caso contrario o python dava exception se o object nao existisse e parava o programa.
                if( (hasattr(childNode.value.func,"id") and (childNode.value.func.id in buildInFunctions) ) or ( hasattr(childNode.value.func,"attr") and (childNode.value.func.attr in buildInFunctions) ) ) : # Assim que encontra uma builtin function nos childnodes volta ao parent e encontra a posicao do child dentro do parent.
                    for field, value in ast3.iter_fields(node): 
                        if isinstance(value,list):
                            for i in range(len(value)):
                                if isinstance(value[i], ast3.AST) and equalNodes(value[i], childNode):


                                    if hasattr(childNode.value.func,"id") and any(isinstance(childNode.value.args[0],x) for x in astBuiltInTypeTuple): # para o caso de se usar uma funçao com um builtIn type e nao variavel ex: print("fd")
                                        continue


                                    elif hasattr(childNode.value.func,"id") and ("attr" in childNode.value.func.id): #Se tivermos no caso de hasattr, delattr etc..

                                        addedLineCounter += 2
                                        warningLine = unparseTypedASt(childNode)
                                        warningLine = warningLine.strip('\n')

                                        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine])
                                
                                        numberId += 1
                                        value.insert(i + 1,getFirstStatement(numberId))
                                        value.insert(i + 2, getAssignStatementForAttrCases(numberId,childNode.value.args[0].id,childNode.value.args[1].id)) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
                                
                            
                                    elif hasattr(childNode.value.func,"id") and ( isinstance(childNode.value.args[0], ast3.Attribute) or isinstance(childNode.value.args[0], ast3.Subscript) ): #no caso de termos print("objecto"."argumento") 
 
                            
                                        addedLineCounter += 2
                                        warningLine = unparseTypedASt(childNode)
                                        warningLine = warningLine.strip('\n')

                                        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine])
                                
                                        numberId += 1
                                        value.insert(i + 1,getFirstStatement(numberId))
                                        value.insert(i + 2, getAssignStatementForSubscriptCases(numberId,childNode.value.args[0])) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
                                    else:

                                                                                    
                                        for childNodesArg in childNode.value.args: # se a funcao builtIn em questao tiver mais do que um argumento teremos que analiza-los a todos.
                                            addedLineCounter+=2

                                            warningLine = unparseTypedASt(childNode)
                                            warningLine = warningLine.strip('\n') 
                                            logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine])

                                            numberId += 1
                                            value.insert(i + 1,getFirstStatement(numberId))
                                            value.insert(i + 2, getAssignStatement(numberId,childNodesArg.id))
    print(logDict)
    return logDict



def classGenerator(classAddedLines,UserClasses,childNode,node):
    '''
        classAddedLines -> The lines added because of the creation of the initial classes.
        UserClasses -> The classes that the user has defined in the originalCode
        childNode -> The node that we are handling now.
        node -> the father node of childNode

        This function, for each user-made class, generates two more that correspond to a High Level object and to a Low level object. Its attributes all have 
        the corresponding type which is either Low/High, and its methods all return the corresponding type.

    '''

    UserClasses.append(childNode.name) # Cada vez que encontramos um objecto criado pelo programador guardamo-lo para mais tarde podemos saber quando o programador quer inicializar algum objeto.

    #Both these nodes will correspond to the equivalent High/Low ones. 
    newNodeHigh = copy.deepcopy(childNode)  # Need to to use copy because if i try to use an assignment it ll only make another object with the same reference so if i change the copies, it also changes the original
    newNodeLow = copy.deepcopy(childNode) 

    newNodeLow.name ="LCHI" + childNode.name
    newNodeHigh.name = "HCLI" + childNode.name

    for field, value in ast3.iter_fields(node):

        if isinstance(value,list):
            for i in range(len(value)):


                if isinstance(value[i], ast3.AST) and equalNodes(value[i], childNode): #CHANGETHISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsizeOfNodeInLinesClass
                #   if isinstance(value[i], ast3.AST) and equalNodesDifLines(value[i], childNode):

                    for Childfield, Childvalue in ast3.iter_fields(childNode): 
                        if isinstance(Childvalue,list):
                            for childIndex in range(len(Childvalue)):
                                
                                if hasattr(childNode.body[childIndex],"returns"): #Se for um metodo
                            
                                    newNodeHigh.body[childIndex].returns = ast3.Name(lineno=0, col_offset=0,id='HCLI', ctx=ast3.Load())
                                    newNodeLow.body[childIndex].returns  = ast3.Name(lineno=0, col_offset=0,id='LCHI', ctx=ast3.Load())

                                    continue #para nao meter alterar o type_comment no caso de ser um metodo

                                else: #para o caso de ser uma variavel
                                    newNodeHigh.body[childIndex].type_comment = "HCLI"
                                    newNodeLow.body[childIndex].type_comment = "LCHI"

                    print("Tamanho a adicionar por causa das classes:",sizeOfNodeInLinesClass(newNodeHigh))

                    classAddedLines+=sizeOfNodeInLinesClass(newNodeHigh)*2 + 2 # need to know how many lines the class is to add to counter
                    print("total de linhas adicionadas classes:",classAddedLines)
                    value.insert(i + 1,newNodeLow)
                    value.insert(i + 2,newNodeHigh) 
                    break


    return classAddedLines,UserClasses,node 




def cycleLineSync(Cycleflag,addedLineCounter,AddedLinesBecauseOFCycle,node,childNode):
    '''
        Cycleflag-> Checks if we are inside a cycle.
        addedLineCounter-> Total number of lines added.
        AddedLinesBecauseOFCycle-> Number of added lines of the assignments added because of the existance of a cycle.
        node-> the father node of childNode
        childNode-> The node that we are handling now.

        This function checks if we are inside a cycle, if we are it updates de addedLineCounter, it also checks if the built-in function is the last one in the body
        of the cycle.
    '''
    
    if(Cycleflag):
        for arg in AddedLinesBecauseOFCycle:
            addedLineCounter += arg
        Cycleflag = False

        # if(checkIfLastBuiltIn(childNode,node)):
        #     AddedLinesBecauseOFCycle.pop(0)

    return Cycleflag,AddedLinesBecauseOFCycle,addedLineCounter



def builtInAttrFunctionHandler(addedLineCounter,logDict,childNode,numberId,value,i):  #Se tivermos no caso de hasattr, delattr etc..
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        childNode-> The node that we are handling now.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes. 

        This function handles the insertion of nodes if we are in the presence of a built in function like hasatrr, delatrr etc.

    '''
    addedLineCounter += 2
    warningLine = unparseTypedASt(childNode)
    warningLine = warningLine.strip('\n')

    logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True])

    numberId += 1
    value.insert(i + 1,getFirstStatement(numberId))
    value.insert(i + 2, getAssignStatementForAttrCases(numberId,childNode.value.args[0].id,childNode.value.args[1].s)) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
    
    return addedLineCounter,logDict,numberId,value #Maybe need to also pass the new value since we added nodes.

def builtInAttrFunctionHandler2(addedLineCounter,logDict,childNode,numberId,value,i,trybeginline):  #Se tivermos no caso de hasattr, delattr etc..
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        childNode-> The node that we are handling now.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes. 

        This function handles the insertion of nodes if we are in the presence of a built in function like hasatrr, delatrr etc.

    '''
    addedLineCounter += 2
    warningLine = unparseTypedASt(childNode)
    warningLine = warningLine.strip('\n')
    
    if trybeginline != 0:
        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True,trybeginline])
    else:
        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True])

    numberId += 1
    value.insert(i + 1,getFirstStatement(numberId))
    value.insert(i + 2, getAssignStatementForAttrCases(numberId,childNode.value.args[0].id,childNode.value.args[1].s)) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
    
    return addedLineCounter,logDict,numberId,value #Maybe need to also pass the new value since we added nodes.



def builtInObjectCase(addedLineCounter,childNode,logDict,numberId,value,i): #no caso de termos print("objecto"."argumento")
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        childNode-> The node that we are handling now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes

        This function handles the insertion of the nodes if we are in the presence of a built in function in which the argument is a field of an object like print(Person.age) (Object Person, field age)

    '''
    addedLineCounter += 2
    warningLine = unparseTypedASt(childNode)
    warningLine = warningLine.strip('\n')

    logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True])

    numberId += 1
    value.insert(i + 1, getFirstStatement(numberId))
    value.insert(i + 2, getAssignStatementForSubscriptCases(numberId,childNode.value.args[0])) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
                                    
    return addedLineCounter,logDict,numberId,value #Maybe need to also pass the new value since we added nodes.

def builtInObjectCase2(addedLineCounter,childNode,logDict,numberId,value,i,trybeginline): #no caso de termos print("objecto"."argumento")
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        childNode-> The node that we are handling now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes

        This function handles the insertion of the nodes if we are in the presence of a built in function in which the argument is a field of an object like print(Person.age) (Object Person, field age)

    '''

    print(addedLineCounter)
    addedLineCounter += 2
    warningLine = unparseTypedASt(childNode)
    warningLine = warningLine.strip('\n')
    if trybeginline != 0:
        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True,trybeginline])
    else:
        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True])

    numberId += 1
    value.insert(i + 1, getFirstStatement(numberId))
    value.insert(i + 2, getAssignStatementForSubscriptCases(numberId,childNode.value.args[0])) # neste caso e necessario enviar o objecto e o argumento que vao ser acedidos.
                                    
    return addedLineCounter,logDict,numberId,value #Maybe need to also pass the new value since we added nodes.

def builtInMultipleArgs(addedLineCounter,childNode,logDict,numberId,value,i):
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        childNode-> The node that we are handling now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes

        This function handles the insertion of values in the presence of a built in function if the function has more than one argument. like print(a,b)
    '''

    for childNodesArg in childNode.value.args: # se a funcao builtIn em questao tiver mais do que um argumento teremos que analiza-los a todos.
        
        addedLineCounter+=2

        warningLine = unparseTypedASt(childNode)
        warningLine = warningLine.strip('\n')

        logDict[childNode.lineno + addedLineCounter].append([childNode.lineno,warningLine,True])
        print("Linhas suposta no ficheiro alterado", childNode.lineno + addedLineCounter)
        print("Linha no original",logDict[childNode.lineno + addedLineCounter])
        numberId += 1
        value.insert(i + 1,getFirstStatement(numberId))
        value.insert(i + 2, getAssignStatement(numberId,childNodesArg.id))
        i+=2

    return addedLineCounter,logDict,numberId,value

def builtInMultipleArgs2(addedLineCounter,childNode,logDict,numberId,value,i,trybeginline):
    '''
        addedLineCounter -> Counter to know how many lines were added to the original program until now.
        childNode-> The node that we are handling now.
        logDict-> Log of all the lines added aswell as the original line and the line after the changes.
        numberId-> The number(identifier) of the assignment that is being added. leftside20 = ... (The id here would be 20 and we would know that there were added 19 lines previously)
        value-> The structure in which we add the newly created nodes.
        i-> the position in which we are going to insert the new nodes

        This function handles the insertion of values in the presence of a built in function if the function has more than one argument. like print(a,b)
    '''

    for childNodesArg in childNode.value.args: # se a funcao builtIn em questao tiver mais do que um argumento teremos que analiza-los a todos.
        
        addedLineCounter+=2

        warningLine = unparseTypedASt(childNode)
        warningLine = warningLine.strip('\n')

        if trybeginline != 0:
            logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True,trybeginline])
        else:
            logDict[childNode.lineno + addedLineCounter].append([childNode.lineno ,warningLine,True])
        #logDict[childNode.lineno + addedLineCounter].append([childNode.lineno,warningLine,True])
        #print("Linhas suposta no ficheiro alterado", childNode.lineno + addedLineCounter)
        #print("Linha no original",logDict[childNode.lineno + addedLineCounter])
        numberId += 1
        value.insert(i + 1,getFirstStatement(numberId))
        value.insert(i + 2, getAssignStatement(numberId,childNodesArg.id))
        i+=2

    return addedLineCounter,logDict,numberId,value

def objectReplacement(UserClasses,node,childNode):  # Exemplo : Election() -> HCLIElection()
    '''
        UserClasses -> The classes that the user has defined in the originalCode
        node -> the father node of childNode
        childNode -> The node that we are handling now.

        This function's goal is to, in the presence of the initialization of a class and in the presence of a comment that signalizes that the 
        programmer wants to change all the elements of it(attributes and returns of methods) to a specific level, it swap the original class with the corresponding to the 
        level chosen.

         testClass =  Election() # type:HCLIElection  ->    testClass = HCLIElection() 
    '''

    if not isinstance(childNode.func,ast3.Attribute) and childNode.func.id in UserClasses and node.type_comment != None : # Ver se e de facto uma criacao de objecto pois pode ser uma chamada a uma funcao e ai nao nos interessa.
        childNode.func.id = node.type_comment + childNode.func.id #Assim que temos a certeza que o programador quer criar um objecto "dele" e tem um anotacao de tipo convertemos o nome do objecto inicializado para o ja criado anteriormente.
        node.type_comment = None # Exemplo : Election() -> HCLIElection()
    
    return node,childNode


def variableSortingInsideCycle(forChildnode,buildInFunctions,uselessVar,LineOfBuiltInsINCycle,temporaryList,allVars):
    '''
        forChildnode-> Node inside the for Cycle.
        buildInFunctions-> List with all the builtIn python functions.
        uselessVar-> Varariables in the condition of the cycle that we do not care.
        LineOfBuiltInsINCycle-> Line where the builtIn functions are inside the cycle. 
        temporaryList-> temporaryList with the variables and the respective lines. 

        This function sorts the variables inside the cycle and organizes them with the corresponding lines in a structure that is easier to work in.
    '''
    

    if forChildnode.id not in buildInFunctions and forChildnode.id != uselessVar[0] and forChildnode.lineno not in LineOfBuiltInsINCycle:
        for itemm in temporaryList: # To deal with replicates and builtinfuncts
            if itemm[0] == forChildnode.id and itemm[1] == forChildnode.lineno: #no caso em que sao iguais..
                Insert = False

        if Insert:
            temporaryList.append([forChildnode.id,forChildnode.lineno])
        

        allVars.append(forChildnode.id)
    

    return temporaryList,allVars



def expressionPreparation(LatticeList,args): #LatticeList = ['Top','Left','Right','Bot'] args will be the maximum number of arguments in a function in the whole program
    '''
    This function's purpose is to get ready for expression like "a + b". First step would be create as many Typevar variables as security levels.
    e.g. T0 = TypeVar('T0','Top','Left','Right','Bot')

    Second step would be to create the functions: as many functions as possible arguments in expressions
    
    e.g. def add2(x : Tuple[A,S], y : Tuple[A,T]) -> Tuple[A,Union[S,T]]:
            return
    e.g. def add3(x : Tuple[A,S], y : Tuple[A,T], z: Tuple[A,O]) -> Tuple[A,Union[S,T,O]]:
            return

    '''
    typeVarNodeList = [] # Cada node vai ser uma linha a inserir, talvez separar os typevars numa lista e as funcoes def noutra lista e retornar 2 listas?
    functionNodeList = []
    for i in range(0, args): #alterar isto porque e preciso criar tantos destes typevar como variaveis necessarias
        node = getAssignmentForExpressions(i,LatticeList)
        typeVarNodeList.append(node)


    for i in range(2,args + 1): #alterar isto porque e preciso criar tantos destes typevar como variaveis necessarias
        prettyprinting(node)
        node = getFunctionForExpressions(i)
        functionNodeList.append(node)


    return typeVarNodeList, functionNodeList


def classGenReplacement(UserClasses, typeVarNodeList, functionNodeList, classAddedLines, childNode, node):
    UserClasses.append(childNode.name) # Cada vez que encontramos um objecto criado pelo programador guardamo-lo para mais tarde podemos saber quando o programador quer inicializar algum objeto.

    wheretoinsertfunctionNodes = 0

    for field, value in ast3.iter_fields(node):

        if isinstance(value,list):
            for i in range(len(value)):

            
                if isinstance(value[i], ast3.AST) and equalNodes(value[i], childNode): #CHANGETHISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsizeOfNodeInLinesClass
                #   if isinstance(value[i], ast3.AST) and equalNodesDifLines(value[i], childNode):

                    for typevarNode in typeVarNodeList:

                        value.insert(i + 1,typevarNode)
                        wheretoinsertfunctionNodes += 1
                        classAddedLines+=1 # para cada uma linha de um assignment typevar adicionamos 1 linha.

                    for functionNode in functionNodeList:
                        value.insert(i + 1 + wheretoinsertfunctionNodes,functionNode)
                        classAddedLines+=2 # para cada funcao adicionamos 2 linhas por causa do return
                    
                    

                    outputTofile(unparseTypedASt(node),"outPut.py")
                    classAddedLines += 1 #adicionamos 1 aqui por causa das linha em branco que tambem sao adicionadas entre os typevar e as funcoes

                    return classAddedLines,UserClasses,node




def overload_Operation(expnode):

    operators = [ast3.Add, ast3.Sub , ast3.Mult , ast3.MatMult , ast3.Div  , ast3.Mod , ast3.Pow , ast3.LShift
                 ,ast3.RShift , ast3.BitOr , ast3.BitXor , ast3.BitAnd , ast3.FloorDiv ]
    # rewrite all additions to calls to our addition function
    class SumTransformer(ast3.NodeTransformer):
        def visit_BinOp(self, node):
            lhs = self.visit(node.left)
            rhs = self.visit(node.right)

            fl = False
            for operator in operators:
                if isinstance(node.op,operator):
                    fl = True
            if not fl:
                
                node.left = lhs
                node.right = rhs
                return node

            else:     
                name = ast3.Name('expressionHandler2', ast3.Load())
                args = [lhs, rhs]
                kwargs = []
                return ast3.Call(name, args, kwargs)

    expnode = SumTransformer().visit(expnode)
    expnode = ast3.fix_missing_locations(expnode)

    '''
    # inject the custom addition function into the sytnax tree
    code = 
def __custom_add(lhs, rhs):
    if isinstance(lhs, list) and isinstance(rhs, list):
        return [__custom_add(l, r) for l, r in zip(lhs, rhs)]

    if isinstance(lhs, dict) and isinstance(rhs, dict):
        keys = lhs.keys() | rhs.keys()
        return {key: __custom_add(lhs.get(key, 0), rhs.get(key, 0)) for key in keys}

    return lhs + rhs
    
    '''
    #add_func = ast3.parse(code).body[0]
    #expnode.body.insert(0, add_func)

    prettyprinting(expnode)
    unparseTypedASt(expnode)
    return expnode


def overload_try(tnode):

   
    # rewrite all additions to calls to our addition function
    class TryTransformer(ast3.NodeTransformer):
        def visit_Try(self, node):
            lhs = self.visit(node.left)
            rhs = self.visit(node.right)

            fl = False
            for operator in operators:
                if isinstance(node.op,operator):
                    fl = True
            if not fl:
                print(node.op)
                print("SUPPPPP")
                node.left = lhs
                node.right = rhs
                return node

            else:     
                name = ast3.Name('expressionHandler2', ast3.Load())
                args = [lhs, rhs]
                kwargs = []
                return ast3.Call(name, args, kwargs)

    expnode = TryTransformer().visit(tnode)
    expnode = ast3.fix_missing_locations(expnode)

    prettyprinting(tnode)
    unparseTypedASt(tnode)
    return tnode


# test23 = "(expression has type 'HCLI', target has type 'LCHI')"
# test24 = "(expression has type 'LCHI', target has type 'HCLI')"

def filteringUsefulWarnings(stre):
    return (bool(re.search(r'HCLI.*LCHI',stre)))



def addAssignBuiltIn(tree): # For each class it makes 2 of them, 1 low 1 high with every attribute and returning method of the corresponding level.
    

    originalCode = separateCodeThroughLines(tree)

    classAddedLines = 0

    numberId = 0 

    addedLineCounter = 0 #its purpose is to have information to track the line that generates the warning in the original, we also need this line.
    
    AddedLinesBecauseOFCycle = [] #O porque desta variavel e algo complicado, existe porque quando estamos a correr um ciclo:
    #Vamos adicionar ao codigo original a comparar o que esta na condicao de teste com o corpo, COmo tal actualizamos o contador de linhas adicionadas.
    #Mas depois de adicionadas essas linhas, o codigo vai ser corrido sobre o que esta dentro do corpo, para detectar leaks que nao tenham a ver com o ciclo em si.  por exemplo um simples print(HighVar)
    #Ou seja quando o script tiver dentro do ciclo, o contador de linhas ja vai estar mais a frente porque adicionou as linhas depois do ciclo, o que vai provocar uma discrepancia.
    builtInAddedLines = 0


    logDict = defaultdict(list) # Dicionario que vai ter {"linha ficheiro alterado": [linha original, conteudo da linha]}

    astBuiltInTypeTuple = (ast3.NameConstant,ast3.Str,ast3.Num) # Os 3 tipos de builtInTypes para o loop conseguir ignorar o caso print("ola") ou print(10)

    astCyclePossibilitiesTuple =(ast3.While,ast3.If,ast3.For) 

    classesIgnored = ("HCLI","HCHI","LCLI","LCHI") # When the program runs through the classes to add the Low and High equivalents it must ignore the classes regarding the levels themselves.
    UserClasses=[] # when there is an AST.call in the code, we need to know if it is a creation of the a user object so that if there is a type-comment we can convert it.
    Cycleflag = False  #Esta flag fica verdadeira quando nos encontramos dentro de um ciclo. 
    # Para as atribuicoes normais basta ver se quantas linhas foram adicionadas ate la e adicionar ao numero. 

    testBoolean = False
    typeVarNodeList, functionNodeList = [], []

    LatticeList = ["HCLI","HCHI","LCLI","LCHI"]
    args=2

    for node in ast3.walk(tree): # Para cada ParentNode (node)

        tryBeginLine = 0



        for childNode in ast3.iter_child_nodes(node): #percorre childs de cada parent.
            
            if isinstance (childNode,ast3.ClassDef) and childNode.name == classesIgnored[-1]:
                typeVarNodeList, functionNodeList = expressionPreparation(LatticeList,args)
                classAddedLines,UserClasses,node = classGenReplacement(UserClasses,typeVarNodeList,functionNodeList,classAddedLines,childNode,node)

            elif (isinstance(childNode, ast3.Assign)):
                overload_Operation(childNode)        

            elif (isinstance (childNode,ast3.Expr)): 

                #tive de por o hasattr caso contrario o python dava exception se o object nao existisse e parava o programa.
                if( (hasattr(childNode.value.func,"id") and (childNode.value.func.id in buildInFunctions) ) or ( hasattr(childNode.value.func,"attr") and (childNode.value.func.attr in buildInFunctions) ) ) : # Assim que encontra uma builtin function nos childnodes volta ao parent e encontra a posicao do child dentro do parent.
                    for field, value in ast3.iter_fields(node): 
                        if isinstance(value,list):
                            for i in range(len(value)):
                                if isinstance(value[i], ast3.AST) and equalNodes(value[i], childNode):

                                


                                    if hasattr(childNode.value.func,"id") and any(isinstance(childNode.value.args[0],x) for x in astBuiltInTypeTuple): # para o caso de se usar uma funçao com um builtIn type e nao variavel ex: print("fd")
                                        continue

                                    elif hasattr(childNode.value.func,"id") and ("attr" in childNode.value.func.id): #Se tivermos no caso de hasattr, delattr etc..

                                        addedLineCounter,logDict,numberId,value = builtInAttrFunctionHandler2(addedLineCounter,logDict,childNode,numberId,value,i,tryBeginLine) #Maybe add value here since we added 2 nodes and not sure if it updates this way.

                                        Cycleflag,AddedLinesBecauseOFCycle,addedLineCounter = cycleLineSync(Cycleflag,addedLineCounter,AddedLinesBecauseOFCycle,node,childNode)

                            
                                    elif hasattr(childNode.value.func,"id") and ( isinstance(childNode.value.args[0], ast3.Attribute) or isinstance(childNode.value.args[0], ast3.Subscript) ): #no caso de termos print("objecto"."argumento") 
                            
                                        addedLineCounter,logDict,numberId,value = builtInObjectCase2(addedLineCounter,childNode,logDict,numberId,value,i,tryBeginLine)
 
                                        Cycleflag,AddedLinesBecauseOFCycle,addedLineCounter = cycleLineSync(Cycleflag,addedLineCounter,AddedLinesBecauseOFCycle,node,childNode)


                                    else:
                                        addedLineCounter,logDict,numberId,value = builtInMultipleArgs2(addedLineCounter,childNode,logDict,numberId,value,i,tryBeginLine)
                                        Cycleflag,AddedLinesBecauseOFCycle,addedLineCounter = cycleLineSync(Cycleflag,addedLineCounter,AddedLinesBecauseOFCycle,node,childNode)
                 

            # elif (isinstance (childNode,ast3.Call)): # cria-se um objecto da mesma maneira que se chama uma funcao.
               
            #     # node,childNode = objectReplacement(UserClasses,node,childNode) #  Exemplo : Election() -> HCLIElection()
            #      # No if em baixo a primeira verificao exclui a chamada de metodos pois possuem sempre essa estrutura, ou seja childNode.func e sempre um ast3.Attribute

            #     if not isinstance(childNode.func,ast3.Attribute) and childNode.func.id in UserClasses and node.type_comment != None : # Ver se e de facto uma criacao de objecto pois pode ser uma chamada a uma funcao e ai nao nos interessa.
            #         childNode.func.id = node.type_comment + childNode.func.id #Assim que temos a certeza que o programador quer criar um objecto "dele" e tem um anotacao de tipo convertemos o nome do objecto inicializado para o ja criado anteriormente.
            #         node.type_comment = None
            #             # Exemplo : Election() -> HCLIElection()

    #print("LOGDICT",logDict)
    return logDict,originalCode,classAddedLines


def outputTofile(code,filename):
    '''
        code-> correspoding code.
        fileName-> correspoding file.

        This function outputs the code to a respective file.
    '''
    with open(filename, 'w') as f:
        for line in code.split("\n"):
            print(line,file = f)
            


def executeMypy(fileName):
    '''
        fileName-> The file that has the corresponding code.


        This function executes mypy on the correspoding file above.
        Equivalent to "mypy filename" in the console.

    '''
    return subprocess.call(['mypy', fileName])

def filterMypyOutput(fileName,logDict,originalCode,classAddedLines):
    '''
        fileName-> The file that has the corresponding code.
        logDict-> Log of all the lines added as well as the original line and the line after the changes.
        originalCode-> Original code without any lines added to it.

        This function removes the "useless" warning for our tool, makes the correspondance between the lines in the changed code with the original lines so
        that the programmer can have an accurate line of where the warning happened, and also turns the output into something more friendly and readable.   


    '''
    nativeTypes = ["indexable","Unsupported","exception","note","not defined","already defined","Exception","overload","not callable","Union[Any, LCHI]"," Method must have at least one argument","Unsupported left operand type","str", "int","is not indexable","has no attribute","expected","No library stub","Cannot find","Need type annotation","Trying to read", "Cannot determine", "Tuple[A, Any]","Invalid type","Cast target"]


    p = Popen(['mypy', fileName], stdin=PIPE, stdout=PIPE, stderr=PIPE) # subprocess.PIPE for the stderr, stdout, and/or std,in parameters and read from the pipes by using the communicate()

    output, err = p.communicate() # the output comes in bytes so it is necessary to convert it to string.


    unfilteredMypy = output.decode("utf-8").split("\n")
    filteredMypy = []

    for line in unfilteredMypy:
        #if not any(nativeType in line for nativeType in nativeTypes):
        if not any(nativeType in line for nativeType in nativeTypes) and filteringUsefulWarnings(line):
            filteredMypy.append(line)
    print(*filteredMypy,sep = "\n")

    


    for line in filteredMypy:

        flag = False
        dictEntryCounter=0  #This counter exists so we can count how many entries we went through and through that know how many lines were added before the line we are handling atm.

        try: # easy way to deal with the last line not having this format.(being an empty line)

            warningLineRegex = re.match("output.py:(.*): error", line) # Warningline from changedFile(MYPY)
            warningLine = int(warningLineRegex.group(1))
       
        except AttributeError:
            return
        
        
        print("\n")
        # if the warningline is equal to a key that means the warning came from a builtin function so we know the corresponding line is stored directly in the dict.
        #print("warningLine",warningLine)

        warningLine -= classAddedLines  # As soon as we get the warningLine we subtract the classAddedLines in the beginning.

        if not logDict: #Checking if the dictionary is empty, if it is the only possible added lines would be of the initial classes.
            print("There is an error in line: ",warningLine)
            print("The corresponding code is: ",originalCode[warningLine - 1].lstrip())
            continue


        if warningLine in logDict.keys():
            print("There is an error in line: ",logDict[warningLine][0][0])  # this corresponds to the line in the programmers file
            print("The corresponding code is: ", logDict[warningLine][0][1]) # the contents of that line.
            continue
        correctLine=0


        for key in sorted(logDict.keys()):

            a = 0
             # this counter's purpose is knowing how many dict entries we went through and it is important to do the line correspondance.
            #This is not enough since first we add 2 lines each time a builtin function appears, and we add 1 line for each line in a cycle.
            
            if len(logDict[key][0]) == 3 :
                a = 2 # 2 lines added if it was a builtinfunction
                
            else:
                a = 1 #1 line added if it was because of a cycle.

            dictEntryCounter+=a   
            if warningLine < key and flag == False:
                print("There is an error in line: ",warningLine)
                print("The corresponding code is: ",originalCode[warningLine - 1].lstrip())
                break
        

            elif warningLine > key and flag == False: # We know that we added some lines before the warning, how many we don't know.
                flag = True
                continue

            elif warningLine < key and flag == True: # We went through the dictionary, summed the entries but in order to know when to stop we went 1+ than we needed to  
                correctLine = warningLine - dictEntryCounter + a  # here we already passed the line so we have to decrease the last a (the last added lines)
                break


        if(correctLine!=0):        
            print("There is an error in line: ",correctLine)
            print("The corresponding code is: ",originalCode[correctLine - 1].lstrip())

        else:  # Here we already went through all the dict which means the line what has the error is after all of the added lines.
            print("There is an error in line: ",warningLine - dictEntryCounter)
            print("The corresponding code is: ",originalCode[warningLine - dictEntryCounter - 1].lstrip())

                

    return filteredMypy




def main(tree):

    confListFinal,intListFinal = inputIntoConfAndIntLists()

    tree = generateSecurityClasses2(tree,confListFinal,intListFinal)

    outputTofile(unparseTypedASt(tree),"outputBeforeChanges.py")

    unparseTypedASt(treeBeforeChanges)

    #prettyprinting(treeBeforeChanges)

    
    #prettyprinting(treeBeforeChanges1)

    unparseTypedASt(treeBeforeChanges)

    logDict1,originalC1,classAddedLines1 = addAssignBuiltIn(treeBeforeChanges)

    # prettyprinting(implicitTree)

    # unparseTypedASt(implicitTree)

    assignmentTransformer(treeBeforeChanges)
    
    outputTofile(unparseTypedASt(treeBeforeChanges),"output.py")

    filterMypyOutput("output.py",logDict1,originalC1,classAddedLines1)

main(ElectionServerTree)
