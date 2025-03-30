from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
fish_api = os.getenv("fish_api")

session = Session(fish_api)
PETER_GRIFFIN_MODEL_ID = os.getenv("PETER_GRIFFIN_MODEL_ID")


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



with open("peter_output.mp3", "wb") as f:
    for chunk in session.tts(TTSRequest(
        reference_id=PETER_GRIFFIN_MODEL_ID,
        text=miles_speech
    )):
        f.write(chunk)


"""
TODO:
Look into local hosting, can leverage shared compute provided by stanford to do the audio generation"""