import subprocess, json, sys, datetime, time 
import concurrent.futures


"""usage
- python mig.py json_file 
"""

def record_date_check(date, cast_start_time):
    y = int(date[:4])
    m = int(date[4:6])
    d = int(date[6:])
    h = int(cast_start_time[:2])
    min = int(cast_start_time[3:])

    nowtime = datetime.datetime.now()
    year = int(nowtime.year)
    month = int(nowtime.month)
    day = int(nowtime.day)
    #hour = int(nowtime.hour) + 9  # Raspberrypi time deviate 9 hours
    hour = int(nowtime.hour)  # refer: http://raspi-mc.blogspot.com/2017/01/linux-why-utc-900-cron-timedatectl.html
    minute = int(nowtime.minute)

    if y == year and m == month and d == day and h == hour and min == minute:
        return True

    return False

def mig(json_file):
    json_data = ""
    with open(json_file) as f:
        json_data = json.load(f)

        def thread1(i):
            while True: 
                if record_date_check(json_data[str(i)][2], json_data[str(i)][0]): 
                    break
                time.sleep(1)

            try: 
                subprocess.call("python record_and_generate_caption_file.py" + " " + str(i) + " " + json_data[str(i)][0] + " " + json_data[str(i)][1] + " " + json_data[str(i)][4], shell=True)
            except:
                pass

        def thread2(i):
            while True:
                if record_date_check(json_data[str(i+1)][2], json_data[str(i+1)][0]):
                    break
                time.sleep(1)
 
            try:
                subprocess.call("python record_and_generate_caption_file.py" + " " + str(i+1) + " " + json_data[str(i+1)][0] + " " + json_data[str(i+1)][1] + " " + json_data[str(i+1)][4], shell=True)
            except:
                pass
                
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # i correspond filename
            for i in xrange(500, 1000, 2):
                executor.submit(thread1, i)
                executor.submit(thread2, i)


            
if __name__ == "__main__":
    mig(sys.argv[1])
