from glob import glob
import pandas as pd

def load_subtitle_dataset(dataset_path):

  subtitles_paths = glob(dataset_path)

  scripts = []
  episodes = []

  for path in subtitles_paths:
    episode = int(path.split('-')[-1].split('.')[0].strip())
    with open(path) as file:
      lines = file.readlines()
      lines = lines[27:]
      lines = [','.join(line.split(',')[9:]) for line in lines]

    lines = [line.replace('\\N', ' ') for line in lines]
    script = ' '.join(lines)

    scripts.append(script)
    episodes.append(episode)

  df = pd.DataFrame.from_dict({'episode' : episodes, 'script' : scripts})

  return df