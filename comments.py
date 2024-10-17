import requests

URL = "https://www.tiktok.com/api/comment/list/?WebIdLastTime=1727180845&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id=7421531998088432897&browser_language=ru&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F605.1.15%20%28KHTML%2C%20like%20Gecko%29%20Version%2F17.5%20Safari%2F605.1.15&channel=tiktok_web&cookie_enabled=true&count=120&current_region=JP&cursor=0&data_collection_enabled=true&device_id=7418185203753764370&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=4&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&odinId=7418185169246831623&os=mac&priority_region=&referer=&region=KZ&screen_height=1440&screen_width=2560&tz_name=Asia%2FAlmaty&user_is_login=false&verifyFp=verify_m2c7g6oe_iO9wDbVl_sJEx_4wYl_8KYG_GKXHJlXaIBfv&webcast_language=ru-RU&msToken=q9D_OQ61XHsUaUWO40zO0cUHzSfdcqNPA2WtE9w92niVV9BJ8oYvrmtDUhFv7H27-SO4eQIw9qzgc2DX6hwOnvSzRbadaLNSLPk1hSBBgRShzXcud0HvtZGAT0lPjt4ibPW8E6FPWKx5qMpueBZXGYNa&X-Bogus=DFSzsIVYGmiANHsttQ3E6jf5-d-G&_signature=_02B4Z6wo00001OelLMwAAIDDgb8-p0unO1znpyhAAF7.fc"
response = requests.get(
    URL,
    headers={
        "User-Agent": "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/538.3"
    },
)
data = response.json()

comments = data.get("comments")

for comment in comments:
    print(f"Автор: {comment.get('user').get('nickname')}")
    print(f"Комментарий: {comment.get('text')}")
    print("\n")
