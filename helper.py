from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import db_ops


class CustomTextInput(TextInput):

    def __init__(self, field=None, **kwargs):
        super().__init__(**kwargs)
        self.field = field


class CustomButton(Button):

    def __init__(self, name=None, addr=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.addr = addr


class Table(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_new_rows(self, sno, cols, n, data=None):
        for i in range(n):
            self.add_widget(Label(
                text=str(sno+i),
                size=(50, 30),
                size_hint=(None, None)))
            for col in cols[1:]:
                width = (1 if col['wid'] is 0 else None)
                if data is None:
                    self.add_widget(CustomTextInput(
                        size=(col['wid'], 30),
                        size_hint=(width, None),
                        field=col['id']
                    ))
                else:
                    self.add_widget(Label(
                        size=(col['wid'], 30),
                        size_hint=(width, None),
                        text=data[i][col['id']]
                    ))

    def save_entry(self, tab, *args):
        rows = int(len(self.children)/self.cols)
        entries = []
        for i in range(rows-1):
            entry = {}
            for j in range(self.cols-1):  # ignore the S. No.
                cell = self.children[i*self.cols+j]
                # print(cell.text)
                entry[cell.field] = cell.text.strip()
                cell.text = ''
            # check if whole row is empty
            if all([v == '' for v in entry.values()]):
                continue
            entries.append(entry)
        ids = db_ops.insert_update_many(tab._id, entries, tab.cust_id)
        print(ids)

    def cancel(self, popup, *args):
        # this function assumes the table is in Popup widget
        popup.dismiss()

        
def add_item_in_tab(tab_widget, columns, tab_type, n_rows=0):
    n_cols = len(columns)
    tab_content = BoxLayout(orientation='vertical')
    table = Table(cols=n_cols)
    for col in columns:
        width = (1 if col['wid'] is 0 else None)
        table.add_widget(Label(
            text=col['text'],
            size=(col['wid'], 50),
            size_hint=(width, None)
        ))
    tab_content.add_widget(table)
    tab_widget.add_widget(tab_content)

def add_buttons(target, buttons):
    # btn id is should be same as the call function name for that button
    # and must be defined in Table class
    table = target.content.children[0]
    for btn in buttons:
        target.content.add_widget(Button(
            text=btn['text'],
            on_release=partial(getattr(table, btn['id']), target)
        ))

def calculate_bal(transacs):
    if transacs is None:
        return 0
    
    debit = 0
    credit = 0
    for t in transacs:

        debit += (int(t['debit']) if t['debit'] is not '' else 0)
        credit += (int(t['credit']) if t['credit'] is not '' else 0)
    return (credit - debit)
