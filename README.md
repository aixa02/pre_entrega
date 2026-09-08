# pre_entrega
Un cliente asincrónico universal para interactuar con múltiples proveedores de LLM (OpenAI, Anthropic, Google Gemini) usando una **interfaz común**.

## 🎯 Características

- ✅ Soporte para **OpenAI**, **Anthropic** y **Google Gemini**
- ✅ Interfaz **intercambiable** (cambia de proveedor sin cambiar código)
- ✅ Modo **streaming** (tokens en tiempo real)
- ✅ Modo **normal** (respuesta completa)
- ✅ Validación con **Pydantic**
- ✅ Manejo de excepciones y errores
- ✅ API keys seguras con `SecretStr`

---

## 📋 Requisitos

- Python 3.12+
- pip

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/unified-llm-client.git
cd unified-llm-client
```

### 2. Crear entorno virtual

```bash
# Windows (Git Bash):
python -m venv venv
source venv/Scripts/activate

# Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Configurar Variables de Entorno

### 1. Copiar archivo de ejemplo

```bash
cp .env.example .env
```

### 2. Agregar tus API keys en `.env`