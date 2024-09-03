from transformers import pipeline
from nltk.tokenize import sent_tokenize
import numpy as np
import pandas as pd
import nltk

import os
import sys
import pathlib

nltk.download('punkt')
nltk.download('punkt_tab')

folder_path = pathlib.Path(__file__).resolve()
sys.path.append(os.path.join(folder_path, '../'))
from utils import load_subtitle_dataset

class ThemeClassifier():
    def __init__(self, theme_list) -> None:
        self.model_name = "facebook/bart-large-mnli"
        self.device = 0 # if torch.cuda.is_available() else 'cpu'
        self.theme_list = theme_list
        self.theme_classifier = self.load_model()

    def load_model(self):
        theme_classifier = pipeline(
        "zero-shot-classification",
        model = self.model_name,
        device = self.device
        )

        return theme_classifier

    
    def get_theme_inference(self, script):
        # sentence tokenize
        script_sentence = sent_tokenize(script)

        # batching the sentences
        sentence_batch_size = 20
        sentence_batch = []
        for index in range(0, len(script_sentence), sentence_batch_size):
            batch = ' '.join(script_sentence[index : index + sentence_batch_size])
            sentence_batch.append(batch)

        # finding the theme by running the model
        theme_output = self.theme_classifier(
            sentence_batch,
            self.theme_list,
            multi_label=True
        )

        # wrangling the theme
        themes = {}
        for output in theme_output:
            for label,score in zip(output['labels'], output['scores']):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)

        # find mean value
        themes = {key : np.mean(np.array(value)) for key,value in themes.items()}

        return themes
    
    def get_themes(self, dataset_path, save_path=None):
        # read if save path exists
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            return df

        # load dataset
        df = load_subtitle_dataset(dataset_path)
        
        # get theme inference
        output_theme = df['script'].apply(self.get_theme_inference)
        df_theme = pd.DataFrame(output_theme.tolist())
        df[df_theme.columns] = df_theme
        
        # save to save_path
        if save_path is not None:
            df.to_csv(save_path, index=False)

        return df