import requests, os, mimetypes, json, logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.download_from_url import get_size
from requests.exceptions import RequestException
from urllib.parse import unquote

logger = logging.getLogger(__name__)

async def linfo2(bot , m):

  upload_button = InlineKeyboardMarkup(
      [[InlineKeyboardButton("Upload", callback_data="upload_file")]]
  )
    
  if ("youtube.com" in m.text) or ("youtu.be" in m.text):
    await m.reply_text(text=f"Youtube Link", reply_markup=upload_button, quote=True)
    return
  
  if "|" in m.text:
    url , cfname = m.text.split("|", 1)
    url = url.strip()
    cfname = cfname.strip()
    cfname = cfname.replace('%40','@')
    mt = mimetypes.guess_type(str(cfname))[0]
  elif 'drive.google.com' in m.text:
    url = m.text
    r = requests.get(url, allow_redirects=True, stream=True)
    fn = str(r.text)
    if "\'title\':" in fn:
        fn = fn.split('window.viewerData')[-1].split('configJson')[0]
        fn = fn.split("\'title\': \'", 1)[1]
        fn = fn.strip()
        fn = fn.split("\',", 1)[0]
    #logger.info(r.text)
    logger.info(fn)
    await m.reply_text(text=f"📋 Link Info:\n\nFile: `{fn}`\n\nUse /upload.\n\nSee /help.", reply_markup=upload_button, quote=True)
    return
  else:
    url = m.text.strip()
    if os.path.splitext(url)[1]:
      cfname = unquote(os.path.basename(url).split('?')[0])
      mt = mimetypes.guess_type(str(url))[0]
    else:
      try:
        r = requests.get(url, allow_redirects=True, stream=True)
        if "Content-Disposition" in r.headers.keys():
          cfname = r.headers.get("Content-Disposition")
          cfname = cfname.split("filename=")[1]
          if '\"' in cfname:
            cfname = cfname.split("\"")[1]
          mt = mimetypes.guess_type(str(cfname))[0]
        else:
          await m.reply_text(text=f"I Could not Determine The FileType !\nPlease Use Custom Filename With Extension\n\nSee /help.", quote=True)
          return
      except RequestException as e:
        await m.reply_text(text=f"Error:\n\n{e}", quote=True)
        return
        
  r = requests.get(url, allow_redirects=True, stream=True)
  url_size = int(r.headers.get("content-length", 0))
  url_size = get_size(url_size)

  await m.reply_text(text=f"📋 Link Info:\n\nFile: `{cfname}`\nMime-Type: `{mt}`\nSize: `{url_size}`\n\nClick below to upload your link to telegram.\n\nSee /help.", 
                     reply_markup=upload_button,
                     quote=True)
