# -*- coding: utf-8 -*-
"""
Analizador de la Conjetura de Collatz

Este módulo implementa un analizador interactivo para la Conjetura de Collatz,
con múltiples visualizaciones y análisis estadísticos.
"""

# Bibliotecas estándar
import os
import json
import random
import time
from pathlib import Path

# Bibliotecas de visualización y análisis numérico
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider
from matplotlib import style

# Configuración del estilo visual para las gráficas
style.use('ggplot')

class CollatzAnalyzer:
    """
    Clase principal para el análisis y visualización de la Conjetura de Collatz.
    
    Esta clase proporciona métodos para generar, analizar y visualizar secuencias
    de Collatz, así como para guardar y cargar resultados.
    """
    
    def __init__(self):
        """
        Inicializa el analizador de Collatz con valores predeterminados.
        """
        # Límite máximo para números de entrada (10^21)
        self.MAX_NUM = 1000000000000000000000
        
        # Estado de ejecución del programa
        self.ejecutando = True
        
        # Ejemplos predefinidos para análisis rápido
        self.ejemplos = {
            '1': {'nombre': 'clásico', 'valor': 27},    # Ejemplo clásico
            '2': {'nombre': 'largo', 'valor': 97},      # Secuencia larga
            '3': {'nombre': 'extremo', 'valor': 871},   # Valores extremos
            '4': {'nombre': 'simple', 'valor': 13},     # Secuencia simple
            '5': {'nombre': 'gigante', 'valor': 999999999999999999999}  # Número enorme
        }
        
        # Configuración de animación
        self.animation_speed = 200  # Milisegundos entre fotogramas
        self.current_animation = None  # Referencia a la animación actual
        
    def guardar_secuencia(self, numero, secuencia, archivo):
        """
        Persiste una secuencia de Collatz en formato JSON.
        
        Args:
            numero (int): Número inicial que generó la secuencia
            secuencia (list): Lista de enteros que conforman la secuencia de Collatz
            archivo (str): Ruta del archivo donde se guardará la secuencia
            
        Returns:
            None
        """
        # Estructura de datos para almacenamiento
        datos = {
            'numero_inicial': numero,
            'secuencia': secuencia
        }
        
        # Escritura del archivo JSON
        with open(archivo, 'w') as f:
            json.dump(datos, f)
            
    def cargar_secuencia(self, archivo):
        """
        Recupera una secuencia de Collatz desde un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo JSON que contiene la secuencia
            
        Returns:
            tuple: Par (numero_inicial, secuencia) donde:
                - numero_inicial (int): Valor que generó la secuencia
                - secuencia (list): Lista de enteros que conforman la secuencia
                
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el formato del archivo es inválido
        """
        with open(archivo, 'r') as f:
            datos = json.load(f)
        return datos['numero_inicial'], datos['secuencia']

    def generar_aleatorio(self):
        """
        Genera un número entero aleatorio para análisis.
        
        Returns:
            int: Número aleatorio entre 2 y el máximo permitido (10^21)
        """
        return random.randint(2, self.MAX_NUM)

    def analizar_collatz(self, numero_inicial, guardar=None):
        if numero_inicial > self.MAX_NUM:
            print("Advertencia: Números muy grandes pueden requerir más tiempo de procesamiento")
        elif numero_inicial < 2:
            raise ValueError("El número debe ser mayor que 1")
            
        secuencia = self.collatz(numero_inicial)
        
        # Ofrecer diferentes tipos de visualización
        self.limpiar_pantalla()
        print("\n=== Opciones de Visualización ===")
        print("1. Gráficas estáticas (original)")
        print("2. Animación de la secuencia")
        print("3. Visualización en espiral")
        print("4. Visualización de árbol")
        
        opcion = input("\nSeleccione un tipo de visualización (1-4): ").strip()
        
        if opcion == '1':
            self.mostrar_graficas(numero_inicial, secuencia)
        elif opcion == '2':
            self.mostrar_animacion(numero_inicial, secuencia)
        elif opcion == '3':
            self.mostrar_espiral(numero_inicial, secuencia)
        elif opcion == '4':
            self.mostrar_arbol(numero_inicial, secuencia)
        else:
            print("Opción no válida, mostrando gráficas estáticas por defecto")
            self.mostrar_graficas(numero_inicial, secuencia)
        
        if guardar:
            self.guardar_secuencia(numero_inicial, secuencia, guardar)
            
        return secuencia

    def collatz(self, n):
        """
        Implementa el algoritmo de la Conjetura de Collatz.
        
        Para cada número n:
        - Si n es par, se divide entre 2
        - Si n es impar, se multiplica por 3 y se suma 1
        - Se repite hasta llegar a 1
        
        Args:
            n (int): Número inicial para generar la secuencia
            
        Returns:
            list: Secuencia completa de Collatz, comenzando con n y terminando en 1
        """
        secuencia = [n]  # Inicializar secuencia con el número de entrada
        
        # Iterar hasta llegar a 1
        while n != 1:
            # Aplicar regla de Collatz: n/2 si es par, 3n+1 si es impar
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            secuencia.append(n)
            
        return secuencia

    def mostrar_graficas(self, numero_inicial, secuencia):
        """Muestra las gráficas estáticas originales"""
        plt.figure(figsize=(12, 8))
        
        # Convertir a numpy array para mejor manejo de números grandes
        seq_array = np.array(secuencia, dtype=object)
        
        # Gráfica normal
        plt.subplot(2, 1, 1)
        plt.plot(range(len(seq_array)), seq_array, 'b-o', label='Secuencia')
        plt.title(f'Conjetura de Collatz para n = {numero_inicial:,}')
        plt.xlabel('Pasos')
        plt.ylabel('Valor')
        plt.grid(True)
        plt.legend()
        
        # Gráfica logarítmica
        plt.subplot(2, 1, 2)
        plt.plot(range(len(seq_array)), seq_array, 'r-o', label='Secuencia (escala log)')
        plt.yscale('log')
        plt.xlabel('Pasos')
        plt.ylabel('Valor (log)')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Mostrar estadísticas con formato para números grandes
        self.mostrar_estadisticas(numero_inicial, secuencia)

    def mostrar_estadisticas(self, numero_inicial, secuencia):
        """Muestra estadísticas sobre la secuencia"""
        print(f"\nEstadísticas para n = {numero_inicial:,}")
        print(f"Longitud de la secuencia: {len(secuencia):,}")
        print(f"Valor máximo alcanzado: {max(secuencia):,}")
        print("\nPrimeros 5 términos:")
        for i, num in enumerate(secuencia[:5], 1):
            print(f"  {i}. {num:,}")
        print("\nÚltimos 5 términos:")
        for i, num in enumerate(secuencia[-5:], len(secuencia)-4):
            print(f"  {i}. {num:,}")

    def mostrar_animacion(self, numero_inicial, secuencia):
        """Muestra una animación de la secuencia de Collatz"""
        # Crear figura y subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle(f'Animación de la Conjetura de Collatz para n = {numero_inicial:,}', fontsize=16)
        
        # Configurar los ejes
        ax1.set_xlabel('Pasos')
        ax1.set_ylabel('Valor')
        ax1.grid(True)
        
        ax2.set_xlabel('Pasos')
        ax2.set_ylabel('Valor (log)')
        ax2.set_yscale('log')
        ax2.grid(True)
        
        # Inicializar líneas vacías
        line1, = ax1.plot([], [], 'b-o', lw=2)
        line2, = ax2.plot([], [], 'r-o', lw=2)
        
        # Texto para mostrar el valor actual
        text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.7))
        
        # Establecer límites
        max_val = max(secuencia)
        ax1.set_xlim(0, len(secuencia))
        ax1.set_ylim(0, max_val * 1.1)
        ax2.set_xlim(0, len(secuencia))
        ax2.set_ylim(1, max_val * 1.1)
        
        # Función de inicialización
        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            text.set_text('')
            return line1, line2, text
        
        # Función de animación
        def animate(i):
            x = range(i+1)
            y = secuencia[:i+1]
            line1.set_data(x, y)
            line2.set_data(x, y)
            if i < len(secuencia):
                text.set_text(f'Paso {i}: {secuencia[i]:,}')
            return line1, line2, text
        
        # Crear botones para controlar la animación
        plt.subplots_adjust(bottom=0.2)
        
        # Área para los botones
        play_ax = plt.axes([0.3, 0.05, 0.1, 0.075])
        pause_ax = plt.axes([0.41, 0.05, 0.1, 0.075])
        reset_ax = plt.axes([0.52, 0.05, 0.1, 0.075])
        
        # Área para el slider de velocidad
        speed_ax = plt.axes([0.3, 0.15, 0.4, 0.03])
        
        # Crear los botones y el slider
        play_button = Button(play_ax, 'Play')
        pause_button = Button(pause_ax, 'Pause')
        reset_button = Button(reset_ax, 'Reset')
        speed_slider = Slider(speed_ax, 'Velocidad', 10, 500, valinit=self.animation_speed)
        
        # Crear la animación
        ani = animation.FuncAnimation(fig, animate, frames=len(secuencia),
                                      init_func=init, interval=self.animation_speed, 
                                      blit=True, repeat=False)
        
        self.current_animation = ani
        
        # Funciones de control
        def play(event):
            self.current_animation.event_source.start()
            
        def pause(event):
            self.current_animation.event_source.stop()
            
        def reset(event):
            self.current_animation.frame_seq = self.current_animation.new_frame_seq()
            self.current_animation.event_source.start()
            
        def update_speed(val):
            self.animation_speed = int(val)
            self.current_animation.event_source.interval = self.animation_speed
        
        # Conectar los eventos
        play_button.on_clicked(play)
        pause_button.on_clicked(pause)
        reset_button.on_clicked(reset)
        speed_slider.on_changed(update_speed)
        
        plt.show()
        
        # Mostrar estadísticas después de la animación
        self.mostrar_estadisticas(numero_inicial, secuencia)

    def mostrar_espiral(self, numero_inicial, secuencia):
        """Muestra la secuencia como una espiral"""
        # Crear figura
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        
        # Calcular ángulos y radios para la espiral
        n = len(secuencia)
        theta = np.linspace(0, 10*np.pi, n)  # 10 vueltas
        
        # Normalizar los valores para el radio
        max_val = max(secuencia)
        radii = np.array([val/max_val for val in secuencia])
        
        # Convertir a coordenadas cartesianas
        x = theta * np.cos(theta) * radii
        y = theta * np.sin(theta) * radii
        
        # Crear colores basados en si el número es par o impar
        colors = ['blue' if val % 2 == 0 else 'red' for val in secuencia]
        
        # Dibujar la espiral con puntos coloreados
        scatter = ax.scatter(x, y, c=colors, s=50, alpha=0.7)
        
        # Dibujar líneas conectando los puntos
        ax.plot(x, y, 'gray', alpha=0.3)
        
        # Añadir título y leyenda
        ax.set_title(f'Espiral de Collatz para n = {numero_inicial:,}')
        ax.axis('equal')
        ax.axis('off')
        
        # Añadir leyenda
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Número par'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Número impar')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Animación de la espiral
        def init():
            scatter.set_offsets(np.column_stack([[], []]))
            return scatter,
        
        def animate(i):
            data = np.column_stack([x[:i+1], y[:i+1]])
            scatter.set_offsets(data)
            return scatter,
        
        ani = animation.FuncAnimation(fig, animate, frames=n,
                                     init_func=init, interval=50, 
                                     blit=True, repeat=False)
        
        plt.show()
        
        # Mostrar estadísticas
        self.mostrar_estadisticas(numero_inicial, secuencia)

    def mostrar_arbol(self, numero_inicial, secuencia):
        """Muestra un árbol de decisiones para la secuencia de Collatz"""
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Inicializar posiciones
        x = [0]  # Posición x inicial
        y = [0]  # Posición y inicial
        
        # Crear posiciones para cada número en la secuencia
        for i in range(1, len(secuencia)):
            prev_val = secuencia[i-1]
            curr_val = secuencia[i]
            
            # Si el número anterior era par, moverse a la derecha y abajo
            if prev_val % 2 == 0:
                x.append(x[-1] + 1)
                y.append(y[-1] - 0.5)
            # Si era impar, moverse a la izquierda y abajo
            else:
                x.append(x[-1] - 1)
                y.append(y[-1] - 0.5)
        
        # Normalización de valores para visualización
        # Convertimos explícitamente a float para evitar desbordamientos con números grandes
        # y problemas con la función isnan() en la visualización
        max_val = float(max(secuencia))
        
        # Creamos valores normalizados en el rango [0,1] para el mapa de colores
        norm_values = [float(val) / max_val for val in secuencia]
        
        # Aplicamos el mapa de colores 'viridis' a los valores normalizados
        colors = plt.cm.viridis(norm_values)
        
        # Inicializar scatter plot
        scatter = ax.scatter([], [], s=100, c=[], cmap='viridis')
        
        # Inicializar líneas
        line, = ax.plot([], [], 'gray', alpha=0.5)
        
        # Configurar ejes
        ax.set_title(f'Árbol de Collatz para n = {numero_inicial:,}')
        ax.set_xlabel('Dirección (izquierda: impar, derecha: par)')
        ax.set_ylabel('Pasos')
        
        # Ajustar límites
        margin = 1
        ax.set_xlim(min(x) - margin, max(x) + margin)
        ax.set_ylim(min(y) - margin, max(y) + margin)
        
        # Añadir colorbar
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=1, vmax=max_val))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Valor en la secuencia')
        
        # Función de animación
        def init():
            scatter.set_offsets(np.empty((0, 2)))
            line.set_data([], [])
            return scatter, line
        
        def animate(i):
            data = np.column_stack([x[:i+1], y[:i+1]])
            scatter.set_offsets(data)
            scatter.set_color(colors[:i+1])
            line.set_data(x[:i+1], y[:i+1])
            return scatter, line
        
        ani = animation.FuncAnimation(fig, animate, frames=len(secuencia),
                                     init_func=init, interval=50, 
                                     blit=True, repeat=False)
        
        plt.tight_layout()
        plt.show()
        
        # Mostrar estadísticas
        self.mostrar_estadisticas(numero_inicial, secuencia)

    def salir_graciosamente(self):
        """Maneja la salida limpia del programa"""
        self.limpiar_pantalla()
        print("\n\n¡Hasta luego!")
        print("  _____")
        print(" /     \\")
        print("|  Bye! |")
        print(" \\_____/\n")
        self.ejecutando = False

    def menu_principal(self):
        try:
            while self.ejecutando:
                self.limpiar_pantalla()
                print("\033[1;34m=== COLLATZ - 686f6c61 ===\033[0m")
                print("\033[0m")
                
                print("\033[1;32m=== Analizador de la Conjetura de Collatz ===\033[0m")
                print("\033[1;34mRepositorio:\033[0m https://github.com/686f6c61/Conjetura-de-Collatz")
                print("\033[1;34mAutor:\033[0m 686f6c61")
                
                print("\033[1;36mMenú Principal:\033[0m")
                print("  \033[1;33m1.\033[0m Analizar un número específico")
                print("  \033[1;33m2.\033[0m Usar ejemplo predefinido")
                print("  \033[1;33m3.\033[0m Generar número aleatorio")
                print("  \033[1;33m4.\033[0m Cargar secuencia guardada")
                print("  \033[1;33m5.\033[0m Comparar secuencias")
                print("  \033[1;33m6.\033[0m Salir")
                
                try:
                    opcion = input("\nSeleccione una opción (1-6): ").strip()
                    
                    if opcion == '1':
                        self.analizar_numero_especifico()
                    elif opcion == '2':
                        self.usar_ejemplo()
                    elif opcion == '3':
                        self.analizar_aleatorio()
                    elif opcion == '4':
                        self.cargar_secuencia_interactiva()
                    elif opcion == '5':
                        self.comparar_secuencias()
                    elif opcion == '6':
                        self.salir_graciosamente()
                        break
                    else:
                        input("\nOpción no válida. Presione Enter para continuar...")
                except KeyboardInterrupt:
                    self.salir_graciosamente()
                    break

        except KeyboardInterrupt:
            self.salir_graciosamente()

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def analizar_numero_especifico(self):
        try:
            self.limpiar_pantalla()
            print("\n=== Analizar número específico ===")
            while True:
                try:
                    entrada = input(f"\nIngrese un número entre 2 y {self.MAX_NUM:,}: ")
                    # Eliminar comas y espacios para facilitar la entrada de números grandes
                    entrada = entrada.replace(',', '').replace(' ', '')
                    numero = int(entrada)
                    if 2 <= numero <= self.MAX_NUM:
                        break
                    print(f"El número debe estar entre 2 y {self.MAX_NUM:,}")
                except ValueError:
                    print("Por favor, ingrese un número válido")

            # Advertencia para números muy grandes
            if numero > 1000000000:
                print("\n⚠️  ADVERTENCIA: Números muy grandes pueden requerir más tiempo")
                print("   y memoria para procesar. ¿Desea continuar? (s/n)")
                if input().lower() != 's':
                    return
            
            guardar = input("\n¿Desea guardar la secuencia? (s/n): ").lower() == 's'
            archivo = None
            if guardar:
                archivo = input("Nombre del archivo para guardar (sin extensión): ").strip() + '.json'
            
            self.analizar_collatz(numero, archivo if guardar else None)
            input("\nPresione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para volver al menú principal...")

    def usar_ejemplo(self):
        try:
            self.limpiar_pantalla()
            print("\n=== Ejemplos predefinidos ===")
            for key, valor in self.ejemplos.items():
                print(f"{key}. {valor['nombre'].title()} (n = {valor['valor']})")
            
            while True:
                opcion = input("\nSeleccione un ejemplo (1-5): ").strip()
                if opcion in self.ejemplos:
                    numero = self.ejemplos[opcion]['valor']
                    self.analizar_collatz(numero)
                    break
                print("Opción no válida")
            
            input("\nPresione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para volver al menú principal...")

    def analizar_aleatorio(self):
        try:
            self.limpiar_pantalla()
            print("\n=== Número Aleatorio ===")
            numero = self.generar_aleatorio()
            print(f"\nNúmero generado: {numero}")
            
            guardar = input("\n¿Desea guardar la secuencia? (s/n): ").lower() == 's'
            archivo = None
            if guardar:
                archivo = input("Nombre del archivo para guardar (sin extensión): ").strip() + '.json'
            
            self.analizar_collatz(numero, archivo if guardar else None)
            input("\nPresione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para volver al menú principal...")

    def cargar_secuencia_interactiva(self):
        try:
            self.limpiar_pantalla()
            print("\n=== Cargar Secuencia ===")
            archivo = input("\nNombre del archivo a cargar (con extensión .json): ").strip()
            
            try:
                numero, secuencia = self.cargar_secuencia(archivo)
                
                # Ofrecer opciones de visualización
                print("\n=== Opciones de Visualización ===")
                print("1. Gráficas estáticas")
                print("2. Animación de la secuencia")
                print("3. Visualización en espiral")
                print("4. Visualización de árbol")
                
                opcion = input("\nSeleccione un tipo de visualización (1-4): ").strip()
                
                if opcion == '1':
                    self.mostrar_graficas(numero, secuencia)
                elif opcion == '2':
                    self.mostrar_animacion(numero, secuencia)
                elif opcion == '3':
                    self.mostrar_espiral(numero, secuencia)
                elif opcion == '4':
                    self.mostrar_arbol(numero, secuencia)
                else:
                    print("Opción no válida, mostrando gráficas estáticas por defecto")
                    self.mostrar_graficas(numero, secuencia)
                
            except FileNotFoundError:
                print(f"\nError: No se encontró el archivo {archivo}")
            except json.JSONDecodeError:
                print(f"\nError: El archivo {archivo} no tiene un formato JSON válido")
            
            input("\nPresione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para volver al menú principal...")

    def comparar_secuencias(self):
        """Compara dos secuencias de Collatz visualmente"""
        try:
            self.limpiar_pantalla()
            print("\n=== Comparar Secuencias ===")
            
            # Obtener el primer número
            while True:
                try:
                    entrada1 = input(f"\nIngrese el primer número (entre 2 y {self.MAX_NUM:,}): ")
                    entrada1 = entrada1.replace(',', '').replace(' ', '')
                    numero1 = int(entrada1)
                    if 2 <= numero1 <= self.MAX_NUM:
                        break
                    print(f"El número debe estar entre 2 y {self.MAX_NUM:,}")
                except ValueError:
                    print("Por favor, ingrese un número válido")
            
            # Obtener el segundo número
            while True:
                try:
                    entrada2 = input(f"\nIngrese el segundo número (entre 2 y {self.MAX_NUM:,}): ")
                    entrada2 = entrada2.replace(',', '').replace(' ', '')
                    numero2 = int(entrada2)
                    if 2 <= numero2 <= self.MAX_NUM:
                        break
                    print(f"El número debe estar entre 2 y {self.MAX_NUM:,}")
                except ValueError:
                    print("Por favor, ingrese un número válido")
            
            # Generar secuencias
            secuencia1 = self.collatz(numero1)
            secuencia2 = self.collatz(numero2)
            
            # Crear figura para comparación
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            fig.suptitle(f'Comparación de secuencias: {numero1:,} vs {numero2:,}', fontsize=16)
            
            # Gráfica normal
            ax1.plot(range(len(secuencia1)), secuencia1, 'b-', label=f'n = {numero1:,}')
            ax1.plot(range(len(secuencia2)), secuencia2, 'r-', label=f'n = {numero2:,}')
            ax1.set_xlabel('Pasos')
            ax1.set_ylabel('Valor')
            ax1.grid(True)
            ax1.legend()
            
            # Gráfica logarítmica
            ax2.plot(range(len(secuencia1)), secuencia1, 'b-', label=f'n = {numero1:,}')
            ax2.plot(range(len(secuencia2)), secuencia2, 'r-', label=f'n = {numero2:,}')
            ax2.set_yscale('log')
            ax2.set_xlabel('Pasos')
            ax2.set_ylabel('Valor (log)')
            ax2.grid(True)
            ax2.legend()
            
            plt.tight_layout()
            plt.show()
            
            # Mostrar estadísticas comparativas
            print(f"\n=== Estadísticas Comparativas ===")
            print(f"Número inicial 1: {numero1:,}")
            print(f"Longitud de secuencia 1: {len(secuencia1):,}")
            print(f"Valor máximo alcanzado 1: {max(secuencia1):,}")
            print(f"\nNúmero inicial 2: {numero2:,}")
            print(f"Longitud de secuencia 2: {len(secuencia2):,}")
            print(f"Valor máximo alcanzado 2: {max(secuencia2):,}")
            
            input("\nPresione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            input("\nPresione Enter para volver al menú principal...")

def main():
    try:
        analizador = CollatzAnalyzer()
        analizador.menu_principal()
    except KeyboardInterrupt:
        analizador.salir_graciosamente()
    except Exception as e:
        print(f"\n\nError inesperado: {e}")
        print("\nEl programa se cerrará.")

if __name__ == "__main__":
    main()
