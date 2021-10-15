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