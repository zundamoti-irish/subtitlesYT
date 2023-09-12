from youtube_transcript_api import YouTubeTranscriptApi
import PySimpleGUI as sg
import os
import subprocess


#テーマを決めます。
#テーマの種類は、sg.preview_all_look_and_feel_themes()で確認できます。
sg.theme("DarkBlue")
#表示する画面の設定をします。"初期値"はGUIを起動したときにテキストボックスに表示される値です。
layout=[[sg.Text("VideoID(URLの○○○部分[https://www.youtube.com/watch?v=○○○])を入力してください")],
        [sg.Text("VideoID"),sg.InputText("",key="text")],
        [sg.Button("出力開始",key="ok")]]

window=sg.Window("字幕出力",layout)

#無限ループで画面を表示します。×ボタンかOKボタンで無限ループを抜けます。OKボタンの場合はテキストボックスの値も取得します。
while True:
    event,values=window.read()
    if event==sg.WIN_CLOSED:
        exit()
    elif event=="ok":
        video_id=values["text"]
        break

try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
except:
    sg.popup_error('字幕表示できませんでした。字幕に対応している動画か確認してください。')
    exit()

#追加するコード↓
fileName =  video_id + "_字幕.txt"
file = open(fileName, mode='w', encoding='utf_8')


for transcript in transcript_list:
    for tr in transcript.fetch():
        sec = tr['start']
        hour = int(sec / 3600) 
        minutes = int((sec % 3600) / 60)
        second = int(sec - (hour * 3600) - (minutes * 60))
        time = str(hour) + ':' + str(minutes) + ':' + str(second)
        outputTxt = time + ',' + str(tr['text']) + '\n'
        #print(outputTxt)
        file.write(outputTxt)

file.close()
path = os.getcwd() + '\\' +fileName
subprocess.Popen(["start", path], shell=True)