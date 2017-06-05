Software documentation

The whole system has two sub-systems, the folder “dcrwler” contains the distributed list crawler which prepares data in the Redis database and the folder “projectv2” contains the sub-system that used by users. 

The running sequence is to run the “DistributedCrawler” project first to collect and store data in Redis database, then run the “PeopleSearching” project and visit the website.



Python project name: “DistributedCrawler”
Folder name: “dcrawler”
Develop tool:  Pycharm 2016.3.3
Building environment: Python3.6.0a2
Operation system: macOS Sierra Version 10.12.4 
Required software: Redis-3.2.8
External libraries: bs4, Scrapy, requests, scrapy-redis
Running process: 
1.    Install Redis if necessary, the name of the install file is “redis-3.2.9.tar.gz” that attached in the folder.
2.    Install the external libraries.
3.    Open the terminal and go to the folder of redis: ~/redis-3.2.8/src/
4.    Run command: “./redis-server” to run the redis server.
5.    Redis address: localhost; Port: 6379
6.    Open one or more terminal (multi instances) and go to the project folder ~/dcrawler/crawler (the same location with the file “scrapy.cfg”).
7.    Run same command in all instances: “scrapy crawl wikipedia”. 
8.    Wait for finish (would be a long time) or using “control+c” to abort.
9.    Now there should be data in the database.



Python project name: “PeopleSearching”
Folder name: “projectv2”
Develop tool: Pycharm 2016.3.3
Building environment: Python3.6.0a2
Operation system: macOS Sierra Version 10.12.4
Required software: Redis-3.2.8
External libraries: bs4, requests, Django, xlwt, redis
Running process: 
1.    Install the external libraries.
2.    The best way to run Django project: using the Pycharm run button.
      Another way to run Django project (complicate): First run the virtualenv by command: “virtualenv python_env” and “source ./python_env/bin/activate”
      If the virtualenv yield a mistake, try the command: “sudo lsof -t -i tcp:8000 | xargs kill -9” to kill the process. 
      Then go to the project folder ”~/projectv2/” run the command: “python manage.py runserver” 
3.    Open the browser and type the address: “http://127.0.0.1:8000/search”
4.    Enter the person’s name in the input box one, the name must be the full name and not allowed spelling mistake. The result is supposed shown in the user table on the page.
5.    Enter the list name in the input box two, the list name must in the form as “list of …” and the string must in lowercase, also not allowed spelling mistake. The resulting file will be downloaded. If there are many people on the list, it needs to wait for some time.



