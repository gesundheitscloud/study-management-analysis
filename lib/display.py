from IPython.display import display, HTML

class Display:
    @staticmethod
    def header(s, header='h1'):
        display(HTML("<%s>%s</%s>" % (header, s, header)))
   
    @staticmethod
    def text(s, color='black'):
        display(HTML("<text style=color:{}>{}</text>".format(color, s)))
    
    @staticmethod
    def frame(df, num_rows=None):
        df = df[:num_rows] if num_rows else df
        display(HTML(df.to_html()))             
        
    @staticmethod
    def warning(s):
        display(HTML("<text style=color:{}>{}</text>".format('red', s))) 

    @staticmethod
    def tag_bars(ax, size=None):
        for p in ax.patches:
            value = f'{round(100 * p.get_height() / size, 2)}%' if size else f'{p.get_height()}'
            ax.annotate(value, (p.get_x() * 1.005, p.get_height() * 1.005))