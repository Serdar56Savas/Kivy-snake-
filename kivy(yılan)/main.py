from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


class SnakePart(Widget):
    pass

class GameScreen(Widget):
    adim_sayisi=40
    x_hareket=0
    y_hareket=0
    snake_parts=[]

    def yeni_oyun(self):

        kaldırılacak_nesne=[]
        for child in self.children:
            if isinstance(child,SnakePart):  #belirtilen bir nesneyi ya da değeri belirtilen tür üzerinden doğrulamasını yapar
                kaldırılacak_nesne.append(child)

        for child in kaldırılacak_nesne:
            self.remove_widget(child)

        self.snake_parts=[]
        x_hareket=0
        y_hareket=0
        head=SnakePart()
        head.pos=(0,0)
        self.snake_parts.append(head)
        self.add_widget(head)

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):                  #abs içerisindeki sayının mutlağını veriyo
            #yatayda hareket
            self.y_hareket= 0
            if dx > 0:
                self.x_hareket=self.adim_sayisi
            else:
                self.x_hareket=-self.adim_sayisi

        else:
            #dikey hareket için
            self.x_hareket=0
            if dy > 0:
                self.y_hareket=self.adim_sayisi
            else:
                self.y_hareket=-self.adim_sayisi

    def collides_widget(self, wid1,wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True


    def next_frame(self,*args):
        #Yılanın hareketi
        head=self.snake_parts[0]
        food=self.ids.food

        last_x=self.snake_parts[-1].x
        last_y=self.snake_parts[-1].y

        #Vücudun hareketi
        for i,part in enumerate(self.snake_parts):# nesneyi bir listeye çevirmek için kullandık
            if i==0:
                continue
            part.yeni_y=self.snake_parts[i-1].y
            part.yeni_x=self.snake_parts[i-1].x

        for part in self.snake_parts[1:]: #1 den sonra artık kaç eleman gelecekse
            part.y=part.yeni_y
            part.x=part.yeni_x

        #kafa hareketi
        head.x += self.x_hareket
        head.y += self.y_hareket


        if self.collides_widget(head,food): #yiyeceğe teması var mı?
            food.x=randint(0,Window.width - food.width)
            food.y=randint(0,Window.height - food.height)
            yeni_parca=SnakePart()
            yeni_parca.x=last_x
            yeni_parca.y=last_y
            self.snake_parts.append(yeni_parca)
            self.add_widget(yeni_parca)

        for part in self.snake_parts[1:]: #kendisi ile temas var mı?
            if self.collides_widget(part,head):
                self.yeni_oyun()
        #Yılan duvara temas ediyor mu?
        if not self.collides_widget(self,head):
            self.yeni_oyun()


    pass

class yılan(App):
    def on_start(self):
        self.root.yeni_oyun()
        Clock.schedule_interval(self.root.next_frame, .15)
    pass

yılan().run()