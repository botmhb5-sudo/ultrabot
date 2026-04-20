import random, json, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

Window.clearcolor = (0, 0, 0.05, 1)

class UltraBotApp(App):

    def build(self):
        self.data_file = "save.json"
        self.invite_codes = ["DOG1", "CAT2", "VIP3"]  # ДАЙ ИХ ДРУЗЬЯМ
        self.load_data()

        root = BoxLayout(orientation='vertical')

        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.history = BoxLayout(orientation='vertical', size_hint_y=None)
        self.history.bind(minimum_height=self.history.setter('height'))
        self.scroll.add_widget(self.history)

        bottom = BoxLayout(size_hint=(1, 0.1))
        self.inp = TextInput(multiline=False, hint_text="Команда...")
        self.inp.bind(on_text_validate=self.run_cmd)

        btn = Button(text="SEND")
        btn.bind(on_press=self.run_cmd)

        bottom.add_widget(self.inp)
        bottom.add_widget(btn)

        root.add_widget(self.scroll)
        root.add_widget(bottom)

        self.msg("Введи /вход КОД", False)
        return root

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.u = json.load(f)
        else:
            self.u = {
                "bal": 500,
                "inv": [],
                "pet": None,
                "pet_stage": 0,
                "auth": False
            }

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump(self.u, f)

    def msg(self, text, user=True):
        color = (0,1,0,1) if user else (1,0,0,1)
        l = Label(text=text, size_hint_y=None, height=40, color=color)
        self.history.add_widget(l)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0))

    def run_cmd(self, *args):
        t = self.inp.text.strip().lower()
        if not t: return
        self.msg("> " + t, True)
        self.inp.text = ""
        Clock.schedule_once(lambda dt: self.logic(t), 0.2)

    def logic(self, c):
        u = self.u

        # 🔒 БЛОКИРОВКА БЕЗ ВХОДА
        if not u.get("auth") and not c.startswith("/вход"):
            self.msg("Сначала введи /вход КОД", False)
            return

        r = ""

        # ВХОД
        if c.startswith("/вход"):
            try:
                code = c.split()[1].upper()
            except:
                r = "Напиши: /вход КОД"
                self.msg(r, False)
                return

            if code in self.invite_codes:
                u["auth"] = True
                self.invite_codes.remove(code)
                r = "Доступ открыт!"
            else:
                r = "Неверный код"

        elif c == "/баланс":
            r = f"Баланс: {u['bal']}"

        elif c == "/бонус":
            b = random.randint(50,150)
            u['bal'] += b
            r = f"+{b}"

        else:
            r = "Команда?"

        self.msg(r, False)
        self.save()

if __name__ == "__main__":
    UltraBotApp().run()
