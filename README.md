# Hábitos API

Aplicación full-stack para el seguimiento de hábitos diarios. Los usuarios pueden registrarse, crear sus hábitos personales y hacer seguimiento de rachas de días consecutivos desde una interfaz web propia.

**Deploy activo:** https://habitos-api.onrender.com  
**API docs:** https://habitos-api.onrender.com/docs

## Stack

FastAPI · SQLAlchemy · SQLite · JWT · Pytest · HTML/CSS/JS

## Características

- Autenticación con JWT — cada usuario solo accede a sus propios datos
- CRUD completo de hábitos
- Registro de completaciones por fecha con historial
- Cálculo de racha de días consecutivos
- Frontend integrado servido desde el mismo servidor
- 9 tests automatizados con pytest

## Correr localmente
```bash
git clone https://github.com/EmiDelgadoV/habitos-api.git
cd habitos-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Creá un archivo `.env` en la raíz:
```
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///./habitos.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
```bash
uvicorn app.main:app --reload
```

La app queda disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

## Endpoints

### Autenticación

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Iniciar sesión, devuelve JWT |

### Hábitos — requieren `Authorization: Bearer <token>`

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/habits/` | Crear hábito |
| GET | `/habits/` | Listar hábitos del usuario |
| PUT | `/habits/{id}` | Editar hábito |
| DELETE | `/habits/{id}` | Eliminar hábito |
| POST | `/habits/{id}/log` | Registrar completación por fecha |
| GET | `/habits/{id}/history` | Ver historial y racha actual |

## Tests
```bash
pytest tests/ -v
```

9 tests cubriendo registro, login y operaciones sobre hábitos.

---

Desarrollado por **Emiliano Delgado** - https://github.com/EmiDelgadoV)
