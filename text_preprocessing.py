# encoding: utf-8
import sys

"""usage
- python text_preprocessing.py file_name
"""

def text_preprocessing(file_name):
    counter = 0
    with open(file_name, "r") as f:
        for l in f: 
            counter += 1
            if counter > 7: 
                l = l[50:].replace("\n", "").replace("≫", "").replace("「", "").replace("」", "").replace(".", "").replace("、", "").replace("。", "").replace("　", "").replace("？", "").replace("！", "").replace("♬", "").replace("〜", "").replace(" ", "").replace("＞", "").replace("＜", "").replace("…", "")

                try: 
                    l = l[:l.index("\\n")] + "\n" + l[l.index("\\n") + 2:]
                except:
                    pass

                bracket_start_pivot = 0
                bracket_end_pivot = 0

                if l.find("（") > -1 and l.find("）") > -1:
                    bracket_start_pivot = l.find("（")
                    bracket_end_pivot = l.find("）")

                    if l.find("（") == 0:
                        l = l[bracket_end_pivot + 3:]
                    else:
                        l = l[:bracket_start_pivot] + l[bracket_end_pivot + 3:]

                if len(l) > 2:
                    with open(file_name[:-4] + ".txt", "a") as ff:
                        ff.write(l + "\n")

if __name__ == "__main__":
    text_preprocessing(sys.argv[1])
