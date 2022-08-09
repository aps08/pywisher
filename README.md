# pywisher

pywisher is a python scripts, which uses gmail to read records and send birthday wishes to all your friends, it's scheduled to run every day at **```00:01 IST```** using github actions.


## Made with
![code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)
![Github Action](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## How to use

For using this script, you require:
   - Github Account.
   - Gmail Account.
   - Birthday record (**in csv, as given in below image**).

If you have the requirements completed, follow the steps below:
  - ### Gmail setup
      - Go to this [link](https://myaccount.google.com/).
      - On the left hand side, click on ***security***.
      - Under Signing in to Google click ***App passwords.***(*It will be visible only, if you have 2FA on*)
      - In the next screen, under *Select app* option select **Other**, and type your app name as ***pywisher***.
      - Click done, and in the next screen, you will get your pass code.
  - ### Birthday record setup
      - Using your gmail account, send yourself an email keeping birthday record as attchment, and keep a unique subject. (*This unique subject will be used by the code to read the email from the inbox.*)
  - ### Github project setup
      - ***Fork*** this project.
      - Go to setting of your pywisher repository.
      - On the left hand panel, go to ***secrets*** under security section, and click actions.
      - Now, create new secrets by clicking ***New repository secret***. You have to create 4 secrets having same name as given in the ***actions.yml*** file.
  
           ```
           EMAIL - your-github-email@email.com
           KEY_ID - your-gmail-for-reading-and-writing@gmail.com
           KEY_SECRET - app password you create in the Gmail ***setup section***.
           SEARCH_KEY - unique subject for the email you sent in ***Birthday record setup***
           ```

## Where to find me
 
<p align="left">
 <a href="https://twitter.com/aps08__"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white"></a>
 <a href="https://medium.com/@aps08"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white"></a>
 <a href="https://www.linkedin.com/in/aps08"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
 <a href="https://github.com/aps08"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>
 <a href="https://www.youtube.com/channel/UC8biJQnoqm1s2FZ8LK90baA"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
 <a href="mailto:anoopprsingh@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"></a>
</p>

