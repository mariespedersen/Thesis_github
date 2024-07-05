import os

current_dir = os.path.dirname(__file__)  # Directory of the current script
setup_path = os.path.join(current_dir, 'setup.py')

with open(setup_path) as file:
    exec(file.read())


def main():

    print('*** RUNNING SCRIPT get_citation.py ***')
    print()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Loading of data, time:", current_time)
    
    # load data
    df_invited = pd.read_csv('Data/factInvited.csv')
    df_proceedings = pd.read_csv('Data/factProceedings.csv')

    df = pd.concat([df_invited, df_proceedings], ignore_index=True)
    pd.set_option('display.max_rows', 15)

    # consider just unique name
    full_name = df['Full name'].unique()
    
    BASE_URL = 'https://api.openalex.org/'
    ENDPOINT = 'authors'
    MAIL = 'elsa@itu.dk'
    mail = f'&mailto={MAIL}'

    current_time = (datetime.now()).strftime("%H:%M:%S")
    print("Start author data retreival, time:", current_time)

    chunk_size = 100

    # creating an empty dataframe
    columns = ['Full name', 'OpenAlex ID', 'ORCID', 'Works count']
    df_author_id =  pd.DataFrame({col: [None]*len(full_name) for col in columns})

    for j in range(0, len(full_name), chunk_size):

        chunk = full_name[j:j+chunk_size]
        ids = []
        orcids = []
        works_count = []
        results = []
        failure = False

        for i in chunk:

            filter = f'?search={i}'
            complete_url = BASE_URL + ENDPOINT + filter + mail
            
            try:
                response = requests.get(complete_url)
                response.raise_for_status()
                response_json = response.json()
                author_data = response_json['results']

            except requests.exceptions.RequestException as e:
                print(f"Request failed for {i}: {e}")
                failure = True
                continue
            except ValueError as e:
                print(f"JSON decoding failed for {i}: {e}")
                failure = True
                continue
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSON decoding failed for {i}: {e}")
                failure = True
                continue

            results.append(len(author_data))

            # API failures
            if failure:

                # nan value is manually add to the arrays
                works_count.append([float('nan')])
                ids.append([float('nan')])
                orcids.append([float('nan')])

            # no results found
            elif len(author_data) == 0:

                works_count.append([None])
                ids.append([None])
                orcids.append([None])

            # found only one results
            elif len(author_data) == 1:

                works_count.append([author_data[0]['works_count']])
                ids.append([author_data[0]['id']])
                orcids.append([author_data[0]['orcid']])

            # found more results
            else:
                
                # store a list with the works count for every result
                works_count.append([author_data[result]['works_count'] for result in range(len(author_data))])
                # store a list with the ids for every result
                ids.append([author_data[result]['id'] for result in range(len(author_data))])
                # check on the orcid codes
                orcid_codes = [author_data[result]['orcid'] for result in range(len(author_data))]
                different_orcids = set(code for code in orcid_codes if code is not None)
                # manually adding a None value if no orcid code is found
                if not different_orcids:
                    different_orcids.add(None)

                orcids.append(list(different_orcids))

        # the dataframe is filled after every chunk to not loose data
        df_author_id['Full name'][j:j+chunk_size] = chunk
        df_author_id['OpenAlex ID'][j:j+chunk_size] = ids
        df_author_id['ORCID'][j:j+chunk_size] = orcids
        df_author_id['Works count'][j:j+chunk_size] = works_count

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("FInish biulding dataframe\nStart saving data, time:", current_time)

    # converitng the dataframe to a csv and saving it among the data
    filename = "authorID.csv" # or factProceedings.csv
    filepath = "./Data/"
    df_author_id.to_csv(os.path.join(filepath, filename), index=False)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("The file is now saved, time:", current_time)

if __name__ == '__main__':
    main()