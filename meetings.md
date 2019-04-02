# Meetings notes

## Meeting 1.
* **DATE: 14.02.2019**
* **ASSISTANTS: Ivan Sanchez Milara**
* **GRADE:** *To be filled by course staff*

### 20 Minutes 
*Summary of what was discussed during the meeting*

At first we were asked to remove the extra stuff from the GitHub code page. These were added by accident while creating a local repository in order to work from home. After this we disscussed about the task included in the deadline 1 (RESTful API description). Overall, our thinking was still too broad and we were asked to narrow it down even more. At this point we only have to worry about the API itself, no about the client or the server. This means we need to focus more on the aspect of how the API will be used. We were also asked to think about why, for example, people from our university would want to use it.

In the overview part of the deadline 1, we should make it more selling. This is the part were we are supposed to market our API, so adding some details should fix it. In the main concepts and relations, we should make things more simple. We came to a conclusion that the throw itself is one of our most important entities. We had drawn an early version of our ER model to illustrate our thinking. In this model we should make sure we don´t use same attribute inside different entitites. These should be replaced with relationships between the entities. We concluded the most relevant entities right now are the throw, the player and the team. In API uses part, we should be more specific in the other APIs which could be used with our API, for example, using Google Maps to track down the location were the game will be played. These don´t need to be implemented in the final work. Lastly, in the related work part, we should find another API which includes same kind of functionality than our API. It should include things like URL, GET and POST functionalities.

### Action points
*List here the actions points discussed with assistants*

* remove extra stuff from the GitHub code page DONE
* write about why people from uni would want to use the app (overview) DONE
* advertise your API more (overview) DONE
* focus more on the how the API is used and make things more simple (main concepts) DONE
* be more specific on which other APIs could be used with our API (API uses)
* find another API which includes same kind of functionality than our API (related work)

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE: 28.2.2019**
* **ASSISTANTS: Ivan Sanchez Milara**
* **GRADE:** *To be filled by course staff*

### 30 Minutes
*Summary of what was discussed during the meeting*

At first, our assistant checked our readme file and concluded it was okay and even more detailed than was required. After this our models were checked. Our models were okay, but we were missing one resource from our API. Ivan suggested we should add a new resource: player. Player model should have a relationship to the throw model. In the player model, name will be our foreign key. Next, we discussed about the team_points attribute. In this, nullable should be changed to True, so we can create a new match without adding the final results. This could be done in the client side, maybe? Ivan promised to try to find us a solutions for this. We should also put our model codes into different files to follow the protocols. In the future we should make sure our DELETE and UPDATE are working. For example, when we remove a match from the database, all the throws related to this deleted match will be also deleted.

### Action points
*List here the actions points discussed with assistants*

* update player model in Table 3 (database design)
* add fifth resource: player (database design)
* in code, put models in different file (database implementation)
* solve how to restrick team_points between -80 and 80 (database implementation)
* in the future, implement DELETE and PUT

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE: 29.3.2019**
* **ASSISTANTS: Mika Oja**
* **GRADE:** *To be filled by course staff*

### 30 Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*

* Fix the relations diagram with following:
    * upper categories need to be linked. Rigth now matches/match is isolated resource
    * add collection arrow between matches/match
    * remove the link between player/throws and replace it with: throws are a list under the player resource
    * list of throws need to be added to Url or request body
* REST conformation task
    * present all the methods, some are missing
    * MIME type is hypermedia + JSON, fix this
    * name your hypermedia type
    * connectedness part needs improvements, it is lacking
* Apiary code
    * throws-by link relation is wrong in matches
    * invent our own namespace, replace mumeta with kyykka or something  

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*


## Final meeting
* **DATE:**
* **ASSISTANTS:**
* **GRADE:** *To be filled by course staff*

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

