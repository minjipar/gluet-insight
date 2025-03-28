import instaloader
from datetime import datetime, timedelta
import pandas as pd

def crawl_gluort_hashtag(username, password, days=7):
    L = instaloader.Instaloader(download_pictures=False, download_videos=False)
    L.login(username, password)

    today = datetime.now()
    since_date = today - timedelta(days=days)

    posts = []
    for post in instaloader.Hashtag.from_name(L.context, "글루어트").get_posts():
        post_date = post.date_local
        if post_date < since_date:
            break
        caption = post.caption or "(캡션 없음)"
        url = f"https://www.instagram.com/p/{post.shortcode}/"
        thumb = post.url
        posts.append({
            "date": post_date.strftime('%Y-%m-%d'),
            "caption": caption.strip(),
            "link": url,
            "image": thumb
        })

    pd.DataFrame(posts).to_csv("posts.csv", index=False)
    print(f"{len(posts)}개 게시물 저장 완료!")

if __name__ == "__main__":
    crawl_gluort_hashtag("mz00zm93", "omzomz0039")
