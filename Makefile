MANAGE := poetry run python manage.py

.PHONY: runserver
runserver:
	@$(MANAGE) runserver

.PHONY: makemigrations
makemigrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic

.PHONY: shell
shell:
	@$(MANAGE) shell_plus

.PHONY: flake8
flake8:
	poetry run flake8 task_manager

.PHONY: black-check
black-check:
	poetry run black --check task_manager  
# poetry run black --check --exclude=migrations task_manager (без настроек в pyproject)

.PHONY: black-diff
black-diff:
	poetry run black --diff task_manager
# poetry run black --diff --exclude=migrations task_manager  (без настроек в pyproject)

.PHONY: black
black:
	poetry run black task_manager
# poetry run black --exclude=migrations task_manager  (без настроек в pyproject)

.PHONY: isort-check
isort-check:
	poetry run isort task_manager --check-only

.PHONY: isort-diff
isort-diff:
	poetry run isort task_manager --diff

.PHONY: isort
isort:
	poetry run isort task_manager

.PHONY: exportreq
exportreq:
	poetry export -f requirements.txt --output requirements.txt

.PHONY: makemessages
makemessages:
	cd task_manager/ ;\
	poetry run django-admin makemessages -l ru_RU ;\
	cd ..

.PHONY: compilemessages
compilemessages:
	cd task_manager/ ;\
	poetry run django-admin compilemessages ;\
	cd ..

.PHONY: test
test:
	poetry run pytest