import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def red_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 100%%, %d%%)" % random.randint(60, 100)

def blue_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(248, 100%%, %d%%)" % random.randint(60, 100)

stopwords = list(STOPWORDS)
file = open("../dataset/left_tweet_dataset.tsv")
mask = np.array(Image.open("../images/gun.png"))
dataset = file.readlines()
data = ""

for row in dataset:
	records = row.split("\t")
	if records[0] not in data:
		data += records[0]
	data += records[1]

stopwords += ["https", "co"]

wordcloud = WordCloud(max_font_size=30, max_words=1000, stopwords=set(stopwords), mask=mask, margin=10,
						random_state=1, background_color="black", collocations=False, contour_width=3,
						contour_color='white').generate(data)
plt.figure(figsize=[20,10])
plt.imshow(wordcloud.recolor(color_func=blue_color_func,random_state=3), interpolation='bilinear')
plt.axis("off")
plt.savefig("../images/right.png", format="png")
plt.show()