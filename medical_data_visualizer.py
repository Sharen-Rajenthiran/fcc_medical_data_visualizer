import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#Author: SHAREN RAJENTHIRAN
#REFERENCE: https://github.com/fuzzyray/medical-data-visualizer.git (used as a reference to learn and code this project)

# Read data
df = pd.read_csv('medical_examination.csv')

#Add overweight column
df['overweight'] = (df['weight']/(df['height']/100)**2 > 25).astype(int)

# Normalize the data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, make the value 0. 
# If the value is more than 1, make the value 1
df['cholesterol'] = (df['cholesterol']>1).astype(int)
df['gluc'] = (df['gluc']>1).astype(int)

def draw_catplot():
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
      # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename
      # one of the collumns for the catplot to work correctly
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_cat = df_cat.rename(columns={0: 'total'})
    # Draw the catplot with 'sns.catplot()'
    graph = sns.catplot(data=df_cat, kind='bar', x="variable", y="total", hue="value", col="cardio")  
    fig = graph.fig
    fig.savefig('catplot.png')
    return fig

# Clean the data
def draw_heatmap():
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))
                 ]
    corr = df_heat.corr() # Calculate the correlation matrix
    mask = np.triu(np.ones_like(corr, dtype=bool))  # Generate a mask for the upper triangle
    fig, ax = plt.subplots(figsize=(16,9))  # Set up the matplotlib figure
    sns.heatmap(corr, mask=mask, square=True, linewidths=0.5, annot=True, fmt='0.1f') # Draw the heatmap with 'sns.heatmap()'
    fig.savefig('heatmap.png')
    return fig


