# IFlow-Tool


A static analysis tool that is able to prevent illegal information flows in Python. It allows for a high degree of flexibility since the programmer can define multiple 
security levels regarding confidentiality and integrity, while still remaining easy to use since it resorts to basic type annotations to the code.

As the tool is executing the target code, two python files will be generated.

1) The first with the name "outputBeforeChanges.py", is vital and is the equivalent to the original code of the programmer. 
The output of the tool will be regarding this file in specific.

2) The second generated file, named "output.py" is only being created for demonstration purposes and will consist of the code after the changes done to its original counterpart.
