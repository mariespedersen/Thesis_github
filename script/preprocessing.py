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