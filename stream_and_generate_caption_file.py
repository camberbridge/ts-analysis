# encoding: utf-8

import sys, subprocess, json
import concurrent.futures, threading
import time

"""usage
- python record_and_generate_caption_file.py file_name, from_time, to_time, ch
-- from_time, to_time are 5 characters. e.g. 12:23
"""

def main_record(file_name, from_time, to_time, ch):
    # from_time, to_time are converted to sec from hour
    to_h = int(to_time[:2]) * 3600
    to_m = int(to_time[3:]) * 60
    from_h = int(from_time[:2]) * 3600
    from_m = int(from_time[3:]) * 60
    to_time =  to_h + to_m
    from_time = from_h + from_m
    print "from: " + str(from_time) + ", " + "to: " + str(to_time) + ", diff: " + str(to_time - from_time) 

    def record():
        subprocess.call("recdvb --b25 --strip " + ch + " " + str(to_time - from_time) + " " + file_name + ".m2ts", shell=True)
    
    def printer():
        try:
            text_processing = False

            # Dump a caption.
            subprocess.call("assdumper " + file_name + ".m2ts" + " > " + file_name + ".ass", shell=True)

            # Write a caption.
            with open(file_name + ".ass", "r") as f:
                line = f.readlines()[-1]

                if line.find("Dialogue:") == 0:
                    with open(file_name + "_single.ass", "a+") as ff:
                        try:
                            if ff.readlines()[-1] != line:
                                ff.write(line)
                                print(line)
                                text_processing = True
                        except:
                            ff.write(line)
                            print(line)
                            text_processing = True

            # Text reprocessing.
            if text_processing:
                with open(file_name + "_single.ass", "r") as f:
                    l = f.readlines()[-1]
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
                        with open(file_name + ".txt", "a") as ff:
                            ff.write(l + "\n")

            text_processing = False

        except:
            pass

        # Execute a process per 0.5 sec.
        threading.Timer(0.5, dump).start()

    def dump():
        threading.Thread(target=printer).start()

    def crop_image():
        start_time = time.time()
        i = 0
        while i < to_time - from_time:
            time.sleep(3)
            i = round(time.time() - start_time)
            subprocess.call("ffmpeg -ss " + str(i) + " -t 1 -r 1 -i hoge.m2ts -f image2 " + str(i) +".jpg", shell=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(record)
        executor.submit(dump)
        executor.submit(crop_image)


if __name__ == "__main__":
    main_record(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
