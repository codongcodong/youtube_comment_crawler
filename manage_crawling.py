import os
import time

path = "/home/netlab/youtube_comment_crawler/"
os.chdir(path)

pid = os.fork()

if pid == 0:
    os.system('python main.py')
    exit(0)

else:
    time.sleep(5.0)
    os.system('ls -l *.txt > state1')

    while True:
        time.sleep(10800)
        os.system('ls -l *.txt > state2')
        res = os.popen('diff state1 state2').read()

        if not res:
            print('#############################')
            print("[ERROR] No changes in result")
            print('#############################')
            os.system('rm state*')
        
            now = time.localtime() 
            now_str = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            os.system('mkdir result_'+now_str)
            os.system('mv *.txt result_'+now_str)

            pid = os.fork()

            if pid == 0: 
                os.system('python main.py')
                exit(0)
            else:
                time.sleep(5.0)
                os.system('ls -l *.txt > state1')

        else:
            os.system('mv state2 state1')
