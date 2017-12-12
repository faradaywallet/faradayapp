# faradayapp

Running the system:

INSTALLING REQUIRED SW & LIBRARIES:
	-run 'pip install flask' to install flask
	-Ensure that python 3.4+ is installed 
	-ensure that pymysql is installed by running 'pip install pymysql' in your command line
	-MySQL Workbench was used for the DB. Visual Studio 2013 Redistributable will be needed to use MySQL Workbench.
		-the access to the DB is made with user: root, with password "cybr200"; You can create this user while setting up MySQL Workbench, or you can add this allowed user to the DB server when setting up the DB. This can be done from the 'Users and Pricileges' option under MANAGEMENT in the Navigator. This option is accessable after you are running your MySQL Connection.
	
GETTING THE DB SERVER RUNNING:
	-manually create the tables in MySQL Workbench as such:
		-open MySQL Workbench
		-create a new MySQL Connection(+), on 127.0.0.1 and port 3310
		-test your connection and open it
		-create a new schema named 'faraday'
		-double click your new schema under the SCHEMAS list in the Navigator
		-create a new table in this schema and name it 'user'. Add the columns: 'user' , 'email', 'createDate', 'salt', 'auth', and 'symmetricBox'. these are all VARCHAR(255)
		-create another table and name it 'card'. Add the columns: 'userid' and 'payload'. These are also all VARCHAR(255)
	-once the tables are created, restart the server by clicking on 'Startup/Shutdown' in the INSTANCE section of the Navigator.
		-click on the 'Stop Server' button above the Startup Message Log, next to the green text that says 'running.' If the server does not stay off (indicated by red text replacing the green text), then you will also have to click the button that says 'Bring Offline'
		-turn the server back on by bringing it back online (if neccessary) and starting the server by pressing the correspoinding buttons

GETTING FARADAY WALLET RUNNING:
	-run the faraday.py python file in your prefered method of running python
	
USING THE SYSTEM:
	-system is set to run on port 3310, on http://127.0.0.1:5000/
		-open your preffered web browser and go to http://localhost:5000/
		-register your new user
		-after registering, click on the logo in the upper-left-hand corner to go back to the login screen.
		-login with your user credentials
		-add credit card information
		-logout
		-log back in and see that the data is still there