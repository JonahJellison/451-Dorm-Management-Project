
# Sprint 1 Report
* Video Link: https://youtu.be/o8HnFasjYvQ
* Repo Link: https://github.com/JonahJellison/451-Dorm-Management-Project/
## What's New (User Facing)
### Frontend
* created new angular project with components for each page
* login page
* create account page
* Admin dashboard
* Booking page
* account settings page
### Backend
* Created Django backend project
* Created data models to represent the user data
* Wrote login api to authenticate username and passwords
* Wrote create account api
### Database
* Created database using azure and linked it to our project
## Work Summary (Developer Facing)
This sprint was primarially focused on getting our project set up as well as outlining a skeleton 
for the project. We get the frontend completed with html and css. Right now it is full of "dummy" data,
so it needs to be connected with the backend, but it serves as a good starting point for our sprint 2. Additionally,
we set up the backend with django and completed the user authentication and login system. Finally, we worked on the 
database and got it initially ready to interface with the rest of the project. For the database we used the Azure
portal to create the server and database and then linked that to our project. Then in the models.py file we added our 
table definitions for all entities. 
## Unfinished Work
N/A
## Completed Issues/User Stories
Github project board: https://github.com/users/JonahJellison/projects/3
## Incomplete Issues/User Stories
We kept this sprint pretty simple to create the backbone of our project, which will allow
us to move quickly next sprint.
## Code Files for Review
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/app-frontend/src/app/account-info
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/app-frontend/src/app/admin-dashboard
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/app-frontend/src/app/create-account
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/app-frontend/src/app/dorm-bookings
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/app-frontend/src/app/login
https://github.com/JonahJellison/451-Dorm-Management-Project/tree/main/backend/backend
## Retrospective Summary
Here's what went well:

*   **Team collaboration:** Our team worked effectively together, communicating well and supporting each other throughout the sprint. This allowed us to overcome challenges and stay on track.

*   **Frontend design:** We successfully created a visually appealing and user-friendly frontend design. The components for each page were well-structured and easy to navigate.

*   **Creating all necessary parts of the project (frontend, backend, and database initialization):** We successfully set up the basic structure for the frontend, backend, and database, providing a solid foundation for future development.

*   **User sign-in:** We implemented a functional user sign-in system, allowing users to create accounts and log in securely.

Here's what we'd like to improve:

*   **Moving/iterating faster:** We want to improve our velocity and complete more tasks within each sprint. This could involve better planning, task breakdown, and time management.

*   **Procrastination:** We need to address procrastination within the team to ensure that tasks are completed in a timely manner. This could involve setting deadlines, breaking down tasks into smaller steps, and using time management techniques.

*   **Getting more progress done next sprint:** We aim to make more significant progress in the next sprint by focusing on key features and prioritizing tasks effectively.

Here are changes we plan to implement in the next sprint:

*   **Populate database with data about rooms:** We will populate the database with detailed information about the available rooms, including their features, capacity, and pricing.

*   **Link all frontend pages to the backend:** We will connect all frontend pages to the backend, enabling data to be dynamically displayed and updated.

*   **Create sample student data to fill the database with:** We will create sample student data to populate the database, allowing us to test the functionality of the application with realistic data.

*   **Admin pages:** We will develop the admin pages, providing administrators with the ability to manage users, rooms, and bookings.

*   **Connecting database to backend:** We will fully integrate the database with the backend, allowing the application to store and retrieve data efficiently.
