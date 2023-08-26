# Amazon Product Project

This Amazon Product project allows users to input the item that the users want given specific constraints, which then the five products, based on reasonably well priced items and good reviews, will then be outputted to the user.

## Installation

First, check to see if Selenium is installed on by using [pip](https://pip.pypa.io/en/stable/).

```bash
pip3 --version
```

If not installed, install pip (for Mac)

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Then, install Selenium

```bash
pip3 install selenium
```

## Usage

After running the file, the user will be able to input their
- Wanted product
- Minimum star rating (Reviews)
- Maximum budget (Price) 

allowing the program to choose five products that is at the given star rating or higher and below the maximum budget. The five products are chosen based on the relative price to all of the products, and the given products will be the most reasonably priced items, so it is not too expensive or inexpensive.

## Authors and Acknowledgments 

This project was completed Winter 2022 by Minsuk "Sean" Hue and Sangsoo "Andy" Lim.
