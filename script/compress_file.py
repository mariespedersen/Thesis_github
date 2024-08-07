import os

current_dir = os.path.dirname(__file__)  # Directory of the current script
setup_path = os.path.join(current_dir, 'setup.py')

with open(setup_path) as file:
    exec(file.read())

def main():

    print('*** RUNNING SCRIPT compress_file.py ***')
    print()

    # load the dataframe
    data_types = {
              'Full name' : str
             }

    converters = {
                    'OpenAlex ID' : pre.tranform_to_list_of_string,
                    'ORCID' : pre.tranform_to_list_of_string,
                    'Works count' : pre.tranform_to_list_of_int
        }

    df_author = pd.read_csv('Data/authorID.csv', dtype=data_types, converters=converters)

    filepath='./Data/'
    filename='authorID.csv.gz'
    df_author.to_csv(os.path.join(filepath, filename), index=False, compression='gzip')


if __name__ == '__main__':
    main()