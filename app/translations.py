

class ButtonTranslations:
    SEARCH_RECIPE_BY_CATEGORY = "Поиск по категориям"
    SEARCH_RECIPE_BY_Q ="Найти рецепт"
    RANDOM_RECIPE = "Выдать случайный рецепт"

    NEXT='Далее'
    PREV='Назад'
    DONE="Готово"

    YES='Да'
    NO='Нет'

    MAIN_MENU='🔙 Главное меню'

    ADMIN_ADD_TAG = """Добавить категорию"""
    ADMIN_ADD_INGREDIENT = """Добавить продукт"""
    ADMIN_ADD_RECIPE = """Добавить рецепт"""
    ADMIN_ADD_STEP_MORE = """Добавить еще один этап"""

    ADMIN_EDIT_RECIPE = """Изменить"""

    ADMIN_EDIT_RECIPE_NAME = """Изменить название рецепта"""
    ADMIN_EDIT_RECIPE_DESCRIPTION = """Изменить описание рецепта"""
    ADMIN_EDIT_RECIPE_IMAGE = """Изменить картинку рецепта"""

    ADMIN_EDIT_RECIPE_DELETE_TAG = """Удалить тег"""
    ADMIN_EDIT_RECIPE_ADD_TAG = """Добавить тег"""

    ADMIN_EDIT_RECIPE_DELETE_INGREDIENT = """Удалить ингредиент"""
    ADMIN_EDIT_RECIPE_ADD_INGREDIENT = """Добавить ингредиент"""

    ADMIN_EDIT_RECIPE_DELETE_STEP = """Удалить этап"""
    ADMIN_EDIT_RECIPE_ADD_STEP = """Добавить этап"""
    ADMIN_EDIT_RECIPE_CHANGE_STEP_INDEXES = """Изменить порядок шагов рецепта"""

    ADMIN_DELETE_RECIPE= """Удалить рецепт"""



    ADMIN_PANEL = """Админ панель"""

    CANCEL='Отмена'
    

    

class MessageTranslations:
    START = """Привет 

Я чат бот, который поможет тебе приготовить что-то вкусненькое покушать.
Выбирай один из пунктов меню и пошли готовить."""

    INVALID_VALUE_IS_NOT_DIGIT="""Необходимо указать число, попробуйте еще раз"""

    RECIPE_SEARCH = """Для начала попробуем найти рецепт по названию.
Введи название рецепта, a я попробую вспомнить что-нибудь похожее."""
    RECIPE_SEARCH_NOT_FOUND = """Похоже что я не припоминаю таких рецептов"""
    RECIPE_SEARCH_FOUND = """Вот что я помню похожее.
Посмотри, может тебе что-то понравится"""
    RECIPE_SEARCH_VIEW_RESULT_HTML="""<b>{title}</b>
{description}

Категории: {category_list}

Необходимые ингредиенты:
{ingredient_list}
"""
    RECIPE_STEP_NOT_FOUND="""Я забыл как готовиться это блюдо"""
    RECIPE_DONE="""Приятного аппетита"""

    RECIPE_SEARCH_BY_CATEGORY="""Выбери одну из категорий"""
    SHOW_MORE_CATEGORY="""Вот еще категории"""
    SELECTED_CATEGORY="""Вот что я помню из этой категории"""

    CHOOSE_BUTTON_OPTION = """Нажмите одну из предложенных кнопок"""

    ADMIN_SET = """Хочешь стать админом?
Скажи пароль"""
    ADMIN_SET_WRONG_PASSWORD="""Неа... Пароль не такой"""
    ADMIN_SET_SUCCESS="""Пароль принят, теперь ты админ"""
    ADMIN_PANEL_GREETING="""Добро пожаловать в админ панель"""

    ADMIN_ADD_TAG="Введи имя категории"
    ADMIN_ADD_TAG_EMPTY_NAME="Имя категории не может быть пустое"
    ADMIN_ADD_TAG_SUCCESS="Категория успешно добавлена"
    ADMIN_ADD_INGREDIENT="Введи название продукта"
    ADMIN_ADD_INGREDIENT_SUCCESS="Продукт успешно добавлен"
    ADMIN_ADD_INGREDIENT_EMPTY_NAME="Имя категории не может быть пустое"

    ADMIN_ADD_RECIPE = """Чтобы добавить новый рецепт, я буду задавать тебе вопросы, а ты отвечай на них текстом или с помощью клавиатуры"""
    ADMIN_ADD_RECIPE_NAME = """Какое название рецепта?"""
    ADMIN_ADD_RECIPE_DESCRIPTION = """Введи описание рецепта"""
    ADMIN_ADD_RECIPE_IMAGE = """Отправь фото блюда в формате jpg или png"""
    
    ADMIN_ADD_RECIPE_TAGS = f"""Выбери категории для рецепта или нажмите '{ButtonTranslations.DONE}'"""

    ADMIN_ADD_RECIPE_INGREDIENT = """Добавь ингредиент
Можно добавлять много ингредиентов. По окончанию нажми Готово"""
    ADMIN_ADD_RECIPE_INGREDIENT_MORE = """Можешь добавить еще ингредиент или нажми готово чтобы продолжить дальше"""
    ADMIN_ADD_RECIPE_INGREDIENT_AMOUNT_TYPE = """Выберите в чем измеряется количество продукта"""
    ADMIN_ADD_RECIPE_INGREDIENT_AMOUNT = """Введите необходимое количество продукта для рецепта"""

    ADMIN_ADD_RECIPE_INGREDIENT_ADDED = """Ингридиент добавлен"""

    ADMIN_ADD_RECIPE_STEP = """Сейчас будем добавлять карточки для пошаговой инструкции инструкции."""
    ADMIN_ADD_RECIPE_STEP_DESCRIPTION = """Введи описание этапа"""
    ADMIN_ADD_RECIPE_STEP_IMAGE = """Отправь фото для этапа"""
    ADMIN_ADD_RECIPE_STEP_MORE = f"""Если вы хотите добавить еще этап нажмите '{ButtonTranslations.ADMIN_ADD_STEP_MORE}', если нет то '{ButtonTranslations.DONE}'"""
    ADMIN_ADD_RECIPE_SAVED = """Поздравляют вы добавили новый рецепт """

    ADMIN_UPDATE_RECIPE_NAME = """Введите новое имя"""
    ADMIN_UPDATE_RECIPE_DESCRIPTION = """Введите новое описание"""
    ADMIN_UPDATE_RECIPE_IMAGE = """Отправьте новое фото рецепта в формате jpg или png"""

    ADMIN_UPDATE_RECIPE_ADD_TAG = """Выберите категорию для добавления в рецепт"""
    ADMIN_UPDATE_RECIPE_DELETE_TAG = """Выберите категорию для удаления"""
    ADMIN_UPDATE_RECIPE_ADD_INGREDIENT = """Выберите ингредиент для добавления"""
    ADMIN_UPDATE_RECIPE_ADD_INGREDIENT_AMOUNT_TYPE = """Выберите в чем измеряется количество продукта"""
    ADMIN_UPDATE_RECIPE_ADD_INGREDIENT_AMOUNT = """Введите необходимое количество продукта для рецепта"""
    ADMIN_UPDATE_RECIPE_DELETE_INGREDIENT = """Выберите ингредиент для удаления"""
    ADMIN_UPDATE_RECIPE_DELETE_STEP= """Выберите этап для удаления"""
    ADMIN_UPDATE_RECIPE_DELETE_NO_STEP = """Для этого этапа нет шагов"""
    ADMIN_DELETE_RECIPE = """Вы действительно хотите удалить рецепт"""
    ADMIN_DELETED_RECIPE = """Рецепт успешно удален"""

    ADMIN_UPDATE_RECIPE_ADD_NO_INGREDIENTS_IN_DB= """В базе больше нет продуктов которые можно добавить"""
    ADMIN_UPDATE_RECIPE_ADD_STEP_DESCRIPTION = """Введите описание этапа"""
    ADMIN_UPDATE_RECIPE_ADD_STEP_IMAGE = """Отправьте картинку для этапа в формате jpg или png"""
    ADMIN_UPDATE_RECIPE_STEPS_INDEX = """Для изменения напишите строку из чисел как показано в примере
Пример: 
    В данном промере меняется местами этап 2 и 3
    Этапы:
        1. ...
        2. ...
        3. ...
    
    Строка ввода:
        1 3 2
"""
    INVALID_INDEXES_STRING_NOT_DIGIT = """Все элементы должны быть числами""" 

    ADMIN_RECIPE_UPDATED = """Рецепт успешно обновлен"""