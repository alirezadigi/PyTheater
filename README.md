# PyTheater :movie_camera:
A Project for building Media Center

Steps for using PyTheater:
```
git clone https://github.com/alirezadigi/PyTheater.git
cd PyTheater
pip install -r requirements.txt
```
**EDIT THE static.txt file (in same directory)!
Put videos path on it!
Videos must be under ***'videos'*** path.**

**for example, put videos in */mnt/static/videos/* and add  */mnt/static/* to static.txt**

Then Run the below command to run PyTheater:

### in linux
```
python3 db_gen.py
python3 PyTheater.py 
```
### in windows
```
python db_gen.py
python PyTheater.py
```

Then open http://127.0.0.1:9995/videos in your browser!
### Dont forget to refresh videos by clicking Refresh button!
### Remember These Tips:
- Videos must be near eachother (not in folders) and right below the videos folder
- videos covers will be generated with the same names , so dont delete them
- only english names are accepted
