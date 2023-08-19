import pickle
import pandas as pd
import os

csv_dataset_path = "data/dataset.csv"
pkl_file_path = "data/serialised_matrix_text.pkl"


def load_csv(path=csv_dataset_path):
    df = pd.read_csv(path)
    return df


def save_matrix_to_local(tfidf_matrix, tfidf_vectorizer, pkl_file_path=pkl_file_path):
    """
    Serialise data set from variable to pkl file
    :param matrix: data set variable to serialise
    :param pkl_file_path: name of file to save data set
    :return: None
    """
    data = {"tfidf_matrix": tfidf_matrix, "tfidf_vectorizer": tfidf_vectorizer}

    with open(pkl_file_path, 'wb') as f:
        pickle.dump(data, f)


def load_matrix_from_local(pkl_file_path=pkl_file_path):
    """
    Deserialise data set from pkl file to load in variable
    :param path: path of the pkl file
    :return tfidf matrix 
    """
    if not os.path.exists(pkl_file_path):
        """
        just to insure no error is raised in run time
        and we always have datset.csv in environment 
        so for the first run we can create a matrix 
        """
        convert_and_save()

    with open(pkl_file_path, 'rb') as file:
        data = pickle.load(file)

    return data["tfidf_matrix"], data["tfidf_vectorizer"]


def convert_to_matrix(data_set=csv_dataset_path):
    """
    Convert data set to tfidf matrix
    :param data_set: csv data set path to convert
    :return: tfidf matrix

    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    df = pd.read_csv(data_set)
    df.fillna(value='None', inplace=True)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        df['product_name'] + " " + df["brand"]+" " + df["description"]+" " + df["category"])

    return tfidf_matrix, tfidf_vectorizer


def convert_and_save():
    """
    Convert data set to tfidf matrix and save
    :return none
    """

    print("making tfidf format")
    tfidf_matrix, tfidf_vectorizer = convert_to_matrix(csv_dataset_path)
    print("saving the pkl file")
    save_matrix_to_local(tfidf_matrix, tfidf_vectorizer)
    print("done")
