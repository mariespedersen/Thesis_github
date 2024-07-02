import os

current_dir = os.path.dirname(__file__)  # Directory of the current script
setup_path = os.path.join(current_dir, 'setup.py')

with open(setup_path) as file:
    exec(file.read())


def tranform_to_list_of_string(data):

    data = data.replace("'", "").strip("[").strip("]").replace(" ", "")
    converted_data = data.split(",")
    converted_data = [None if i == 'None' else np.nan if i == 'nan' else i for i in converted_data]

    return converted_data

def tranform_to_list_of_int(data):

    data = data.replace("'", "").strip("[").strip("]")
    convetred_data = data.split(",")
    #most likely this is deleting all the None, this is not what I want
    convetred_data = [None if i == 'None' else np.nan if i == 'nan' else int(i) for i in convetred_data]

    return convetred_data


def filter_authors_for_field(author_id, field_id='https://openalex.org/fields/17'):

    BASE_URL = 'https://api.openalex.org/'
    ENDPOINT = 'works'
    MAIL = 'elsa@itu.dk'
    mail = f'&mailto={MAIL}'
    
    next_cursor = "*"
    works_topics = [] # contains the topics for all the work of the searche author
    cs_works = 0

    while True:
        filter = f'?filter=author.id:{author_id}&select=topics&per-page=200&cursor={next_cursor}'
        works_url = BASE_URL + ENDPOINT + filter + mail
        response = requests.get(works_url)
        response.raise_for_status()
        response_json = response.json()
        works_topics.extend(response_json['results'])
        
        # Check if there's a next page
        if 'meta' in response_json and 'next_cursor' in response_json['meta']:
            next_cursor = response_json['meta']['next_cursor']
         
            if next_cursor is None:
                break
        else:
            break
    
    for works_topic in works_topics:
        fields = [field_id['field']['id'] for field_id in works_topic['topics']]
    
        if any(field  == field_id for field in fields):
            cs_works += 1

    if cs_works >= 1:
        return author_id, cs_works