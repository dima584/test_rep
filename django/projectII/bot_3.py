import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QSlider, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QStackedWidget, QHeaderView,
                             QRadioButton, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def gaussian_wave(t, amplitude, mu, b_left, b_right):
    b_t = np.where(t <= mu, b_left, b_right)
    return amplitude * np.exp(-((t - mu)**2) / (2 * b_t**2))

# Експоненціальне згладжування
def exponential_smoothing(signal, alpha=0.1):
    smoothed = np.zeros_like(signal)
    smoothed[0] = signal[0]
    for k in range(1, len(signal)):
        smoothed[k] = alpha * signal[k] + (1 - alpha) * smoothed[k-1]
    return smoothed

# Метод ковзного середнього
def moving_average(signal, window_size=5):
    if window_size < 1: window_size = 1
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(signal, window, 'same')

# --- ГОЛОВНИЙ КЛАС ДОДАТКУ ---
class ECGApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Симулятор ЕКГ та Фільтрації (КП-5)")
        self.resize(1000, 750)
        
        # СТАН ПРОГРАМИ
        self.is_paused = False
        self.current_time = 0
        self.params = {
            'P':  [0.12, 0.15, 0.02, 0.02],
            'Q':  [-0.05, 0.25, 0.01, 0.01],
            'R':  [1.0, 0.35, 0.01, 0.01],
            'S':  [-0.2, 0.42, 0.02, 0.02],
            'T':  [0.3, 0.7, 0.08, 0.04] # Асиметрія зубця Т
        }
        
        # СТЕК СТОРІНОК
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)
        
        # Ініціалізація всіх 3-х сторінок одразу
        self.setup_page1_settings()
        self.setup_page2_monitor()
        self.setup_page3_filter()
        
        # Таймер для анімації (Працює тільки на 2 сторінці)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(40)

    # --- СТОРІНКА 1: ТАБЛИЦЯ ПАРАМЕТРІВ ---
    def setup_page1_settings(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>Крок 1: Налаштування параметрів зубців (КП-4)</h2>"))
        
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Амплітуда (A)", "Час (mu)", "b_left", "b_right"])
        self.table.setVerticalHeaderLabels(["P", "Q", "R", "S", "T"])
        
        for row, (wave, vals) in enumerate(self.params.items()):
            for col, val in enumerate(vals):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        btn_start = QPushButton("ЗБЕРЕГТИ ТА ПЕРЕЙТИ ДО МОНІТОРА >>>")
        btn_start.setFixedHeight(50)
        btn_start.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; font-size: 14px;")
        btn_start.clicked.connect(self.save_params_and_switch)
        layout.addWidget(btn_start)
        
        self.central_stack.addWidget(page)

    # --- СТОРІНКА 2: LIVE МОНІТОР ---
    def setup_page2_monitor(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.figure_live = Figure(figsize=(10, 4))
        self.canvas_live = FigureCanvas(self.figure_live)
        self.ax_live = self.figure_live.add_subplot(111)
        layout.addWidget(self.canvas_live)
        
        # Кнопки
        ctrl_layout = QHBoxLayout()
        btn_back = QPushButton("<<< Назад до таблиці")
        btn_back.clicked.connect(lambda: self.central_stack.setCurrentIndex(0))
        
        self.btn_pause = QPushButton("FREEZE / LIVE")
        self.btn_pause.clicked.connect(self.toggle_pause)

        self.btn_filter_page = QPushButton("ПЕРЕЙТИ ДО ЗГЛАДЖУВАННЯ (КП-5) >>>")
        self.btn_filter_page.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold;")
        # Перехід на сторінку 3 і оновлення графіка фільтрації
        self.btn_filter_page.clicked.connect(self.go_to_filter_page) 
        
        ctrl_layout.addWidget(btn_back)
        ctrl_layout.addWidget(self.btn_pause)
        ctrl_layout.addWidget(self.btn_filter_page)
        layout.addLayout(ctrl_layout)
        
        # Повзунки
        self.bpm_slider, self.bpm_label = self.create_slider("Пульс (BPM)", 40, 160, 60)
        self.alt_slider, self.alt_label = self.create_slider("Альтернація T", 0, 100, 0)
        self.noise_slider, self.noise_label = self.create_slider("Шум", 0, 100, 10)
        
        for w in [self.bpm_label, self.bpm_slider, self.alt_label, self.alt_slider, self.noise_label, self.noise_slider]:
            layout.addWidget(w)
            
        self.central_stack.addWidget(page)

    # --- СТОРІНКА 3: ФІЛЬТРАЦІЯ (КП-5) ---
    def setup_page3_filter(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.fig_filter = Figure(figsize=(10, 5))
        self.canvas_filter = FigureCanvas(self.fig_filter)
        layout.addWidget(self.canvas_filter)
        
        controls = QHBoxLayout()
        
        # Вибір методу
        method_group = QGroupBox("Метод приглушення завад")
        method_layout = QVBoxLayout()
        self.radio_exp = QRadioButton("Експоненціальне згладжування")
        self.radio_ma = QRadioButton("Ковзне середнє")
        self.radio_exp.setChecked(True)
        
        self.radio_exp.toggled.connect(self.toggle_filter_method)
        self.radio_ma.toggled.connect(self.toggle_filter_method)
        
        method_layout.addWidget(self.radio_exp)
        method_layout.addWidget(self.radio_ma)
        method_group.setLayout(method_layout)
        controls.addWidget(method_group)
        
        # Налаштування параметрів
        params_group = QGroupBox("Параметри")
        params_layout = QVBoxLayout()
        
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Рівень згладжування α:"))
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setRange(1, 99) 
        self.alpha_slider.setValue(20) # α = 0.2
        self.alpha_slider.valueChanged.connect(self.update_filter_plot)
        alpha_layout.addWidget(self.alpha_slider)
        params_layout.addLayout(alpha_layout)
        
        w_layout = QHBoxLayout()
        w_layout.addWidget(QLabel("Ширина вікна W:"))
        self.w_slider = QSlider(Qt.Orientation.Horizontal)
        self.w_slider.setRange(1, 50)
        self.w_slider.setValue(15)
        self.w_slider.valueChanged.connect(self.update_filter_plot)
        w_layout.addWidget(self.w_slider)
        params_layout.addLayout(w_layout)
        
        params_group.setLayout(params_layout)
        controls.addWidget(params_group)
        layout.addLayout(controls)
        
        btn_back = QPushButton("<<< ПОВЕРНУТИСЬ ДО МОНІТОРА")
        btn_back.setFixedHeight(40)
        btn_back.clicked.connect(lambda: self.central_stack.setCurrentIndex(1))
        layout.addWidget(btn_back)
        
        self.central_stack.addWidget(page)
        self.toggle_filter_method()

    # --- ДОПОМІЖНІ ФУНКЦІЇ ---
    def create_slider(self, name, min_val, max_val, start_val):
        label = QLabel(f"{name}: {start_val}")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(start_val)
        return slider, label

    def save_params_and_switch(self):
        try:
            for row, wave in enumerate(['P', 'Q', 'R', 'S', 'T']):
                for col in range(4):
                    self.params[wave][col] = float(self.table.item(row, col).text())
            self.central_stack.setCurrentIndex(1)
        except ValueError:
            print("Помилка: введіть коректні числа!")

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def go_to_filter_page(self):
        self.central_stack.setCurrentIndex(2)
        self.update_filter_plot()

    def toggle_filter_method(self):
        # Блокування неактивного повзунка згідно з КП-5
        is_exp = self.radio_exp.isChecked()
        self.alpha_slider.setEnabled(is_exp)
        self.w_slider.setEnabled(not is_exp)
        self.update_filter_plot()

    # --- ЛОГІКА МАЛЮВАННЯ (МОНІТОР) ---
    def update_animation(self):
        if self.is_paused or self.central_stack.currentIndex() != 1:
            return

        bpm = self.bpm_slider.value()
        alt_level = self.alt_slider.value() / 100.0
        noise_level = self.noise_slider.value() / 500.0
        
        self.bpm_label.setText(f"Пульс (BPM): {bpm}")
        self.alt_label.setText(f"Рівень альтернації зубця T: {alt_level:.2f}")
        self.noise_label.setText(f"Шум: {self.noise_slider.value()}")

        cycle_len = 60.0 / bpm 
        window_size = 3.0
        t = np.linspace(self.current_time, self.current_time + window_size, 600)
        signal = np.zeros_like(t)

        start_cycle = int(self.current_time / cycle_len)
        end_cycle = int((self.current_time + window_size) / cycle_len) + 1

        for i in range(start_cycle, end_cycle):
            t_offset = i * cycle_len
            t_factor = 1.0 + (alt_level if i % 2 == 0 else -alt_level)
            
            for wave, (A, mu, bl, br) in self.params.items():
                curr_A = A * t_factor if wave == 'T' else A
                actual_mu = (mu * cycle_len) + t_offset
                signal += gaussian_wave(t, curr_A, actual_mu, bl * cycle_len, br * cycle_len)

        signal += np.random.normal(0, noise_level, len(signal))

        self.ax_live.clear()
        self.ax_live.plot(t, signal, color='#2ecc71', lw=2)
        self.ax_live.set_ylim(-0.6, 1.6)
        self.ax_live.set_facecolor('#0d0d0d')
        self.ax_live.grid(True, color='#1a3320', linestyle=':')
        self.canvas_live.draw()
        
        self.current_time += 0.05

    # --- ЛОГІКА МАЛЮВАННЯ (ФІЛЬТРАЦІЯ) ---
    def update_filter_plot(self):
        # Генеруємо статичний шматок ЕКГ (5 секунд)
        t = np.linspace(0, 5, 1000)
        clean_signal = np.zeros_like(t)
        cycle_len = 60.0 / self.bpm_slider.value() # Беремо поточний пульс
        
        for i in range(10): # Генеруємо з запасом
            t_offset = i * cycle_len
            for wave, (A, mu, bl, br) in self.params.items():
                actual_mu = (mu * cycle_len) + t_offset
                clean_signal += gaussian_wave(t, A, actual_mu, bl * cycle_len, br * cycle_len)
                
        # Беремо рівень шуму з повзунка монітора
        noise_level = self.noise_slider.value() / 500.0
        if noise_level == 0:
            noise_level = 0.08 # Якщо шуму не було, додаємо мінімальний для тесту
            
        noisy_signal = clean_signal + np.random.normal(0, noise_level, len(clean_signal))
        
        # Застосовуємо обраний метод
        if self.radio_exp.isChecked():
            alpha = self.alpha_slider.value() / 100.0
            smoothed_signal = exponential_smoothing(noisy_signal, alpha)
            title = f"Експоненціальне згладжування (α = {alpha})"
        else:
            w = self.w_slider.value()
            smoothed_signal = moving_average(noisy_signal, w)
            title = f"Ковзне середнє (W = {w})"
            
        # Малюємо графік
        self.ax_filter = self.fig_filter.gca()
        self.ax_filter.clear()
        
        # Спочатку червоний шумний сигнал, потім зверху синій очищений
        self.ax_filter.plot(t, noisy_signal, color='#e74c3c', alpha=0.6, label="Зашумлений сигнал")
        self.ax_filter.plot(t, smoothed_signal, color='#2c3e50', lw=2, label="Згладжений сигнал")
        
        self.ax_filter.set_xlim(0, 5)
        self.ax_filter.set_ylim(-0.6, 1.6)
        self.ax_filter.set_title(title)
        self.ax_filter.legend(loc="upper right")
        self.ax_filter.grid(True, linestyle='--')
        self.canvas_filter.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECGApp()
    window.show()
    sys.exit(app.exec())