# NLP - whisky reviews analysis
## Problem definition
This NLP project aims to find strong and weak points of products by Word Clouds analysis for classified reviews.

- What are strong and weak points of the Japanese whisky in general?
- What words describe each of the brands?
- Which words are used for objective and subjective reviews, respectively?
- Which brand has the largest number of non-negative reviews?
- What are the numbers of reviews, with respect to brand and polarity?

## Dataset
[Japanese Whisky Reviews dataset](https://www.kaggle.com/koki25ando/japanese-whisky-review) scrapped by [Koki Ando](https://github.com/koki25ando/Scraping-Japanese-Whisky-Dataset/blob/master/japanese.R).

## Methodology
First step was to perform **sentimental analysis** in order to classify reviews regarding their polarity, and subjectivity as well (with adjustible parameters). 

Then **word clouds** were generated for each class, as well as for each brand. 

For polarity, aim was to get strong and weak points of the product.

For subjectivity, aim was to check which words are used for more and less subjective reviews.

Numbers of positive, neutral and negative opinions were gathered together and stacked in a bar plot.

## Results 
Results presented were obtained with parameters as in config file. Adjustable parameters: additional stopwords, polarity and subjectivity range limiters.

![](https://github.com/hvkat/nlp-whisky-reviews-analysis/blob/main/results/japanese-whisky-wordclouds-all-polarity.JPG?raw=true)

![](https://github.com/hvkat/nlp-whisky-reviews-analysis/blob/main/results/japanese-whisky-wordclouds-all-sujectivity.JPG?raw=true)

![](https://github.com/hvkat/nlp-whisky-reviews-analysis/blob/main/results/japanese-whisky-wordclouds-brands.JPG?raw=true)

![](https://github.com/hvkat/nlp-whisky-reviews-analysis/blob/main/results/japanese-whisky-reviews-score-brands.JPG?raw=true)



