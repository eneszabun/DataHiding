# -*- coding: utf-8 -*-

from typing import IO, Text
from PyQt5 import QtCore,QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Ui_kriptoloji_arayuz import Ui_MainWindow
from PyQt5.QtCore import QBuffer, dec, endl, lowercasebase, pyqtSlot
import cv2
import numpy as np
import os
import shutil

# * gelen değeri binary yapan metod
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        # * girilen metni 9lu bitlere çevirip dönderiyoruz.
        return ''.join([ format(ord(i),"09b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "09b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "09b")
    else:
        raise TypeError("Type not supported.")
# * bütün işlemlerin yapıldığı arayuz class'ımız.
class arayuz(QMainWindow):
    def __init__(self):
        global fname
        
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        channel_list=["R","G","B","RG","RB","GB","RGB"]
        self.ui.comboBox.addItems(channel_list)
        
        # * Butonların bağlantısı ayarlandı.
        self.ui.ceaser_buton.pressed.connect(self.ceaser_cipher)
        self.ui.ceaser_buton_2.pressed.connect(self.ceaser_decipher)
        self.ui.vigenere_buton.pressed.connect(self.vigenerEncrypt)
        self.ui.vignere_buton_2.pressed.connect(self.vigenereDecrypt)
        self.ui.open_pathButon.pressed.connect(self.choosePath)
        self.ui.save_pathButton.pressed.connect(self.savePath)
        self.ui.steno_buton.pressed.connect(self.steganography)
        self.ui.steno_dec_buton.pressed.connect(self.steganographyDecrypt)
        self.ui.clear_buton.pressed.connect(self.clear)
# * ceaser_buton isimli butonun bağlantısını ceaser_cipher olarak atadık ve bunun tanımlanmasını yazacağız.
    def ceaser_cipher(self):
        # * Kullanılacak alfabaler tanımlandı
        lowercase = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş','t', 'u', 'ü', 'v', 'y', 'z', 'q', 'w', 'x']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
        # * text_edit isimli arayüz değişkeninin toPlainText isimli metodu kullanılarak girilen yazıyı alıp lower metodu ile
        # * bütün metni küçük harfe çevirdik.
        realText = self.ui.text_edit.toPlainText().lower()
        # * kaydırma düzeyinin girildiği key_edit isimli arayüz değikeninden text metodu ile yazıyı alıyoruz.
        step= self.ui.key_edit.text()
        # ! try-execpt metodu kullanarak hata alınıp programın hemen kapanmasına engel oluyoruz.
        if len(realText)!=0:
            try:
                # * outText isimli bir liste tanımladık sonuç metnini içine yazdıracağız.
                outText = []
                # * cryptText isimli bir liste tanımladık şifrelenmiş metni içine yazdıracağız.
                cryptText = []
                # * yazının içindeki her bir harfin alınmasını sağlayan for döngüsü
                for eachLetter in realText:
                    # !sıradaki harf lowercase alfabesinin içinde mi diye kontrol ediyor ve yapılması gerekenleri tanımlıyoruz.
                    if eachLetter in lowercase:
                        # * o harfin lowecase alfabesinde hangi indexte olduğunu alıp index değişkeninde tutuyoruz.
                        index = lowercase.index(eachLetter)
                        # * şifreleme işlemini yapıyoruz index değişkenine kaydırma sayısı ekleyip lowercase alfabesinin
                        # * uzunluğunun modunu alıyor ve şifrelenmiş harfimizi buluyoruz.
                        crypting = (index + int(step)) % len(lowercase)
                        cryptText.append(crypting)
                        newLetter = lowercase[crypting]
                        # * yeni harfimizi outText listesine ekliyourz.
                        outText.append(newLetter)
                    # !sıradaki harf numbers alfabesinin içinde mi diye kontrol ediyor ve yapılması gerekenleri tanımlıyoruz.
                    elif eachLetter in numbers:
                        # * o harfin sayılar alfabesinde hangi indexte olduğunu alıp index değişkeninde tutuyoruz.
                        index = numbers.index(eachLetter) 
                        # * şifreleme işlemini yapıyoruz index değişkenine kaydırma sayısı ekleyip 10'a göre modunu alıyoruz
                        # * böylelikle şifrelenmiş sayımızı buluyoruz.
                        crypting = (index + int(step)) %10
                        cryptText.append(crypting)
                        newLetter=numbers[crypting]
                        # * yeni sayımızı outText listesine ekliyourz.
                        outText.append(newLetter)
                    # !sıradaki harf herhangi bir alfabenin içinde değilse yapılması gerekenleri tanımlıyoruz.
                    else:
                        # * yazının içinde bulunan harfler ve sayılar hariç bütün işaretler olduğu gibi kalacak bu yüzden
                        # * gelen eachLetter'i olduğu gibi outText listesine ekliyoruz.
                        outText.append(eachLetter)
                    str1 = ""
                    # * çıktımız bir liste olduğundan dolayı bunu düz yazı olarak çevirmemiz lazım bundan dolayı for döngüsü
                    # * tanımladık ve str1 isimli değişkene verdik bilgiyi
                    for ele in outText: 
                        str1 += ele
                    # * str1 değişkenini text_edit_2'nin setPlainText metodu ile yazdırdık.
                    self.ui.text_edit_2.setPlainText(str1)
            # ! kaydırma miktarı boş bırakıldığında ya da geçersiz değer girilği durumda hata mesajı verilmesi için
            # ! execpt metodunu ValueError olarak ayarladık.
            except ValueError:
                # * QT5 ile gelen QMessageBox class'ın hazır tanımlı warning metodunu çağırıp mesajımı yazdırıyoruz. 
                QMessageBox.warning(self, "Fatal Error","Please, enter a current scroll level!")
        else:
            QMessageBox.warning(self, "Fatal Error","Please, enter a text!")
# * ceaser_buton isimli butonun bağlantısını ceaser_cipher olarak atadık ve bunun tanımlanmasını yazacağız.
    def ceaser_decipher(self):
        self.ui.text_edit_2.clear()
         # * Kullanılacak alfabaler tanımlandı
        lowercase = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş','t', 'u', 'ü', 'v', 'y', 'z', 'q', 'w', 'x']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
        # * text_edit isimli arayüz değişkeninin toPlainText isimli metodu kullanılarak girilen yazıyı alıp lower metodu ile
        # * bütün metni küçük harfe çevirdik.
        realText = self.ui.text_edit.toPlainText().lower()
        # * kaydırma düzeyinin girildiği key_edit isimli arayüz değikeninden text metodu ile yazıyı alıyoruz.
        step= self.ui.key_edit.text()
        # ! try-execpt metodu kullanarak hata alınıp programın hemen kapanmasına engel oluyoruz.
        try:
           # * outText isimli bir liste tanımladık sonuç metnini içine yazdıracağız.
            outText = []
            # * cryptText isimli bir liste tanımladık şifrelenmiş metni içine yazdıracağız.
            cryptText = []
            # * yazının içindeki her bir harfin alınmasını sağlayan for döngüsü
            for eachLetter in realText:
                
                if eachLetter in lowercase:
                    # * o harfin lowecase alfabesinde hangi indexte olduğunu alıp index değişkeninde tutuyoruz.
                    index = lowercase.index(eachLetter)
                    # * deşifreleme işlemini yapıyoruz index değişkeninden kaydırma sayısını çıkarıyoruz lowercase alfabesinin
                    # * uzunluğunun modunu alıyor ve şifrelenmiş harfimizi buluyoruz.
                    crypting = (index - int(step)) % len(lowercase)
                    cryptText.append(crypting)
                    newLetter = lowercase[crypting]
                    outText.append(newLetter)
                elif eachLetter in numbers:
                    # * o harfin sayılar alfabesinde hangi indexte olduğunu alıp index değişkeninde tutuyoruz.
                    index = numbers.index(eachLetter) 
                    # * deşifreleme işlemini yapıyoruz index değişkeninden kaydırma sayısını çıkarıp 10'a göre modunu alıyoruz
                    # * böylelikle şifrelenmiş sayımızı buluyoruz.
                    crypting = (index - int(step)) %10
                    cryptText.append(crypting)
                    newLetter=numbers[crypting]
                    outText.append(newLetter)
                else:
                    outText.append(eachLetter)
                str2 = ""
                # * çıktımız bir liste olduğundan dolayı bunu düz yazı olarak çevirmemiz lazım bundan dolayı for döngüsü
                # * tanımladık ve str1 isimli değişkene verdik bilgiyi 
                for ele in outText: 
                    str2 += ele
            # * str2 değişkenini text_edit_2'nin setPlainText metodu ile yazdırdık.
            self.ui.text_edit_2.appendPlainText(str2)  
        # ! kaydırma miktarı boş bırakıldığında ya da geçersiz değer girilği durumda hata mesajı verilmesi için
        # ! execpt metodunu ValueError olarak ayarladık.     
        except ValueError:
            QMessageBox.warning(self, "Fatal Error","Please, enter a current scroll level!")
        except UnboundLocalError:
            QMessageBox.warning(self, "Fatal Error","Please, enter a text!")
# * vigenere_buton isimli butonun bağlantısını vigenerEncrypt olarak atadık ve bunun tanımlanmasını yazacağız.    
    def vigenerEncrypt(self):
        self.ui.text_edit_2.clear()
        #birleştirilmiş özel bir alfabe oluşturduk.
        alphabet = "abcçdefgğhıijklmnoöpqrsştuüvwxyzABCÇDEFGĞHIİJJKLMNOÖPRSŞTUÜVWXYZ0123456789'""!'^+%&/()=*?:,;_-#$+[{ é]}. "
        #orjinal metni ve anahtarı toPlainText metodu ile arayüz değişkenlerinden çektik.
        message = self.ui.text_edit.toPlainText()
        key=self.ui.key_edit.text()
        #harf ve indeksini zip fonksiyonu ile birleştirip dict fonksiyonu ile bir sözlük haline  getirdik range ile alfabe uzunluğuna kadar indeksleri aldık.
        letter_to_index = dict(zip(alphabet, range(len(alphabet)))) #[harf,index]
        index_to_letter = dict(zip(range(len(alphabet)), alphabet)) #[index,harf]
        #şifreli metni tutacak boş bir değişken oluşturduk
        encrypted = ""
        if len(message)!=0:
            try:
                split_message = [
                    message[i : i + len(key)] for i in range(0, len(message), len(key))
                    ]
                #her bir split_message a ulaşan döngü
                for each_split in split_message:
                    i = 0
                    #her bir karaktere  ulaşan döngü
                    for letter in each_split:
                        #mesajdaki karakterin alfabedeki indexi ile key deki denk gelen karakterin alfabedeki indeksini toplayıp alfabe uzunluğunu bölerek şifreli harfin indexini bulduk.
                        number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
                        #oluşturduğumuz boş encrypted değişkenine şifreli karakterin indexine denk gelen alfabe indexindeki karakteri ekledik
                        encrypted += index_to_letter[number]
                        i += 1
                self.ui.text_edit_2.appendPlainText(encrypted)
            except ValueError:
                QMessageBox.warning(self, "Fatal Error","Please,enter a key!")
        else:
            QMessageBox.warning(self, "Fatal Error","Please, enter a text!")
# * vignere_buton_2 isimli butonun bağlantısını vigenerDecrypt olarak atadık ve bunun tanımlanmasını yazacağız.        
    def vigenereDecrypt(self):
        self.ui.text_edit_2.clear()
        #birleştirilmiş özel bir alfabe oluşturduk.
        alphabet = "abcçdefgğhıijklmnoöpqrsştuüvwxyzABCÇDEFGĞHIİJJKLMNOÖPRSŞTUÜVWXYZ0123456789'""!'^+%&/()=*?:,;_-#$+[{ é]}. "
        #şifreli metni ve anahtarı toPlainText metodu ile arayüz değişkenlerinden çektik.
        cipher = self.ui.text_edit.toPlainText()
        key=self.ui.key_edit.text()
        #harf ve indeksini zip fonksiyonu ile birleştirip dict fonksiyonu ile bir sözlük haline  getirir range ile alfabe uzunluğuna kadar indeksleri alır
        letter_to_index = dict(zip(alphabet, range(len(alphabet))))#[harf,index]
        index_to_letter = dict(zip(range(len(alphabet)), alphabet)) #[index,harf]
        #deşifreli metni tutacak boş bir değişken oluşturduk
        decrypted = ""
        if len(cipher)!=0:
            try:
                split_encrypted = [
                    cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
                    ]
                #her bir split_message a ulaşan döngü
                for each_split in split_encrypted:
                    i = 0
                    #her bir karaktere  ulaşan döngü
                    for letter in each_split:
                        #mesajdaki karakterin alfabedeki indexi ile key deki denk gelen karakterin alfabedeki indeksini toplayıp alfabe uzunluğunu bölerek şifreli harfin indexini bulduk.
                        number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
                        #oluşturduğumuz boş decrypted değişkenine şifreli karakterin indexine denk gelen alfabe indexindeki karakteri ekledik
                        decrypted += index_to_letter[number]
                        i += 1
                self.ui.text_edit_2.appendPlainText(decrypted)
            except ValueError:
                QMessageBox.warning(self, "Fatal Error","Please, enter a key!")
        else:
            QMessageBox.warning(self, "Fatal Error","Please, enter a text!")
# * pathButon isimli butonun bağlantısını choosePath olarak atadık ve bunun tanımlanmasını yazacağız.
    def choosePath(self):
        global fname
        self.ui.steno_label.clear()
        self.ui.steno_label_2.clear()
        # * QFileDialog classının getOpenFileName metodu ile dosya seçtirme işlemini yapıp bu dosyanın
        # *  path'ini fname olarak atadık
        fname=QFileDialog.getOpenFileName(self, 'Open File','','Image Files(*.png)')
        fname=fname[0]
        # * fname isimli path'te bulunan dosyayı label'in içine yazdık.
        self.ui.steno_label.setPixmap(QtGui.QPixmap(fname))
# * save_pathButton isimli butonun bağlantısını savePath olarak atadık ve bunun tanımlanmasını yazacağız.
    def savePath(self):
        global save_fname
        global dir_path
        # * QFileDialog classının getExistingDirectory metodu ile klasör seçtirme işlemini yapıp bu dosyanın
        # *  path'ini save_fname olarak atadık
        save_fname=QFileDialog.getExistingDirectory(self, 'Open File','')
        img_pth=os.path.join(dir_path,"encrypted_image.png")
        # * resmin konumunu ve kaydetmek istediğimiz konumu kullanarak resmi istenilen konuma taşıyoruz.
        shutil.move(img_pth,save_fname)
# * stene_buton isimli butonun bağlantısını steganography olarak atadık ve bunun tanımlanmasını yazacağız.
    def steganography(self):
        channel_content=self.ui.comboBox.currentText()
        global fname
        global dir_path
        # * data isimli değişkene değiştirilmiş metni veriyoruz.
        data = self.ui.text_edit_2.toPlainText()
        # * fotoğrafı okuyoruz
        stream = open(fname, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img= cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        # * saklanabilecek maksimum bit değerini hesaplıyoruz.
        n_bytes = img.shape[0] * img.shape[1] * 3 // 9
        if data != "":
            if len(data) > n_bytes:
                raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
            # * durma noktasını belirliyoruz.
            data += "====="
            data_index = 0
            # * mesajı binary'i formatına çeviriyoruz.
            binary_secret_data  = to_bin(data)
            data_len = len(binary_secret_data)
            if channel_content=="RGB":
                # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            # * en az önemli kırmızı piksel biti
                            pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        if data_index < data_len:
                            # * en az önemli yeşil piksel biti
                            pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        if data_index < data_len:
                            # * en az önemli mavi piksel biti
                            pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path) 
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="R":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b,a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite(os.path.join("encrypted_image.png"),img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="G":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="B":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="RG":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        if data_index < data_len:
                            pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="RB":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a = to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        if data_index < data_len:
                            pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
            elif channel_content=="GB":
                 # * fotoğrafın ilk sırasında geziniyoruz.
                for row in img:
                    # * fotoğrafın o an bulunduğumuz sırasında bulunan piksellerde geziniyoruz.
                    for pixel in row:
                        # * rgba değerlerini binary formatında yazıyoruz.
                        r, g, b, a= to_bin(pixel)
                        # * en az anlamlı biti yalnızca depolanacak veri varsa değiştirin
                        if data_index < data_len:
                            pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        if data_index < data_len:
                            pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                            data_index += 1
                        # * eğer veri gizlenmişse looptan çık
                        if data_index >= data_len:
                            break
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.chdir(dir_path)    
                # * fotoğrafı kaydet.
                cv2.imwrite("encrypted_image.png",img)
                # * kaydedilen fotoğrafı göster.
                self.ui.steno_label_2.setPixmap(QtGui.QPixmap("encrypted_image.png"))
                reply=QMessageBox.question(self, "Save in","Your image with hidden text at: {} "
                    "\nDo you want to open your image with hidden text?".format(os.path.join(dir_path)),
                    QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.Yes:
                    path=os.path.join(dir_path,"encrypted_image.png")
                    path=os.path.realpath(path)
                    os.startfile(path)
                else:
                    pass
        else:
                QMessageBox.warning(self, "Fatal Error","Please, enter a text.")
# * steno_dec_buton isimli butonun bağlantısını steganographyDecrypt olarak atadık ve bunun tanımlanmasını yazacağız.
    def steganographyDecrypt(self):
        self.ui.text_edit_2.clear()
        channel_content=self.ui.comboBox.currentText()
        global fname
        try:
            # * fotoğrafı okuyoruz
            stream = open(fname, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            img= cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            binary_data = ""
            if channel_content=="RGB":
                for row in img:
                    for pixel in row:
                        r, g, b, a= to_bin(pixel)    
                        binary_data += r[-1]
                        binary_data += g[-1]
                        binary_data += b[-1]
            elif channel_content=="R":
                for row in img:
                    for pixel in row:
                        r, g, b, a= to_bin(pixel)
                        binary_data += r[-1]
            elif channel_content=="G":
                for row in img:
                    for pixel in row:
                        r, g, b, a = to_bin(pixel)
                        binary_data += g[-1]
            elif channel_content=="B":
                for row in img:
                    for pixel in row:
                        r, g, b, a= to_bin(pixel)
                        binary_data += b[-1]
            elif channel_content=="RG":
                for row in img:
                    for pixel in row:
                        r, g, b, a = to_bin(pixel)
                        binary_data += r[-1]
                        binary_data += g[-1]
            elif channel_content=="RB":
                for row in img:
                    for pixel in row:
                        r, g, b, a= to_bin(pixel)
                        binary_data += r[-1]
                        binary_data += b[-1]                         
            elif channel_content=="GB":
                for row in img:
                    for pixel in row:
                        r, g, b, a= to_bin(pixel)
                        binary_data += g[-1] 
                        binary_data += b[-1] 
            # * 9li bitlere bölüyoruz.
            all_bytes = [ binary_data[i: i+9] for i in range(0, len(binary_data), 9) ]
            # *bitlerden karakterlere dönüştürüyoruz.
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                # * durması gereken nokta olarak ===== girdiğimizden dolayı, görene kadar devam ediyoruz. gelince
                # * döngü kırılıyor.
                if decoded_data[-5:] == "=====":
                    break
            ascii_text=decoded_data[:-5]
            self.ui.text_edit_2.appendPlainText(ascii_text)
        except ValueError:
            QMessageBox.warning(self, "Fatal Erreor","Please, choice a image with hidden text")
# * clear_buton isimli butonun bağlantısını clear olarak atadık ve bunun tanımlanmasını yazacağız.
    def clear(self):
        # * key_edit isimli QPLineEdit class'ının clear metodunu kullanarak içeriğini temizliyoruz.
        self.ui.key_edit.clear()
        # * text_edit isimli QPlainTextEdit class'ının clear metodunu kullanarak içeriğini temizliyoruz.
        self.ui.text_edit.clear()
        # * key_edit isimli QPlainTextEdit class'ının clear metodunu kullanarak içeriğini temizliyoruz.
        self.ui.text_edit_2.clear()
        # * steno_label isimli QLabel class'ının clear metodunu kullanarak içeriğini temizliyoruz.
        self.ui.steno_label.clear()
        # * steno_label_2 isimli QLabel class'ının clear metodunu kullanarak içeriğini temizliyoruz.
        self.ui.steno_label_2.clear()