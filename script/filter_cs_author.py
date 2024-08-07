import os

current_dir = os.path.dirname(__file__)  # Directory of the current script
setup_path = os.path.join(current_dir, 'setup.py')

with open(setup_path) as file:
    exec(file.read())

def main():

    print('*** RUNNING SCRIPT filter_cs_authors.py ***')
    print()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Loading of data, time:", current_time)

    # load data from existing dataframe
    data_types = {
                'Full name' : str
                }

    converters = {
                'OpenAlex ID' : pre.tranform_to_list_of_string,
                'ORCID' : pre.tranform_to_list_of_string,
                'Works count' : pre.tranform_to_list_of_int
    }

    df_author = pd.read_csv('Data/authorID.csv', dtype=data_types, converters=converters)
    # adding column with number of results
    number_of_results = df_author['OpenAlex ID'].apply(len)
    df_author['Number of results'] = number_of_results

    # define the dataframe with disambiguated authors
    df_disambiguated = df_author[(df_author['Number of results'] > 1)]

    df_cleaned= df_author.copy()
    df_cleaned['Computer science works'] = [None]*len(df_author)
    filename = 'authorID_cleaned.csv.gz'
    filepath = './Data/'
    chunk_size = 100

    current_time = (datetime.now()).strftime("%H:%M:%S")
    print("Start author data retreival, time:", current_time)

    for j in range(0, len(df_disambiguated), chunk_size):

        chunk = df_disambiguated[j:j+chunk_size]['OpenAlex ID']

        for index, possible_authors in chunk.items():

            number_cs_works = []
            cs_authors = []

            for candidate in possible_authors:
                
                filtered_authors = q.filter_authors_for_field(candidate)
                if filtered_authors is not None:
                    cs_authors.append(filtered_authors[0])
                    number_cs_works.append(filtered_authors[1])
            
            df_cleaned.at[index, 'OpenAlex ID'] = cs_authors
            df_cleaned.at[index, 'Computer science works'] = number_cs_works
        
        # saving and overwriting the dataframe every chunk
        df_cleaned.to_csv(os.path.join(filepath, filename), index=False, compression='gzip')

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("The file is now saved, time:", current_time)

if __name__ == '__main__':
    main()