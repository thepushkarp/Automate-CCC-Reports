<h1 align = 'center'>Automate-CCC-Reports</h1>

<h2 align = 'center'>Automate and simplify the process of making reports of contests hosted by IIITV CodeChef Campus Chapter</h2>

### Inspiration

The work of creating CodeChef contest reports after the contest is rather boring and repetitive. One needed to open the contest page and copy-paste the content to make a post of the contest report for Social Media. As this work could be automated using web-scraping, I decided to make this script.

This repository can be used for making the contest report of any other contest (except Long Chllenges, Cook-Offs and Lunchtimes and other such contests) by changing the template as per requirement.

## How to Use? 😀

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
pip install -r requirements.txt
```

- Download the version of Chrome Driver as per your Chrome Version from http://chromedriver.chromium.org/downloads

- Put the Chrome Driver in the same folder as postGen.py

- Run and the script using `python postGen.py` and enter the contest link and the contest type in the prompt that follows.

### License

[MIT License](LICENSE)

---

<p align="center"> Made from scratch by <a href="https://github.com/thepushkarp">Pushkar Patel</a></p>
