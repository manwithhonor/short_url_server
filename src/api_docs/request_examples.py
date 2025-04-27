from fastapi import Body


example_create_task = Body(
    openapi_examples={
        "normal":   {
            "summary": "Типовой запрос",
            "description": "Типовой запрос для создания задачи",
            "value": {
                "url_description": "Подготовить презентацию",
                "full_url":  "https://lms.mipt.ru/pluginfile.php/228695/mod_book/chapter/4274/Введение_в_FastAPI_и_REST_сервисы_Конспект.pdf",
                "due_date": "2025-01-20"
            }
        }
    }
)