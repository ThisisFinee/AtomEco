# Тестовое задание 1 (backend)
## Оглавление
1) [Архитектура проекта](#Aрхитектура-проекта)
   * [Модели](#Модели)
   * [Сериализаторы](#Сериализаторы)
   * [Views](#Views)
   * [Вспомогательные классы](#Вспомогательные-классы)
2) [Запросы(API)](#Запросы(API))
   * [ORGANIZATION](#ORGANIZATION)
   * [WASTE_STORAGE](#WASTE_STORAGE)
   * [RELATIONS](#RELATIONS)
   * [CONNECTION](#CONNECTION)
3) [Сборка и запуск](#Сборка-и-запуск)
4) [Тестирование](#Тестирование)
## Архитектура проекта
* ### [Модели](waste/project_models)
  * #### [Relations](waste/project_models/Relations.py)
    ***Описание:***    
    Набор отношений, который служит является объеденением всех сущностей графа(позволяет создавать множество независимых графов), ссодержит в себе информацию о структуре графа, а также о путях для всех организаций    
    ***Содержание:***
    ```python
    graph_structure = models.JSONField(null=True, blank=True)
    ways_structure = models.JSONField(null=True, blank=True)
    relations_name = models.TextField(null=True, blank=True)
    ```
    * relations_name: Наименование relations
    ```json
    {
    "nodes": [
        {"id": 1, "type": "Organization", "name": "Org A"},
        {"id": 2, "type": "WasteStorage", "name": "Storage 1"},
        {"id": 3, "type": "WasteStorage", "name": "Storage 2"}
    ],
    "edges": [
        {"from": 1, "to": 2, "distance": 50, "id": 5},
        {"from": 2, "to": 3, "distance": 30, "id": 6}
    ]
    }
    ```
    nodes: список объектов (узлов) в графе.
      * id: идентификатор узла.
      * type: тип узла (Organization или WasteStorage).
      * name: название узла.
    
    edges: список связей (ребер) между узлами.
      * from: идентификатор начального узла.
      * to: идентификатор конечного узла.
      * distance: расстояние между узлами.
      * id: идентификатор связи.
  
    ```json
    {
      "1": {
        "error": false,
        "paths": [
          {
            "path": [
              [1, 2],
              5
            ],
            "distance": 50,
            "waste_distribution": {
              "glass": 0,
              "plastic": 10,
              "bio_wastes": 50
            }
          },
          {
            "path": [
              [2, 3],
              6
            ],
            "distance": 30,
            "waste_distribution": {
              "glass": 50,
              "plastic": 0,
              "bio_wastes": 0
            }
          }
        ],
        "result_path": [
          [1, 2],
          [2, 3]
        ],
        "result_distance": 80
      }
    }
    ```
    1: ID узла(organization), от которого рассчитываются пути.
      * error: флаг ошибки расчета.
      * paths: список возможных путей. Формат:
          * path: маршрут в виде пар узлов и идентификатора связи.
          * distance: расстояние для данного маршрута(единичной дороги).
          * waste_distribution: распределение отходов по маршруту(для единичной дороги)(по типам отходов: glass, plastic, bio_wastes).
      * result_path: итоговый маршрут с узлами([from,to], [from,to]).
      * result_distance: общее расстояние итогового маршрута.
  * #### [BasePoint](waste/project_models/BasePoint.py)
    ***Описание:***    
      Родительская модель для organization и waste_storage, частично объеденяет поля для них, а также логику,
      главный плюс - отсутствие одинаковых id у organization и waste_storage(нужно для дальнейшей логики расчёта пути + делает ways_structure более простым к восприятию)
    ***Содержание:***
      ```python
      class BasePoint(PolymorphicModel):
        relations = models.ForeignKey(Relations, on_delete=models.CASCADE)
        name = models.CharField(max_length=255)
      ```
      * relations: Ключ, который показывает принадлежность organization или waste_storage к relations
      * name: Наименование organization или waste_storage
  * #### [Organization](waste/project_models/Organization.py)
    ***Описание:***    
      Модель содержит информацию об отходах организации.    
    ***Содержание:***
      ```python
      generate_plastic = models.IntegerField(null=True, blank=True)
      generate_glass = models.IntegerField(null=True, blank=True)
      generate_bio_wastes = models.IntegerField(null=True, blank=True)
      plastic = models.IntegerField(null=True, blank=True)
      glass = models.IntegerField(null=True, blank=True)
      bio_wastes = models.IntegerField(null=True, blank=True)
      ```
      * generate_plastic: Генерируемый пластик
      * generate_glass: Генерируемое стекло
      * generate_bio_wates: Генерируемые биоотходы
      * plastic: Остатки пластика на данный момент
      * glass: Остатки стекла на данный момент
      * bio_wates: Остатки биоотходов на данный момент    
        (P.s. На данный момент - последнее состояние при вызоыве перерасчёта путей)
  * #### [WasteStorage](waste/project_models/WasteStorage.py)
    ***Описание:***    
      Модель содержит информацию о хранилище.    
    ***Содержание:***
      ```python
      max_plastic = models.IntegerField(null=True, blank=True, default=0)
      max_glass = models.IntegerField(null=True, blank=True, default=0)
      max_bio_wastes = models.IntegerField(null=True, blank=True, default=0)
      plastic = models.IntegerField(null=True, blank=True, default=0)
      glass = models.IntegerField(null=True, blank=True, default=0)
      bio_wastes = models.IntegerField(null=True, blank=True, default=0)
      ```
      * max_plastic: Максимальная вместимость пластика в хранилище
      * max_glass: Максимальная вместимость стекла в хранилище
      * max_bio_wates: Максимальная вместимость биоотходов в хранилище
      * plastic: Количество пластика на данный момент
      * glass: Количество стекла на данный момент
      * bio_wates: Количество биоотходов на данный момент    
        (P.s. На данный момент - последнее состояние при вызоыве перерасчёта путей)
  * #### [Connection](waste/project_models/Connection.py) 
    ***Описание:***    
      Модель содержит информацию о дороге/связи.    
    ***Содержание:***
      ```python
      relations = models.ForeignKey(Relations, on_delete=models.CASCADE)
      first_point = models.ForeignKey(BasePoint, on_delete=models.CASCADE, related_name='first_point')
      second_point = models.ForeignKey(BasePoint, on_delete=models.CASCADE, related_name='second_point')
      distance = models.IntegerField(blank=True)
      ```
      * relations: Ключ, который показывает принадлежность organization или waste_storage к relations
      * first_point: Первый узел, содержащий ключ на organization или waste_storage(from)
      * second_point: Второй узел, содержащий ключ на organization или waste_storage(to)
      * distance: Длина дороги

* ### [Сериализаторы](waste/project_serializers)
  * #### [RelationsSerializer](waste/project_serializers/RelationsSerializer.py)
    Стандартый сериализатор модели Relations, не позволяет обновлять никакие поля в ручную кроме relations_name
  * #### [BaseSerializer](waste/project_serializers/BaseSerializer.py)
    Родительский сериализатор для OrganizationSerializer, Relations, WasteStorageSerializer, содержит:
     * Метод для валидации данных(передаём allowed непосресдственно в каждом сериализаторе)(filter_validated_data)
     * Метод для вызова действий после сохранения(post_save_actions)(генерация графа + перерасчёт путей)
     * Метод для вызова генерации графа
  * #### [OrganizationSerializer](waste/project_serializers/OrganizationSerializer.py)
    Стандартый сериализатор модели Organization, разрешённые для обновления поля allowed_keys = ['name', 'generate_plastic', 'generate_glass', 'generate_bio_wastes']
  * #### [ConnectionSerializer](waste/project_serializers/ConnectionSerializer.py)
    Стандартый сериализатор модели Connection, разрешённые для обновления поля allowed_keys = ['distance']
  * #### [WasteStorageSerializer](waste/project_serializers/WasteStorageSerializer.py)
    Стандартый сериализатор модели Organization, разрешённые для обновления поля allowed_keys = ['name', 'max_plastic', 'max_glass', 'max_bio_wastes']

* ### [Views](waste/project_views)
  * #### [RelationsView](waste/project_views/RelationsView.py)
    View serializer_class = RelationsSerializer (GET, PATCH, DELETE, POST)    
    Дополнительные методы API:
    * PATCH recalculate_paths - Вызывает перерасчёт путей для определённого relations
    * PATCH generate_graph_structure - Вызывает генерацию структуры графа для определенного relations
    * POST generate_graph - Создаёт граф(и relations для него) с несколькими возможными типами(требует парметр type):
      * base: Стандартный вариант из примера задания
      * spec: Специальный граф(Полный обхода всех хранилищ, проверка функции возврата к организации в случае тупика(имеются тупики), производимое кол-во отходов == ёмкостям хранилищ)
      * intersection: Полный обход хранилищ, кол-во отходов == ёмкостям хранилищ, у организаций есть общие пути
      * error: Полный обход хранилищ, кол-во отходов > сумма ёмкости хранилищ(причём для каждой организации)
    * POST generate_random_graphs - Создаёт несколько рандомных графов(и их relations)(Параметры type(обязательный параметр), number(если не вводить по стандарту 5)(p.s. лучше не вводить больше 5, так как генерация достаточно долгая)):
      * type=full: сгенерирует графы, в которых все организации имеют возможность разгрузиться(достаточно скучный вариант, так как обычно все организации разгрузятся за 1-2 шага)
      * type=partial: сгенерирует графы, в которых не все организации имеют возможность разгрузиться (более интересный вариант, позволит чуть лучше отсмотреть логику расчёта путей)
  * #### [OrganizationView](waste/project_views/OrganizationView.py)
    View serializer_class = OrganizationSerializer (GET, PATCH, DELETE, POST) 
  * #### [WasteStorageView](waste/project_views/WasteStorageView.py)
    View serializer_class = WasteStorageSerializer (GET, PATCH, DELETE, POST) 
  * #### [ConnectionView](waste/project_views/ConnectionView.py)
    View serializer_class = ConnectionSerializer (GET, PATCH, DELETE, POST)
    
* ### [Вспомогательные классы](waste/workfiles)
  * #### [Generator](waste/workfiles/Generator.py)
    ***Описание:***
     Генерирует разнообразные графы в зависимости от задачи      
    ***Функции:***
      * generate_test_graph() - создаёт стандартный граф из примера
      * generate_specific_graph() - создаёт специальный граф (Полный обхода всех хранилищ, проверка функции возврата к организации в случае тупика(имеются тупики), производимое кол-во отходов == ёмкостям хранилищ)
      * generate_graph_with_intersections() - создаёт граф с полным обходом хранилищ, кол-во отходов == ёмкостям хранилищ, у организаций есть общие пути
      * generate_error_graph() -  создаёт граф с полным обходом хранилищ, кол-во отходов > сумма ёмкости хранилищ(причём для каждой организации)
      * generate_random_graph(name, full_discharge=True) - создаёт случайный граф, логика:
        1. Сначала создаётся relations для объеденения
        2. создаётся от 3-х до 5 организаций(generate = от 10 до 100)
        3. в зависимости от full_discharge(полная разгрузка или нет) создаётся либо 3-6 хранилищ(full_discharge==False), либо от len(organizations)*2 до len(organizations)*2 +3 (full_discharge==True)
        4. Каждому хранилищу во время создания присваивается либо значение 0-50(full_discharge==False), либо 50-150(full_discharge==True)
        5. Далее создаются дороги для каждой организации
        6. Выполняется функция, для проверки и избавления от изолированных узлов(ensure_connected_graph)
        7. Генерируется структура графа в relations(GraphConstructor.generate_graph_structure(relaltions))
        8. Расчитываются пути для графа в relations(Navigator.recalculate_all_paths(relations))
        9. Возвращается relations
      * generate_fully_graphs(n=5) - n(по стандарту 5) раз выполняет generate_random_graph(name="Full graph", full_disharge=True), возвращает массив relations
      * generate_partially_graphs(n=5) - n(по стандарту 5) раз выполняет generate_random_graph(name="Partially graph", full_disharge=False), возвращает массив relations
  * #### [GraphConstructor](waste/workfiles/GraphConstructor.py)
    ***Описание:***
     Генерирует структуру графа для relations    
    ***Функции:***    
      * generate_graph_structure(relations) - генерирует структуру графа, логика:
        1. Сначала находим все сущности привязанные к relations
        2. Все Organization и WasteStorages записываем в grap_structure['nodes']
        3. Все Connection записываем в grap_structure['edges']
        4. Сохраняем в бд, возвращаем graph_structure
   * #### [Navigator](waste/workfiles/Navigator.py)
      ***Описание:***
       Рассчитывает пути графа для relations     
      ***Функции:***    
        * calculate_path_for_organization(organization) - рассчитывает путь для организации, логика:
          1. Сначала находим привязанный к организации relations
          2. Собираем все edges графа
          3. Пока есть отходы находим кратчайший путь от нынешнего узла(объеденение жадного алгоритма и drf)(find_shortest_edge(from_node, exclude_edges=None)):
              1) Если тупик возвращаемся к ближайшему перекрёстку(в result_path записываем весь путь от организации до перкрёстка): идея в том, что если условный грузовик заехал в тупик, то организация отправляет следующий(до ближайшего доступного перекрёстка(а далее по условию), так как в этом случае соблюдается условие с жадным алгоритмом)
                * Если ближайшего перекрёстка нет, то break(все пути исследованы)
                * В ином случае проверяем наличие бесполезных путей и отчищаем их(clean_useless_paths)(бесполезный путь - путь, который не привёл к узлу в который можно разгрузиться и при этом не используется как промежуточный путь до узла) continue
              2) Если не тупик, то переходим к следующему узлу
                * Если узел - организация, то вызываем continue
                * Если узел - хранилище, то распределяем отходы организации и сохраняем изменения в бд
              3) Добавляем путь в пройденные(именно путь, а не узел)
              4) Добавляем в paths, result_path, result_distance всю необходимую информацию
              5) Проверяем состояние при возврате:
                * Если кол-во путей из нынешнего узла больше одного, то добавляем его в стек
                * Если меньше, то исключаем путь, так как он полностью исследован
          4. Проверяем на оставшиеся отходы
          5. Сохраняем relations.ways_structure[organization.id] в бд
        * recalculate_all_paths(relations) - перерасчитывает все пути для органиаций в relations, логика:
            1. Находим все organization привязанные к relations
            2. Очищаем ways_structure(StateReturner.relations_all_paths_clear(relations))
            3. Возвращаем объектам(организациям и хранилищам), привязанным к relations, их изначальное кол-во отходов(для организаций - кол-во = генерации, для хранилищ - кол-во = 0)(StateReturner.relations_objects_state_return(relations))
            4. Если в relations пустой graph_structure, то вызываем генерацию графа(GraphConstructor.generate_graph_structure(relations))
            5. Приравниваем двунаправленные дороги(если дорога равна n в одну сторону, значит, если существует обратная она будет равняться тому же n)(normalize_bidirectional_paths)
            6. Перебираем все организации и пересчитываем пути(Navigator.calculate_path_for_organization(organization))
        * normalize_bidirectional_paths(relations) - приравнивает пути в обе стороны для двунаправленных дорог, логика:
          1. Проверяем наличие edges
          2. Составляем edge_map
          3. Пробегаем по всем edges:
             1) Создаём прямой путь и обратный путь
             2) Если прямой путь в уже обработанных парах или обратный путь в обработанных парах, то continue
             3) Если обратный путь есть в edge_map, то меняем его дистанцию, на дистанцию прямого пути
             4) Обновляем данные для обратного пути в бд(именно connection)
             5) Помечаем пару как обработанную
             6) Сохраняем в relations.graph_structure['edges'] новые edges
* #### [StateReturner](waste/workfiles/StateReturner.py)
  ***Описание:***
   Возвращает объекты к изначальному состоянию(именно генерируемые значения и подверженные автоматическому изменению)    
  ***Функции:***    
  * relations_objects_state_return(relations) - Возвращаем сущностям relations(Organization и WasteStorage) изначальное кол-во отходов, логика:
    1. Находим все организации и хранилища relations
    2. Пробегаем по все организациям и обновляем им нынешнее кол-во отходов до уровня генерируемых
    3. Пробегаем по все хранилищам и обновляем им нынешнее кол-во отходов до 0
  * relations_all_paths_clear(relations) - очищает ways_structure у relations
## Запросы(API)
  ### Удобнее кидать запросы через Postman, но если его нет или не хочется его запускать, я также оставил тут запросы через базовый curl
  ### ORGANIZATION
1. Получение списка организаций    
  Описание: Возвращает список всех организаций.    
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/organizations/    
  ***cURL:***    
     ```bash
      curl -X GET http://localhost/waste/organizations/
     ```
2. Создание организации    
  Описание: Добавляет новую организацию.    
  ***Postman:***    
    Метод: POST    
    URL: http://localhost/waste/organizations/    
    Body:    
      ```json
        {
        "name": "Организация 1",
        "generate_plastic": 100,
        "generate_glass": 50,
        "generate_bio_wastes": 30
        }
      ```    
   ***cURL:***    
     ```bash
     curl -X POST http://localhost/waste/organizations/ -H "Content-Type: application/json" -d "{\"name\": \"Организация 1\", \"generate_plastic\": 100, \"generate_glass\": 50, \"generate_bio_wastes\": 30}"
     ```    
3. Обновление данных об организации     
  Описание: Частично обновляет данные организации.      
***Postman:***    
  Метод: PATCH     
  URL: http://localhost/waste/organizations/1/    
  Body:
      ```json
    {
      "generate_plastic": 150,
      "generate_glass": 30
    }
    ```
***cURL:***    
  ```bash
  curl -X PATCH http://localhost/waste/organizations/1/ -H "Content-Type: application/json" -d "{\"generate_plastic\": 150, \"generate_glass\": 30}"
  ```
4. Получение детальной информации:   
  Описание: Возвращает информацию об одной организации.      
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/organizations/1/   
  ***cURL:***    
    ```bash
    curl -X GET http://localhost/waste/organizations/1/"
    ```    
5. Удаление организации    
Описание: Удаляет организацию по её ID.    
***Postman:***     
  Метод: DELETE    
  URL: http://localhost/waste/organizations/1/    
***cURL:***    
  ```bash
  curl -X DELETE http://localhost/waste/organizations/1/
  ```    
  ### WASTE_STORAGE
1. Получение списка хранилищ    
Описание: Возвращает список всех хранилищ отходов.    
***Postman:***    
  Метод: GET    
  URL: http://localhost/waste/waste_storages/    
***cURL:***    
  ```bash
  curl -X GET http://localhost/waste/waste_storages/
  ```    
2. Получение детальной информации о хранилище    
Описание: Возвращает детальную информацию о хранилище.    
***Postman:***    
  Метод: GET    
  URL: http://localhost/waste/waste_storages/1/     
***cURL:***    
  ```bash
  curl -X GET http://localhost/waste/waste_storages/1/
  ```     
3. Создание хранилища    
Описание: Создаёт новое хранилище.     
***Postman:***     
  Метод: POST    
  URL: http://localhost/waste/waste_storages/    
  Body:    
  ```json
  {
    "name": "Хранилище 1",
    "max_plastic": 1000,
    "max_glass": 500
  }
  ```    
***cURL:***    
  ```bash
  curl -X POST http://localhost/waste/waste_storages/ -H "Content-Type: application/json" -d "{\"name\": \"Хранилище 1\", \"max_plastic\": 1000, \"max_glass\": 500}"
  ```    
4. Обновление хранилища    
Описание: Частично обновляет данные хранилища.     
***Postman:***     
  Метод: PATCH    
  URL: http://localhost/waste/waste_storages/1/    
  Body:    
  ```json
  {
    "plastic": 200,
    "glass": 40
  }
  ```    
***cURL:***     
  ```bash
  curl -X PATCH http://localhost/waste/waste_storages/1/ -H "Content-Type: application/json" -d "{\"plastic\": 200, \"glass\": 40}"
  ```
5. Удаление хранилища    
Описание: удаляет хранилище    
***Postman:***    
  Метод: DELETE    
  URL: http://localhost/waste/waste_storages/1/    
***cURL:***     
  ```bash
  curl -X DELETE http://localhost/waste/waste_storages/1/"
  ```
  ### RELATIONS
1. Список
  Описание: Возвращает все записи Relations.
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/relations/    
  ***cURL:***    
     ```bash
      curl -X GET http://localhost/waste/relations/
     ```
2. Создание relations    
  Описание: Добавляет новые relations.    
  ***Postman:***    
    Метод: POST    
    URL: http://localhost/waste/relations/    
    Body:    
      ```json
        {
          "relations_name": "Отношение 1"
        }
      ```    
   ***cURL:***    
     ```bash
     curl -X POST http://localhost/waste/relations/ -H "Content-Type: application/json" -d "{\"relations_name\": \"Отношение 1\"}"
     ```    
3. Обновление данных об relations     
  Описание: Частично обновляет данные relations.      
***Postman:***    
  Метод: PATCH     
  URL: http://localhost/waste/relations/1/    
  Body:
      ```json
    {"relations_name": "Отношение обновлённое"}
    ```
***cURL:***    
  ```bash
  curl -X PATCH http://localhost/waste/relations/1/ -H "Content-Type: application/json" -d "{\"relations_name\": \"Отношение обновлённое\"}"
  ```
4. Получение детальной информации:   
  Описание: Возвращает информацию об одном relations.      
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/relations/1/   
  ***cURL:***    
    ```bash
    curl -X GET http://localhost/waste/relations/1/"
    ```    
5. Удаление relations    
Описание: Удаляет relations по ID.    
***Postman:***     
  Метод: DELETE    
  URL: http://localhost/waste/relations/1/    
***cURL:***    
  ```bash
  curl -X DELETE http://localhost/waste/relations/1/
  ```
6. Генерация графа   
Описание: Генерирует граф указанного типа.    
***Postman:***     
  Метод: POST    
  URL: http://localhost/waste/relations/generate_graph/
  Params: type=base       
***cURL:***    
  ```bash
  curl -X POST "http://localhost/waste/relations/generate_graph/?type=base"
  ```    
7. Перерасчёт путей    
Описание: Пересчитывает пути внутри графа.    
***Postman:***     
  Метод: PATCH    
  URL: http://localhost/waste/relations/1/recalculate_paths/       
***cURL:***    
  ```bash
  curl -X PATCH http://localhost/waste/relations/1/recalculate_paths/
  ```
8. Генерация структуры графа    
Описание: генерирует структуру графа.    
***Postman:***     
  Метод: PATCH    
  URL: http://localhost/waste/relations/1/generate_graph_structure/       
***cURL:***    
  ```bash
  curl -X PATCH http://localhost/waste/relations/1/generate_graph_structure/
  ```
9. Генерация рандомных графов    
Описание: Генерирует рандомные графы указанного количества и типа.    
***Postman:***     
  Метод: POST    
  URL: http://localhost/waste/relations/generate_random_graphs/
  Params: type=base, number=2       
***cURL:***    
  ```bash
  curl -X POST "http://localhost/waste/relations/generate_random_graphs/?type=partial&number=2"
  ```    
  ### CONNECTION
1. Получение списка дорог    
  Описание: Возвращает список всех дорог.    
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/connections/    
  ***cURL:***    
     ```bash
      curl -X GET http://localhost/waste/connections/
     ```
2. Создание дороги    
  Описание: Добавляет новую дорогу.    
  ***Postman:***    
    Метод: POST    
    URL: http://localhost/waste/connections/    
    Body:    
      ```json
        {
          "relations": 1,
          "first_point": 1,
          "second_point": 2,
          "distance": 100
        }
      ```    
   ***cURL:***    
     ```bash
     curl -X POST http://localhost/waste/connections/ -H "Content-Type: application/json" -d "{\"first_point\": 1, \"second_point\": 2, \"distance\": 15, \"relations\": 1}"
     ```    
3. Обновление данных о дороге     
  Описание: Частично обновляет данные дороги.      
***Postman:***    
  Метод: PATCH     
  URL: http://localhost/waste/connections/1/    
  Body:
      ```json
    {
      "distance": 150
    }
    ```
  ***cURL:***    
  ```bash
  curl -X PATCH http://localhost/waste/connections/1/ -H "Content-Type: application/json" -d "{\"distance\": 150}"
  ```
4. Получение детальной информации:   
  Описание: Возвращает информацию об одной дороге.      
  ***Postman:***    
    Метод: GET    
    URL: http://localhost/waste/connections/1/   
  ***cURL:***    
    ```bash
    curl -X GET http://localhost/waste/connections/1/"
    ```    
5. Удаление дороги    
Описание: Удаляет дорогу по её ID.    
***Postman:***     
  Метод: DELETE    
  URL: http://localhost/waste/connections/1/    
***cURL:***    
  ```bash
  curl -X DELETE http://localhost/waste/connections/1/
  ```
---
## Сборка и запуск
### Для сборки и запуска потребуется установленный Docker, docker-compose и свободный 80 порт, если 80 порт занят, то:
1) Заходим в [docker-compose.yml](docker-compose.yml) и в образе nginx меняем ports на любые другие(эти порты надо будет указывать при запросе):
 ```yml
    nginx:
        image: nginx:alpine
        container_name: nginx_server
        depends_on:
          - web
        volumes:
          - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
        ports:
          - "80:80"
  ```
2) Заходим в [nginx.conf](nginx/nginx.conf) и в нём меняем число во второй строчке на указанный порт:
  ```conf
  server {
    listen 80;
    server_name localhost;
  ```
### Сборка:
1. Через консоль открываем корневую папку проекта(там должен находиться manage.py и docker-compose.yml)
2. Вводим команду:
   ```bash
   docker-compose build
   ```
3. Ждём окончания сброки
### Запуск
1. Через консоль открываем корневую папку проекта
2. Вводим команду:
   ```bash
   docker-compose up -d
   ```
3. Ждём запуска и используем
## Тестирование
[Все тесты находятся тут](waste/tests/test_api.py)
1. Через консоль открываем корневую папку проекта
2. Запускаем проект через
   ```bash
    docker-compose up -d
   ```
4. после запуска вводим команду:
   ```bash
   docker-compose exec web pytest
   ```
5. Смотрим на результат в консоли
