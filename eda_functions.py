def boxplot_loop(df,features,label):
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")
    for col in features:
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca()
        df.boxplot(column=label, by=col, ax=ax)
        ax.set_title('Label by '+col)
        ax.set_ylabel(label)
    plt.show()
        
def barplot_loop(df,features):
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")
    for col in features:
        counts = df[col].value_counts().sort_index()
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca()
        counts.plot.bar(ax = ax, color='steelblue')
        ax.set_title(col + ' counts')
        ax.set_xlabel(col) 
        ax.set_ylabel("Frequency")
    plt.show()
    
def scatterplot_loop(df,features,label):
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")
    for col in features:
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca()
        feature = df[col]
        label = df['rentals']
        correlation = feature.corr(label)
        plt.scatter(x=feature, y=label)
        plt.xlabel(col)
        plt.ylabel('Bike Rentals')
        ax.set_title('rentals vs ' + col + '- correlation: ' + str(correlation))
    plt.show()
