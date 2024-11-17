#PROG_ASSIGN2_23915_700743277
from neo4j import GraphDatabase
from flask import Flask, request, jsonify
import json

#Creating the Flask app
app=Flask(__name__)

# Connect to the Neo4j database
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "<password>"))

#Define a route to get all Movie nodes
@app.route('/imdb', methods=['GET'])
def searchall():
    # Define a query to retrieve all records
    query = """MATCH (m:Movie) RETURN m.id AS id, m.title AS title,m.description AS description,m.rating AS rating,
            m.revenue AS revenue,m.runtime AS runtime,m.votes AS votes,m.year AS year"""
# Execute the query and print the results
    with driver.session() as session:
      result = session.run(query)
      json_result = []
      for record in result:
        json_result.append(record.data())
      return jsonify(json_result)   
# Close the database connection
driver.close()    


#Define a route to get all nodes and all it relationships
@app.route('/imdb/<string:fname>', methods=['GET'])
def search_with_title(fname):
    cypher_query="""MATCH (m:Movie {title: $title})<-[:DIRECTED]-(d:Person) OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)OPTIONAL MATCH (m)-[:IN]->(g:Genres)
    RETURN m.title AS title, m.id as id, m.description as description,m.rating as rating,m.revenue as revenue,m.runtime as runtime,m.year as year,m.votes as votes,
    collect(DISTINCT d.name) AS directors, collect(DISTINCT a.name) AS actors, collect(DISTINCT g.type) AS genres"""
    with driver.session() as session:
        result = session.run(cypher_query, title=fname)
        if result.peek() is not None:
            json_result = []
            for record in result:
                json_result.append(record.data())
            return jsonify(json_result)
        else: 
            return "There is no movie with title '"+fname+"'"         
# Close the database connection
driver.close()    


# Define a route to handle POST requests
@app.route('/imdb', methods=['POST'])
def insert_record():
    data = request.get_json()
    id= data['id']
    title = data['title']
    description = data['description']
    rating = data['rating']
    revenue = data['revenue']
    runtime = data['runtime']
    votes = data['votes']
    year = data['year']
    actors = data.get("actors", [])
    directors = data.get("directors", [])
    genres = data.get("genres", [])
    
    with driver.session() as session:
        # Create the Movie node
        session.run("CREATE (:Movie {id: $id, title: $title, description: $description, year: $year, runtime: $runtime, rating: $rating, votes: $votes, revenue: $revenue})", 
                    id=id, title=title, description=description,rating=rating,revenue=revenue,runtime=runtime,votes=votes,year=year)
        
        # Create the Person nodes and ACTED_IN relationships
        for actor in actors:
            result=session.run("match(p:Person{name:$name})-[:ACTED_IN]->(m:Movie)",name=actor)
            if result.peek() is None:            
              session.run("MERGE (a:Person {name: $name}) "
                        "MERGE (m:Movie {id: $id}) "
                        "CREATE (a)-[:ACTED_IN]->(m)", name=actor, id=id)
            else:
                session.run("MERGE (a:Person {name: $name}) "
                        "MERGE (m:Movie {id: $id}) "
                        "CREATE (a)-[:ACTED_IN]->(m)", name=actor, id=id)
        
        # Create the Person nodes and DIRECTED relationships
        for director in directors:
            session.run("MERGE (d:Person {name: $name}) "
                        "MERGE (m:Movie {id: $id}) "
                        "CREATE (d)-[:DIRECTED]->(m)", name=director, id=id)
        
        # Create the Genres nodes and IN relationships
        for genre in genres:
            session.run("MERGE (g:Genres {type: $type}) "
                        "MERGE (m:Movie {id: $id}) "
                        "CREATE (m)-[:IN]->(g)", type=genre, id=id)
    # Return a success message
    return f"Movie node with '{title}' has been created with all its relationships "
# Close the database connection
driver.close()    

#Update route to update title,description and rating of movie node
@app.route('/imdb/<string:fname>', methods=['PATCH'])
def update_movie(fname):
    status="Movie node with title '"+fname+"' has been updated successfully"
    
    #Checking if json contains required values
    if 'title' in request.json:
        new_title = request.json['title']
    else:
        return jsonify('Please add title to update')
    if 'description' in request.json:
        description = request.json['description']
    else:
        return jsonify('Please add description to update')
    if 'rating' in request.json:
        rating = request.json['rating']
    else:
       return jsonify('Please add rating to update')
    
    #Cipher query to update the movie node
    with driver.session() as session:
        session.run("MATCH (m:Movie {title: $title}) SET m.title=$new_title,m.description=$description,m.rating=$rating", title=fname,new_title=new_title,description=description,rating=rating)

    return jsonify(status)

# Close the database connection
driver.close()    


#Delete route to delete the Movie node
@app.route('/imdb/<string:fname>', methods=['DELETE'])
def delete_movie(fname):
    #Cipher query to delete the movie node
    with driver.session() as session:
        session.run("MATCH (m:Movie {title: $title})  DETACH DELETE m", title=fname)     
    return f"Movie '{fname}' and all its relationships deleted from database."
# Close the database connection
driver.close()    

@app.route('/imdb/stat/<string:fname>', methods=['GET'])
def search_movie(fname):
    #Cipher query to delete the movie node
    with driver.session() as session:
        result22=session.run("MATCH (m:Movie) WHERE m.city =~ '^$fname.*' RETURN m",fname=fname)
        #MATCH (n) WHERE "Airport" in LABELS(n) AND n.name =~ '^H.*' RETURN n
        result=session.run("MATCH (m:Movie{title:$title}) return m,count(m)",title=fname) 
        print(result22)
        json_result=[]
        json_result1=[]
        json_result2=[]
        record=list(result)
        print(len(record))
        print(result)
        for i in range(0,len(record)):
         if(result.peek()):
            json_result.append(result.data())
            print(len(json_result))
            for i in range(0,len(json_result)):
              result2=json_result[0][i] 
              title=result2['m']['title']
              print(title)
              if(title.startswith(fname)):
                  actors=session.run("Match(m:Movie{title:$title})<-[:ACTED_IN]-(p:Person) with count(p) as c return c ",title=title)
                  json_result1.append(actors.data())
                  print("ACTORS:")
                  print(json_result1)
                  directors=session.run("Match(m:Movie{title:$title})<-[:DIRECTED]-(p:Person) with count(p) as c return c ",title=title)
                  json_result1.append(directors.data())
                  print("DIRECTORS:")
                  print(json_result1)


           # if title

    return "Empty"
# Close the database connection
driver.close()    



#Launching the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)


