import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QSlider, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Функція для генерації гаусівської хвилі
def gaussian_wave(t, amplitude, mu, b_left, b_right):
    b = np.where(t < mu, b_left, b_right)
    return amplitude * np.exp(-((t - mu)**2) / (2 * b**2))

class ECGApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECG Simulator Pro")
        self.resize(900, 700)
        
        # Стан програми та параметри за замовчуванням
        self.is_paused = False
        self.current_time = 0
        self.params = {
            'P': [0.12, 0.15, 0.02, 0.02],
            'Q': [-0.05, 0.25, 0.01, 0.01],
            'R': [1.0, 0.35, 0.01, 0.01],
            'S': [-0.2, 0.42, 0.02, 0.02],
            'T': [0.3, 0.7, 0.05, 0.08]
        }
        
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)
        
        self.setup_page1_settings()
        self.setup_page2_monitor()
        
        # Таймер для анімації (40 мс)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(40)

    def setup_page1_settings(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("<h2>Налаштування параметрів моделі</h2>")
        layout.addWidget(title)
        
        # Таблиця для редагування
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Амплітуда (A)", "Зсув (mu)", "Ширина L", "Ширина R"])
        self.table.setVerticalHeaderLabels(["P", "Q", "R", "S", "T"])
        
        # Заповнення таблиці
        for row, (name, vals) in enumerate(self.params.items()):
            for col, val in enumerate(vals):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))
        
        layout.addWidget(self.table)
        
        btn_go_to_monitor = QPushButton("ЗАПУСТИТИ МОНІТОР")
        btn_go_to_monitor.setStyleSheet("font-weight: bold;")
        btn_go_to_monitor.clicked.connect(self.save_params_and_switch)
        layout.addWidget(btn_go_to_monitor)
        
        self.central_stack.addWidget(page)

    def setup_page2_monitor(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas)
        
        # Керування
        ctrl_layout = QHBoxLayout()
        btn_back = QPushButton("<<< НАЗАД")
        btn_back.clicked.connect(lambda: self.central_stack.setCurrentIndex(0))
        
        self.btn_pause = QPushButton("FREEZE")
        self.btn_pause.clicked.connect(self.toggle_pause)
        
        ctrl_layout.addWidget(btn_back)
        ctrl_layout.addWidget(self.btn_pause)
        layout.addLayout(ctrl_layout)
        
        # Слайдери
        self.bpm_slider, self.bpm_label = self.create_slider("Пульс (BPM)", 40, 160, 60)
        self.alt_slider, self.alt_label = self.create_slider("Рівень альтернації зубця T", 0, 100, 0)
        self.noise_slider, self.noise_label = self.create_slider("Шум", 0, 100, 5)
        
        for w in [self.bpm_label, self.bpm_slider, self.alt_label, self.alt_slider, self.noise_label, self.noise_slider]:
            layout.addWidget(w)
            
        self.central_stack.addWidget(page)

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
            print("Помилка: введіть коректні числа")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.btn_pause.setText("LIVE" if self.is_paused else "FREEZE")

    def update_animation(self):
        if self.is_paused or self.central_stack.currentIndex() == 0:
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
                actual_mu = mu * cycle_len + t_offset
                signal += gaussian_wave(t, curr_A, actual_mu, bl * cycle_len, br * cycle_len)
                
        # Додавання шуму
        signal += np.random.normal(0, noise_level, len(signal))
        
        # Малювання графіка
        self.ax.clear()
        self.ax.plot(t, signal, color='#2ecc71', lw=2)
        self.ax.set_ylim(-0.6, 1.6)
        self.ax.set_facecolor("#111111")
        self.ax.grid(True, color='#1a3320', linestyle=":")
        self.canvas.draw()
        
        self.current_time += 0.05

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECGApp()
    window.show()
    sys.exit(app.exec())