import tkinter.ttk as ttk


class BestWorkerView:
    def __init__(self, notebook, post_name):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.notebook.insert("end", self.mainFrame, text="Найкращий працівник на посаді: " + post_name)
        self.notebook.select(self.mainFrame)

        self.worker_frame = ttk.Frame(self.mainFrame)
        self.worker_frame.pack(padx=5, pady=5)

        self.close_button = ttk.Button(self.mainFrame, text="Закрити вкладку")
        self.close_button.pack(fill='both', padx=5, pady=5)
