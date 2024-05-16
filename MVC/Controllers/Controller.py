from MVC.Controllers.app import AppController
from MVC.Controllers.home import HomeController
from MVC.Controllers.all_positions import PositionsController
from MVC.Controllers.all_units import UnitsController
from MVC.Controllers.all_workers import AllWorkersController
from MVC.Controllers.all_projects import AllProjectsController
from MVC.Controllers.add_new_worker import AddNewWorkerController


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model

        self.app = AppController(model, view)
        self.home_controller = HomeController(self, model, view)
        self.add_new_worker_controller = None
        self.all_positions_controller = None
        self.all_units_controller = None
        self.all_workers_controller = None
        self.all_projects = None

    def create_all_positions_controller(self):
        self.all_positions_controller = PositionsController(self.model, self.view)

    def create_all_units_controller(self):
        self.all_units_controller = UnitsController(self, self.model, self.view)

    def create_all_workers_controller(self):
        self.all_workers_controller = AllWorkersController(self, self.model, self.view)

    def create_add_new_worker_controller(self):
        self.add_new_worker_controller = AddNewWorkerController(self, self.model, self.view)

    def create_all_projects_controller(self):
        self.all_projects = AllProjectsController(self, self.model, self.view)

    def start(self):
        self.view.start_app()
