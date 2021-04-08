"""
BrainFuck Compiler
author: @FrozenLemonTee
version: 1.0
"""

import ctypes
import argparse
from typing import List, NoReturn, Text

colour = {"red": 0x0c, "blue": 0x0b}
errors_code = {"notBfFile": 1, "canNotOpen": 2, "bracketsMismatch": 3, "ASCIIConvertingError": 4, "OutOfBound": 5}


class ArgumentParserError(Exception):
    pass


class myArgumentParser(argparse.ArgumentParser):
    def error(self, message: Text) -> NoReturn:
        raise ArgumentParserError(message)


def cmdParse() -> str:
    try:
        des = "BrainFuck Compiler PyBrainFuck@1.0  By @FrozenLemonTee"
        parser = myArgumentParser(description=des)
        parser.add_argument("file_name", help="the path of brainFuck file(.bf)")
        return parser.parse_args().file_name
    except ArgumentParserError:
        printCmd("[PyBrainFuck@1.0] usage:python PyBrainFuck.py file_name", color=colour["blue"])
        printError(error_info="Wrong usage of the command")


def openFile(pth: str) -> List[str]:
    split = pth.split("\\")
    file_name = split[-1]
    if file_name.split(".")[-1] != "bf":
        printError(error_info="'" + pth + "' is not a .bf file", error_code=errors_code["notBfFile"])
    try:
        fp = open(pth)
        text = fp.read().split("\n")
        fp.close()
        return text
    except OSError:
        printError(error_info="Can not open '" + pth + "'", error_code=errors_code["canNotOpen"])


def printCmd(*info: str, color: int = 0x07, sep: str = ' ', end: str = '\n') -> NoReturn:
    ctypes.WinDLL("Kernel32.dll").SetConsoleTextAttribute(ctypes.WinDLL("Kernel32.dll").GetStdHandle(-11), color)
    print(*info, sep=sep, end=end, flush=True)
    ctypes.WinDLL("Kernel32.dll").SetConsoleTextAttribute(ctypes.WinDLL("Kernel32.dll").GetStdHandle(-11), 0x07)


def inputsCmd() -> str:
    printCmd("[PyBrainFuck@1.0] input>>>", color=colour["blue"], end="")
    return input()


def outputStream(opt: str, add: int, src: List[str], i: int, j: int) -> str:
    try:
        res = opt + chr(add)
        return res
    except ValueError:
        printError(i=i, j=j, src=src, error_info="Error in converting ASCII code",
                   error_code=errors_code["ASCIIConvertingError"])


def outputsCmd(opt: str) -> str:
    printCmd("[PyBrainFuck@1.0] output>>>", color=colour["blue"], end="")
    print(opt)
    return ""


def printError(i: int = 0, j: int = 0, src=None, error_info: str = "", error_code: int = -1) -> NoReturn:
    if src is None:
        src = [""]
    printCmd("[PyBrainFuck@1.0] error:", color=colour["red"], end="")
    printCmd(error_info, color=colour["red"], end="")
    if error_code >= 3:
        if error_code > 3:
            printCmd(" while in Runtime", color=colour["red"], end="")
        print()
        printCmd("At line " + str(i + 1) + ", char " + str(j + 1) + ":", color=colour["red"])
        left = j - 6 if j >= 6 else 0
        right = j + 7 if j <= len(src[i]) - 7 else len(src[i])
        printCmd(src[i][left: right], color=colour["red"])
        fill = ""
        for k in range(left, right):
            if k == j:
                fill += "^"
            else:
                fill += "~"
        printCmd(fill, color=colour["red"])
    exit(error_code)


def check(src: List[str]) -> NoReturn:
    st = []
    for i in range(0, len(src)):
        for j in range(0, len(src[i])):
            if src[i][j] == "[":
                st.append([i, j])
                continue
            if src[i][j] == "]":
                if not st:
                    printError(i=i, j=j, error_info="Square brackets are mismatch",
                               error_code=errors_code["bracketsMismatch"], src=src)
                else:
                    st.pop(-1)
    if st:
        printError(i=st[-1][0], j=st[-1][1], error_info="Square brackets are mismatch",
                   error_code=errors_code["bracketsMismatch"],
                   src=src)


def evaluate(src: List[str]) -> NoReturn:
    check(src)
    opt = ""
    arr = [0] * 300000
    ptr = 0
    tmp = []
    i = 0
    while i < len(src):
        j = 0
        while j < len(src[i]):
            if src[i][j] == "[":
                tmp.append([i, j])
            elif src[i][j] == "]":
                if arr[ptr] != 0:
                    i = tmp[-1][0]
                    j = tmp[-1][1]
                else:
                    tmp.pop(-1)
            elif src[i][j] == "+":
                arr[ptr] += 1
            elif src[i][j] == "-":
                arr[ptr] -= 1
            elif src[i][j] == "<":
                ptr -= 1
            elif src[i][j] == ">":
                ptr += 1
            elif src[i][j] == ".":
                if ptr < 0 or ptr > 299999:
                    printError(i=i, j=j, error_info="Pointer out of bound", error_code=errors_code["OutOfBound"],
                               src=src)
                opt = outputStream(opt=opt, i=i, j=j, src=src, add=arr[ptr])
            elif src[i][j] == ",":
                if ptr < 0 or ptr > 299999:
                    printError(i=i, j=j, error_info="Pointer out of bound", error_code=errors_code["OutOfBound"],
                               src=src)
                if opt:
                    opt = outputsCmd(opt)
                ipt = ""
                while not ipt:
                    ipt = inputsCmd()
                arr[ptr] = ord(ipt[0])
            elif src[i][j] == "#":
                j = len(src[i])
            j += 1
        i += 1
    if opt:
        outputsCmd(opt)


def main() -> NoReturn:
    try:
        evaluate(openFile(cmdParse()))
    except KeyboardInterrupt:
        printError(error_info="Interrupted by Ctrl+C")


if __name__ == "__main__":
    main()
