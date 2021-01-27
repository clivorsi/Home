class eda_functions:
    """commonly used eda functions"""
    
    def __init__(self,df,num_features,cat_features,label):
        """Create an eda instance
        
        df            the data in dataframe form
        num_features  the numerical features of the dataset in list form
        cat_features  the categorical features of the dataset in list form
        label         the label in string form
        
        """
        self._df = df
        self._num_features = num_features
        self._cat_features = cat_features
        self._label = label
    
    def get_df(self):
        """return top 10 rows"""
        return self._df.head()
    
    def get_num_features(self):
        """return list of numerical features"""
        return self._num_features
    
    def get_cat_features(self):
        """return list of categorical features"""
        return self._cat_features
    
    def get_label(self):
        """return label"""
        return self._label
    
    def boxplot_loop(self):
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings("ignore")
        for col in self._cat_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            self._df.boxplot(column=self._label, by=col, ax=ax)
            ax.set_title('Label by '+col)
            ax.set_ylabel(self._label)
        plt.show()

    def barplot_loop(self):
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings("ignore")
        for col in self._cat_features:
            counts = self._df[col].value_counts().sort_index()
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            counts.plot.bar(ax = ax, color='steelblue')
            ax.set_title(col + ' counts')
            ax.set_xlabel(col) 
            ax.set_ylabel("Frequency")
        plt.show()

    def scatterplot_loop(self):
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings("ignore")
        for col in self._num_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            feature = self._df[col]
            label = self._df[self._label]
            correlation = feature.corr(label)
            plt.scatter(x=feature, y=label)
            plt.xlabel(col)
            plt.ylabel(self._label)
            ax.set_title(self._label +' vs ' + col + '- correlation: ' + str(correlation))
        plt.show()
