from os.path import exists, join
import pickle
from pathlib import Path


def diff(dif):
    def readfile(filename: str):
        data_path = join(Path(__file__).parent.parent, "data")
        file_path = join(data_path, f"{filename}.txt")

        if not exists(file_path):
            a = open(file_path, "w")
            pickle.dump("tc", a)
            a.close()
            return "tc"

        with open(file_path, "rb") as ffile:
            result = pickle.load(ffile)

        return result

    langchoose = readfile("langchoose")
    if langchoose == "sc":
        import lang.sc as lang
    else:
        import lang.tc as lang
    if dif == 0:
        return lang.peaceful
    if dif == 1:
        return lang.easy
    if dif == 2:
        return lang.normal
    else:
        return lang.diff
