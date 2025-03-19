from os.path import exists
import pickle


def diff(dif):
    # key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
    # cs = Fernet(key)

    # def readfile(cs: object, filename: str):
    def readfile(filename: str):
        if not exists(f"data\\{filename}.txt"):
            a = open(f"data\\{filename}.txt", "w")
            if filename == "hp":
                content = "100"
            elif filename == "playerinfo":
                content = "Player|.20"
            elif filename == "password":
                content = ""
            elif filename == "cu":
                content = "1"
            elif filename == "cuosf":
                content = "1"
            elif filename == "langchoose":
                content = "tc"
            elif filename == "darkmodecolor":
                content = "#000000"
            elif filename == "difficult":
                content = "1"
            else:
                content = "0"
            # a.write(cs.encrypt(content.encode()).decode())
            pickle.dump(content, a)
            a.close()
        with open(f"data\\{filename}.txt", "rb") as ffile:
            # result = ffile.read()
            result = pickle.load(ffile)
        # return cs.decrypt(result.encode()).decode()
        return result

    # langchoose = readfile(cs, "langchoose")
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
