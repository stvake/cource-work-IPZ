class SearchController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['Search'] = self.view.create_tab('Search')
        self.tab = self.view.tabs['Search']
