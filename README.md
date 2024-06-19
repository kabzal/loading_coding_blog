# Loading Coding Blog

Loading Coding - это блог на Django, который включает в себя функциональность авторизации пользователей, создания и редактирования статей, раздел "Избранное", комментарии и счетчик просмотров.

## Установка

### Шаги установки

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/username/loading-coding-blog.git
    cd loading-coding-blog
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate
    # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корневой папке проекта и добавьте необходимые переменные окружения:

    ```plaintext
    SECRET_KEY = 'your_secret_key'

    EMAIL_HOST_USER = 'username@domain.com'
    EMAIL_HOST_PASSWORD = 'your_email_host_password'

    SOCIAL_AUTH_GITHUB_KEY = 'your_github_key'
    SOCIAL_AUTH_GITHUB_SECRET = 'your_github_secret'
    ```

5. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

Проект будет доступен по адресу `http://127.0.0.1:8000/`.

