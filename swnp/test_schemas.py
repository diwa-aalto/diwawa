ProjectSchema = {
        "type": ["object", "number"],
        "properties": {
            "id": {
                "description": "The unique identifier",
                "type": ["number","string"]
            },
            "name": {
                "type": "string"
            },
            "company": {
                "type": ["number","string"]
            },
            "password": {
                "type": [ "string", "null" ],
                "minLength": 0,
                "blank": True
            },
            "dir": {
                "type": "string"
            }
        }
    }
NodesJsonSchema = {
    "type":"array",
    "$schema": "http://json-schema.org/draft-03/schema",
    "items": {
            "type":"object",
            "properties":{
                "img": {
                    "type":"string"
                },
                "node": {
                    "type":"object",
                    "properties":{
                        "id": {
                            "type":"number"
                        },
                        "ip": {
                            "type":"number"
                        },
                        "mac": {
                            "type":"string"
                        },
                        "name": {
                            "type":"string"
                        },
                        "pgm_group": {
                            "type":"number"
                        },
                        "responsive": {
                            "type":"number"
                        },
                        "screens": {
                            "type":"number"
                        },
                        "time": {
                            "type":"string"
                        },
                        "user": {
                            "type":"null"
                        },
                        "wos_id": {
                            "type":"number"
                        }
                    }
                }
            
        }
    }
}

ActivityJsonSchema = {
    "type":"object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "properties":{
        "project":ProjectSchema,
        "room": {
            "type":"number",
            "required":False
        },
        "session": {
            "type":["number","object"],
            "properties":{
                "endtime": {
                    "type":["string","null"],
                    "required":False
                },
                "id": {
                    "type":"number",
                    "required":False
                },
                "name": {
                    "type":["string","null"],
                    "required":False
                },
                "previous_session": {
                    "type":["number","null"],
                    "required":False
                },
                "project": {
                    "type":"number",
                    "required":False
                },
                "starttime": {
                    "type":"string"
                }
            }
        },
        "status": {
            "type":"string"
        }
    }
}

ProjectJsonSchema = {
    "type":"object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "properties":{
        "events": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "desc": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        },
                        "time": {
                            "type":"string"
                        },
                        "title": {
                            "type":"string"
                        }
                    }
                }
            

        },
        "fileactions": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "action__name": {
                            "type":"string"
                        },
                        "action_time": {
                            "type":"string"
                        },
                        "file__id": {
                            "type":"string"
                        },
                        "file__path": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        }
                    }
                }
            

        },
        "project": ProjectSchema,
        "sessions": {
            "type":"array",
            "items":
                {
                    "type":"object",
                    "properties":{
                        "endtime": {
                            "type":"string"
                        },
                        "id": {
                            "type":"string"
                        },
                        "name": {
                            "type":"string"
                        },
                        "starttime": {
                            "type":"string"
                        }
                    }
                }
        }
    }
}

ProjectsJsonSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Projects set",
    "type": "array",
    "items": ProjectSchema
}