from prefect_email import EmailServerCredentials

def create_email_block():
    credentials = EmailServerCredentials(
        username="example@gmail.com", ## must be your real email password
        password="abcdefgh@!",  # must be an app password generated from google settings
    )
    credentials.save("email-block")

if __name__ == "__main__":
    create_email_block()