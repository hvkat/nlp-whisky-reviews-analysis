# Dataset: https://www.kaggle.com/koki25ando/japanese-whisky-review
# This NLP project aims to find strong and weak points of products
# by Word Clouds analysis for classified reviews

import pandas as pd
from textblob import TextBlob
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import yaml

config_path = 'config.yml'
with open(config_path) as c:
    configs = yaml.safe_load(c)

# Read data, explore and preprocess

print('---DATA EXPLORATION---')
df = pd.read_csv(configs['data_path'],delimiter=',')
df = df.iloc[:,1:]
df = df.drop_duplicates()
df = df.reset_index(drop=True)
print(df.head(3))
print(f'\nNumber of unique instances: {len(df)}.\nHeaders: {df.columns.values}')
brands = df["Brand"].unique()
print(f'\nBrands and their frequency: \n{df["Brand"].value_counts()}')
for b in brands:
    print(f'\n>Products of brand {b}:\n{df[df["Brand"]==b]["Bottle_name"].value_counts()}')

# Sentimental analysis

print('\n---PERFORMING SENTIMENTAL ANALYSIS---')
reviews_tb = [TextBlob(review) for review in df['Review_Content']]
titles_tb = [TextBlob(title) for title in df['Title']]
df['Title_pol'] = [title.sentiment.polarity for title in titles_tb]
df['Title_subj'] = [title.sentiment.subjectivity for title in titles_tb]
df['Review_pol'] = [review.sentiment.polarity for review in reviews_tb]
df['Review_subj'] = [review.sentiment.subjectivity for review in reviews_tb]

# Classification positive (1) / neutral (0) / negative (-1)

lim1 = float(configs['polarity_limit_lower'])
lim2 = float(configs['polarity_limit_upper'])
cond_pol = [(df['Review_pol']<lim1),
              (df['Review_pol']>=lim1)&(df['Review_pol']<=lim2),
              (df['Review_pol']>lim2)]
scores_pol = [-1,0,1]
df['Review_score'] = np.select(condlist=cond_pol,choicelist=scores_pol)

print(f'\nDistribution of polarity scores:\n{df["Review_score"].value_counts(normalize=True)}')

# Word clouds for positives and negatives - all brands

stop_words1 = set.union(STOPWORDS,configs['stopwords_polarity'])
text_pol_sets = [('general',df["Review_Content"]), ('positive',df[df["Review_score"]==1]["Review_Content"]), ('neutral',df[df["Review_score"]==0]["Review_Content"]), ('negative',df[df["Review_score"]==-1]["Review_Content"])]

fig, axs = plt.subplots(2,2)
plt.suptitle('Word Clouds - Japanese whisky reviews - Polarity')
for idx,instance in enumerate(text_pol_sets):
    name,text = instance[0],instance[1]
    locals()[name] = WordCloud(stopwords=stop_words1).generate(text=str(text))
    if idx<2:
        ax = axs[0][idx]
    else:
        ax = axs[1][idx-2]
    ax.imshow(locals()[name]), ax.set_title(name), ax.axis('off')

# Classification subjective (1)  / objective (0)

cond_subj = [(df['Review_subj']<configs['subjectivity_limit']),
             (df['Review_subj']>=configs['subjectivity_limit'])]
scores_subj = [0,1]
df['Subjectivity'] = np.select(condlist=cond_subj,choicelist=scores_subj)

print(f'\nDistribution of subjectivity scores: \n{df["Subjectivity"].value_counts(normalize=True)}')

# Word clouds for subjectivity - all rands

stop_words2 = set.union(STOPWORDS,configs['stopwords_subjectivity'])
text_subj_sets = [('objective',df[df['Subjectivity']==0]['Review_Content']),('subjective',df[df['Subjectivity']==1]['Review_Content'])]

fig, axs = plt.subplots(1,2)
plt.suptitle('Word Clouds - Japanese whisky reviews - Subjectivity')
for idx, instance in enumerate(text_subj_sets):
    name,text = instance[0],instance[1]
    locals()[name] = WordCloud(stopwords=stop_words2).generate(str(text))
    axs[idx].imshow(locals()[name]), axs[idx].set_title(name), axs[idx].axis('off')


# General word clouds - with respect to brands

text_pol_brands_sets = []
for b in brands:
    text_pol_brands_sets.append((b,df[df['Brand']==b]['Review_Content']))

fig, axs = plt.subplots(2,2)
plt.suptitle('General Word Clouds with respect to brands')
for idx,instance in enumerate(text_pol_brands_sets):
    name,text = instance[0],instance[1]
    locals()[name] = WordCloud(stopwords=stop_words1).generate(str(text))
    if idx<2:
        ax = axs[0,idx]
    else:
        ax = axs[1,idx-2]
    ax.imshow(locals()[name]), ax.set_title(name), ax.axis('off')



# Percentage of positive reviews - with respect to brands

posits, neutrals, negats = [], [], []
print(f'\nPercentage of non-negative reviews:')
for b in brands:
    print(f'{b} {(df[(df["Review_score"]>=0)&(df["Brand"]==b)].shape[0] / df[df["Brand"]==b].shape[0]):.2f}')
    posits.append(df[(df["Review_score"]==1)&(df["Brand"]==b)].shape[0])
    neutrals.append(df[(df["Review_score"]==0)&(df["Brand"]==b)].shape[0])
    negats.append(df[(df["Review_score"]==-1)&(df["Brand"]==b)].shape[0])


#bar plot (słupkowy) stacked, dla każdej z brands, pos/neutr/neg (ilość, nie percantage)

df_pol = pd.DataFrame({'Positive':posits,'Neutral':neutrals,'Negative':negats},index=brands)
aks = df_pol.plot.bar(stacked=True, title='Reviews number with respect to brand and polarity',xlabel='Brands', ylabel='Number of reviews')

plt.show()


