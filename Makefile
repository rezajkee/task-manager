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
	poetry run flake8 carzone

.PHONY: black-check
black-check:
	poetry run black --check carzone  
# poetry run black --check --exclude=migrations carzone (без настроек в pyproject)

.PHONY: black-diff
black-diff:
	poetry run black --diff carzone
# poetry run black --diff --exclude=migrations carzone  (без настроек в pyproject)

.PHONY: black
black:
	poetry run black carzone
# poetry run black --exclude=migrations carzone  (без настроек в pyproject)

.PHONY: isort-check
isort-check:
	poetry run isort carzone --check-only

.PHONY: isort-diff
isort-diff:
	poetry run isort carzone --diff

.PHONY: isort
isort:
	poetry run isort carzone

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
