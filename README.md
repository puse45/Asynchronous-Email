# Asynchronous Email Sender


#### Description

You are given a folder containing PDF files. Your task is to develop a Python program that asynchronously processes these PDF files, extracts email addresses from their content, and sends emails to the identified email addresses with the PDF files attached. After sending each email, move the corresponding PDF file to a "Sent" folder. If any errors occur during the email sending process, move the PDF file to an "Error" folder for further investigation.


#### Requirements:

Use Python's asyncio and aiohttp libraries for asynchronous operations and HTTP requests.
Implement functions for extracting email addresses from PDF files and sending emails asynchronously.
Ensure proper error handling for email sending failures.
Create directories for "PDFs," "Sent," and "Error" folders, if they don't already exist.
Use environment[requirements.txt](requirements.txt) variables for configuration, including SMTP server details, email credentials, and folder paths.
#### Evaluation Criteria: 

You will be evaluated based on the following criteria:
* Correctness: Does the program extract email addresses accurately and send emails without errors?
* Asynchronous Implementation: Are asynchronous operations used effectively to process PDF files and send emails concurrently?
* Error Handling: Does the program handle email sending failures gracefully and move PDF files to the appropriate folders?
* Code Quality: Is the code well-structured, readable, and maintainable?
* Documentation: Is there clear documentation explaining how to run the program and interact with its functionalities?

#### Requirements

* Python 3.8+

#### Run app
```shell
python main.py
```
