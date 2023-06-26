# Creating a venv
We advise the creation of a virtual enviroment. Run this:
`python -m venv venv`
Then, activate the venv.

on linux:
`source ./venv/bin/activate`

on windows:

`.\venv\Scripts\`

Now, you must install the dependencies.

# Installing
To run the program, you must install some packages. Run this: 

`pip install -r requirements.txt`

After downloading everything, you must download spacy's model.

`python -m spacy download en_core_web_trf`
`python -m spacy download en_core_web_lg`


After this, you are done.

# Running
To run the program, simply call it using the python runner and follow the instructions:

`python main.py english`

# After running
After the program has ended, a .csv file will be created. It will always be named following this format:
`result-date-time-model.csv`
