This app will log in to my work website and download my inputed date pay stub.
Then using pandas it will use the downloaded excel file and parse the information requested.
After parsing the selected info, it will be emailed to the selected address.
When the app is ran from the command line there will be 3 questions to be answered.
    
    1. enter username
    2. enter password
    3. pay date to be parsed and emailed, use a date format of ##/##/####

This is the first initial working version for myself. I will be modifying the code in the future to make the app more versatile for anyone to use.
All usernames and password are kept in my personal environment so that they are not made public. Using linux, I added an export to the end my .bashrc file ie.
    
    export EMAIL_USERNAME="your email goes here"

Then do the same for the other sensitive information variables.
This script is written in Python 3.7, any version before 3.6, you will need to replace the f string format with another form.