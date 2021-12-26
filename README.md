RSS feeds reader README file.

useful information is available at docs/
    docs/task.md contains the requirements to this project
    docs/rss_sources.md  contains links to RSS feeds, which are used at time of developing the project

logs save at the user's home directory at directory rss_log/

files with parsed information save in .json format at the user's home directory at directory rss_data/

Installation

files for installation placed id directory dist/
better to install package at virtual environment, but anybody free to choose
create any directory and come to the directory
run 'python -m venv name_of_your_venv' to create virtual environment
run 'name_of_your_venv/Scripts/activate' to activate the virtual environment
run 'pip install correct_path_to/package_name' to install the package at virtual environment
run 'python -m rss_reader', 'rss_reader', 'rss-reader' to execute
use 'rss-reader --help' to get run options

https://news.yahoo.com/rss/                     ok
https://news.google.com/rss/                    ok, without media:content
https://www.rt.com/rss/news/                    ok
https://www.theguardian.com/world/rss           ok
https://habr.com/ru/rss/hubs/all/               ok, without media:content. Works just when epam VPN disconnected.
https://rss.dw.com/xml/rss-ru-all               ok
https://rss.dw.com/xml/rss-ru-discover-ger      ok
https://www.liga.net/news/all/rss.xml           ok
https://www.finam.ru/analysis/conews/rsspoint   ok
https://www.svaboda.org/rss/                    ok

climage==0.1.3
simple-imshow==1.0.post1
scipy==1.7.3
numpy==1.21.4
pre-commit==2.15.0
black==21.11b1
flake8==3.9.2
