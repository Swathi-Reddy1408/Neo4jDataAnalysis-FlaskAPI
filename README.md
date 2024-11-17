# IMDb Neo4j Flask API

This project is a Flask-based API for managing and retrieving movie data stored in a Neo4j graph database. The API supports CRUD operations for movies and their relationships, such as actors, directors, and genres.

## Requirements

Before running this application, ensure you have the following installed:

- Python 3.7+
- Neo4j Community or Enterprise Edition
- Flask
- Neo4j Python Driver (`neo4j`)

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/Swathi-Reddy1408/Neo4jDataAnalysis-FlaskAPI.git
    cd <repository_folder>
    ```

2. Install the required Python libraries:
    ```bash
    pip install flask neo4j
    ```

3. Ensure your Neo4j database is running and update the following in the code:
    - Replace `<password>` with your Neo4j database password.
    - Ensure the URI matches your Neo4j instance (default: `bolt://localhost:7687`).

4. Run the Flask application:
    ```bash
    python <filename>.py
    ```

5. Access the API at:
    ```
    http://127.0.0.1:5000/
    ```

## API Endpoints

### 1. Get All Movies
**GET** `/imdb`

- Retrieves all movies in the database.
- **Response**: JSON array of movies.

### 2. Get Movie by Title with Relationships
**GET** `/imdb/<string:fname>`

- Retrieves a movie by its title, including its directors, actors, and genres.
- **Response**: JSON object with movie details and related nodes.

### 3. Add a Movie
**POST** `/imdb`

- Creates a new movie node and its relationships.
- **Request Body Example**:
    ```json
    {
        "id": "1",
        "title": "Inception",
        "description": "A mind-bending thriller",
        "rating": 9.0,
        "revenue": 800000000,
        "runtime": 148,
        "votes": 2000000,
        "year": 2010,
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
        "directors": ["Christopher Nolan"],
        "genres": ["Sci-Fi", "Thriller"]
    }
    ```
- **Response**: Confirmation message.

### 4. Update a Movie
**PATCH** `/imdb/<string:fname>`

- Updates the title, description, and rating of a movie.
- **Request Body Example**:
    ```json
    {
        "title": "Inception Updated",
        "description": "An updated description",
        "rating": 9.5
    }
    ```
- **Response**: Confirmation message.

### 5. Delete a Movie
**DELETE** `/imdb/<string:fname>`

- Deletes a movie and all its relationships.
- **Response**: Confirmation message.

### 6. Movie Statistics
**GET** `/imdb/stat/<string:fname>`

- Retrieves movie statistics, including actor and director counts. *(This route is a work in progress.)*

## Code Explanation

### Libraries Used
- `neo4j`: For connecting and executing queries on the Neo4j graph database.
- `flask`: For building the web application and handling API routes.
- `json`: For managing JSON data.

### Key Features
1. **Neo4j Connection**:
    - Established using the Neo4j driver.
    - All operations interact with the graph database.

2. **Routes**:
    - Routes are defined using Flask decorators.
    - Each route corresponds to a specific CRUD operation.

3. **CRUD Operations**:
    - Add, retrieve, update, and delete movie nodes and their relationships.

4. **Relational Queries**:
    - Cypher queries are used for interacting with the Neo4j database.
    - Relationships like `ACTED_IN`, `DIRECTED`, and `IN` (for genres) are handled.

### Future Enhancements
1. Add better error handling and validations.
2. Implement user authentication.
3. Paginate the results for large datasets.
4. Optimize Cypher queries for better performance.
