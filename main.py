from MVC.Views.View import View
from MVC.Models.db_handle import HandleDataBaseModel
from MVC.Controllers.Controller import Controller


def main():
    model = HandleDataBaseModel()
    view = View()
    controller = Controller(model, view)

    controller.start()


if __name__ == '__main__':
    main()
