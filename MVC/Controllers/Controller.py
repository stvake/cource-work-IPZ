from MVC.Controllers.home import HomeController
from MVC.Controllers.all_positions import PositionsController
from MVC.Controllers.all_units import UnitsController
from MVC.Controllers.all_workers import AllWorkersController
from MVC.Controllers.worker import WorkerController
from MVC.Controllers.add_new_worker import AddNewWorker


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model

        self.home_controller = HomeController(model, view)
        self.all_positions_controller = PositionsController(model, view)
        self.all_units_controller = UnitsController(model, view)
        self.all_workers_controller = AllWorkersController(model, view)
        self.add_new_worker_controller = AddNewWorker(model, view)

        self.workers_controllers = {}
        for worker in self.view.worker_tabs.items():
            self.workers_controllers[worker[0]] = WorkerController(model, view, worker[0])

    def start(self):
        self.view.start_app()
