from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
fish_api = os.getenv("fish_api")

session = Session(fish_api)

# Open the voice files in binary read mode
# with open("miles_morales_one_edited.mp3", "rb") as voice_file, open("miles_morales_two.mp3", "rb") as other_voice_file:
#     # Read the file contents as binary data
#     voice_data = voice_file.read()
#     other_voice_data = other_voice_file.read()
    
#     # Create the model with the voice data
#     model = session.create_model(
#         title="test miles",
#         description="test miles",
#         voices=[voice_data, other_voice_data],
#     )

#     print(model)

"""
id='7d564204c88746e4a6ffb6a8060e7e2a' type='tts' title='test miles' description='test miles' 
cover_image='coverimage/7d564204c88746e4a6ffb6a8060e7e2a' train_mode='fast' state='trained' 
tags=[] samples=[] created_at=datetime.datetime(2025, 3, 6, 9, 52, 14, 460793, tzinfo=TzInfo(UTC)) 
updated_at=datetime.datetime(2025, 3, 6, 9, 52, 14, 460411, tzinfo=TzInfo(UTC)) languages=['en'] 
visibility='private' lock_visibility=False like_count=0 mark_count=0 shared_count=0 task_count=0 
liked=False marked=False author=AuthorEntity(id='f1ab7c2e9e8b4fb984557951eb946b0f', nickname='mantaray714', avatar='')
"""

miles_speech = """\
Aight, listen up! File systems? They’re like a web... organized, connected... holdin’ everything together!

First, you got the boot block - starts it all up. Then, the superblock - it’s the boss... trackin’ files, space... all that.

Files ain’t just sittin’ there. They got inodes - little info packets... tellin’ where data lives, who owns it, how big it is. The real content? That’s in data blocks... straight-up storage space.

And yo... don’t forget the free list - it’s like cleanin’ up your room... makin’ sure new stuff got space to drop in.

Mess up your superblock? You’re done. Keep it clean... keep it tight... Webs don’t tangle themselves - same with file systems!"""


miles_speech = """\
alright lets talk about the unix v6 file system its old school but real important its got a simple structure that keeps everything organized first you got the boot block thats what starts up the system then the superblock this thing holds all the key info about the file system if it gets messed up youre in trouble next up are inodes every file and directory has one it tracks the files metadata and where the data is actually stored then theres the data blocks where the real content lives finally the free list keeps track of empty space so new files can be saved without chaos unix v6 might be classic but its still the foundation for a lot of modern systems"""



miles_speech = """\
alright. so uh. let's talk about the unix v6 file system. it's old but solid. real simple. real clean.  

first. you got the boot block. it kicks things off. like. without it. the system ain't wakin' up. then. there's the superblock. the big boss. it knows where everything is. mess that up. and uh. you're done. 

(break)  

now. files? they don't just sit somewhere. they got inodes. tiny little ID cards. holdin' all the details. name. size. permissions. even where the data is actually stored.  

then you got data blocks. that's where the real stuff lives. all your files. all your content. locked in those blocks.  

and uh. don't sleep on the free list. that's how the system keeps track of empty space. makin' sure new files got room to drop in. no free list. no new files.  

(long-break)  

so yeah. unix v6? old-school. but still the foundation for so much. keep your inodes tight. watch your superblock. and uh. don’t mess up your file system. 

(laugh)"""



with open("output1.mp3", "wb") as f:
    for chunk in session.tts(TTSRequest(
        reference_id="7d564204c88746e4a6ffb6a8060e7e2a",
        text=miles_speech
    )):
        f.write(chunk)


"""
TODO:
Look into local hosting, can leverage shared compute provided by stanford to do the audio generation"""