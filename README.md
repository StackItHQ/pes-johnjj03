[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [x] My code's working just fine! 🥳
- [ ] I have recorded a video showing it working and embedded it in the README ▶️
- [x] I have tested all the normal working cases 😎
- [x] I have even solved some edge cases (brownie points) 💪
- [x] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section
*Add your video here, and your approach to the problem (optional). Leave some comments for us here if you want, we will be reading this :)*

### Video 


### My Approach
- After I read the problem statement, my first thought was to initially synchronize both the dataabase and the sheet, giving the user the choice to pick their preference.
- Next, I wanted the changes in the database to reflect in the Google Sheet. My first attempt with MySQL proved unsuccessful as there was no native way to notify a service outside of MySQL when a CRUD operation had happened on a table.
- I initally had tried to make a timestamp based approach. When a CRUD operation occured on a table, there would be a new table called table_name_timestamps, which would record both the old and new changes, however this approach would not work out for a few reasons.

  - I had to create a new table with essentially the same values again, which would be costly in the long run.
  - Deleted values and newly created values would have a lot of columns with nothing in them.
  - And the previous problem remained where I had to continuosuly keep querying the last_modified column for changes and adding those to Google Sheets.

- All of these problems were solved once I made the decision to move to PostgreSQL. PostgreSQL has a feature called LISTEN/NOTIFY which allows you to listen to a channel and notify a service when a CRUD operation has happened on a table.
- I then created a trigger function that would notify a channel when a CRUD operation had happened on a table.
- A python service would continously poll for just this notification, and once it recieved it, it would just update the Google Sheet with the new changes.
- By far the biggest blocker was the MySQL issue, which was solved by moving to PostgreSQL.
- Next comes the second part of the problem, which would be updating the changes in the Google Sheet to the database. This is obviously harder, since Google Sheets can be edited in a number of ways, and I would have to keep track of all of them.
- My first hurdle was figuring out a way for Google Sheets to notify a service when a CRUD operation had happened on a sheet. I found out that Google Sheets has a feature called Google Apps Script, which allows you to write scripts that can be run on Google Sheets.
- I had setup a script to run on my Google Sheet,such that whenever a change occured, it would send a POST request to a service I had setup on my local machine.
- However, after a few hours of debugging, I found out that my router does not support port forwarding, and that the trigger I had setup on my Google Apps script would not work.
- I realised that continously polling the Google Sheet for changes would be an expensive approach, and decided to not implement that method into my project.
- Since I had already made a script that copys the existing data from Google Sheets into the database, I decided to just run that script whenever I wanted to update the database with the Google Sheet.
- I have solved a few edge cases, an example being when the Google Sheet has completely empty rows, they get skipped instead of directing being added into the database, causing an error.