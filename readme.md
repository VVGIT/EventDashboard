Dashboard using Highcharts, NodeJS, Express

Steps to execute the source code and view the dashboards:

At command prompt, execute the following command: git config core.longpaths true

Copy the source code folders and files into your local drive in an appropriate project directory.

From within the project directory, at the command prompt, use "gulp serve" command so that gulp can automatically install all of the required library dependencies. This command will also start a web server and begin listening to the port 3000.

In a different command prompt window, from the project directory, open the /public/Python directory and issue the command: getData.py

Open a web browser and type the URL: "localhost:3000/index.html". You should see the dashboard.