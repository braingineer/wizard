from IPython.core.display import HTML

def make_wider(percentage=80):
    return HTML("""
     <style>
    .container {{
      width:{percentage}% !important;
     }}
    </style>
    """.format(percentage=percentage))
