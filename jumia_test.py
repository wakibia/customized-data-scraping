import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import os
from email.message import EmailMessage

# Define the URL to scrape
url = "https://www.jumia.co.ke/catalog/?q=oven+cooker"

sender = 'your email'
receiver = 'recipient email'
password = os.environ.get('PASSWORDKEY')


def send_email(product_name, product_price, product_discount, product_link):
    # Define email sender and receiver

    email_sender = sender
    email_receiver = receiver
    email_password = password

    subject = "Oven Cooker Deal Alert!"
    body = f"""
    Product: {product_name}\nPrice: {product_price}\nDiscount: {product_discount}%\nLink: {product_link} 
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server
        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, em.as_string())

        print("Email notification sent successfully!")

    except Exception as e:
        print(f"Email notification failed: {str(e)}")

    # finally:
    #     server.quit()


# Define your criteria (e.g., discount percentage threshold)
discount_threshold = 30

# Add SSL (layer of security)
context = ssl.create_default_context()

try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product details

    product_listings = soup.find_all("article", class_="prd _fb col c-prd")

    for product in product_listings:
        product_name = product.find("h3", class_="name").text.strip()
        product_price = product.find('div', class_='prc').text.strip()
        discout = product.find("div", class_="bdg _dsct _sm")
        product_discount = int(discout.text.strip().strip('%')) if discout is not None else 0
        product_link = "https://www.jumia.co.ke" + product.find("a", class_="core")["href"]

        # Check if the product meets the criteria
        if product_discount > discount_threshold:
            send_email(product_name, product_price, product_discount, product_link)

except Exception as e:
    print(f"An error occurred: {str(e)}")
