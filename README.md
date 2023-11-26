<ol>
    <li>
        <b>Первоначальная настройка</b>
        <ol>
            <li>Запускаем программу Docket Desktop</li>
            <li>Открываем удобный терминал и переходим в папку где расположен файл «docker-compose.yml»</li>
            <li>Вводим туда команду docker-compose build</li>
            <li>
                Когда сборка завершится, нужно прописываем:
                <ul>
                    <li>docker-compose run --rm web-app sh -c "python manage.py makemigrations"</li>
                    <li>docker-compose run --rm web-app sh -c "python manage.py migrate"</li>
                    <li>docker-compose run --rm web-app sh -c "python manage.py createsuperuser"</li>
                </ul>
            </li>
            <li>После третьей команды запустится процесс создания суперпользователя. Следуем командам в терминале и
                вводим данные от учётной записи, для доступа ко всему функционалу приложения Запуск проекта</li>
            <li>Убедившись, что первоначальная настройка завершилась, открываем удобный терминал и переходим в папку где
                расположен файл «docker-compose.yml»</li>
            <li>Вводим туда команду: docker-compose up</li>
            <li>Переходим на локальный сервер как в системе указав порт “8000”. На windows это - “http://127.0.0.1:8000”
            </li>
        </ol>
    </li>
    <li>
        <b>Функционал</b>
        <ol>
            <li>
                <p>
                    Админ-панель. Чтобы сюда войти, нужно добавить постфикс - “/admin/” к основному адресу и ввести логин и пароль суперпользователя в открывшейся форме. Здесь есть возможность:
                </p>
                <ul>
                    <li>Смотреть, добавлять, редактировать и удалять клиентов, рассылки и сообщения.</li>
                    <li>Для просмотра объектов модели, нужно нажать на её название.</li>
                    <li>Для добавления нового объекта модели нужно нажать на плюс рядом с названием модели, заполнить
                        все поля и нажать кнопку сохранить.</li>
                    <li>Нажав на id объекта можно перейти на страницу его редактирования, где также есть возможность
                        удалить.</li>
                    <li>Добавлять новых пользователей сервиса, менять пароли и удалять существующих. Смотреть их токены
                        для API запросов.</li>
                    <li>Новая учётная запись создаётся как и другой объект.</li>
                    <li>Чтобы получить токен для пользователя, находясь на главной странице админ-панели, нужно нажать
                        на поле “Tokens”, выбрать нужного пользователя из списка и нажать кнопку сохранить.</li>
                </ul>
            </li>
            <li>
                <p>API</p>
                <ul>
                    <li>Неавторизованный пользователь не сможет получить информацию.</li>
                    <li>
                        Если используется учётная запись суперпользователя, то доступ будет к взаимодействию со всей
                        информации, а у обычных пользователей, только связанной с ними.
                    </li>
                    <li>Для выполнения любого запроса (GET, PUT, PATCH, DELETE, HEAD, OPTIONS), нужно в Headers указать
                        ключ - “Authorization” и значение к нему - “Token [значение токена без квадратных скобок]“</li>
                    <li>
                        Для перехода на главную страницу с основными API маршрутами, нужно добавить постфикс -
                        “/api/v1/” в адресную строку. Для получения более конкретной информации нужно добавить
                        постфиксы, приведённые ниже, где [i] - целые числа. [i] не обязательно указывать, а [o]
                        обязательно. Постфиксы:
                    </li>
                    <li>
                        <ul>
                            <li>
                                /client/[i] - Без [i] будет получить список клиентов. Добавив целое число на место [i],
                                можно получить информацию о пользователе с id равным этому числу, а также возможность
                                его отредактировать и удалить
                                (GET, PUT, PATCH, DELETE, HEAD, OPTIONS).
                            </li>
                            <li>
                                /message/[i] - Без [i] будет получить список сообщений. Добавив целое число на место
                                [i], можно получить информацию о сообщении с id равным этому числу, а также возможность
                                его отредактировать и удалить (GET,
                                PUT, PATCH, DELETE, HEAD, OPTIONS).
                            </li>
                            <li>
                                /mailing/[i] - Без [i] будет получить список сообщений. Добавив целое число на место
                                [i], можно получить информацию о рассылке с id равным этому числу, а также возможность
                                её отредактировать и удалить (GET,
                                PUT, PATCH, DELETE, HEAD, OPTIONS).
                            </li>
                            <li>
                                /statistic-messages/[i] - Без [i] будет получить список сообщений по статусам (GET,
                                HEAD, OPTIONS). Добавив целое число на место [i], можно получить информацию о сообщениях
                                с конкретным статусом где:
                            </li>
                            <li>
                                <ol>
                                    <li>Ожидает отправки</li>
                                    <li>Отправлено</li>
                                    <li>Не отправлено. Дата и время клиента больше выбранного в рассылке</li>
                                    <li>Не отправлено. Ошибка внешнего API</li>
                                </ol>
                            </li>
                            <li>/messages-in-mailing/[o] - Получить детальную статистику по рассылке со всеми её
                                сообщениями (GET, HEAD, OPTIONS).</li>
                            <li>/auth-rest/login/ - Страница с авторизацией</li>
                            <li>/auth-rest/logout/ - Выйти из учётной записи</li>
                            <li>Постфикс “/docs/” добавленный к основному адресу направит на страницу Swagger UI с
                                OpenAPI.</li>
                            <li>Постфикс “/add-users/” добавленный к основному адресу запустит создание 2160 клиентов
                                для тестов.</li>
                            <li>Сработает только если используется учётная запись суперпользвателя.</li>
                            <li>Постфикс “/del-users/” добавленный к основному адресу удаляет всех пользователей.
                                Сработает только если используется учётная запись суперпользвателя.</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ol>
    </li>
</ol>
