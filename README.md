#RSS feeds reader README file.

>useful information is available at docs/
    docs/task.md contains the requirements to this project
    docs/rss_sources.md  contains links to RSS feeds, which are used at time of developing the project

###logs save at the user's home directory at directory rss_log/

###files with parsed information save in .json format at the user's home directory at directory rss_data/

>Installation

####files for installation placed id directory dist/
####better to install package at virtual environment, but anybody free to choose
####create any directory and come to the directory
####run 'python -m venv name_of_your_venv' to create virtual environment
####run 'name_of_your_venv/Scripts/activate' to activate the virtual environment
####run 'pip install correct_path_to/package_name' to install the package at virtual environment
####run 'python -m rss_reader', 'rss_reader', 'rss-reader' to execute
####use 'rss-reader --help' to get run options

>example usage for search in cashed news for date 2021 12 26 and "all" sources

###'python -m rss_reader all --verbose --to-html C:\Users\Siarhei_Papina\rss_data\file11.html --date 20211226 --limit 5'

>and for one source

###python -m rss_reader https://news.yahoo.com/rss/ --verbose --to-html C:\Users\Siarhei_Papina\rss_data\file10.html --date 20211226 --limit 3

##links, used at time of developing this module
>https://news.yahoo.com/rss/                     
https://news.google.com/rss/                    
https://www.rt.com/rss/news/                   
https://www.theguardian.com/world/rss           
https://habr.com/ru/rss/hubs/all/               
https://rss.dw.com/xml/rss-ru-all               
https://rss.dw.com/xml/rss-ru-discover-ger     
https://www.liga.net/news/all/rss.xml           
https://www.finam.ru/analysis/conews/rsspoint   
https://www.svaboda.org/rss/                   


