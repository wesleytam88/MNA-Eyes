import requests
from Character import *
from ordered_list_iterative import *

# https://anilist.github.io/ApiV2-GraphQL-Docs/
url = 'https://graphql.anilist.co'

def create_vars(username):
    # Define query variables and values that will be used in the query request
    variables = {
        'name': username
    }
    return variables

query = '''
query ($name: String) {             # Define variables to be used in query (id)
    anime: MediaListCollection(userName: $name, type: ANIME) {
        lists {
            status                  # WATCHING, REWATCHING, COMPLETED, etc.
            entries {
                media {
                    title {
                        english
                        romaji
                    }
                    characters(role: MAIN) {
                        nodes {
                            name {
                                full
                                alternative
                                alternativeSpoiler
                            }
                            image {
                                large
                            }
                        }
                    }
                }
            }
        }
    }
}
''' 

def character_list(username):
    '''Returns a hash table of a user's characters from the animes they watch.
    Only stores main characters (as determined by AniList) and characters from
    certain lists (completed and rewatching)'''
    char_list = {}
    variables = create_vars(username)
    response = requests.post(url, json={'query':query, 'variables':variables})
    response = response.json()    # Turn json into hash table
    acceptedStatusLists = ["REWATCHING", "COMPLETED"]

    data = response.get('data')
    anime = data['anime']
    if anime == None:
        # Query failure (ex. nonexistent user, no anime completed)
        return None
    lists = anime.get('lists')
    for listType in lists:  # Ex. Completed, Watching, Custom Lists, etc.
        status = listType['status']
        if status in acceptedStatusLists:
            for entries in listType['entries']:
                media = entries['media']
                titles = media['title']
                if titles['english'] != None:
                    title = titles['english']
                else:
                    title = titles['romaji']
                characters = media['characters']
                if len(characters['nodes']) == 0:
                    # Anime has no main characters
                    break
                nodes = characters['nodes']  # characters['nodes'] is a list
                for node in nodes:
                    names = node['name']
                    full_name = names['full']
                    alt_names = names['alternative']
                    alt_names += names['alternativeSpoiler']
                    image = node['image']
                    img_link = image['large']
                    if full_name not in char_list.keys():
                        # Use names as keys, may skip chars if same full name
                        # May not use most popular title char was in as title
                        char_list[full_name] = Character(full_name, alt_names, img_link, title)
    return char_list