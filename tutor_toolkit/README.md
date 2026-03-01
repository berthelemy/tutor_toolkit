# Tutor Toolkit

Django web application for tutors to manage schools, students, groups, and lessons.

## Prerequisites

- Python 3

## Setup

1. Create and activate a virtual environment.
2. Install dependencies (use your preferred method; for example, if you maintain a requirements file):

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

Then open:

- http://127.0.0.1:8000/

## Internationalization (i18n)

This project supports English and French.

### Update translations

1. Extract messages:

   ```bash
   python manage.py makemessages -l fr
   ```

2. Edit translations:

- `locale/fr/LC_MESSAGES/django.po`

3. Compile messages:

   ```bash
   python manage.py compilemessages
   ```

If translations do not appear immediately, restart the Django dev server.

## GitHub

Push updates:

```bash
git status
git add -A
git commit -m "Your message"
git push
```
