from youtube_transcript_api import YouTubeTranscriptApi

class Scraper():
  def __init__(self, video_url: str):
    self.video_url = video_url
    self.transcript_downloads_path = 'downloads/transcripts'

  def get_video_url(self) -> str:
    return self.video_url

  def get_video_transcript_to_file(self) -> str:
    video_url = self.get_video_url()
    video_id = video_url.split('=')[1]

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    try:
      with open(f'{self.transcript_downloads_path}/{video_id}.txt', 'w') as f:
        for i in transcript:
          text = i['text']
          start_time = i['start']
          duration_time = i['duration']

          f.write(f'{start_time} | {text}\n')

      return f'{self.transcript_downloads_path}/{video_id}.txt'

    except Exception as e:

      print(f'Error: ', e)


