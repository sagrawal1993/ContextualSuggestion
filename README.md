**TREC Contextual Suggestion** : https://sites.google.com/site/treccontext/

**Significant test file**: t-test.sh 

**Sample request query for the task**: 
```json

{
  "id": 1,  
  
  "body": {
  
    "group": "Family",
    "season": "Summer",
    "trip_type": "Holiday",
    "duration": "Weekend trip",
    "location": {
      "id": 152,
      "name": "Chicago",
      "state": "IL",
      "lat": 41.85003,
      "lng": -87.65005
    },
    
    "person": {
      "gender": "Male",
      "age": 23,
      "id": "A00126103VB6TFM3EITH9",
      
      "preferences": [
        {
          "rating": 3,
          "documentId": "TRECCS-00247633-160",
          "tags": [
            "History",
            "Museums"
          ]
        },
        {
          "rating": 2,
          "documentId": "TRECCS-00674898-160",
          "tags": [
            "Beer",
            "Cocktails",
            "Restaurants",
            "Sushi",
            "Seafood"
          ]
        },
        {
          "rating": 3,
          "documentId": "TRECCS-00018094-160",
          "tags": [
            "Theatre"
          ]
        },
        {
          "rating": 3,
          "documentId": "TRECCS-00247656-160",
          "tags": [
            "Beer",
            "Bar-hopping",
            "Cocktails",
            "Entertainment",
            "Live Music"
          ]
        },
        {
          "rating": 2,
          "documentId": "TRECCS-00018110-160",
          "tags": [
            "Food",
            "Organic Food",
            "Shopping for food",
            "Markets"
          ]
        },
        {
          "rating": 3,
          "documentId": "TRECCS-00087026-160",
          "tags": [
            "Beer",
            "Fine Dining",
            "Cocktails",
            "Restaurants",
            "History"
          ]
        },
        {
          "rating": 4,
          "documentId": "TRECCS-00087258-160",
          "tags": [
            "Art",
            "Culture",
            "Family Friendly",
            "Food",
            "Museums",
            "Art Galleries"
          ]
        }
      ]
    }
  },
  
  
  "candidates": [
    {
      "documentId": "TRECCS-00405100-152",
      "tags": [
        "Beer",
        "Bar-hopping",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00066766-152",
      "tags": [
        "Culture",
        "Entertainment",
        "Live Music",
        "Theatre"
      ]
    },
    {
      "documentId": "TRECCS-00062115-152",
      "tags": [
        "Outdoor Activities",
        "Family Friendly",
        "Parks"
      ]
    },
    {
      "documentId": "TRECCS-00405173-152",
      "tags": [
        "Tourism",
        "Culture",
        "Family Friendly",
        "History"
      ]
    },
    {
      "documentId": "TRECCS-00259846-152",
      "tags": [
        "Bar-hopping",
        "Sport"
      ]
    },
    {
      "documentId": "TRECCS-00010510-152",
      "tags": [
        "Beer",
        "Bar-hopping",
        "Cocktails",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00062723-152",
      "tags": [
        "Family Friendly",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00405075-152",
      "tags": [
        "Business"
      ]
    },
    {
      "documentId": "TRECCS-00064571-152",
      "tags": [
        "Culture",
        "Entertainment",
        "Live Music",
        "Theatre"
      ]
    },
    {
      "documentId": "TRECCS-00066672-152",
      "tags": [
        "Beer",
        "Bar-hopping",
        "Cocktails",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00010484-152",
      "tags": [
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00405702-152",
      "tags": [
        "Tourism",
        "Culture",
        "Family Friendly",
        "Food",
        "Entertainment",
        "Live Music"
      ]
    },
    {
      "documentId": "TRECCS-00061864-152",
      "tags": [
        "Beer",
        "Cocktails"
      ]
    },
    {
      "documentId": "TRECCS-00010473-152",
      "tags": [
        "Cocktails",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00065493-152",
      "tags": [
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00010463-152",
      "tags": [
        "Tourism",
        "Culture",
        "Art",
        "Family Friendly",
        "History",
        "Restaurants",
        "Museums"
      ]
    },
    {
      "documentId": "TRECCS-00259823-152",
      "tags": [
        "Cocktails",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00066353-152",
      "tags": [
        "Food",
        "Markets"
      ]
    },
    {
      "documentId": "TRECCS-00064588-152",
      "tags": [
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00405444-152",
      "tags": [
        "Tourism",
        "History",
        "Museums"
      ]
    },
    {
      "documentId": "TRECCS-00405327-152",
      "tags": [
        "Shopping"
      ]
    },
    {
      "documentId": "TRECCS-00010457-152",
      "tags": [
        "Culture",
        "Entertainment",
        "Live Music",
        "Theatre"
      ]
    },
    {
      "documentId": "TRECCS-00062393-152",
      "tags": [
        "Family Friendly",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00620829-152",
      "tags": [
        "Cafes",
        "Family Friendly"
      ]
    },
    {
      "documentId": "TRECCS-00010477-152",
      "tags": [
        "Family Friendly",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00010468-152",
      "tags": [
        "Beer",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00010486-152",
      "tags": [
        "Bar-hopping",
        "Cocktails",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00620569-152",
      "tags": [
        "Family Friendly",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00010480-152",
      "tags": [
        "Culture",
        "Restaurants",
        "Live Music"
      ]
    },
    {
      "documentId": "TRECCS-00620843-152",
      "tags": [
        "Family Friendly",
        "Restaurants"
      ]
    },
    {
      "documentId": "TRECCS-00062142-152",
      "tags": [
        "Family Friendly",
        "Restaurants",
        "Food"
      ]
    }
  ]
}
```
