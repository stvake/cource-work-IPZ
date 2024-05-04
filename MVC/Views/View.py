from MVC.Views.app import App
from MVC.Views.home import HomeView
from MVC.Views.all_workers import AllWorkersView
from MVC.Views.all_units import AllUnitsView
from MVC.Views.all_positions import AllPositionsView
from MVC.Views.search import SearchView
from MVC.Views.all_projects import AllProjectsView
from MVC.Views.worker import WorkerView
from MVC.Views.full_worker_info import FullWorkerInfoView
from MVC.Views.add_new_worker import AddNewWorkerView
from MVC.Views.worker_project import WorkerProjectView


class View:
    def __init__(self):
        self.app = App()
        self.worker_tabs = {}
        self.full_info_tabs = {}
        self.worker_projects_tabs = {}
        self.tabs = {
            'Home': HomeView(self.app.notebook),
            'Workers': AllWorkersView(self.app.notebook),
            'Units': AllUnitsView(self.app.notebook),
            'Positions': AllPositionsView(self.app.notebook),
            'Search': SearchView(self.app.notebook),
            'AddNewWorker': AddNewWorkerView(self.app.notebook),
            'AllProjects': AllProjectsView(self.app.notebook),
        }

    def create_tab(self, worker_id, view_type, *args):
        if view_type == 'Worker':
            self.worker_tabs[worker_id] = WorkerView(*args)
        elif view_type == 'FullWorkerInfo':
            self.full_info_tabs[worker_id] = FullWorkerInfoView(*args)
        elif view_type == 'OpenProjects':
            self.worker_projects_tabs[worker_id] = WorkerProjectView(*args)

    def add_new_worker(self):
        self.tabs['AddNewWorker'].add_tab()

    def start_app(self):
        self.app.mainloop()
