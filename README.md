# Beauty City
Service for a beauty salon

## About

Service allows:
* sign up for the procedure at a convenient time;
* sign up without a call, no need to communicate with people;
* automate the acceptance of orders.
* pay order
* change profile information

## Website example

You can see this project [here](https://etokosmo.ru/).

* Login

![image](https://user-images.githubusercontent.com/93794917/208603947-920f279b-9c9d-41e0-876d-a8e8edbee4e5.png)
![image](https://user-images.githubusercontent.com/93794917/208605518-cd4d7a47-0ab1-4201-9ef4-ce12338fa199.png)
* Service selection

![image](https://user-images.githubusercontent.com/93794917/208604297-8f0df77a-31b9-4ca5-8deb-56d316414068.png)
![image](https://user-images.githubusercontent.com/93794917/208604402-652f0c3a-5d4d-4bd5-9cac-75b23e744649.png)

* Profile

![image](https://user-images.githubusercontent.com/93794917/208604934-bf4b8751-92c6-4f8d-a90b-a2fd46b08b9b.png)
![image](https://user-images.githubusercontent.com/93794917/208604994-34940cef-2a67-4536-bdef-ded1c041a5f0.png)

* Payment

![image](https://user-images.githubusercontent.com/93794917/208605115-a4dc6ba2-e50a-42ac-bce7-139eacb643df.png)
![image](https://user-images.githubusercontent.com/93794917/208605214-888c6129-3403-4897-b2d4-04f9e1756da2.png)


## Configurations

* Python version: 3.10
* Libraries: [requirements.txt](https://github.com/etokosmo/beauty_city/blob/main/requirements.txt)

## Launch

### Local server

- Download code
- Through the console in the directory with the code, install the virtual environment with the command:
```bash
python3 -m venv env
```

- Activate the virtual environment with the command:
```bash
source env/bin/activate
```

- Install the libraries with the command:
```bash
pip install -r requirements.txt
```

- Write the environment variables in the `.env` file in the format KEY=VALUE

`SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

`ALLOWED_HOSTS` - A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.

`DEBUG` - A boolean that turns on/off debug mode. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py).

`DATABASE_URL` - URL to db. For more information check [this](https://github.com/jazzband/dj-database-url).

`STRIPE_PUBLIC_KEY` - Stripe public API key. For more information check [this](https://stripe.com/docs/keys).

`STRIPE_SECRET_KEY` - Stripe secret API key. For more information check [this](https://stripe.com/docs/keys).

`TELEGRAM_ACCESS_TOKEN` - Telegram Bot Token. You can get it here [BotFather](https://telegram.me/BotFather).

`TELEGRAM_CHAT_ID` - Chat ID to send passcode to login. Your BOT must be in chat and have access to send messages.


- Create your database with the command:
```bash
python manage.py makemigrations
python manage.py migrate
```

- Run local server with the command (it will be available at http://127.0.0.1:8000/):
```bash
python manage.py runserver
```
