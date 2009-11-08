from waveapi import events
from waveapi import model
from waveapi import robot

def OnParticipantsChanged(properties, context):
	added = properties['participantsAdded']
	for p in added:
		Notify(context)

def OnBlipSubmitted(properties, context):
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	Search7Digital(contents, blip, context)

def Search7Digital(text, blip, context):
	if text.find("The Who") != -1:
		replacedText = '<a href="http://www.7digital.com/artists/the-who/" target="_blank">The Who on 7digital</a>'
		
		reply = blip.CreateChild()
		
		context.builder.DocumentAppendMarkup(
			blip.waveId, 
			blip.waveletId, 
			reply.GetId(), 
			replacedText
		)

def OnRobotAdded(properties, context):
	root_wavelet = context.GetRootWavelet()  
	root_wavelet.CreateBlip().GetDocument().SetText("I'm alive!")

def Notify(context):
	root_wavelet = context.GetRootWavelet()
	root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

if __name__ == '__main__':
	myRobot = robot.Robot(
		'7digital-finder', 
		image_url='http://7digital-finder.appspot.com/icon.png',
		version='1',
		profile_url='http://7digital-finder.appspot.com/'
	)

	myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
	myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
	myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)

myRobot.Run()