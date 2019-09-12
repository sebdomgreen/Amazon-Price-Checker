# Amazon Price Checker - A Drop Shipper's ToolKit
An automatic Amazon price tracker which uses html parsing (instead of API) to track a product's price.

- Alert via email (and console) if a product price passes bounds
- Alert via email (and console) if a product becomes out of stock
- Alert via email (and console) if a product becomes no longer prime

## Getting Started
### Installing
- Make sure Python3 and Pip3 are installed
- Run `sudo pip3 install -r requirements.txt` to install all needed packages
- Run `sudo pip3 install requests_html` to install the `requests_html` package

## Usage
### Console Arguments
The script uses Gmail's SMTP server: requiring a valid Gmail address and password to send the emails *
- `--email/-e ...` to set email address to send emails from **
- `--password/-p ...` to set password for the above email address **
- `--time/-t ...` to set wait time, in minutes, between price checks (Default 60 minutes). Minimum of 15 minutes recommended to avoid Amazon blocking requests
- `--recipient/-r ...` to set recipient email address to receive alerts (Default is email set above)

*Note: Google blocks usage of real password requests and requires an "App Password" to be made. Create a "Mail" password here: https://myaccount.google.com/apppasswords
**required.

Example:
```
python3 PriceCheck.py -e sendaccount@gmail.com -p sendaccountpassword
```

### Adding Products
Products, to be price checked, can be added by adding lines to the `items.txt` file. Products take the following form:
```
['Product Name','https://amazon.co.uk/AmazonProductHere','Lower Bound','Upper Bound']
```
- You can add a `Lower Bound` and an `Upper Bound` for each product; you will receive an email alert if the Amazon product price passes or equals one of these bounds