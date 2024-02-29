from bs4 import BeautifulSoup
from urllib.request import urlopen
from nltk.sentiment import SentimentIntensityAnalyzer
import re

class AmazonSentiment():

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def getSentiment(self, url):
        pass

    def openURL(self, url):
        try:
            # Open url
            page = urlopen(url)
            html = page.read().decode("utf-8")
            self.soup = BeautifulSoup(html, "html.parser")
            return True
        except Exception as e:
            # If url not found, print the error message
            print(e)
            return False

    def createReviewsList(self):
        '''Returns a list of all of the reviews in the self.soup object'''

        # Create list of all reviews
        htmlList = self.soup.find_all("div", {"class" : "a-expander-content reviewText review-text-content a-expander-partial-collapse-content"})
        comments = []
        for i in htmlList:
            currentComments = re.findall("<span>.*?</span>", str(i))
            for j in currentComments:
                j = re.sub("<span>", "", j)
                comments.append(re.sub("</span>", "", j))

        return(comments)
    
    def printComments(self, comments):
        # Print comments
        print("Comments:\n")
        for comment in comments:
            print(comment)
            print()

    def getSentiment(self, comments):
        sentimentScores = []
        for comment in comments:
            sentimentScores.append(self.sia.polarity_scores(comment)["compound"])

        return sum(sentimentScores)/len(sentimentScores)
    
    def getNumStars(self):
        div = self.soup.find_all("div", {"id" :"averageCustomerReviews"})
        span = re.findall('<span class="a-size-base a-color-base">.*?</span>', str(div))[0]
        numStars = re.sub("<span.*?>", "", span)
        numStars = re.sub("</span>", "", numStars)
        return float(numStars.strip())
    
    def getTitle(self):
        div = self.soup.find_all("div", {"id" :"titleSection"})
        span = re.findall('<span.*?>.*?</span>', str(div))[0]
        title = re.sub("<span.*?>", "", span)
        title = re.sub("</span>", "", title)
        return title.strip()

    def loop(self):
        while True:
            url = input("Copy the amazon link you would like to analyze. Type 'end' to stop:\n")

            if url == "end":
                break

            if self.openURL(url):

                print("\nTitle of Product: {}".format(self.getTitle()))

                comments = self.createReviewsList()

                sentiment = self.getSentiment(comments)
                print("Average Sentiment of Reviews: {}".format(sentiment))

                print("{} starts out of 5\n".format(self.getNumStars()))

if __name__ == "__main__":
    sent = AmazonSentiment()
    sent.loop()