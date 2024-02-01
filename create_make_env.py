import os
import sys
import time
import subprocess
def create_make_file_content_legitly() -> str:
    gcc = "compile: run clean\n\t"
    gcc += "g++ main.cpp -o main.exe\n" if os.name == "nt" else "g++ main.cpp -o main\n"
    gcc+="run:\n\t"
    gcc+="cmd.exe /c %CD%\main.exe\n" if os.name == "nt" else "./main\n"
    gcc+="clean:\n\t"
    gcc+="cmd.exe /c del %CD%\main.exe" if os.name == "nt" else "rm main"
    return gcc
def create_cpp_template() -> str:
    data = ""
    data += "#include <iostream>\n"
    data += "// File Created automatically \n"
    data += "// Creation time: %s" % time.ctime() + "\n"
    data += "int main(int argc,char* argv[]) {\n"
    data += "\tstd::cout << \"Hello World \" << std::endl;\n"
    data += "\treturn 0;\n"
    data += "}"
    return data
def printfs(*args):
    '''when process handled succefully'''
    print("[ + ]",*args)
def printff(*args):
    '''when process handled failed'''
    print("[ - ]",*args)
def printfst(*args):
    '''printing status'''
    print("[ * ]",*args)
def create_make_file(content: str):
    with open("Makefile","w") as fd:
        fd.write(content)
def is_gcc_exists() -> tuple:
    command = "where" if os.name == "nt" else "which"
    result = ''
    try:
        result = subprocess.check_output([command,"g++"],stderr=subprocess.DEVNULL).decode("utf-8").strip()
    except: # G++ Doesnt exists
        return (False,result)
    return (True,result)
def create_env():
    path_seperator = ";" if os.name == "nt" else ":"
    shell_paths = os.path.expandvars("%PATH%" if os.name == "nt" else "$PATH")
    result,output = is_gcc_exists()
    if not result:
        printff("Cannot founded g++ Please install Mingw or Define specified path and try again :/")
        sys.exit(1) # exit failure
    printfs("Founded at",output)
    if os.path.exists("Makefile") and input("Founded already existing makefile do you wanna overwrite this ?(Y/N): ").lower() != "y":
        printff("Aborted!")
        sys.exit(1)
    printfst("Creating Makefile")
    if not os.path.exists("main.cpp"):
        with open("main.cpp","w") as cpptemplatefd:
            cpptemplatefd.write(create_cpp_template())
    try:
        with open("Makefile","w") as mkfilefd:
            mkfilefd.write(create_make_file_content_legitly())
    except Exception as exception:
        printfs("Cannot create Makefile because: ",str(exception))
        sys.exit(1) #exit failure
if __name__ == "__main__":
    create_env()