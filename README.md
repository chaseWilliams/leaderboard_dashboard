# Leaderboard Automated Dashboard
Project that fills out a Google Sheets with data from Google Analytics (monthly analysis of pageviews and top URLs)

## Installation
Clone this project and navigate to the project directory. Then, run `pip3 install -r requirements.txt`

## Configuration
The project depends on the presence of two files that currently do not exist: `client_secret.json` and `view_ids.csv`. These files are necessary for authorizing the program and specifying what websites to pull data for. 
First, visit the [Developer Console](https://console.developers.google.com/). Make sure the selected project is “leaderboard-dashboard”. Navigate to APIs and Services, then Credentials, and click on “Manage service accounts”. 
You’ll see a curiously long email address. This email address belongs to a service account, which essentially acts as a fake user that can perform tasks on our behalf. This is important, because what you’ll notice is that both the google sheets and the google analytics for the website have been shared with that email to give it appropriate permissions. This fake user will allow us to programmatically pull data and make changes without having to jump through a lot of other authorization hoops. This also means if you wanted to use a different google sheets or add a new website, you’ll have to share it with this fake user first. 
Click the triple dots to the right of the email, and hit “Create key”. Make sure its JSON, and download it as `client_secret.json` in the same directory as the source code. 
To create the view_ids.csv, simply create an empty file (perhaps by using touch view_ids.csv), and put in data in this format:
```
[view id],[website name]
```
Be sure to edit using a program like Notepad or Visual Studio Code, NOT Microsoft Word. This should be a very small and simple file. You can get the view id from Google Analytics, when you’re selecting a website it’s that long number underneath its name. 
Finally, we need to set some parameters within the source code. Open up main.py. Go ahead and change `YEAR`, `MONTH`, and `MONTHS_TO_RETURN` as necessary, where `YEAR` is, obviously, the year you want to start in, `MONTH` is the starting month (jan = 1, feb = 2, etc.), and `MONTHS_TO_RETURN` is how many months to go forward. Note that going into the future is safe, as the APIs will just return empty data, as reflected in the leaderboard dashboard. However, the code is only tested to work with 12 months. Going past 20 months of data at once may result in exceeding the project’s quota. 

## Running and Troubleshooting
To run it, just type `python3 main.py` in the console. 
The program will take approximately 250 seconds longer to run for every website it has to handle. You can also see the Google Sheets get updated in real time, which is pretty cool. 
The program has to take so long because of quota restraints. There’s a restraint on how many requests a project can make every 100 seconds, so I have the program wait 100 seconds between each website. If you get an error with `‘USER-100s’` somewhere in the error message, that means its a quota problem. Wait a couple minutes and try again, and if it fails again, maybe reduce the months being returned. 
Other possible issues are left as an exercise to the reader to solve.
Or you can always submit an issue on the github :) 
