from MVC.Controllers.app import AppController
from MVC.Controllers.home import HomeController
from MVC.Controllers.all_positions import PositionsController
from MVC.Controllers.all_units import UnitsController
from MVC.Controllers.all_workers import AllWorkersController
from MVC.Controllers.all_projects import AllProjectsController
from MVC.Controllers.search import SearchController
from MVC.Controllers.add_new_worker import AddNewWorkerController


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model

        self.app = AppController(model, view)
        self.home_controller = HomeController(model, view)
        self.all_positions_controller = PositionsController(model, view)
        self.all_units_controller = UnitsController(model, view)
        self.all_workers_controller = AllWorkersController(model, view)
        self.all_projects = AllProjectsController(model, view)
        self.search_controller = SearchController(model, view)
        self.add_new_worker_controller = AddNewWorkerController(self, model, view)

    def start(self):
        self.view.start_app()
