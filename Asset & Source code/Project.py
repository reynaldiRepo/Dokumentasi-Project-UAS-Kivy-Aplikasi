from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
Window.fullscreen = 'auto'

class Screen1(BoxLayout):
    def build(self):
        self.user={}
        self.LoadData()
        self.orientation = "vertical"
        self.spacing = 2
        self.padding = [80,80]
        self.layoutIng()
    
    def layoutIng(self):
        self.title = Label(text="TAKE YOUR BOOK APP", font_size="18",padding=[0,0],valign='bottom')
        self.logo = Image(source="logo.png",size_hint_y=None,height=150)
        self.UsernameIPT  = TextInput(font_size="24sp",padding=10,multiline=False)
        self.PasswordIPT = TextInput(password=True, font_size="24sp", padding=10, multiline=False)
        self.LoginBtn = Button(text="Login",font_size="24sp")
        self.LoginBtn.bind(on_press=self.LoginClicked)
        self.Register = Button(text="Register",font_size="24sp")
        self.add_widget(self.title)
        self.add_widget(self.logo)
        self.add_widget(Label(text="Username : ", font_size="24", halign='left'))
        self.add_widget(self.UsernameIPT)
        self.add_widget(Label(text="Password : ",
                              font_size="24", halign="left"))
        self.add_widget(self.PasswordIPT)
        self.add_widget(Label(text=""))
        self.add_widget(self.LoginBtn)
        self.add_widget(self.Register)

    def LoadData(self):
        file = open("user.txt")
        for x in file:
            temp = x.split()
            self.user[temp[0]] = [str(temp[1]), str(temp[2])]
        print(self.user)


    def LoginClicked(self,btn):
        warning = Popup(title='No Username Or Pasword Found',
                       content=Label(text='Check your spell on Username and Password \nor create account \npress "esc" for close'),
                       size_hint=(None, None), size=(400, 200))
        usernameCheck = self.UsernameIPT.text
        print(usernameCheck)
        passwordCheck = self.PasswordIPT.text
        if usernameCheck in self.user.keys() :
            if passwordCheck == self.user[usernameCheck][0]:
               print('True')
            else :
                print('No Name')
                warning.open()
        else :
            print('No name')
            warning.open()


        


class BooksApp(App):
    def build(self):
        root = Screen1()
        root.build()
        return root

if __name__ == '__main__':
    BooksApp().run()


BooksApp().run()

