class UnitsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Units']