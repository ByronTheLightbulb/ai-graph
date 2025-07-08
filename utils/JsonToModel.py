from json_schema_to_pydantic import create_model

import json 

def JsonToModel(json_str:str):
    json_dict = json.loads(json_str) 
    DynamicClass =create_model(json_dict)
    return DynamicClass


if __name__=="__main__":
    
    json_str = '''{
                    "title": "DarkJokeCategories",
                    "description": "Describes three distinct categories of dark jokes.",
                    "type": "object",
                    "properties": {
                        "categories": {
                        "title": "Categories",
                        "description": "A list of distinct categories for dark jokes.",
                        "type": "array",
                        "items": {
                            "title": "JokeCategory",
                            "description": "Represents a single category of dark jokes.",
                            "type": "object",
                            "properties": {
                            "name": {
                                "title": "Name",
                                "description": "The name of the dark joke category.",
                                "type": "string"
                            },
                            "description": {
                                "title": "Description",
                                "description": "A brief description of what this category entails.",
                                "type": "string"
                            }
                            },
                            "required": [
                            "name",
                            "description"
                            ]
                        }
                        }
                    },
                    "required": [
                        "categories"
                    ],
                    "example": {
                        "categories": [
                        {
                            "name": "Death & Grief",
                            "description": "Jokes that make light of mortality, funerals, the deceased, or the process of dying and losing someone."
                        },
                        {
                            "name": "Illness & Disability",
                            "description": "Jokes that humorously address chronic illnesses, physical disabilities, or mental health issues, often pushing boundaries."
                        },
                        {
                            "name": "Social & Historical Taboos",
                            "description": "Jokes that touch upon sensitive social issues (e.g., racism, poverty) or historical tragedies (e.g., genocide, natural disasters), often for shock value or critique."
                        }
                        ]
                    }
                    }
                    '''
    c = JsonToModel(json_str)
    print(c) 