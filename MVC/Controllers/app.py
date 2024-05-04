class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.app = view.app

        self.app.protocol("WM_DELETE_WINDOW", self.close_app)

    def close_app(self):
        self.model.connection.close()
        self.app.destroy()
