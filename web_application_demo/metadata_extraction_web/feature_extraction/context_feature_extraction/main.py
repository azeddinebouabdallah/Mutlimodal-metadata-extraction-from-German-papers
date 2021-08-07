from elmoformanylangs import Embedder
import pickle
from conllu import parse # consider using parse incr

import os

import pandas as pd

import numpy as np
import pandas as pd

class ContextFeatureExtractor:
    
    def __init__(self, folder_direction, output_direction):
        # Folder direction is the direction of the pickle files generated by layout features. 
        # Therefore, it is really important to run first the layout extractor.
        self.folder_direction = folder_direction
        # output direction should be a folder
        self.output_direction = output_direction

    def word_embedding(self, pickle_file, file_name):

        with open(pickle_file, 'rb') as file:
            words_list = pickle.load(file)
            file.close()

        print(pickle_file)
        embedder = Embedder('./de.model')

        feature_vectors = embedder.sents2elmo(words_list)

        feature_vectors = np.array(feature_vectors)

        # concatinate layout features and context 

        layout_features_csv = pd.read_csv('./feature_vectors/{0}vectors.csv'.format(file_name))

        layout_features = np.array(layout_features_csv)

        feature_vectors = np.concatenate((layout_features, feature_vectors.reshape(feature_vectors.shape[0], -1)), axis=1)

        df = pd.DataFrame(data=feature_vectors)
        df.to_csv('{0}{1}.csv'.format(self.output_direction, file_name))

        with open('{0}{1}.pickle'.format(self.output_direction, file_name), 'wb') as handle:
            pickle.dump(feature_vectors, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()
            
    def get_features(self):
        # Loop through the folder of the word lists extracted by cermine.
        for file in os.scandir(self.folder_direction):
            if not os.path.exists('./feature_vectors/{0}vectors.csv'.format(file.name.split('.')[0])):
                continue
            if file.name.endswith('pickle'):
                if not os.path.exists('./word_lists/'+file.name.split('.')[0]+'csv'):
                    print('exists')
                    self.word_embedding(file.path, file.name.split('.')[0])
                    print('end')


if __name__ == "__main__":
    contextExtractor = ContextFeatureExtractor("../layout_feature_extraction/word_lists/", "../features/")
    contextExtractor.get_features()