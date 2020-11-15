# markovscope-api

Web service to generate horoscopes in Russian (other languages planned for future versions). It uses Markov Chains to generate sequence of words and Yandex.Translate API to enhance texts and make them more “consistent”.

[Try Demo](https://t.me/markovscope_bot)

This project started as a joke, but actually has commercial application.

**NOTE:** If you need collected data set please e-mail me (look for contact e-mail address [on my profile](https://github.com/tomakado)) or DM me via [Telegram](https://t.me/tomakado).

# Table of Contents

1. [Examples](#examples)
   1. [Daily horoscope for all sun signs](#daily-horoscope-for-all-sun-signs)
   2. [Daily horoscope for single sun sign](#daily-horoscope-for-single-sun-sign)
   
2. [Configuration and Dependencies](#configuration-and-dependencies)
   1. [Environment](#environment)
   
3. [Run](#run)
1. [Running on host machine](#running-on-host-machine)
   
2. [Running with Docker and/or Docker Compose](#running-with-docker-andor-docker-compose)
   
4. [TODOs](#todos)

# Examples

## Daily horoscope for all sun signs
URL `http://localhost:8000/` gives result:

```json
{
    "result": [
        {
            "sun_sign": "aries",
            "text": "Овнам сегодня лучше отказаться от активных развлечений. День предлагает разумную экономию и помогает вам тратить деньги строго в рамках бюджета."
        },
        {
            "sun_sign": "taurus",
            "text": "Сегодня мало что изменится в близком окружении Тельца. Звезды советуют не делать из этого обстоятельства драму и пока делать только то, что происходит."
        },
        {
            "sun_sign": "gemini",
            "text": "В начале дня Близнецам лучше провести этот день без принятия окончательных решений, например, покупки тура, выбора рейса или бронирования гостиницы."
        },
        {
            "sun_sign": "cancer",
            "text": "Сегодня Раки смогут успешно преодолевать препятствия и устранять противоречия, в том числе ненужные разговоры и излишнюю откровенность."
        },
        {
            "sun_sign": "leo",
            "text": "Для Львова день начнется с момента инерции и лени, зависимости от повседневной рутины, не исключена необходимость оставаться дома. Не стоит начинать важные переговоры, назначать романтическое свидание."
        },
        {
            "sun_sign": "virgo",
            "text": "Для девственниц день пролетит незаметно, если они будут страстными. В этом случае вы можете быть чрезмерно внушаемым и рисковать, принимая то, что вы хотите, за реальность."
        },
        {
            "sun_sign": "libra",
            "text": "Сегодня Весы пригодятся для эффективности и воинственности. Вам будет легче решать насущные задачи, если вы обладаете пытливым умом, а жизнь даст вам отличный повод для познавательной экскурсии или исследования."
        },
        {
            "sun_sign": "scorpio",
            "text": "Скорпионы до вечера наслаждаются удачным для себя сочетанием событий. В это время вы сможете проявить себя перед нужными людьми."
        },
        {
            "sun_sign": "sagittarius",
            "text": "Сегодня звезды укажут Стрельцам ключевые приоритеты и ценности, в том числе нюансы семейной истории, происхождения и воспитания."
        },
        {
            "sun_sign": "capricorn",
            "text": "Козероги сегодня хотят \"жить полной жизнью\", например, дать больше свободы чувствам. Скорее всего, вы решитесь на импровизированное мероприятие не ради себя, а чтобы порадовать окружающих."
        },
        {
            "sun_sign": "aquarius",
            "text": "Сегодня Водолеи и их окружение подвержены влиянию эмоций. Это может напоминать вам о переутомлении, болезни, служебных обязанностях или домашних делах."
        },
        {
            "sun_sign": "pisces",
            "text": "Сегодня звезды не советуют Рыбам копировать чужие эксперименты. Это также не самый лучший день для личных и деловых встреч, семейных мероприятий. Не стоит заниматься хозяйственными и хозяйственными вопросами, ремонтом, покупками, обменом, поиском жилья."
        }
    ],
    "status": "ok"
}
```

## Daily horoscope for single sun sign
URL `http://localhost:8000/sagittarius` gives result:

```json
{
    "status": "ok",
    "sun_sign": "sagittarius",
    "text": "Сегодня звезды покажут Стрельцам свои ключевые приоритеты и ценности, в том числе в плане финансов и безопасности."
}
```

# Data format

Data set must be CSV table without header and with following schema:

| Sun Sign  | Date         | Text                              |
| --------- | ------------ | --------------------------------- |
| `sunsign` | `yyyy-mm-dd` | Text for given sun sign and date. |

`sunsign` is name of sun sign in lower case.

# Configuration and Dependencies

Service requires Yandex.Cloud OAuth token and Folder ID to enhance text. `YandexTranslateTextEnhancer` will be optional in future releases, but is required to use now.

## Environment

| Variable         | Type    | Comment                                                      |
| ---------------- | ------- | ------------------------------------------------------------ |
| `LISTEN_HOST`    | string  | Default: `0.0.0.0`                                           |
| `LISTEN_PORT`    | integer | Default: `8000`                                              |
| `YC_OAUTH_TOKEN` | string  | Yandex.Cloud OAuth token                                     |
| `YC_FOLDER_ID`   | string  | Yandex.Cloud Folder ID                                       |
| `DATA_PATH`      | string  | Path to CSV file with data set.                              |
| `DEBUG_ENABLED`  | mixed   | Determines if should service log messages at `debug` level. Possible values: `1`, `true`, `yes`, `on`. Other values considered as `False`. |

# Run

## Running on host machine

1. (Create and) activate virtual environment;

2. Make sure you've set all required environment variables;

3. Run service with command:

   ```bash
   $ (venv) python run.py
   ```
   
## Running with Docker and/or Docker Compose

To run the service with Docker:

1. Pull the latest image:

   ```bash
   docker pull ghcr.io/tomakado/markovscope-api:<current_latest_version>
   ```

   or

   ```bash
   docker pull ghcr.io/tomakado/markovscope-api:latest
   ```
2. Start container:

   With environment variables from file:

   ```bash
   docker run --env-file .env -d -p 8000:8000 ghcr.io/tomakado/markovscope-api 
   ```
   
   or with environment variables set in command:
   
   ```bash
   docker run -e YC_OAUTH_TOKEN=<token> -e YC_FOLDER_ID=<folder_id> -e DATA_PATH=<data_path> -d -p 8000:8000 ghcr.io/tomakado/markovscope-api
   ```

If you want to run service with Docker Compose, take a look at [example of docker-compose.yml](docker-compose.yml).

# TODOs

* Complete TODOs in source code :)
* Make `YandexTranslateTextEnhancer` optional;
* Add alternative text enhancers;
* Add support for more languages;
* Cover code with tests.