# How to use.
1. Create a tv programs list json file (e.g. program.json).
2. Run a mig.py that used a created json file.



# Examples.
- Run

$ python mig.py json_file 

- Kill a process
$ ps u
$ kill -KILL PID

- How to use the screen command
  - Create a session
$ screen
  - Show sessions
$ screen -ls
  - Retouch a session
$ screen -r 
  - Detouch a session.
Ctrl-a Ctrl-d
- Stream
  - TS to text
    $ python stream_and_generate_caption_file.py file_name start_time end_time ch
  - Image to text
    $ python watching.py
