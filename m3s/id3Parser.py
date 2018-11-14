import io
import os
import mimetypes
import mutagen
# from mutagen.easyid3 import EasyID3
# from mutagen.id3 import ID3, TIT2
# from PIL import Image

class mp3:
    def load(self,file):
        self.data = mutagen.File(file)

    def remove_name(self,name):
        if name and name in self.data.keys():
            self.data.tags.delall(name)

    def title(self,value=False,value_append=False):
        name = 'TIT2'
        if value:
            if value_append:
                self.data.tags.add(mutagen.id3.TIT2(encoding=3,text=[value]))
            else:
                self.data.tags.setall(name,[mutagen.id3.TIT2(encoding=3,text=[value])])
        else:
            return self.data.tags.getall(name)
            # title[0]

    def artist(self,value=False,value_append=False):
        name = 'TPE1'
        if value:
            value = isinstance(value, list) and ', '.join(value) or value
            if value_append:
                self.data.tags.add(mutagen.id3.TPE1(encoding=3,text=[value]))
            else:
                self.data.tags.setall(name,[mutagen.id3.TPE1(encoding=3,text=[value])])
        else:
            return self.data.tags.getall(name)

    def album_artist(self,value=False):
        name = 'TPE2'
        if value:
            value = isinstance(value, list) and ', '.join(value) or value
            self.data.tags.setall(name,[mutagen.id3.TPE2(encoding=3,text=[value])])
        else:
            return self.data.tags.getall(name)

    def album(self,value=False):
        name = 'TALB'
        if value:
            self.data.tags.setall(name,[mutagen.id3.TALB(encoding=3,text=[value])])
        else:
            return self.data.tags.getall(name)

    def year(self,value=False):
        name = 'TYER'
        if value:
            self.data.tags.setall(name,[mutagen.id3.TYER(encoding=3,text=[value])])
        else:
            return self.data.tags.getall(name)

    def cover(self,art=False,art_mime='',art_type=3,art_desc=''):
        name = 'APIC'
        if art:
            try:
                if type(art) is not bytes:
                    art_cover = self.cover_from_file(art)
                    extension = os.path.splitext(art)[1]
                    art_mime = mimetypes.types_map[extension]
                else:
                    art_cover = art
                    # self.data.tags.add(mutagen.id3.APIC(encoding=1, mime=u'', type=3, desc=u'sfe', data=art))
                    # self.data.tags.add(mutagen.id3[name](encoding=3, mime=art_mime, type=art_type, desc=art_desc, data=art))
                self.data.tags.setall(name,[mutagen.id3.APIC(mime=art_mime, type=art_type, desc=art_desc, data=art_cover)])
            except Exception as e:
                pass
        else:
            return self.data.tags.getall(name)

    def cover_from_file(self,filename):
        with open(filename, "rb") as file:
            return file.read()

    def cover_to_file(self,filename='mp3-front_cover.v{}.jpg'):
        cover = self.cover()
        if cover:
            index = 0
            for img in cover:
                index += 1
                with open(filename.format(index), "wb") as file:
                    file.write(img.data)
    def save(self):
        self.data.save()

if __name__=="__main__":
    test = mp3()
    test.load("song.v1.mp3")
    audio = test.data

    # audio.tags.setall('APIC',[mutagen.id3.APIC(encoding=3,text=["new title"])])
    # audio.tags.setall('TIT2',[mutagen.id3.TIT2(encoding=3,text=["new title"])])
    # audio.tags.delall('TIT2')
    # print(dir(audio))
    print(audio.keys())
    # if 'TIT2' in audio.keys():
    #     print('yes')

    with open('mp3.v0.jpg', "rb") as file:
        abc = file.read()
        if type(abc) is not bytes:
            print('yes')
        print(type(abc))
    # print(audio.tags)
    # print(mutagen.id3.Frame)
    # print(mutagen.id3.Frame)

