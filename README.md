<p align="center">
	<!-- Title -->
	<img src="https://i.ibb.co/76pC0Gs/logo.png" width="128"/><br>
	<b>🇺🇦 Kinohub</b><br>
	<a href="https://kinohub.justdawy.pp.ua/">🚀 Live Demo</a>
</p>
<p align="center">
<img src="https://img.shields.io/github/languages/code-size/justdawy/kinohub?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Made_with-Python-3776AB?style=for-the-badge&logo=python"/>
</p>

## About the project
<p align="center">
  <img src="https://i.ibb.co/Q3wNHHLz/image.png" height="800"/><br>
</p>

KinoHub is a Django-powered movie platform inspired by UAKino-style services, offering an easy way to browse, search, and watch films with a fast and modern user experience.

### Built With
![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![uv Badge](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=fff&style=for-the-badge)
![Django Badge](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=fff&style=for-the-badge)
![PostgreSQL Badge](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=fff&style=for-the-badge)
![Docker Badge](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)

## Getting Started

### Prerequisites

- Python 3.13+
- Docker (optional)

### With Docker

```bash
docker compose up --build
```

### Without Docker

**1. Install dependencies**
```bash
pip install uv
uv sync
```

**2. Apply migrations**
```bash
uv run python kinohub/manage.py migrate
```

**3. Run the server**
```bash
uv run python kinohub/manage.py runserver
```

## Screenshots
<p align="center">
  <h3 align="center">Movie Page</h3>
  <img src="https://i.ibb.co/vvQFX6g4/image.png" height="800"/>
  <img src="https://i.ibb.co/WWFGGhbF/image.png"  height="800"/>
  <h3 align="center">Profile Page</h3>
  <img src="https://i.ibb.co/nNsqPLGx/image.png" height="800"/>
</p>
