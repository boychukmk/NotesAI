# NotesAI Project
## Features
- Create, edit, and delete notes
- View history of note changes
- AI-powered note summarization (via Gemini API)
- Analytics dashboard for insights on notes
- Fully async backend for high performance
- Dockerized deployment for easy setup
- REST API with Swagger UI for documentation
- Test Coverage 87%
- Vue.js frontend

## Development Process

### Initial Development & Setup
- **Commit: 08daa8c - CRUD operations for Notes**  
  The initial implementation focused on setting up the core functionality for managing notes. This involved creating the basic CRUD operations such as creating, reading, updating, and deleting notes. 

### History implementation
- **Commit: 74e846d - + corrections in ordering + history saving func + endpoint for history**  
  Introduced a history saving function to track changes made to the notes. The history was stored and retrievable. Corrections were also made in the ordering of notes.

### AI Integration
- **Commit: 397c05a - AI summarizer functionality with endpoint**  
  Integrated AI summarization features using a Gemini API to automatically generate summaries for the notes. An endpoint was created to interact with the summarizer.
### Async db
- **Commit: fcfc220 - moving to async db**
On this stage i transferred my sync db to async to improve the reliability of the application.
### Analytics Feature
- **Commit: 74f2951 - analytics service + routes for app**  
  Added analytics service to collect and analyze data about the notes. This involved calculating metrics such as word count, average note length, and common words.
### Async Database Migration & Dockerization
- **Commit: 065b9cc - docker + alembic migrations**  
  Added Docker support for easier development and deployment. This also included setting up Alembic migrations for database schema changes, ensuring smooth database management in different environments.
### Testing
- **Commit: 280aa07 - Merge pull request #4 from boychukmk/testing**  
  Integrated the testing branch into the main project. This branch covered app on 87% with tests

### UI Development
- **Commit: 0adb9f7 - frontend + structured project**  
  Initial commit of frontend part with structured files and folders

- **Commit: bb29a48 - structured project**  
  Reorganized the project structure with frontend and backend folders 

- **Commit: ee056aa - fix**  
  Fixed minor issues related to the frontend errors and config.py corrections.
- **Commit: 11c85e3 - Merge pull request #6 from boychukmk/frontend**  
  The final frontend integration was completed. This pull request merged the frontend feature branch with the main project, creating the user interface and connecting it to the backend API.



## Tech Stack

- **Frontend**: Vue.js, Vite, Nginx
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose



## Running the Project with Docker

### 1. Clone the repository

```bash
git clone https://github.com/boychukmk/NotesAI.git
cd NotesAI
```

### 2. Create the .env file

Create a .env file in the root of the project with the following content:

MacOS
```bash
echo -e "GENAI_API_KEY=your-gemini-api-key-here" > .env
```
Windows cmd
```bash
echo GENAI_API_KEY=your-gemini-api-key-here > .env
```

### 3. Build and start the services

Run the following command to build and start the frontend and backend services:

```bash
docker-compose up --build
```
or
```bash
docker compose up --build
```
### 4. After building containers you can access app:

- **Frontend**: Visit http://localhost:8080 in your browser.
  In the catalog of notes you can access Note Page clicking on "Read More". There will be buttons to check note history and summarize selected note.
- **Backend**: The backend API will be running on http://localhost:8000 with http://localhost:8000/docs Swagger UI.
- **Tests** will be available while building in terminal, or you can run command 
```bash
docker-compose run tests
```
or
```bash
docker compose run tests
```
