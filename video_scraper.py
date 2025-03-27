from youtube_transcript_api import YouTubeTranscriptApi

video_id = "2spTnAiQg4M"
transcript = YouTubeTranscriptApi.get_transcript(video_id)
for t in transcript:
    print(t['text'])