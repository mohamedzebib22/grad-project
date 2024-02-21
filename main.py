from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.button import MDIconButton
from kivy.uix.screenmanager import ScreenManager , Screen 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.window import Window
import requests
import firebase_admin
from firebase_admin import credentials, auth ,db,firestore
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
import pyrebase
from kivy.uix.widget import Widget
from plyer import filechooser,notification
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
import uuid
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from plyer import call
import subprocess
import webbrowser
import platform as plat
Window.size=(330,590)

config = {
    "apiKey": "AIzaSyDyuEohOlFGGJDDsSAlh9rvjZSZ8shXEig",
    "authDomain": "medicalapp-73d41.firebaseapp.com",
    "databaseURL": "https://medicalapp-73d41-default-rtdb.firebaseio.com/",
    "projectId": "medicalapp-73d41",
    "storageBucket": "medicalapp-73d41.appspot.com",
    "messagingSenderId": "565079436237",
    "appId": "1:565079436237:web:5ac629e5d123113ed3f284",
    "measurementId": "G-1F5LN1DJHW",
    "serviceAccount":"medicalapp-73d41-firebase-adminsdk-8gfnf-c37d4105cb.json"
}

cred = credentials.Certificate("medicalapp-73d41-firebase-adminsdk-8gfnf-fd33dcdc83.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://medicalapp-73d41-default-rtdb.firebaseio.com/"})
ref = db.reference('/Analysis')
firestoree = firestore.client()
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth=firebase.auth()



class Lab(Screen,Widget):
   
    
    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)
    def selected(self,selection):
        self.parent.get_screen('laboratory').ids.img.source=selection[0] 
        
        
    def storage_data(self):
        try:
            # التحقق من أن البيانات غير فارغة
            if not self.parent.get_screen('laboratory').ids.analysis_name.text or not float(self.parent.get_screen('laboratory').ids.lab_price.text) or not self.parent.get_screen('laboratory').ids.img.source:
                self.show_error_dialog("PLease Enter Data")
            analysis_id = str(uuid.uuid4())
            data={
                "lab_name":self.parent.get_screen('laboratory').ids.lab_name.text ,
                "lab_address":self.parent.get_screen('laboratory').ids.lab_address.text ,
                "phone_lab":self.parent.get_screen('laboratory').ids.phone_lab.text ,
                "analysis_name":self.parent.get_screen('laboratory').ids.analysis_name.text ,
                "price":float(self.parent.get_screen('laboratory').ids.lab_price.text),
                "photo":self.parent.get_screen('laboratory').ids.img.source,   
            }
             # حفظ البيانات باستخدام المعرف العشوائي
            
            firestoree.collection("LAB").document(analysis_id).set(data)
            print('Product added successfully.')
            self.parent.get_screen('laboratory').ids.lab_name.text=""
            self.parent.get_screen('laboratory').ids.lab_address.text=""
            self.parent.get_screen('laboratory').ids.phone_lab.text=""
            self.parent.get_screen('laboratory').ids.analysis_name.text=""
            self.parent.get_screen('laboratory').ids.lab_price.text=""
            self.parent.get_screen('laboratory').ids.img.source=""
            self.parent.current="show_lab"
        except Exception as Error:
            self.show_error_dialog("Please check data")
            print(Error)
    
            
    def show_error_dialog(self, error_message):
        dialog = MDDialog(
            title="ُERROR",
            text=error_message,
            size_hint=(0.7, 0.3)
        )
        dialog.open()   
    
    
    
    

    
class StartScreen(Screen):
    pass

class Login_user(Screen):
    pass
        

class Signup_user(Screen):
    pass

class Choose_entery(Screen):
    pass

class Login_admin(Screen):
    pass

class Signup_admin(Screen):
    pass
     

class Choose_signup(Screen):
    pass

class Show_lab(Screen):


    def show_data(self):
        docs = firestoree.collection("LAB").get()
        products_grid = self.ids.products_grid 
        
        for doc in docs:
            data = doc.to_dict()
            lab_name=data.get("lab_name","")
            lab_address=data.get("lab_address","")
            phone_lab=data.get("phone_lab","")
            analysis_name = data.get("analysis_name", "")
            lab_price = str(data.get("price", ""))
            photo = data.get("photo", "")
            
            
            
            card_layout = GridLayout( padding=10, spacing=10,cols=2)
        
            # Agregar los elementos al BoxLayout
            card_layout.add_widget(MDLabel(text=f"Lab Name: {lab_name}"))
            card_layout.add_widget(MDLabel(text=f"Lab Address: {lab_address}"))
            card_layout.add_widget(MDLabel(text=f"Phone: {phone_lab}"))
            card_layout.add_widget(MDLabel(text=f"Analysis Name: {analysis_name}"))
            card_layout.add_widget(MDLabel(text=f"Price: {lab_price}"))
            card_layout.add_widget(Image(source=photo))
            
            whatsapp_button = MDIconButton(icon="whatsapp",font_size=20,md_bg_color="teal")
            whatsapp_button.bind(on_release=lambda button, phone_number=phone_lab: self.contact_whatsapp(phone_number))
            card_layout.add_widget(whatsapp_button)
            
            phone_button= MDIconButton(icon="phone",font_size=20,md_bg_color="teal")
            phone_button.bind(on_release=lambda button, phone_number=phone_lab: self.call_number(phone_number))
            card_layout.add_widget(phone_button)
            # Crear el MDCard
            card = MDCard(size_hint_y=None, height=dp(200), padding=dp(10), md_bg_color="pink",radius= [40,])
            
            # Agregar el BoxLayout al MDCard
            card.add_widget(card_layout)
            
            # Agregar el MDCard al GridLayout
            products_grid.add_widget(card)
            self.ids.products_grid.remove_widget(self.ids.show_data_button)
    def contact_whatsapp(self, phone_number):
        # تحقق من نوع النظام الأساسي
        system_platform = plat.system()
        
        # تنسيق رقم الهاتف
       
        formatted_phone_number = "+20" + phone_number
        
        # إعداد رابط واتساب بناءً على نوع النظام الأساسي
        if system_platform == "Windows":
            whatsapp_link = "https://wa.me/" + formatted_phone_number
        elif system_platform == "Darwin":  # macOS
            whatsapp_link = "https://api.whatsapp.com/send?phone=" + formatted_phone_number
        elif system_platform == "Linux":
            whatsapp_link = "https://wa.me/" + formatted_phone_number
        elif system_platform == "android":
            whatsapp_link = "https://wa.me/" + formatted_phone_number
        elif system_platform == "macosx":
            whatsapp_link = "https://api.whatsapp.com/send?phone=" + formatted_phone_number
        else:
            # Handle other platforms here
            return
        
        notification.notify(
            title='WhatsApp Link',
            message=whatsapp_link,
            app_name='Kivy App',
            app_icon=None,
        )
        # فتح رابط واتساب في المتصفح الافتراضي
        webbrowser.open(whatsapp_link)
        print(whatsapp_link)
        
    def call_number(self, phone_number):
        platform=plat.system()
        formatted_phone_number = "+20" + phone_number
        
        if platform == 'android' or platform == 'ios':
            webbrowser.open('tel://' + formatted_phone_number)
        elif platform == 'Windows':
            webbrowser.open('tel://' + formatted_phone_number)
        elif platform == 'Darwin':
            subprocess.call(['open', 'tel:' + formatted_phone_number])
        elif platform == 'Linux':
            phone = 'tel://' + formatted_phone_number
            webbrowser.open(phone)
        else:
            print("The device is not available")

    def search_product(self):
        search_text = self.ids.search_field.text.strip()  # الحصول على النص المدخل في حقل البحث وحذف الفراغات الزائدة

        # تحديث عرض الصفحة فقط إذا كان هناك نص مدخل في حقل البحث
        if search_text:
            docs = firestoree.collection("LAB").where("lab_address", "==", search_text).get()
            products_grid = self.ids.products_grid
            products_grid.clear_widgets()  # تفريغ العناصر القديمة

            for doc in docs:
                data = doc.to_dict()
                lab_name=data.get("lab_name","")
                lab_address=data.get("lab_address","")
                phone_lab=data.get("phone_lab","")
                analysis_name = data.get("analysis_name", "")
                lab_price = str(data.get("price", ""))
                photo = data.get("photo", "")
                
            
            
                card_layout = GridLayout( padding=10, spacing=10,cols=2)
            
                # Agregar los elementos al BoxLayout
                card_layout.add_widget(MDLabel(text=f"Lab Name: {lab_name}"))
                card_layout.add_widget(MDLabel(text=f"Lab Address: {lab_address}"))
                card_layout.add_widget(MDLabel(text=f"Phone: {phone_lab}"))
                card_layout.add_widget(MDLabel(text=f"Analysis Name: {analysis_name}"))
                card_layout.add_widget(MDLabel(text=f"Price: {lab_price}"))
                card_layout.add_widget(Image(source=photo))
                
                whatsapp_button = MDIconButton(icon="whatsapp",font_size=20,md_bg_color="teal")
                whatsapp_button.bind(on_release=lambda button, phone_number=phone_lab: self.contact_whatsapp(phone_number))
                card_layout.add_widget(whatsapp_button)
                
                phone_button= MDIconButton(icon="phone",font_size=20,md_bg_color="teal")
                phone_button.bind(on_release=lambda button, phone_number=phone_lab: self.call_number(phone_number))
                card_layout.add_widget(phone_button)
                # Crear el MDCard
                card = MDCard(size_hint_y=None, height=dp(200), padding=dp(10), md_bg_color="pink",radius= [40,])
                
                # Agregar el BoxLayout al MDCard
                card.add_widget(card_layout)
                
                # Agregar el MDCard al GridLayout
                products_grid.add_widget(card)
                self.ids.search_field.text=""
    
class RootScreen(ScreenManager):
    pass


Builder.load_file("main.kv")
class Slope(MDApp): 
    
    def build(self):
        self.title="Lab" 
        self.icon="logo.ico"
        return RootScreen()
    
    def login(self, email, password):
        try:
            # تسجيل الدخول باستخدام Firebase Authentication
            auth.sign_in_with_email_and_password(email, password)
            
            # يمكنك إضافة مزيد من الكود هنا، مثل تحويل المستخدم إلى الشاشة المطلوبة
            self.root.current="choose"
        except requests.exceptions.HTTPError as e:
            # إذا كان هناك خطأ أثناء تسجيل الدخول، يمكنك عرض رسالة الخطأ
           
            self.show_error_dialog("password or email is error")
    def show_error_dialog(self, error_message):
        dialog = MDDialog(
            title="ُERROR",
            text=error_message,
            size_hint=(0.7, 0.3)
        )
        dialog.open() 
    def signup_user(self,email,password,user_name,date,phone):
        try:
            from firebase import firebase
            # إنشاء حساب جديد في Firebase Authentication
            firebase=firebase.FirebaseApplication('https://medicalapp-73d41-default-rtdb.firebaseio.com/',None)
            user=auth.create_user_with_email_and_password(email,password)
            data1={
                'email':email,
                'password':password,
                'date':date,
                'phone':phone,
                'user_name':user_name,
            }
            
            firebase.post('https://medicalapp-73d41-default-rtdb.firebaseio.com/Users',data1)
            result=firebase.get('medicalapp-73d41-default-rtdb/Users','')
        except Exception as Er:
            self.show_error_dialog("The Email is invalid")
            print(Er)   
            
    def show_error_dialog(self, error_message):
        dialog = MDDialog(
            title="An Error",
            text=error_message,
            size_hint=(0.7, 0.3)
        )
        dialog.open()
        
    def signup_admin(self,name,email,password,address,phone):
        from firebase import firebase
        try:
            firebase=firebase.FirebaseApplication('https://medicalapp-73d41-default-rtdb.firebaseio.com/',None)
            user=auth.create_user_with_email_and_password(email,password)
            self.root.current="laboratory"
            data={
                'email':email,
                'password':password,
                'address':address,
                'phone':phone,
                'name':name,
            }
            
            firebase.post('https://medicalapp-73d41-default-rtdb.firebaseio.com/Admin',data)
            result=firebase.get('medicalapp-73d41-default-rtdb/Users','')
            
        except Exception as Er:
            self.show_error_dialog("The Email is invalid")
            print(Er) 
            
    
     
if __name__ == "__main__":
    LabelBase.register(name="MPoppins" , fn_regular="Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins" , fn_regular="Poppins-SemiBold.ttf")

    Slope().run()