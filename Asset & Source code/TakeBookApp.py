from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

Window.fullscreen = 'auto'

#Load kv file
Builder.load_file('kivy.kv')

#Load Data from txt
def LoadData(file):
    user = {}
    file = open(file+".txt")
    for x in file:
        temp = x.split()
        if len(temp)==3:
            user[temp[0]] = [str(temp[1]), str(temp[2])]
        else :
            user[temp[0]] = [str(temp[1]), str(temp[2]),str(temp[3])]
    print(user)
    return user

def save(file,DATA):
    file=open(file+".txt",'w')
    for x in DATA.keys():
        file.write(str(x)+" "+ str(DATA[x][0])+" "+str(DATA[x][1])+"\n")
    print(DATA)
    file.close()

DATA = LoadData('user')
listBook = LoadData('book')
SM = ScreenManager()
dataUSER = []

class Login(Screen):
    def LoginClicked(self,uname,pword):
        uname=uname.lower()
        pword=pword.lower()
        warning = Popup(title='No Username Or Pasword Found',
                       content=Label(text='Check your spell on Username and Password \n'
                       +' or create account \npress "esc" for close'),
                       size_hint=(None, None), size = (400, 200))
        if uname in DATA.keys() :
            if pword == DATA[uname][0]:
               file=open("session.txt","w")
               file.write(uname)
               file.close()
               SM.current = 'ROB'
            else :
                warning.open()
        else :
            warning.open()

class Regist(Screen):
    def validateReg(self,un,pw,email):
        un=un.lower()
        pw=pw.lower()
        email=email.lower()
        emailList = []
        data = DATA.copy()
        print(DATA)
        for i in DATA:
            emailList.append(DATA[i][1])
        print(emailList)
        warning = Popup(title='Error Input',
                       content=Label(text=''),
                       size_hint=(None, None), size=(400, 200))
        if un == '' or pw == '' or email == '' :
            warning.content = Label(text="please insert all fields")
            warning.open()
        else :
            if un in DATA :
                warning.content = Label(text="username has been taken")
                warning.open()
            elif email in emailList:
                warning.content = Label(text="email has been taken")
                warning.open()
            elif len(pw) < 8 :
                warning.content = Label(text="Password to Sort minimum char(8)")
                warning.open()
            else :
                Welcome = Popup(title='Welcome',
                       content=Label(text='Please Login To your New Account'),
                       size_hint=(None, None), size=(400, 200))
                Welcome.open()
                DATA[un]=[pw,email]
                save('user',DATA)
                SM.current = 'login'
                
class menu(Screen,BoxLayout):
    pass
        

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    pass

class SelectableBook(RecycleDataViewBehavior, GridLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 5

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.label1_text = str(index+1)
        self.imageBook = data['image']['source']
        self.label2_text = data['label2']['text']
        self.label3_text = data['label3']['text']
        self.label4_text = data['label4']['text']
        return super(SelectableBook, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBook, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            if [rv.data[index]['label2']['text'],rv.data[index]['label3']['text']]  not in dataUSER:
                dataUSER.append([rv.data[index]['label2']['text'],rv.data[index]['label4']['text']])
        else:
            print("selection removed for {0}".format(rv.data[index]))
            
                                
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        for i in listBook.keys():
            d = {'image':{'source':i},'label2': {'text':listBook[i][0]},
                 'label3': {'text': listBook[i][1]},
                 'label4': {'text': listBook[i][2]}}
            self.data.append(d)

class view(Screen):
    def TakeBook(self):
        name=''
        Text = ''
        userVal = open("session.txt")
        temp=[]
        total = 0
        for i in userVal:
            name=i
        for i in dataUSER:
            Text+=i[0]+" Price :  Rp. "+i[1]+"\n"
            total+=int(i[1])
        info = Popup(title='THANKS '+name.upper(),
                        content=Label(text='You Bought : \n'+Text+'\nTotal Price :  Rp. '+str(total)
                                       +'\nThe Confirmation Will be Send to your Email :\n'
                                      +DATA[name][-1]),
                        size_hint=(None, None), size = (400, 300))
        info.open()
        print(dataUSER)
        SM.current='ROB'

SM.transition=WipeTransition()
SM.add_widget(Login(name='login'))
SM.add_widget(Regist(name='reg'))
SM.add_widget(menu(name='ROB'))
SM.add_widget(view(name='view'))

class BooksApp(App):
    def build(self):
        SM.current = 'login'
        return SM


if __name__ == '__main__':
    BooksApp().run()
