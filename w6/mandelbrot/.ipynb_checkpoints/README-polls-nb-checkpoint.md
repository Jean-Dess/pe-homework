---
jupytext:
  custom_cell_magics: kql
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# US polls with altair

+++

```{admonition} download the zip
:class: warning

to run this code on your own laptop,
{download}`start with downloading the zip file<./ARTEFACTS-polls.zip>`
```

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import geopandas as gpd
```

## 1. loading presidential averages

538.com - actually <http://fivethirtyeight.com> - was a site that published data about the US presidential election  
the site is no longer online, so we use a copy of its **presidential averages** that is stored in `data/DATA.csv`

load this file into a dataframe `df`; make sure to
- be careful about the types of the columns, in particular `date`, that must be a proper timestamp
- notice that the first column is a leftover index, and so ensure it does not end up as a column in `df`

```{code-cell} ipython3
:tags: [level_basic]

df=pd.read_csv('data/DATA.csv')
df.head(3)
```

```{code-cell} ipython3
df.drop('Unnamed: 0', axis=1,inplace=True)
df.info()
```

```{code-cell} ipython3
df['date'] = pd.to_datetime(df.date)
df.info()
```

## 2. plotting

And what we want to do is to plot the average of the polls for each candidate.  
In other words, you should obtain something like this - we will arbitrarily focus on the 2024 year only

```{image} media/polls-over-time-2024.png
:width: 800px
:align: center
```

```{code-cell} ipython3
df = df.set_index('date')
```

```{code-cell} ipython3
:tags: [level_basic]

df.loc['2024'].pivot_table(index= 'date', columns='candidate',values='pct_estimate').plot()
```

## 3. use interactivity

using the interactive view (if under Jupyter Lab) make sure to use `%matplotlib ipympl`, and zoom into the figure and retrieve
- the date for the last data about Joe Biden
- the date for the first data about Kamala Harris

```{code-cell} ipython3
:tags: [level_basic]

# your answer in english - as a comment
# mon ordi veut pas désolé
```

also write a line of code to compute this second date

```{code-cell} ipython3
:tags: [level_basic]

# your code
mask = (df.loc['2024']['candidate'] == 'Biden') & (~ df.loc['2024']['pct_estimate'].isnull())
last_biden_date = df.loc['2024'][mask].index[0]
mask = (df.loc['2024']['candidate'] == 'Harris') & (~ df.loc['2024']['pct_estimate'].isnull())
first_harris_date = df.loc['2024'][mask].index[-1]
```

```{code-cell} ipython3
print(last_biden_date,first_harris_date)
```

## 4. race end

from this part we will focus on the period after `first_harris_date`
1. how many candidates are still in the data ?
1. make sure to keep only the 2 most famous ones
1. how many data points do we have now for each of them ?

```{code-cell} ipython3
df
```

```{code-cell} ipython3
:tags: [level_basic]

# there are only two candidates remaining
df=df[df['candidate']!='Kennedy']
df.loc['2024']
```

## 5: loading shapefiles with geopandas

```{code-cell} ipython3
# here's the typical nickname for geopandas

import geopandas as gpd
```

we want to plot this data on a geographic map; first we need a definition of the various US states; this comes from the US Census Bureau (file `us-states.zip`), and we have a copy of it under `data/`

we load this shapefile into a geopandas object

```{code-cell} ipython3
gdf = gpd.read_file("data/us-states.zip")
```

1. how many entries ?

```{code-cell} ipython3
:tags: [level_basic]

len(gdf)
```

2. what are the various column types

```{code-cell} ipython3
gdf.info()
```

as you can see, this is almost like a regular dataframe, except for the `geometry` column; which is a geographic entity, hence the term `geo-dataframe`

+++

## digression: using altair to produce a geographic viz

```{admonition} this may require an installation
:class: dropdown tip
of course you might have to install `altair`...  how do you go about doing that again ?
```

````{admonition} see also on altair and its use on geographic data
:class: dropdown warning

more details on this topic can be found here: 

- <https://altair-viz.github.io/user_guide/marks/geoshape.html>
- <https://idl.uw.edu/visualization-curriculum/altair_cartographic.html>
- <https://altair-viz.github.io/altair-tutorial/notebooks/09-Geographic-plots.html>
````

```{code-cell} ipython3
import altair as alt

# this is for rendering altair charts within the notebook
alt.renderers.enable("html")
```

Here are a few examples of what we can do with this library

+++

### the simplest chart

```{code-cell} ipython3
# to show a geographic map from that geo-df
# (suboptimal, we'll improve that...)

# we could just write this and it would render
# alt.Chart(gdf).mark_geoshape()

# but we can also this more usual form

chart = (
    alt.Chart(gdf)
    .mark_geoshape()
)

chart.display()
```

### improving that view

+++

now in terms of presentation, it is a little suboptimal, let's improve this a bit

```{code-cell} ipython3
# we can improve by:
# (1) setting a width
# (2) using the albersUsa projection, which puts Alaska and Hawai under mainland
#     this way we use space more effectively
# NOTE that in the process Alaska is artificially shrunk down
#      it's actually the largest US state
(
    alt.Chart(gdf)
    .mark_geoshape()
    .properties(width=600)
    .project('albersUsa')
)
```

### using colors

+++

now, the initial geo-dataframe has some numeric values, that we can use to color the map !  
for example, there are `AWATER` and `ALAND`  
which we can interpret as meaning *area of water* (as in lakes) and *area of land* respectively

```{code-cell} ipython3
gdf.head(2)
```

and we can use one of these to color the different states  
for that we would use `encode()` like so

```{code-cell} ipython3
(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color="ALAND:Q",          # Q stands for quantitative
    )
    .properties(width=600)
    .project('albersUsa')
)
```

### better with a legend

```{code-cell} ipython3
# or if we prefer, same result essentially
# but this way we can be more descriptive

(
    alt.Chart(gdf)
    .mark_geoshape()
    # legend
    .encode(
        color=alt.Color(field="ALAND", type="quantitative", title="land area")
    )
    # a bit narrower so the legend shows up
    .properties(width=600)
    .project('albersUsa')
)
```

### even better with tooltips

```{code-cell} ipython3
# also useful with altair, we can give a `tooltip` parameter to encode
# and this shows when your mouse hovers on a state

# NOTE: altair can only see the columns, not the index
# so as we want to show the name of the state, we need it in a regular column
# so you had made the choice to use the state as the index
# you may need to reset_index()

(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color=alt.Color(field="AWATER", type="quantitative", title="water area"),
        # and we can show there anything from the table
        tooltip=["NAME", "ALAND"],
    )
    .properties(width=600)
    .project('albersUsa')
)
```

## our goal: geographic rendering

in this following we will produce a summary map, which looks like this:
- for all the states where we have data
- the color depicts the ratio between, Harris's and Trump's average scores over time
- also the tooltips allow to expose more details on the individual results

```{image} media/states-with-data.png
:width: 800px
:align: center
```

+++

## 6. first map

+++

1. for how many states do we have polls data ? which are they ?

```{code-cell} ipython3
df = df.loc['2024'].drop(columns='pct_trend_adjusted')
```

```{code-cell} ipython3
df = df['2024-08-01'::]
```

```{code-cell} ipython3
:tags: [level_basic]

print(f'we have polls for {len(pd.unique(df.state))-1} different states') #-1 car df contient encore 'national' dans la colone state
```

2. for this data, compute a table with the state as index, and the two contestants polls (averaged)

```{code-cell} ipython3
df.head(1)
```

```{code-cell} ipython3
:tags: [level_basic]

popularity = (
    df[['candidate','state','pct_estimate']].pivot_table(index='state',columns='candidate',values='pct_estimate')
    .drop('National')
    .rename(index = {'Nebraska Cd 2':'Nebraska'})
)
popularity
```

3. using what you've seen in the digression, and what you will gather if needed on the Internet,  produce the above map

```{code-cell} ipython3
gdf.head(3)
```

```{code-cell} ipython3
popularity.index
```

```{code-cell} ipython3
:tags: [level_basic]

carte = (
    gdf.set_index('NAME')
    .loc[popularity.index]
    .merge(popularity,left_index=True,right_index=True)
)
carte['Harris/Trump'] = popularity['Harris']/popularity['Trump']
carte.reset_index(inplace=True)
carte.head(4)
```

```{code-cell} ipython3
(
    alt.Chart(carte)
    .mark_geoshape()
    .encode(
        color=alt.Color(field="Harris/Trump", type="quantitative", title="Harris/Trump"),
        # and we can show there anything from the table
        tooltip=["state", "Harris",'Trump'],
    )
    .properties(width=600)
    .project('albersUsa')
)
```

## 7. outlining swing states

+++

from the graph above, we want to outline the swing states  
for example, we could come up with something like

```{image} media/swing-states-outlined.png
:width: 800px
:align: center
```

````{admonition} *hints*
:class: dropdown

- the method `pd.Series.isin()` might come in handy for this step
- also you will probably need to search a bit by yourself, outside of what we've covered in the digression
````

```{code-cell} ipython3
SWING_STATES = [
    'Nevada',
    'Arizona',
    'Wisconsin',
    'Michigan',
    'Pennsylvania',
    'Georgia',
    'North Carolina',
]
```

```{code-cell} ipython3
:tags: [level_basic]

carte['is_swingstate']=carte['state'].isin(SWING_STATES)
carte.head(2)
```

```{code-cell} ipython3
(
    alt.Chart(carte[carte['is_swingstate']])
    .mark_geoshape(
        stroke='black',
        strokeWidth=2.5
    )
    .encode(
        color=alt.Color(field="Harris/Trump", type="quantitative", title="Harris/Trump"),
        # and we can show there anything from the table
        tooltip=["state", "Harris",'Trump'],
    )
    .properties(width=600)
    .project('albersUsa')
)+(
    alt.Chart(carte[~carte['is_swingstate']])
    .mark_geoshape()
    .encode(
        color=alt.Color(field="Harris/Trump", type="quantitative", title="Harris/Trump"),
        # and we can show there anything from the table
        tooltip=["state", "Harris",'Trump'],
    )
    .properties(width=600)
    .project('albersUsa')
)
```

## 8. filling gaps (optional)

this is not very readable; instead we want to still get the missing states show up in gray,  
and to keep the outlining of the swing states, i.e.

```{image} media/all-states.png
:width: 800px
:align: center
```

```{admonition} tip
:class: dropdown tip
this one is less obvious, and you are allowed to use an IA to find the solution !
```

```{code-cell} ipython3
:tags: [level_basic]

(
    alt.Chart(carte[carte['is_swingstate']])
    .mark_geoshape(
        stroke='black',
        strokeWidth=2.5
    )
    .encode(
        color=alt.Color(field="Harris/Trump", type="quantitative", title="Harris/Trump"),
        # and we can show there anything from the table
        tooltip=["state", "Harris",'Trump'],
    )
    .properties(width=600)
    .project('albersUsa')
)+(
    alt.Chart(carte[~carte['is_swingstate']])
    .mark_geoshape()
    .encode(
        color=alt.Color(field="Harris/Trump", type="quantitative", title="Harris/Trump"),
        # and we can show there anything from the table
        tooltip=["state", "Harris",'Trump'],
    )
    .properties(width=600)
    .project('albersUsa')
)+(
    alt.Chart(gdf[~gdf['NAME'].isin(pd.unique(df.state))])
    .mark_geoshape(
        color = 'grey'
    )
    .encode(
        tooltip=["NAME"]
    )
    .properties(width=600)
    .project('albersUsa')
)
```
