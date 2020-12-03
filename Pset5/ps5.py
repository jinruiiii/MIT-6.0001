# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link 
        
    def get_pubdate(self):
        return self.pubdate               


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = str(phrase).lower()

    def get_phrase(self):
        return self.phrase    

    def is_phrase_in(self, text):
        # standardize every alphabet to lowercase in both phrase and text
        text = text.lower()
        phrase = self.get_phrase()
        phrase = phrase.lower()
        # Initialize a new string that will replace all special chars with space(" "), cannot use text since string is immutable.
        new_text = ""
        # Special chars to be replaced
        special_char = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        # Loop through all char in text. If char is special char, update it to " " in new_text
        for element in text:
            if element in special_char:
                new_text += " "
            else:   
                new_text += element  
        # Contains a list of words and empty string as elements       
        word_list = new_text.split(" ") 
        # Initialize a list that will only contain words as elements and not empty strings  
        word_list_refined = []
        # Loop thorugh the word_list and only append non empty strings in to word_list_refined
        for element in word_list:
            if element != "":
                word_list_refined.append(element) 
        # text_refined is a string that contains a space between each word                          
        text_refined = " ".join(word_list_refined)
        counter = 0
        # Loop through the entire text to see if phrase is in it
        for i in range(len(text_refined)):
            # If char in text = char in phrase, the counter will increment
            if text_refined[i] == phrase[counter]:
                counter = counter + 1
                # If entire phrase in text, check that last word in phrase in text is not subset of another word
                if counter == len(phrase):
                    if i == len(text_refined) - 1:
                        return True
                    elif text_refined[i+1] == " ":
                        return True
                    else:
                        counter = 0 
            # If char in text not the same as char in phrase, counter reset back to 0            
            else:
                counter = 0            
        return False                
        

# Problem 3
class TitleTrigger(PhraseTrigger):
    
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())    


# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())    


# Problem 5
class TimeTrigger(Trigger):

    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")

    def get_time(self):
        return self.time

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        # Create aware timezones for both story.get_pubdate() and self.get_time() in est
        aware1 = self.get_time().replace(tzinfo=pytz.timezone("EST"))
        aware2 = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if aware2 < aware1:
            return True
        else:
            return False    

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        # Create aware timezones for both story.get_pubdate() and self.get_time() in est
        aware1 = self.get_time().replace(tzinfo=pytz.timezone("EST"))
        aware2 = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if aware2 > aware1:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    
    def __init__(self, trigger):
        self.trigger = trigger

    def get_trigger(self):
        return self.trigger    

    def evaluate(self, story):
        # Get the trigger
        trigger = self.get_trigger()
        # Check whether the trigger is fired
        bool = trigger.evaluate(story)
        # Return the opposite
        if bool == True:
            return False
        else:
            return True    
        

# TODO: NotTrigger

# Problem 8
class AndTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def get_trigger1(self):
        return self.trigger1

    def get_trigger2(self):
        return self.trigger2

    def evaluate(self, story):
        # If both triggers are fired, return True else False
        bool1 = self.get_trigger1().evaluate(story)
        bool2 = self.get_trigger2().evaluate(story) 
        if bool1 == True and bool2 == True:
            return True
        else:
            return False           


# Problem 9
class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def get_trigger1(self):
        return self.trigger1

    def get_trigger2(self):
        return self.trigger2

    def evaluate(self, story):
        bool1 = self.get_trigger1().evaluate(story)
        bool2 = self.get_trigger2().evaluate(story)
        if bool1 == True or bool2 == True:
            return True
        else:
            return False              
# TODO: OrTrigger


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                triggered_stories_list.append(story)
                break
    return triggered_stories_list 



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

