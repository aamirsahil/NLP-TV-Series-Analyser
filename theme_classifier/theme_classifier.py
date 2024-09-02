from transformers import pipeline

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

