import asyncio
import time
import traceback

from fastapi import (
    FastAPI,
    HTTPException,
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import (
    USERNAME_SELECTOR,
    FOLLOWERS_COUNT_SELECTOR,
    FOLLOWING_COUNT_SELECTOR,
    LIKES_COUNT_SELECTOR,
    VIDEO_NAME_SELECTOR,
    COMMENT_SELECTOR,
    COMMENT_USER_SELECTOR,
    TIKTOK_URL,
)
from schemas import (
    UserResponseSchema,
    UserDataSchema,
    CommentResponseSchema,
)

app = FastAPI()


# Настройка драйвера Selenium
def get_driver() -> WebDriver:
    chrome_options = Options()

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


# Парсинг данных аккаунта TikTok (синхронная функция)
@app.get("/tiktok/{username}")
async def get_tiktok_user(username: str) -> UserResponseSchema:
    """
    Возвращает информацию о профиле пользователя
    """
    driver = get_driver()

    try:
        url = f"{TIKTOK_URL}/@{username}"

        driver.get(url)

        # Ждем элемент с именем пользователя
        user_name_element = driver.find_element(By.CSS_SELECTOR, USERNAME_SELECTOR)

        await asyncio.sleep(10)

        user_followers_element = driver.find_element(
            By.CSS_SELECTOR, FOLLOWERS_COUNT_SELECTOR
        )

        await asyncio.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        user_following_element = driver.find_element(
            By.CSS_SELECTOR, FOLLOWING_COUNT_SELECTOR
        )
        await asyncio.sleep(1)

        user_likes_element = driver.find_element(By.CSS_SELECTOR, LIKES_COUNT_SELECTOR)

        await asyncio.sleep(0.5)

        # Собираем данные
        username = user_name_element.text
        followers_count = user_followers_element.text
        following_count = user_following_element.text
        likes_count = user_likes_element.text

        return UserResponseSchema(
            username=username,
            followers_count=followers_count,
            following_count=following_count,
            likes_count=likes_count,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Ошибка парсинга: {str(e)}\n{traceback.format_exc()}",
        )

    finally:
        driver.quit()


# Пример получения комментариев к посту (необходимо указать ID поста) (синхронная функция)
@app.get("/tiktok/comments/{video_id}")
async def get_tiktok_comments(video_id: str) -> CommentResponseSchema:
    """
    Возвращает информацию о комментариях и их пользователях определенного видео
    """
    driver = get_driver()

    try:
        url = f"{TIKTOK_URL}/@username/video/{video_id}"
        driver.get(url)

        # Ждем элемент с комментариям
        video_name_element = (
            WebDriverWait(driver, 15)
            .until(
                EC.presence_of_element_located((By.CSS_SELECTOR, VIDEO_NAME_SELECTOR))
            )
            .text
        )

        for _ in range(2):  # Прокрутить 3 раза
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        await asyncio.sleep(2.5)

        comments_elements = driver.find_elements(By.XPATH, COMMENT_SELECTOR)

        await asyncio.sleep(10)

        users_data = []

        await asyncio.sleep(5.5)

        for comment in comments_elements:
            comment_text = comment.find_element(By.TAG_NAME, "span").text

            await asyncio.sleep(3.5)

            # Извлекаем пользователя
            user_link_element = comment.find_element(
                By.CSS_SELECTOR, COMMENT_USER_SELECTOR
            )

            await asyncio.sleep(5)

            username = user_link_element.text
            user_url = user_link_element.get_attribute("href")
            users_data.append(
                UserDataSchema(
                    username=username, user_url=user_url, comment=comment_text
                )
            )

        return CommentResponseSchema(
            video_id=video_id,
            users=users_data,
            video_name=video_name_element,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга: {str(e)}")

    finally:
        driver.quit()
