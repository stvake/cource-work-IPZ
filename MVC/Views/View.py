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
            'AddNewWorker': AddNewWorkerView(self.app.notebook),
            'Workers': AllWorkersView(self.app.notebook)
        }

    def create_tab(self, *args):
        if args[0] == 'Units':
            return AllUnitsView(self.app.notebook)
        elif args[0] == 'Positions':
            return AllPositionsView(self.app.notebook)
        elif args[0] == 'Search':
            return SearchView(self.app.notebook)
        elif args[0] == 'AllProjects':
            return AllProjectsView(self.app.notebook)
        elif args[0] == 'Worker':
            self.worker_tabs[args[1]] = WorkerView(*args[2:])
        elif args[0] == 'FullWorkerInfo':
            self.full_info_tabs[args[1]] = FullWorkerInfoView(*args[2:])
        elif args[0] == 'OpenProjects':
            self.worker_projects_tabs[args[1]] = WorkerProjectView(*args[2:])

    def add_new_worker(self):
        self.tabs['AddNewWorker'].add_tab()

    def start_app(self):
        self.app.mainloop()
