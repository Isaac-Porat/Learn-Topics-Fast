import json
from functions.chatModel import Model
from functions.youtubeFunctions import Scraper
from functions.markdown import saveMarkdown

with open('prompts/general.json', 'r') as file:
  prompt_data = json.load(file)

if __name__ == '__main__':
  scraper = Scraper('https://www.youtube.com/watch?v=UBaJzkfW44U&t=22s')
  file = scraper.get_video_transcript_to_file()
  print(file)

  model = Model(file)
  index = model.load_index()
  query_response = model.query(index, prompt=str(prompt_data), summary_of_data="Educational YouTube video.")
  print(query_response)

  file_path = saveMarkdown(query_response)
  print(file_path)