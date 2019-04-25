FORMAT: 1A
HOST: http://polls.apiblueprint.org/

# Kyykka-Data-API

Kyykkä-Data-API offers different functionalities to store and compare statistics of kyykkä games in real-time. The API serves JSON data extended by the [Mason hypermedia format](https://github.com/JornWildt/Mason). Custom link relations and resource profiles have been included in this API document - they are not resources.

# Group Link Relations

This section described custom link relations defined in this API. These are not resources. The API also uses 
[IANA link relations](http://www.iana.org/assignments/link-relations/link-relations.xhtml) where applicable. Custom link relations are CURIEs that use the kyykka prefix.

## add-throw

This is a control that is used to add an throw to the associated collection resource. The control includes a JSON schema and must be accessed with POST. 

## add-match

This is a control that is used to add a match to an album resource. The control includes a JSON schema and must be accessed with POST.

## matches-all

Leads to the root level albums collection which is a list of all albums known to the API regardless of artist. This collection can be sorted using query parameters as described in the resource documentation.

## throws-by

Leads to a collection resoruce that includes all throws by a player.

## players-all

Leads to the root level artists collection which is a list of all artists known to the API. 

## delete

Deletes the associated resource. Must be accessed with DELETE

# Group Profiles

This section includes resource profiles which provide semantic descriptions for the attributes of each resource, as well as the list of controls (by link relation) available from that resource.

## Match Profile

Profile definition for all album related resources.

### Link Relations

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the kyykka namespace are used:

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

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the kyykka namespace are used:

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

This section lists all possible link relations associated with albums; not all of them are necessarily present on each resource type. The following link relations from the kyykka namespace are used:

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

All of these resources use the [Match Profile](reference/profiles/match-profile). In error scenarios [Error Profile](reference/profiles/error-profile) is used.

## Match Collection [/api/matches/?sortby={field}]

A list of all matches known to the API. This collection can be sorted using the sortby query parameter. Matches can be directly added to this collection, it supports.

+ Parameters

    + field (string, optional) - Field to use for sorting
    
        + Default: `id`
        + Members
            
            + `id`
            + `date`

### List all matches [GET]

Get a list of all matches known to the API.

+ Relation: matches-all
+ Request

    + Headers
    
            Accept: application/vnd.mason+json

+ Response 200 (application/vnd.mason+json)
    
    + Body

            {
                "@namespaces": {
                    "kyykka": {
                        "name": "/kyykka_apiary/link-relations#"
                    }
                },
                "@controls": {
                    "self": {
                        "href": "/api/matches/"
                    },
                    "kyykka:throws-by": {
                        "href": "/api/matches/{id}/throws",
                        "title": "All throws"
                    },
                    "kyykka:add-match": {
                        "href": "/api/matches/",
                        "title": "Add a match to a match collection",
                        "encoding": "json",
                        "method": "POST",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "description": "Match information",
                                    "type": "string"
                                },
                                "team1": {
                                    "description": "Name of the first team",
                                    "type": "string"
                                },
                                "team2": {
                                    "description": "Name of the second team",
                                    "type": "string"
                                },
                                "date": {
                                    "description": "Date when the match was played",
                                    "type": "string"
                                },
                                "team1_points": {
                                    "description": "Final points of the first team",
                                    "type": "integer",
                                    "default": null
                                },
                                "team2_points": {
                                    "description": "Final points of the second team",
                                    "type": "integer",
                                    "default": null
                                },                                
                            },
                            "required": ["team1", "team2", "date"]
                        }
                    },
                },
                "items": [
                    {
                        "team1": "HubbaBubba",
                        "team2": "JeeJee",
                        "date": "24.6.2018",
                        "team1_points": null,
                        "team2_points": null,
                        "@controls": {
                            "self": {
                                "href": "/api/matches/1/"
                            }, 
                            "profile": {
                                "href": "/profiles/matches/"
                            }
                        },
                    }, 
                    {
                        "team1": "Palikat",
                        "team2": "Laatikot",
                        "date": "24.6.2018,
                        "team1_points": null,
                        "team2_points": null,
                        "@controls": {
                            "self": {
                                "href": "/api/matches/2/"
                            },
                            "profile": {
                                "href": "/profiles/matches/"
                            }
                        }
                    }
                ]
            }
            
### Add match [POST]

+ Relation: add-match
+ Request (application/json)

    + Headers

            Accept: application/vnd.mason+json
        
    + Body
    
            {
                "team1": "Omenat",
                "team2": "Banaanit",
                "date": "5.5.2018",
                "team1_points": null,
                "team2_points": null,
                "@controls": {
                    "self": {
                        "href": "/api/matches/3/"
                    }
                }
            }

+ Response 201

    + Headers
    
            Location: /api/matches/3/

+ Response 400 (application/vnd.mason+json)

        The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent release date.

+ Response 415 (application/vnd.mason+json)

        The client did not use the proper content type, or the request body was not valid JSON.

## Match [/api/matches/{id}/]

This resource represents a single match, as identified by the matche`s unique id. It includes the list of tracks on the album in addition to the album's own metadata. Individual tracks are usually only visited when modifying their data. They use the [Track Profile](/reference/profiles/track-profile).

+ Parameters

    + id (integer) - matche`s unique id (id)

### Match information [GET]

Get the match representation.

+ Relation: self
+ Request

    + Headers
    
            Accept: application/vnd.mason+json
        
+ Response 200

    + Body
    
            {
                "@namespaces": {
                    "kyykka": {
                        "name": "/kyykka_apiary/link-relations#"
                    }
                },
                "team1": "Omenat",
                "team2": "Banaanit",
                "date": "5.5.2018",
                "team1_points": null,
                "team2_points": null,
                "@controls": {
                    "author": {
                        "href": "/api/matches/3/"
                    },
                    "kyykka:matches-by": {
                        "href": "/api/matches/3/"
                    },
                    "self": {
                        "href": "/api/matches/3/"
                    },
                    "profile": {
                        "href": "/profiles/matches/"
                    },
                    "collection": {
                        "href": "/api/matches/"
                    },
                    "kyykka:matches-all": {
                        "href": "/api/matches/",
                        "title": "All matches"
                    },
                    
                    "edit": {
                        "href": "/api/matches/3/",
                        "title": "Edit this match",
                        "encoding": "json",
                        "method": "PUT",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "description": "Match`s id",
                                    "type": "string"
                                },
                                "team1": {
                                    "description": "Name of the first team",
                                    "type": "string",
                                },
                                "team2": {
                                    "description": "Name of the second team",
                                    "type": "string"
                                },
                                "date": {
                                    "description": "Date when the match was played",
                                    "type": "string",
                                },
                                "team1_points": {
                                    "description": "Final points of the first team",
                                    "type": "integer",
                                    "default": null
                                },
                                "team2_points": {
                                    "description": "Final points of the second team",
                                    "type": "integer",
                                    "default": null
                                }, 
                            },
                            "required": ["team1", "team2", "date"]
                        }
                    },
                    "kyykka:delete": {
                        "href": "/api/matches/3/",
                        "title": "Delete this match",
                        "method": "DELETE"
                    }
                },
                "items": [
                    {
                "team1": "Omenat",
                "team2": "Banaanit",
                "date": "5.5.2018",
                "team1_points": null,
                "team2_points": null,
                    "@controls": {
                        "self": {
                            "href": "/api/matches/3/"
                            }
                        }
                    }
                ]
            }
            
            
### Edit Match [PUT]

Replace the match's representation with a new one. Missing optional fields will be set to null. 

+ Relation: edit
+ Request (application/json)

    + Headers
        
            Accept: application/vnd.mason+json
        
    + Body
    
            {
                "team1": "Omenat",
                "team2": "Banaanit",
                "date": "5.5.2018",
                "team1_points": 10,
                "team2_points": 20
            }
        
+ Response 204

+ Response 400 (application/vnd.mason+json)

    The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent team points.

    + Body
    
            {
                "resource_url": "/api/matches/",
                "@error": {
                    "@message": "Invalid points format",
                    "@messages": [
                        "Points must be integers"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

+ Response 404 (application/vnd.mason+json)

    The client is trying to edit a match that doesn't exist. 

    + Body
    
            {
                "resource_url": "/api/matches/",
                "@error": {
                    "@message": "Match not found",
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
                "resource_url": "/api/matches/",
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

### Delete Match [DELETE]

Deletes the match.

+ Relation: delete
+ Request

    + Headers
        
            Accept: application/vnd.mason+json
        
+ Response 204

+ Response 404 (application/vnd.mason+json)

    The client is trying to delete a match that doesn't exist. 

    + Body
    
            {
                "resource_url": "/api/matches/",
                "@error": {
                    "@message": "Match not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

# Group Throw

All of these resources use the [Throw Profile](reference/profiles/throw-profile). In error scenarios [Error Profile](reference/profiles/error-profile) is used.

## Throw Collection [/matches/{match_id}/throws/]

This is an throw collection by given match using the match id unique number.

+ Parameters

    + match_id (integer) - matches unique number
    
### List throws by match [GET]

Get a list of throws by a match.

+ Relation: throws-by
+ Request

    + Headers
    
            Accept: application/vnd.mason+json
            
+ Response 200 (application/vnd.mason+json)

    + Body
    
            {
                "@namespaces": {
                    "kyykka": {
                        "name": "/kyykka_apiary/link-relations#"
                    }
                }, 
                "@controls": {
                    "self": {
                        "href": "/api/matches/1/throws/"
                    },
                    "kyykka:throws-all": {
                        "href": "/api/throws/",
                        "title": "All throws"
                    },                    
                    "kyykka:matches-all": {
                        "href": "/api/matches/?{sortby}",
                        "title": "All matches",
                        "isHrefTemplate": true,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "sortby": {
                                    "description": "Field to use for sorting",
                                    "type": "integer",
                                    "default": "match_id",
                                }
                            },
                            "required": []
                        }
                    },
                "items": [
                    {
                        "player": "Keijo",
                        "current_match": 1,
                        "@controls": {
                            "self": {
                                "href": "/api/matches/1/throws/"
                            },
                            "profile": {
                                "href": "/profiles/matches/"
                            }
                        }
                    }
                ]        
            }

+ Response 404 (application/vnd.mason+json)

    The client is trying to retrieve list of throws for an match that doesn't exist.

    + Body
    
            
            {
                "resource_url": "/api/matches/666/throws/",
                "@error": {
                    "@message": "Match not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

## Throw [/matches/{match_id}/throws/{throw_id}/]

This resource represents a single throw, as identified by the matche`s unique id.

+ Parameters

    + throw_id (integer) - throws`s unique id (id)

### Throw information [GET]

Get the throw representation.

+ Relation: self
+ Request

    + Headers
    
            Accept: application/vnd.mason+json
        
+ Response 200

    + Body
    
            {
                "@namespaces": {
                    "kyykka": {
                        "name": "/kyykka_apiary/link-relations#"
                    }
                },
                "player": "Kekkonen",
                "points": 20,
                "match_id": 1,
                "@controls": {
                    "author": {
                        "href": "api/matches/1/throws/3/"
                    },
                    "kyykka:throws-by": {
                        "href": "/api/matches/3/"
                    },
                    "self": {
                        "href": "/api/matches/3/"
                    },
                    "profile": {
                        "href": "/profiles/throw/"
                    },
                    "collection": {
                        "href": "/api/throws/"
                    },
                    "kyykka:throws-all": {
                        "href": "/api/throws/",
                        "title": "All throws"
                    },
                    
                    "edit": {
                        "href": "api/matches/1/throws/3/",
                        "title": "Edit this match",
                        "encoding": "json",
                        "method": "PUT",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "description": "Throws`s id",
                                    "type": "integer"
                                },
                                "player": {
                                    "description": "Name of the player",
                                    "type": "string",
                                },
                                "points": {
                                    "description": "Amount of points for player",
                                    "type": "integer"
                                },
                                "match_id": {
                                    "description": "Identifying number for the match",
                                    "type": "integer",
                                },
                            },
                            "required": ["player", "points", "match_id"]
                        }
                    },
                    "kyykka:delete": {
                        "href": "api/matches/1/throws/3/",
                        "title": "Delete this throw",
                        "method": "DELETE"
                    }
                },
                "items": [
                    {
                "player": "Kekkonen",
                "points": 20,
                "match_id": 1,
                    "@controls": {
                        "self": {
                            "href": "api/matches/1/throws/3/"
                            }
                        }
                    }
                ]
            }
            
            
### Edit Throw [PUT]

Replace the throw's representation with a new one. Missing optional fields will be set to null. 

+ Relation: edit
+ Request (application/json)

    + Headers
        
            Accept: application/vnd.mason+json
        
    + Body
    
            {
                "player": "Geggonen",
                "points": 30,
                "match_id": 12,
            }
        
+ Response 204

+ Response 400 (application/vnd.mason+json)

    The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent player points.

    + Body
    
            {
                "resource_url": "/api/matches/throws/",
                "@error": {
                    "@message": "Invalid points format",
                    "@messages": [
                        "Points must be integers"
                    ]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

+ Response 404 (application/vnd.mason+json)

    The client is trying to edit a throw that doesn't exist. 

    + Body
    
            {
                "resource_url": "/api/matches/throws/",
                "@error": {
                    "@message": "Throw not found",
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
                "resource_url": "/api/matches/throws/",
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

### Delete Throw [DELETE]

Deletes the throw.

+ Relation: delete
+ Request

    + Headers
        
            Accept: application/vnd.mason+json
        
+ Response 204

+ Response 404 (application/vnd.mason+json)

    The client is trying to delete a throw that doesn't exist. 

    + Body
    
            {
                "resource_url": "/api/matches/throws",
                "@error": {
                    "@message": "Throw not found",
                    "@messages": [null]
                },
                "@controls": {
                    "profile": {
                        "href": "/profiles/error/"
                    }
                }
            }

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
                    "kyykka": {
                        "name": "/kyykka_apiary/link-relations#"
                    }
                },
                "@controls": {
                    "self": {
                        "href": "/api/players/"
                    },
                    "kyykka:players-all": {
                        "href": "/api/players/",
                        "title": "All players"
                    },
                    "kyykka:add-player": {
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
                        "team": "kiskojat",
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
                    "kyykka": {
                        "name": "/musicmeta/link-relations#"
                    }
                },
                "name": "pekka",
                "team": "kiskojat",
                "@controls": {
                    "self": {
                        "href": "/api/players/{player}/"
                    },
                    "kyykka:throws-by": {
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
                    "kyykka:delete": {
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
