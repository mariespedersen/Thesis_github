import os

current_dir = os.path.dirname(__file__)  # Directory of the current script
setup_path = os.path.join(current_dir, 'setup.py')

with open(setup_path) as file:
    exec(file.read())


BASE_URL = 'https://api.openalex.org/'
MAIL = 'elsa@itu.dk'
mail = f'&mailto={MAIL}'


def API_query(complete_url):
    '''
    Given a complete url query OpenAlex API handiling API failures.
    Return the response json file.
    '''
    failure=False

    try:
            response = requests.get(complete_url)
            response.raise_for_status()
            response_json = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed for: {e}")
        failure = True
    except ValueError as e:
        print(f"JSON decoding failed for: {e}")
        failure = True
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decoding failed for: {e}")

    if failure:
        return failure
    else:
        return response_json
    

def get_author_works(author_id):
    '''
    Retrieve all the work of an author given the OpenAlex ID
    '''
    works = []
    next_cursor = "*"
    ENDPOINT = 'works'
    while True:
        filter = f'?filter=author.id:{author_id}&per-page=200&cursor={next_cursor}'
        works_url = BASE_URL + ENDPOINT + filter + mail
        response_json = q.API_query(works_url)
        
        if response_json is True:
            break
        
        works.extend(response_json['results'])
        
        # Check if there's a next page
        if 'meta' in response_json and 'next_cursor' in response_json['meta']:
            next_cursor = response_json['meta']['next_cursor']
         
            if next_cursor is None:
                break
        else:
            break
    
    return works


def filter_authors_for_field(author_id, field_id='https://openalex.org/fields/17'):
    '''
    Given the OpenAlex ID of the author, return the author's ID and the number of works classifiend in a specific field.
    The classification is done based on the primary_topic (topic with higest score).
    The autor is considered belonging to the given filed if at least one of its works belong to the field.

    OpenAlex follows this hierarchy of classifications of works: domain > field > subfiled > topic
    '''
    ENDPOINT = 'works'
    
    next_cursor = "*"
    works_topics = [] # contains the topics for all the works of the searche author
    works_in_the_field = 0

    while True:
        filter = f'?filter=author.id:{author_id}&select=topics&per-page=200&cursor={next_cursor}'
        works_url = BASE_URL + ENDPOINT + filter + mail
        response_json = q.API_query(works_url)

        if response_json is True:
            break

        works_topics.extend(response_json['results'])
        
        # Check if there's a next page
        if 'meta' in response_json and 'next_cursor' in response_json['meta']:
            next_cursor = response_json['meta']['next_cursor']
        
            if next_cursor is None:
                break
        else:
            break

    # obtaining the primary topic for each work
    primary_topic = []
    for wt in works_topics:

        if len(wt) != 0:

            if len(wt['topics']) != 0:
                primary_topic.append(wt['topics'][0])
            else:
                primary_topic.append(None)
        else:
            primary_topic.append(None)

    # obtaining the field for each work
    fields = [work['field']['id'] if work is not None else None for work in primary_topic]

    works_in_the_field = fields.count(field_id)

    if works_in_the_field >= 1:
        return author_id, works_in_the_field