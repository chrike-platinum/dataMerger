__author__ = 'christiaan'
from functools import partial

from bokeh.models.widgets import Div
from bokeh.models.widgets import TextInput
from bokeh.models import Button
from bokeh.layouts import layout
import SolcorDashboard as SD

import dataHandler as DH


def saveSettings(middleLayout):
    settings=[]
    for setting in middleLayout:
        settings.append((setting.title,setting.value))
    print('New settings: '+str(settings))
    DH.setSettings(settings)
    SD.goToHomescreen()

def resetSettings():
    DH.resetSettings()
    showSettingsScreen()


def showSettingsScreen(globNewLayout):
    headingTxt = Div(text="""<p style="font-size:20px;text-align: center"> Settings """,
            width=1000, height=30)
    div = Div(text="""<hr noshade size=4 color=green>""",
        width=1000, height=30)


    settingsDict=DH.getSettings()
    middleLayout=[]
    for settingLabel in settingsDict:
        middleLayout.append(TextInput(value=str(settingsDict[settingLabel]), title=settingLabel))


    saveSettingsButton=Button(label='Save settings')
    saveSettingsButton.on_click(partial(saveSettings,middleLayout))

    buttonBack = Button(label="Back")
    buttonBack.on_click(SD.goToHomescreen)

    resetButton = Button(label="Reset settings")
    resetButton.on_click(resetSettings)


    lay = layout([[headingTxt],[div],middleLayout,[saveSettingsButton],[resetButton],[buttonBack]])

    globNewLayout.children = []
    globNewLayout.children =[lay]


