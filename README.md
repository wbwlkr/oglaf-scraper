# Oglaf Scraper

## Description

Oglaf Scraper is a script which download every strips of the [NSFW webcomic Oglaf.com](https://oglaf.com/).
With this script, you are able to either download the strips from the beginning, or you can also start again from the last strips you downloaded.
It uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) Python library.

## Installation

To download the script, type the code below in a shell :

```shell
git clone git@github.com:wbwlkr/oglaf-scraper.git
```

## Getting started

Oglaf Scraper will download every strips in a download folder dubbed "strips_oglaf".
This folder will appear in the same path where the script is.
Make sure to put the script where you want the strips folder to be.

Calling the script with option -h, as below, or without any option will display the help.

```shell
./oscrap.py -h
```

Here is all the options you can use :
```shell
-s : scrap the webcomic
-c : count the stories
-t : give the elapsed time
```

To start downloading the webcomic strips, use the -s option :

```shell
./oscrap.py -s
```

## Requirements

 * python3
 * beautifulsoup4==4.6.0
 * natsort==5.1.0
 * requests==2.9.1
 * wget==3.2

## Author

* **[WebWalker](https://github.com/wbwlkr)**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
