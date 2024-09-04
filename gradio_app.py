import gradio as gr
from theme_classifier import ThemeClassifier

def get_themes(theme_list_str, subtitle_path, save_path):
    # run model to get themes
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    theme_df = theme_classifier.get_themes(subtitle_path, save_path)
    
    # find the sum of output themes
    output_df = theme_df.drop(['episode', 'script'], axis=1).sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    # create bar plot
    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y="Score",
        title="Series Theme",
        tooltip=['Theme', 'Score'],
        vertical=False,
        width=500,
        height=250
    )

    return output_chart



def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML('<h1>Theme Classification (Zero Shot Classifiers)</h1>')
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button = gr.Button("Get themes")
                        get_themes_button.click(get_themes, inputs=[theme_list, subtitles_path, save_path], outputs=[plot])

    iface.launch(share=True)

if __name__ == "__main__":
    main()