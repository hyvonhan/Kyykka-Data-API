FORMAT: 1A
HOST: http://polls.apiblueprint.org/

# Kyykka-Data-API

Kyykkä-Data-API offers different functionalities to store and compare statistics of kyykkä games in real-time. The API serves JSON data extended by the [Mason hypermedia format](https://github.com/JornWildt/Mason). Custom link relations and resource profiles have been included in this API document - they are not resources.

# Group Link Relations

This section described custom link relations defined in this API. These are not resources. The API also uses 
[IANA link relations](http://www.iana.org/assignments/link-relations/link-relations.xhtml) where applicable. Custom link relations are CURIEs that use the mumeta prefix.

## add-throw

This is a control that is used to add an throw to the associated collection resource. The control includes a JSON schema and must be accessed with POST. 

## add-match

This is a control that is used to add a match to an album resource. The control includes a JSON schema and must be accessed with POST.

## matches-all

Leads to the root level albums collection which is a list of all albums known to the API regardless of artist. This collection can be sorted using query parameters as described in the resource documentation.

## throws-by

Leads to a collection resoruce that includes all albums by the associated artist.

## players-all

Leads to the root level artists collection which is a list of all artists known to the API. 

## delete

Deletes the associated resource. Must be accessed with DELETE

# Group Profiles

This section includes resource profiles which provide semantic descriptions for the attributes of each resource, as well as the list of controls (by link relation) available from that resource.

## Match Profile

Profile definition for all album related resources.

### Link Relations

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the mumeta namespace are used:

 * [add-throw](reference/link-relations/add-throw)
 * [add-match](reference/link-relations/add-mathc)
 * [matches-all](reference/link-relations/matches-all)
 * [throws-by](reference/link-relations/throws-by)
 * [players-all](reference/link-relations/players-all)
 * [delete](reference/link-relations/delete)
 
The following [IANA RFC5988](http://www.iana.org/assignments/link-relations/link-relations.xhtml) link relations are also used:

 * author
 * collection
 * edit
 * profile
 * self

### Semantic Descriptors

#### Data type Match

 * `team1`: The name of the team1, including capitalization and punctuation. Mandatory.
 * `team2`: The name of the team2, including capitalization and punctuation. Mandatory.
 * `date`: The time of the match.
 * `team1_points`: Number of points per game for team1.
 * `team2_points`: Number of points per game for team2.

## Throw Profile

Profile definition for all album related resources.

### Link Relations

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the mumeta namespace are used:

 * [add-throw](reference/link-relations/add-throw)
 * [add-match](reference/link-relations/add-mathc)
 * [matches-all](reference/link-relations/matches-all)
 * [throws-by](reference/link-relations/throws-by)
 * [players-all](reference/link-relations/players-all)
 * [delete](reference/link-relations/delete)
 
The following [IANA RFC5988](http://www.iana.org/assignments/link-relations/link-relations.xhtml) link relations are also used:

 * author
 * collection
 * edit
 * profile
 * self

### Semantic Descriptors

#### Data type throw

 * `title`: The albums title as it is written on the release, including capitalization and punctuation. Titles are unique per artist, and are used to address album resources. Mandatory.
 * `release`: Album's release date in [ISO 8601 format](https://www.iso.org/iso-8601-date-and-time-format.html) (YYYY-MM-DD). Use 01 for month or day if not known. Mandatory.
 * `artist`: The album's artist's name (null for VA albums), including capitalization and pucntuation.
 * `discs`: Number of discs the album contains. Default is 1.
 * `genre`: The albums musical genre as a string. Optional.


## Player profile

Profile definition for all players.

### Link Relations

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the mumeta namespace are used:

 * [matches-all](reference/link-relations/matches-all)
 * [throws-by](reference/link-relations/throws-by)
 * [players-all](reference/link-relations/players-all)
 * [delete](reference/link-relations/delete)
 
The following [IANA RFC5988](http://www.iana.org/assignments/link-relations/link-relations.xhtml) link relations are also used:

 * author
 * collection
 * edit
 * profile
 * self

### Semantic Descriptors

#### Data type player

 * `title`: The albums title as it is written on the release, including capitalization and punctuation. Titles are unique per artist, and are used to address album resources. Mandatory.
 * `release`: Album's release date in [ISO 8601 format](https://www.iso.org/iso-8601-date-and-time-format.html) (YYYY-MM-DD). Use 01 for month or day if not known. Mandatory.
 * `artist`: The album's artist's name (null for VA albums), including capitalization and pucntuation.
 * `discs`: Number of discs the album contains. Default is 1.
 * `genre`: The albums musical genre as a string. Optional.


## Error Profile

Profile definition for all errors returned by the API. See [Mason error control](https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md#property-name-error) for more information about errors.

+ Attributes

    + resource_url (string, required) - URI of the resource the error was generated from.
    
# Group Match

# Group Throw

# Group Player

All of these resources use the [Player Profile](reference/profiles/player-profile). In error scenarios [Error Profile](reference/profiles/error-profile) is used.

## Player Collection [/api/players/]

A list of all players known to the API. 

### List all players [GET]

Get a list of all players known to the API.

+ Relation: players-all
+ Request

    + Headers
    
            Accept: application/vnd.mason+json

+ Response 200 (application/vnd.mason+json)
    
    + Body

            {
                "@namespaces": {
                    "mumeta": {
                        "name": "/kyykkadataapi/link-relations#"
                    }
                },
                "@controls": {
                    "self": {
                        "href": "/api/players/"
                    },
                    "mumeta:players-all": {
                        "href": "/api/players/",
                        "title": "All players"
                    },
                    "mumeta:add-player": {
                        "href": "/api/artists/",
                        "title": "Add a new player",
                        "encoding": "json",
                        "method": "POST",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "description": "Name of the player",
                                    "type": "string"
                                },
                                "team": {
                                    "description": "Team of the player",
                                    "type": "string"
                                }
                            },
                            "required": ["name", "team"]
                        }
                    }                    
                },
                "items": [
                    {
                        "name": "pekka",
                        "@controls": {
                            "self": {
                                "href": "/api/players/pekka/"
                            }, 
                            "profile": {
                                "href": "/profiles/player/"
                            }
                        }
                    }
                ]
            }
            
### Add a new player [POST]

Adds a new player.

+ Relation: add-player
+ Request (application/json)

    + Headers
    
            Accept: application/vnd.mason+json
            
    + Body
            
            {
                "name": "pekka",
                "team": "kiskojat"
            }

+ Response 201
    
    + Headers
        
            Location: /api/players/pekka/
            
    + Body
    
            {}

+ Response 400 (application/vnd.mason+json)

    The client is trying to send a JSON document that doesn't validate against the schema.

    + Body
    
            {
                "resource_url": "/api/players/",
                "@error": {
                    "@message": "Invalid JSON document",
                    "@messages": [                    
                        "'name' is a required property
                        
                        Failed validating 'required' in schema:
                        {'properties': {'name': {'description': \"Name of the player\",
                        'type': 'string'},
                        'team': {'description': \"Team of the player\",
                        'type': 'string'}},
                        'required': ['name'],
                        'type': 'object'}
                        
                        On instance:
                        {'name': 'pekka'}"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

+ Response 415 (application/vnd.mason+json)

    The client sent a request with the wrong content type or the request body was not valid JSON.

    + Body
        
            {
                "resource_url": "/api/players/pekka/",
                "@error": {
                    "@message": "Unsupported media type",
                    "@messages": [
                        "Use JSON"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error-profile/"
                    }
                }
            }

## Player [/api/players/{player}/]

This resource represents a single player.

+ Parameters

    + player: pekka (string) - player's name (name)
            

### Player information [GET]

Get the player's representation.

+ Relation: self
+ Request

    + Headers
    
            Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)
 
    + Body
    
            {
                "@namespaces": {
                    "mumeta": {
                        "name": "/musicmeta/link-relations#"
                    }
                },
                "name": "pekka",
                "team": "kiskojat",
                "@controls": {
                    "self": {
                        "href": "/api/players/{player}/"
                    },
                    "mumeta:throws-by": {
                        "href": "/api/players/pekka/throws/",
                        "title": "Throws by player"
                    },
                    "collection": {
                        "href": "/api/players/",
                        "title": "All players"
                    },    
                    "edit": {
                        "href": "/api/players/pekka/",
                        "title": "Edit this player",
                        "encoding": "json",
                        "method": "PUT",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "description": "Name of the player",
                                    "type": "string"
                                },
                                "team": {
                                    "description": "Team of the player",
                                    "type": "string"
                                }
                            },
                            "required": ["name", "team"]
                        }
                    },
                    "mumeta:delete": {
                        "href": "/api/players/pekka/",
                        "title": "Delete this player",
                        "method": "DELETE"
                    }
                },
                "items": [
                    {
                        "name": "pekka",
                        "@controls": {
                            "self": {
                                "href": "/api/players/pekka/"
                            }, 
                            "profile": {
                                "href": "/profiles/player/"
                            }
                        }
                    }
                ]
            }
            
+ Response 404 (application/vnd.mason+json)

    The client is trying to modify a player that doesn't exist.

    + Body
    
            {
            }
            
### Edit player information [PUT]

Replace the player's representation with a new one. Missing optinal fields will be set to null. Must validate against the artist schema. 

+ Relation: edit
+ Request (application/json)

    + Headers
        
            Accept: application/vnd.mason+json
        
    + Body
    
            {
                "name": "pekka",
                "team": "kiskojat"
            }

+ Response 204


+ Response 400 (application/vnd.mason+json)

    The client is trying to send a JSON document that doesn't validate against the schema..

    + Body
    
            {
                "resource_url": "/api/players/pekka/",
                "@error": {
                    "@message": "Invalid format",
                    "@messages": [
                        "Something went wrong"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

+ Response 404 (application/vnd.mason+json)

    The client is trying to edit a player that doesn't exist. 

    + Body
    
            {
                "resource_url": "/api/players/pakke/",
                "@error": {
                    "@message": "Player not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }
            
+ Response 415 (application/vnd.mason+json)

    The client sent a request with the wrong content type or the request body was not valid JSON.

    + Body
        
            {
                "resource_url": "/api/players/pekka/",
                "@error": {
                    "@message": "Unsupported media type",
                    "@messages": [
                        "Use JSON"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error-profile/"
                    }
                }
            }
            
### Delete player [DELETE]

Deletes the player.

+ Relation: delete
+ Request

    + Headers
        
            Accept: application/vnd.mason+json
        
+ Response 204

+ Response 404 (application/vnd.mason+json)

    The client is trying to delete a player that doesn't exist (due to non-existent player). 

    + Body
    
            {
                "resource_url": "/api/players/pekka/",
                "@error": {
                    "@message": "Player not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }
























BOILER PLATE KOODIA ÄLÄ RESSAA
## Questions Collection [/questions]

### List All Questions [GET]

+ Response 200 (application/json)

        [
            {
                "question": "Favourite programming language?",
                "published_at": "2015-08-05T08:40:51.620Z",
                "choices": [
                    {
                        "choice": "Swift",
                        "votes": 2048
                    }, {
                        "choice": "Python",
                        "votes": 1024
                    }, {
                        "choice": "Objective-C",
                        "votes": 512
                    }, {
                        "choice": "Ruby",
                        "votes": 256
                    }
                ]
            }
        ]

### Create a New Question [POST]

You may create your own question using this action. It takes a JSON
object containing a question and a collection of answers in the
form of choices.

+ Request (application/json)

        {
            "question": "Favourite programming language?",
            "choices": [
                "Swift",
                "Python",
                "Objective-C",
                "Ruby"
            ]
        }

+ Response 201 (application/json)

    + Headers

            Location: /questions/2

    + Body

            {
                "question": "Favourite programming language?",
                "published_at": "2015-08-05T08:40:51.620Z",
                "choices": [
                    {
                        "choice": "Swift",
                        "votes": 0
                    }, {
                        "choice": "Python",
                        "votes": 0
                    }, {
                        "choice": "Objective-C",
                        "votes": 0
                    }, {
                        "choice": "Ruby",
                        "votes": 0
                    }
                ]
            }
