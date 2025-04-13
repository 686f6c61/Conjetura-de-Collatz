#!/bin/bash

#######################################################################
# Script de configuración y ejecución para el Analizador de Collatz
# Autor: 686f6c61 (https://github.com/686f6c61)
# Repositorio: https://github.com/686f6c61/Conjetura-de-Collatz
#
# Este script automatiza la configuración del entorno y la ejecución
# del Analizador de la Conjetura de Collatz. Detecta la versión de
# Python, crea un entorno virtual, instala dependencias y ejecuta
# la aplicación.
#######################################################################

# Definición de códigos de color ANSI para mensajes en consola
GREEN='\033[0;32m'  # Verde para mensajes de éxito
BLUE='\033[0;34m'   # Azul para información y títulos
RED='\033[0;31m'    # Rojo para errores y advertencias
NC='\033[0m'        # Restablecer color

# Mostrar presentación visual con ASCII art e información del repositorio
echo -e "\n${BLUE}"
cat << "EOF"
 ________ ________ ________ ________ ________ ________ ________ ____ 
|\   ____\\\   ____\\\   ____\\\   ____\\\   ____\\\   ____\\\   __  \\   \\
\ \  \___|\  \  \___|\  \  \___|\  \  \___|\  \  \___|\  \  \___|\  \  \|\  \  \\
 \ \  \    \ \  \    \ \  \    \ \  \    \ \  \    \ \  \    \ \   __  \  \\
  \ \  \____\ \  \____\ \  \____\ \  \____\ \  \____\ \  \____\ \  \ \  \  \\
   \ \_______\ \_______\ \_______\ \_______\ \_______\ \_______\ \__\ \__\  \\
    \|_______|\_______|\_______|\_______|\_______|\_______|\___|\|__|   \\
EOF
echo -e "${NC}"

echo -e "${GREEN}Analizador de la Conjetura de Collatz${NC}"
echo -e "${BLUE}Repositorio: ${NC}https://github.com/686f6c61/Conjetura-de-Collatz"
echo -e "${BLUE}Autor: ${NC}686f6c61\n"

echo -e "${BLUE}=== Configuración del Entorno ===${NC}"

###############################################################
# FASE 1: Detección de Python
# Comprueba si Python 3 está instalado y disponible en el sistema.
# El script prioriza 'python3', pero también acepta 'python' si
# corresponde a Python 3.x
###############################################################

# Comprobar si el comando 'python3' está disponible
if command -v python3 &>/dev/null; then
    PYTHON="python3"
    echo -e "${GREEN}✓ Usando Python 3${NC}"
elif command -v python &>/dev/null; then
    # Si solo está disponible 'python', verificar que sea versión 3.x
    PY_VERSION=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1)
    if [ "$PY_VERSION" -eq 3 ]; then
        PYTHON="python"
        echo -e "${GREEN}✓ Usando Python 3${NC}"
    else
        echo -e "${RED}✗ Se requiere Python 3 para ejecutar este programa${NC}"
        exit 1
    fi
else
    # Python no está instalado o no está en el PATH
    echo -e "${RED}✗ No se encontró Python. Por favor, instale Python 3${NC}"
    exit 1
fi

###############################################################
# FASE 2: Configuración del entorno virtual
# Crea un entorno virtual para aislar las dependencias del proyecto.
# Si falla, intenta instalar el módulo venv/virtualenv primero.
# Como último recurso, continuará sin entorno virtual.
###############################################################

# Verificar si ya existe un entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creando entorno virtual...${NC}"
    # Intentar crear el entorno virtual
    $PYTHON -m venv venv
    
    # Verificar si la creación fue exitosa
    if [ $? -ne 0 ]; then
        # Primer intento fallido, intentar instalar virtualenv
        echo -e "${RED}✗ Error al crear el entorno virtual. Instalando venv...${NC}"
        $PYTHON -m pip install virtualenv
        $PYTHON -m venv venv
        
        # Verificar segundo intento
        if [ $? -ne 0 ]; then
            # Ambos intentos fallidos, continuar sin entorno virtual
            echo -e "${RED}✗ No se pudo crear el entorno virtual. Continuando sin él...${NC}"
            VENV=""
        fi
    fi
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    # El entorno virtual ya existe
    echo -e "${GREEN}✓ Usando entorno virtual existente${NC}"
fi

###############################################################
# FASE 3: Activación del entorno virtual
# Activa el entorno virtual si existe, o utiliza el intérprete
# de Python del sistema si no hay entorno virtual.
###############################################################

# Verificar si el directorio del entorno virtual existe
if [ -d "venv" ]; then
    echo -e "${BLUE}Activando entorno virtual...${NC}"
    # Activar el entorno para el script actual
    source venv/bin/activate
    # Configurar la ruta al ejecutable de Python del entorno virtual
    VENV="venv/bin/python"
    echo -e "${GREEN}✓ Entorno virtual activado${NC}"
else
    # Usar el intérprete de Python del sistema
    VENV=$PYTHON
fi

###############################################################
# FASE 4: Instalación de dependencias
# Instala las bibliotecas requeridas desde requirements.txt
# Si falla la instalación en el entorno virtual, intenta
# instalar a nivel de usuario como alternativa.
###############################################################

echo -e "${BLUE}Instalando dependencias...${NC}"

# Intentar instalar dependencias en el entorno seleccionado
$VENV -m pip install -r requirements.txt

# Verificar si la instalación fue exitosa
if [ $? -ne 0 ]; then
    # Primer intento fallido, intentar instalar a nivel de usuario
    echo -e "${RED}✗ Error al instalar dependencias. Intentando instalar sin entorno virtual...${NC}"
    $PYTHON -m pip install -r requirements.txt --user
    
    # Verificar segundo intento
    if [ $? -ne 0 ]; then
        # Ambos intentos fallidos, advertir al usuario
        echo -e "${RED}✗ No se pudieron instalar las dependencias. El programa podría no funcionar correctamente.${NC}"
    else
        # Instalación a nivel de usuario exitosa
        echo -e "${GREEN}✓ Dependencias instaladas para el usuario${NC}"
    fi
else
    # Instalación en entorno virtual exitosa
    echo -e "${GREEN}✓ Dependencias instaladas${NC}"
fi

###############################################################
# FASE 5: Ejecución del programa
# Inicia la aplicación utilizando el intérprete de Python
# configurado (entorno virtual o sistema).
###############################################################

# Mostrar mensaje de inicio con información adicional
echo -e "\n${BLUE}Iniciando el Analizador de la Conjetura de Collatz...${NC}"
echo -e "${GREEN}==================================================${NC}"
echo -e "${BLUE}Información del proyecto:${NC}"
echo -e "  - Repositorio: ${GREEN}https://github.com/686f6c61/Conjetura-de-Collatz${NC}"
echo -e "  - Reportar problemas: ${GREEN}https://github.com/686f6c61/Conjetura-de-Collatz/issues${NC}"
echo -e "${GREEN}==================================================${NC}\n"

# Ejecutar el programa con el intérprete adecuado
if [ -d "venv" ]; then
    # Usar Python del entorno virtual
    $VENV collatz_analyzer.py
else
    # Usar Python del sistema
    $PYTHON collatz_analyzer.py
fi

# Fin del script
