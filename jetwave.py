import mysql.connector
from mysql.connector import errorcode
import requests
import time


config = {
    'user': 'jetwaveuser',
    'password': 'mGPCi0P9byMe6FdB',
    'host': 'localhost',  # Możesz zmienić host na odpowiedni dla Twojej bazy danych
    'port': 3316,
    'database': 'jetwave',
}

connection = mysql.connector.connect(**config)
if connection.is_connected():
    print("Pomyślnie połączono z bazą danych")


# Klucz API (zastąp 'YOUR_API_KEY' własnym kluczem)
api_key = 'AIzaSyCS3pYmNkODySpVQnn1CHDuLJA30Z_E6EA'

# Identyfikator kanału, z którego chcesz pobrać filmy (zastąp 'CHANNEL_ID' właściwym ID kanału)
channel_id = 'UCACQpRUoTW-yYM8uYRTmYRQ'

url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=11'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        url2 = f'https://www.youtube.com/shorts/{video_id}'
        
        response2 = requests.get(url2)
        time.sleep (2)
        url3 = response2.url
                    
        current_url = response2.url   
        #response3 = requests.get(url3)
        #time.sleep (1)
        #current_url = response3.url
        if "watch" in current_url :
            parts = video_title.split(" - ")
            artist_name = parts[0]
            track_name = parts[1].split(" (")[0]
            print(f"Artysta: {artist_name}")
            print(f"Utwór: {track_name}")
            url_stat = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
            response_stat = requests.get(url_stat)
            data_stat = response_stat.json()
            view_count = data_stat['items'][0]['statistics']['viewCount']
            like_count = data_stat['items'][0]['statistics']['likeCount']
            fav_count = data_stat['items'][0]['statistics']['favoriteCount']
            comment_count = data_stat['items'][0]['statistics']['commentCount']
            print(f'Viewsy: {view_count}  Likey: {like_count}  Ulubione: {fav_count}  komentarze: {comment_count} \n')
            
            
            query = f"SELECT id FROM jetwave WHERE youtubeid = '{video_id}'"
            dodaj = connection.cursor()
            dodaj.execute(query)
            result = dodaj.fetchone()

            if result is not None:
                # Znaleziono rekord, więc go zaktualizuj
                query = (f"UPDATE jetwave SET title = '{video_title}', artist_name = '{artist_name}', "
                         f"track_name = '{track_name}', views_count = '{view_count}', likes_count = '{like_count}', "
                         f"favourite_count = '{fav_count}', comments_count = '{comment_count}' WHERE id = {result[0]}")
            else:
                # Nie znaleziono rekordu, więc wstaw nowy
                query = (f"INSERT INTO jetwave (youtubeid, title, artist_name, track_name, views_count, likes_count, "
                         f"favourite_count, comments_count) VALUES ('{video_id}', '{video_title}', '{artist_name}', "
                         f"'{track_name}', '{view_count}', '{like_count}', '{fav_count}', '{comment_count}')")

            # Wykonaj zapytanie
            dodaj.execute(query)
            connection.commit()
            dodaj.close()
            
        
            
        
        

else:
    print("Błąd podczas pobierania danych z YouTube API.")
    

connection.close()
