<h1 align = 'center'>Automate-CCC-Reports</h1>

<h2 align = 'center'>Automate and simplify the process of making reports of contests hosted by IIITV CodeChef Campus Chapter</h2>

### Inspiration 💡

The work of creating CodeChef contest reports after the contest is rather boring and repetitive. One needed to open the contest page and copy-paste the content to make a post of the contest report for Social Media. As this work could be automated using web scraping, I decided to make this script.

This repository can be used for making the contest report of any other contest (except Long Chllenges, Cook-Offs and Lunchtimes and other such contests for now) by changing the template as per requirement.

## How to Use? 😀

**Running this script requires Google Chrome to run Selenium. Make sure to [have Google Chrome installed](https://www.google.com/chrome/) before going to the next steps.**

- Clone the repository `$ git clone https://github.com/thepushkarp/Automate-CCC-Reports.git`
- Create a virtual environment ([click here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to learn about Virtual Environment)

```sh
virtualenv env
```

- Activate virtual environment (On macOS and Linux)

```sh
source env/bin/activate
```

- Activate virtual environment (On Windows)

```sh
.\env\Scripts\activate
```

- Install requirements

```sh
pip3 install -r requirements.txt
```

- Download the version of Chrome Driver as per your Google Chrome version from http://chromedriver.chromium.org/downloads

- Add the path of the downloaded Chrome Driver to line no. 31 of [scrape.py](scrape.py)

- Run the script using `python3 post_gen.py` and enter the contest link, and the contest type in the prompt that follows. The posts generated would be saved in the `posts` folder.

**NOTE: All the scripts are written in Python 3. So, make sure to use the appropriate version of pip and python.**

## Known Issues

- On **some** contest pages, there may be empty tags in-between strings (like empty \<strong> tags between '3' and 'hours' in contest duration) due to which insted of '3 hours', it may save only '3' in the duration variable.

## License

[MIT License](LICENSE)

---

<p align="center"> Made with ❤ by <a href="https://github.com/thepushkarp">Pushkar Patel</a></p>
