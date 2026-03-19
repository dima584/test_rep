import tkinter as tkt
from tkinter import ttk, messagebox
import math

class GoldenSectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод Золотого Перетину")
        self.root.geometry("900x600")
        input_frame = ttk.LabelFrame(root, text="Вхідні дані", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Функція
        ttk.Label(input_frame, text="f(x) = ").grid(row=0, column=0, sticky="e")
        self.func_entry = ttk.Entry(input_frame, width=40)
        self.func_entry.insert(0, "x**2 + 4*exp(-0.25*x)")
        self.func_entry.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)
        
        ttk.Label(input_frame, text="", 
                  font=("Arial", 8), foreground="gray").grid(row=0, column=4, sticky="w")

        # Інтервал та точність
        ttk.Label(input_frame, text="a (початок):").grid(row=1, column=0, sticky="e", pady=5)
        self.a_entry = ttk.Entry(input_frame, width=10)
        self.a_entry.insert(0, "-3")
        self.a_entry.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(input_frame, text="b (кінець):").grid(row=1, column=2, sticky="e")
        self.b_entry = ttk.Entry(input_frame, width=10)
        self.b_entry.insert(0, "2")
        self.b_entry.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(input_frame, text="ε (точність):").grid(row=1, column=4, sticky="e")
        self.eps_entry = ttk.Entry(input_frame, width=10)
        self.eps_entry.insert(0, "0.01")
        self.eps_entry.grid(row=1, column=5, sticky="w", padx=5)

        # Кнопка
        calc_btn = ttk.Button(input_frame, text="ОБЧИСЛИТИ", command=self.calculate)
        calc_btn.grid(row=1, column=6, padx=20)

        result_frame = ttk.LabelFrame(root, text="Результат", padding="10")
        result_frame.pack(fill="x", padx=10, pady=5)

        self.res_label_x = ttk.Label(result_frame, text="x_min = ...", font=("Arial", 12, "bold"), foreground="blue")
        self.res_label_x.pack(side="left", padx=20)
        
        self.res_label_y = ttk.Label(result_frame, text="y_min = ...", font=("Arial", 12, "bold"), foreground="green")
        self.res_label_y.pack(side="left", padx=20)

        table_frame = ttk.Frame(root, padding="10")
        table_frame.pack(fill="both", expand=True)

        cols = ("k", "a", "b", "x1", "x2", "f(x1)", "f(x2)")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        
        # Заголовки стовпців
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Скролбар для таблиці
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_func_value(self, expr, x):
        # Безпечне обчислення функції
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names['x'] = x
        return eval(expr, {"__builtins__": {}}, allowed_names)

    def calculate(self):
        # Очищення таблиці
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        try:
            expr = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            epsilon = float(self.eps_entry.get())
            
            # Перевірка формули
            self.get_func_value(expr, a)
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Перевірте дані!\n{e}")
            return

        phi = 1.618
        k = 0
        
        x1 = b - (b - a) / phi
        x2 = a + (b - a) / phi
        f1 = self.get_func_value(expr, x1)
        f2 = self.get_func_value(expr, x2)
 
        
        while abs(b - a) > epsilon:
            # Додаємо рядок у таблицю
            self.tree.insert("", "end", values=(
                k, 
                f"{a:.5f}", f"{b:.5f}", 
                f"{x1:.5f}", f"{x2:.5f}", 
                f"{f1:.5f}", f"{f2:.5f}"
            ))
            
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = b - (b - a) / phi
                f1 = self.get_func_value(expr, x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = a + (b - a) / phi
                f2 = self.get_func_value(expr, x2)
            k += 1
            
            # Запобіжник від зависання
            if k > 1000:
                messagebox.showwarning("Увага", "Занадто багато ітерацій!")
                break

        self.tree.insert("", "end", values=(
                k, 
                f"{a:.5f}", f"{b:.5f}", 
                f"{x1:.5f}", f"{x2:.5f}", 
                f"{f1:.5f}", f"{f2:.5f}"
            ))

        # Результат
        x_min = (a + b) / 2
        y_min = self.get_func_value(expr, x_min)
        
        self.res_label_x.config(text=f"x_min ≈ {x_min:.5f}")
        self.res_label_y.config(text=f"y_min ≈ {y_min:.5f}")

if __name__ == "__main__":
    root = tkt.Tk()
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except:
        pass
        
    app = GoldenSectionApp(root)
    root.mainloop()