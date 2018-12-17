Big Graph Code
===============

In this repository, are the code for practical work on big graphs.<br>
All the description is (in french) in "Rapport TP Big Graphs Tassy Doué"

Installation
------------

### 1. Clone the project : 
``` bash
$ git clone https://github.com/CorentinDoue/tp_big_graph.git
```

### 2. Recreate the Python virtualenv : 
require python 3.6:
``` bash
$ virtualenv venv_tp
$ source venv_tp/bin/activate
(venv_tp)$ pip install -r requirements.txt
```

### 3. Update config : 
In ```main.py``` complete : <br>
```neo4j_bdd = Neo4jBdd('neo4j_bolt_url', 'neo4j_user', 'neo4j_password')```

Use
---

### Neo4j
Run 
``` bash
$ python main.py
```
to import the data in the neo4j database and return the results of some queries.<br>
The database is reachable at ```http://localhost:7474/browser/```

### GraphQL

#### 1. Go to the project directory
``` bash
$ cd emseunions
```

#### 2. Start the server
``` bash
$ python manage.py runserver
```

#### 3. Open the browser
Open ```http://localhost:8000/graphql/```

#### 4. Try some queries
``` bash
query {
  users {
    id
    firstname
    lastname
    type
    promo
  }
}

mutation {
  createUser (
    firstname: "Théophane",
    lastname: "Tassy",
    type: "ICM",
    promo: 2016
  ) {
    id
    firstname
    lastname
    type
    promo
  }
}

mutation {
  createUnion (
    name: "Cercle"
  ) {
    id
    name
  }
}

query {
  unions {
    id
    name
  }
}

mutation{
  addContribution(
    idUnion: 1,
    idUser: 1
  ) {
    user {
      id
      firstname
      lastname
    }
    union {
      id
      name
    }
  }
}

query{
    unions {
      id
      name
      contributors {
        id
        firstname
        lastname
      }
      members{
        id
        firstname
        lastname
      }
    }
}
```
