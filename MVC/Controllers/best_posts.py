
class BestPostsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.create_tab('BestPost')
        self.tab.close_button.config(command=self.close_tab)
        self.find_best_posts()

    def find_best_posts(self):
        hour_salary = list()
        hour_salary_dop = list()
        rows = self.model.get_posts()
        for row in rows:
            hour_salary_dop.append(row[0])
            hour_salary_dop.append(round(row[1] / row[2], 2))
            hour_salary.append(hour_salary_dop)
            hour_salary_dop = list()
        hour_salary_sorted = sorted(hour_salary, key=lambda x: x[1], reverse=True)
        for i in range(len(hour_salary_sorted[:5])):
            hour_salary_dop.append(str(i+1))
            for j in range(2):
                hour_salary_dop.append(hour_salary_sorted[i][j])
            hour_salary_sorted[i] = hour_salary_dop
            hour_salary_dop = list()
        for row in hour_salary_sorted[:5]:
            self.tab.best_posts_table.insert('', 'end', values=tuple(row))

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
