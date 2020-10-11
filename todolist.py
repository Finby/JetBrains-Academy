# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class ToDo:
    def __init__(self):
        self.today_date = datetime.today().date()
        self.class_menu()

    @staticmethod
    def add_new_task(task_=''):
        if task_ == "":
            task_ = input("\nEnter task\n")
        deadline_ = input("Enter deadline\n")
        deadline_ = datetime.strptime(deadline_, '%Y-%m-%d').date()
        new_row = TaskTable(task=task_, deadline=deadline_)
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    @staticmethod
    def __print_task_deadline_format(first_line='', end_line='Nothing to do!', rows=None):
        print("\n" + first_line)
        if rows:
            for i, row in enumerate(rows, 1):
                print("{}. {}. {}".format(i, row.task, row.deadline.strftime('%d %b')))
        else:
            print(end_line)
        print()

    def print_all_tasks(self, first_line="All tasks:", end_line='Nothing to do!', end_of_period='3000-12-30'):
        end_of_period = datetime.strptime(end_of_period, '%Y-%m-%d').date()
        all_tasks = session.query(TaskTable).order_by(TaskTable.deadline).filter(TaskTable.deadline
                                                                                 < end_of_period).all()
        self.__print_task_deadline_format(first_line, end_line=end_line, rows=all_tasks)

    def print_missed_tasks(self):
        self.print_all_tasks(first_line="Missed tasks:",
                             end_line="Nothing is missed!",
                             end_of_period=datetime.today().date().strftime('%Y-%m-%d'))

    def print_week_tasks(self):
        week_dates = [self.today_date + timedelta(days=x) for x in range(7)]
        print()
        for date_iterator in sorted(week_dates):
            date_tasks = session.query(TaskTable).filter(TaskTable.deadline
                                                         == date_iterator).order_by(TaskTable.id).all()
            print("{} {}".format(date_iterator.strftime('%A'), date_iterator.strftime('%d %b')))
            if date_tasks:
                for i, row in enumerate(date_tasks, 1):
                    print("{}. {}".format(i, row.task))
            else:
                print("Nothing to do!")
            print()

    def print_today_tasks(self):
        today_tasks = session.query(TaskTable).filter(TaskTable.deadline == self.today_date).all()
        first_line = ("Today {}".format(self.today_date.strftime('%d %b')))
        self.__print_task_deadline_format(first_line, rows=today_tasks)

    def delete_task_input(self):
        all_tasks = session.query(TaskTable).order_by(TaskTable.deadline).all()
        all_tasks_ordered_enum = enumerate(all_tasks, 1)
        self.__print_task_deadline_format(first_line="Choose the number of the task you want to delete:",
                                          end_line="Nothing to delete",
                                          rows=all_tasks)
        task_number_to_delete = input()
        for el in all_tasks_ordered_enum:
            if el[0] == int(task_number_to_delete):
                task_name_to_delete = el[1].task
        self.delete_row_by_task_name(task_name_to_delete)
        print("The task has been deleted!\n")

    @staticmethod
    def delete_row_by_task_name(task_name):
        session.query(TaskTable).filter(TaskTable.task == task_name).delete()
        session.commit()

    def class_menu(self):
        menu_strings = ["1) Today's tasks",
                        "2) Week's tasks",
                        "3) All tasks",
                        "4) Missed tasks",
                        "5) Add task",
                        "6) Delete task",
                        "0) Exit"]
        menu_actions = {'0': self.todo_exit,
                        '1': self.print_today_tasks,
                       '2': self.print_week_tasks,
                       '3': self.print_all_tasks,
                       '4': self.print_missed_tasks,
                       '5': self.add_new_task,
                       '6': self.delete_task_input
                        }
        while True:
            print(*menu_strings, sep="\n")
            action = input()
            menu_actions[action]()
            if action == '0':
                break

    def todo_exit(self):
        session.close()
        print("\nBye!")


my_todo_list = ToDo()

# my_todo_list.print_all_tasks()
