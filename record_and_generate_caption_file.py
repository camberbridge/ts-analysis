import sys, subprocess, json

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

    # Use a Shell Flag when execute a subprocess (String Type)
    subprocess.call("recdvb --25 --strip " + ch + " " + str(to_time - from_time) + " " + file_name + ".m2ts", shell=True)

    try:
        subprocess.call("assdumper " + file_name + ".m2ts" + " > " + file_name + ".ass", shell=True)
        subprocess.call("python text_preprocessing.py " + file_name + ".ass", shell=True)
    except:
        pass

    try:
        subprocess.call("rm " + file_name + ".m2ts", shell=True)
        subprocess.call("rm " + file_name + ".ass", shell=True)
    except:
        pass

if __name__ == "__main__":
    main_record(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
