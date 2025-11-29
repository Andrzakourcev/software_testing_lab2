# Отчет об интеграционных тестах Django приложения

## Общая информация
Для проведения тестирования использовалась готовая репозитория с Django-приложением `django-todo`. Приложение содержит модели `ToDoList` и `ToDoItem`, а также пользовательскую модель через `get_user_model()`. Тесты написаны с использованием `pytest` и Django ORM для проверки основных операций CRUD и связи между пользователем, списками задач и задачами.

Ссылка на репозиторий: https://github.com/kevinbowen777/django-todo

---

## Что такое интеграционные тесты
**Интеграционные тесты** — это тип тестирования, целью которого является проверка взаимодействия нескольких компонентов системы. В отличие от юнит-тестов, которые проверяют отдельные функции или классы изолированно, интеграционные тесты проверяют:

- Взаимодействие моделей с базой данных.
- Взаимодействие моделей между собой.
- Корректность обработки HTTP-запросов и форм.
- Взаимодействие разных слоев приложения (модель → представление → база данных).

В контексте Django интеграционные тесты часто используют декоратор `@pytest.mark.django_db`, чтобы иметь доступ к тестовой базе данных и проверить реальные изменения данных.

## Разбор интеграционных тестов

Интеграционные тесты предназначены для проверки работы нескольких компонентов системы вместе. В нашем случае это взаимодействие моделей, форм, представлений (views) и базы данных в Django-приложении.

### 1. `test_create_todolist_via_form`
```
@pytest.mark.django_db
def test_create_todolist_via_form():
    """Создание списка задач через HTML-форму"""
    User = get_user_model()
    user = User.objects.create_user(username="bob", password="pass123")

    todo_list = ToDoList.objects.create(title="Bob's List", owner=user)

    todo_list_in_db = ToDoList.objects.get(title="Bob's List")
    assert todo_list_in_db.owner == user
```
Что делает:

Создает пользователя через get_user_model().

Логинится через тестовый клиент Client().

Отправляет POST-запрос на создание нового списка задач (ToDoList).

Проверяет, что список задач действительно появился в базе и принадлежит правильному пользователю.
Почему интеграционный:

Проверяет работу сразу нескольких компонентов: модель ToDoList, view ListCreateView, HTML-форму и базу данных.

### 2. `test_create_todoitem_via_form`
```
@pytest.mark.django_db
def test_create_todoitem_via_form():
    """Создание задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="alice", password="pass123")
    todo_list = ToDoList.objects.create(title="Alice's List", owner=user)

    item = ToDoItem.objects.create(
        title='Task 1',
        description='Do something important',
        todo_list=todo_list,
        due_date=timezone.now()
    )

    item_in_db = ToDoItem.objects.get(title='Task 1')
    assert item_in_db.todo_list == todo_list
    assert item_in_db.todo_list.owner == user
```
Создает пользователя и список задач.

Логинится тестовым клиентом.

Отправляет POST-запрос на создание задачи (ToDoItem).

Проверяет, что задача появилась в базе, связана со списком и с пользователем.
Почему интеграционный:

Проверяет совместную работу моделей ToDoItem и ToDoList, view ItemCreateView, формы и базы данных.

### 3. `test_update_todoitem`
```
@pytest.mark.django_db
def test_update_todoitem():
    """Обновление задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="carol", password="pass123")
    todo_list = ToDoList.objects.create(title="Carol's List", owner=user)
    item = ToDoItem.objects.create(title="Old Task", todo_list=todo_list)

    item.title = "Updated Task"
    item.description = "Updated description"
    item.save()

    updated_item = ToDoItem.objects.get(id=item.id)
    assert updated_item.title == "Updated Task"
    assert updated_item.description == "Updated description"
```

Что делает:

Создает пользователя, список и задачу.

Логинится тестовым клиентом.

Отправляет POST-запрос на обновление задачи через view ItemUpdateView.

Проверяет, что поля задачи обновились.
Почему интеграционный:

Проверяет синхронную работу view, формы, модели и базы данных для обновления данных.

### 4. `test_delete_todoitem`
```
@pytest.mark.django_db
def test_delete_todoitem():
    """Удаление задачи"""
    User = get_user_model()
    user = User.objects.create_user(username="dave", password="pass123")
    todo_list = ToDoList.objects.create(title="Dave's List", owner=user)
    item = ToDoItem.objects.create(title="Task to delete", todo_list=todo_list)
    item.delete()

    assert not ToDoItem.objects.filter(id=item.id).exists()
```

Что делает:

Создает пользователя, список и задачу.

Логинится тестовым клиентом.

Отправляет POST-запрос на удаление задачи через view ItemDeleteView.

Проверяет, что задача больше не существует в базе.
Почему интеграционный:

Проверяет совместную работу модели, view и базы данных при удалении объекта.

### 5. `test_user_lists_and_items_link`
```
@pytest.mark.django_db
def test_user_lists_and_items_link():
    """Проверяем связь пользователя, списков и задач"""
    User = get_user_model()
    user = User.objects.create_user(username="eve", password="pass123")
    list1 = ToDoList.objects.create(title="List 1", owner=user)
    item1 = ToDoItem.objects.create(title="Task 1", todo_list=list1)

    user_lists = ToDoList.objects.filter(owner=user)
    assert list1 in user_lists

    user_items = ToDoItem.objects.filter(todo_list__owner=user)
    assert item1 in user_items
```

Что делает:

Создает пользователя, список и задачу.

Логинится тестовым клиентом.

Проверяет, что пользователь видит свои списки и задачи.
Почему интеграционный:

Проверяет связи между моделями User, ToDoList и ToDoItem и их корректное взаимодействие с базой данных.

Итог
Все эти тесты являются интеграционными, потому что они проверяют совместную работу нескольких компонентов: модели, представления, формы и базу данных. Они не ограничиваются тестированием одной функции или метода, а проверяют реальные сценарии использования приложения.


