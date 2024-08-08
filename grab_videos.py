import requests
import json


def extract_video_data(video_json):
    title = video_json["snippet"]["title"]
    link = f'https://www.youtube.com/watch?v={video_json["id"]["videoId"]}'
    description = video_json["snippet"]["description"]
    thumbnail = video_json["snippet"]["thumbnails"]["medium"]["url"]
    channelName = video_json["snippet"]["channelTitle"]
    channelLink = (
        f'https://www.youtube.com/channel/{video_json["snippet"]["channelId"]}'
    )

    video = {
        "video_selected": "False",
        "video_thumbnail": thumbnail,
        "video_title": title,
        "channel_name": channelName,
        "video_desc": description,
        "video_link": link,
        "channel_link": channelLink,
    }

    return video


def search_yt(api_key, search_phrase):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=8&order=relevance&q={search_phrase}&key={api_key}"
    json_video_info = requests.get(search_url)

    video_data = json.loads(json_video_info.text)
    raw_search_results = video_data.get("items")

    refined_results = refine_results(raw_search_results)
    return refined_results


def refine_results(raw_results):
    all_videos = []

    if raw_results != None:
        for res in raw_results:
            video_data = extract_video_data(res)
            all_videos.append(video_data)
    else:
        return None

    return all_videos


# import json
# with open('outputfile', 'w') as fout:
#     json.dump(results, fout)
