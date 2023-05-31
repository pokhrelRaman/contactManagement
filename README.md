Tech-stacks involved
Language: Python
Framework: Django,Django Rest Framework


How to get started with this repo???
Requirements
System:
OS: Linux/mac/Windows
Browser: Chrome/Safari/Brave/Microsoft Edge
Http Client: Postman or Any Chrome extension
Code Editor: any (recommended VS Code with at least extensions Python and Pylance installed)
Binaries:
Python: >=3
Utilities:
Git: >=2.37.1
Steps to get started with this repo:
Step 1: Choose your command terminal, the built-in one or your editor's built-in one 📦

Step 2: Change directory of your choice 🏗

cd <directory of your choice>
Step 3: Clone the repo 📦

git clone https://github.com/pokhrelRaman/contactManagement.git
Step 4: cd into the project 🏗

Step 5: Create virtual env and install project dependencies 🏗

Method 1: Using MakeFile (make tool)

You can make use of make file available to the root of this project. Make sure you have the tool make available on your system. This will create a virtual env,activate it and install the project dependencies for you
Note: If you are on windows, you can use chocolatey to install make tool: choco install make

For linux/Mac
make venv
For Windows
make venv-win
Activate virtual env
For linux/Mac
source .venv/bin/activate
For Windows
.venv\Scripts\activate
Method 2: Conventional way

You can proceed your regular way of creating virtual env and installing dependencies like below:

Create virtual env
python3 -m venv .venv
Activate virtual env
For linux/Mac
source .venv/bin/activate
For Windows
.venv\Scripts\activate
Install project dependencies
pip install -r requirements.txt
Step 6: Start the development sever 🚀

make run or `python3 manage.py runserver

 Api for User CRUD:
 
 



                  localhost:8000/auth/v1.0/register
                  localhost:8000/auth/v1.0/forgotPassword
                  localhost:8000/auth/v1.0/login
                  localhost:8000/auth/v1.0/update
                  localhost:8000/auth/v1.0/changepassword
                  localhost:8000/auth/v1.0/logout
                  localhost:8000/auth/v1.0/refreshToken

  
  Api for Contacts CRUD:
 
 
 


 
                  localhost:8000/auth/v1.0/contacts                            create/fetch all contacts for specific user
                  localhost:8000/auth/v1.0/contacts/id                         fetch contact with specific id
                  localhost:8000/auth/v1.0/contacts/id/                        update/delete specific id
                  localhost:8000/auth/v1.0/contacts/viewall                    view all contacts of all user 

 
How to contribute to the repo??
Create a brand new branch with the name relevant to the feature/task you are going to work on
Push your changes to the remote repo
Now go to github web and create your PR for your changes(branch) with description of your contribution(changes)
Have fun building! 🚀🚀
