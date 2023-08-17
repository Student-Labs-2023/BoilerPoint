# /view/?... - просмотр опроса

## Пример: 
```
/view?question=Кто лучше? Выбери один из ответов&choices=Котики|Собачки|Антилопы ньялы&imageURL=https://cdn.quasar.dev/img/parallax2.jpg
```
![изображение](https://github.com/dudava/survey-web-app/assets/121783360/fad8f2d9-ca1a-4b05-82a4-fa804ae7eb7a)

## Параметры: 
**question** - вопрос <br>
**choices** - варианты ответов через | без пробелов <br>
**imageURL** - URL изображения для опроса <br>

# /edit/?... - просмотр и редактирование

## Пример: 
```
/edit?question=Что с тобой делать?&choices=Дать леща|Сломать колени&correctAnswer=1
```
![2023-08-14 00-30-15 (online-video-cutter com)](https://github.com/dudava/survey-web-app/assets/121783360/4ff24e3d-1a87-42c4-b5eb-2be45df11543)

## Параметры: 
**question** - вопрос <br>
**choices** - варианты ответов через | без пробелов <br>
**correctAnswer** - индекс правильного ответа (среди choices) начиная с нуля <br>
...  и т.д

## Создание нового опроса:
![2023-08-14 00-44-11 (online-video-cutter com)](https://github.com/dudava/survey-web-app/assets/121783360/87ac8bc5-af83-4fb6-9020-bf55879aec2d)

# Survey Web App Vue JS + Quasar (survey-standalone)

## Install the dependencies
```bash
yarn
# or
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```


### Build the app for production
```bash
quasar build
```

### Customize the configuration
See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).
