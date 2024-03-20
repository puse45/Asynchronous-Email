import os
import ssl
from typing import List

from decouple import config
import asyncio
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import logging
import fitz

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


logger = logging.getLogger("__name__")


def move_file_to_folder(directory: str, filename: str):
    """
    Move the file to a new directory
    :param directory: the directory to move the file to
    :param filename: the name of the file to move
    :return:
    """
    new_file_path = filename.split("/")[-1]
    os.rename(filename, os.path.join(directory, new_file_path))


async def send_email_async(
    send_from="piusmusyoki45@gmail.com",
    subject="Test Email",
    message="Welcome to email",
    server="sandbox.smtp.mailtrap.io",
    port=2525,
    username=config("MAIL_TRAP_USER_NAME"),
    password=config("MAIL_TRAP_PASSWORD"),
    use_tls=True,
    emails=[],
    files=[],
):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    email_status = []
    for email in emails:
        msg = MIMEMultipart()
        msg["From"] = send_from
        msg["To"] = email
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject

        msg.attach(MIMEText(message))

        for path in files:
            file_name_ = path.split("/")[-1]
            part = MIMEBase("application", "octet-stream")
            with open(path, "rb") as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", "attachment; filename={}".format(file_name_)
            )
            msg.attach(part)
        try:
            smtp = smtplib.SMTP(server, port)
            if use_tls:
                smtp.starttls()
            smtp.login(username, password)
            smtp.sendmail(send_from, email, msg.as_string())
            smtp.quit()
            email_status.append(True)
        except Exception as e:
            email_status.append(False)
            logger.error(f"Error sending: {e}")

    if all(email_status):
        move_file_to_folder("Sent", files[0])
    else:
        move_file_to_folder("Error", files[0])


async def extract_text_from_pdf(pdf_file) -> List:
    """
    Extract text from the pdf file
    :param pdf_file: pdf file to read from
    :return: text of the pdf file (emails)
    """
    with fitz.open(pdf_file) as pdf_document:
        text = ""
        for page_num in range(len(pdf_document)):
            text += pdf_document[page_num].get_text()
    return re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text
    )  # regex pattern to findall values with email pattern


async def get_files_in_directory(directory) -> List:
    """
    Get Files from a directory
    :param directory: Directory to get files from
    :return: List of file
    """
    files_list = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            files_list.append(file_path)
    return files_list


# Example usage:


async def main():
    """
    Main function of the app
    :return:
    """
    # dir = input("Enter")
    dir = "PDFs"
    get_files = await get_files_in_directory(dir)
    for pdf_file_path in get_files:
        emails = await extract_text_from_pdf(pdf_file_path)
        if emails:
            await send_email_async(emails=emails, files=[pdf_file_path])
            logger.info("Emails sent successfully!")
        else:
            logger.error("No emails found in the PDF.")


# Run the main function
asyncio.run(main())
