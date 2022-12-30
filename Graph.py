#https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#creates a graph of ranked data, returns the canvas to display
def createGraph(root, ratingHistory):
    closeGraphs() #close any open graphs

    #disable toolbar
    plt.rcParams['toolbar'] = 'None'

    #format is (date, rating, rank)
    dates = []
    ratings = []
    names = []
    ranks = []

    #get lists for each variable
    for point in ratingHistory:
        dates.append(point[0])
        ratings.append(point[1])
        names.append(str(point[1]))
        ranks.append(point[2])

    #set axes
    x = dates
    y = ratings

    #create figure, plot, and set labels
    fig = plt.Figure(figsize = (5.5, 5.5), dpi = 100)
    plot1 = fig.add_subplot(111)

    plot1.set_title('Rating History')
    plot1.set_xlabel('Date')
    plot1.set_ylabel('Elo')

    line, = plot1.plot(x,y, marker="o")
    
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()

    annot = plot1.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        x,y = line.get_data()
        annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        text = [names[n] for n in ind["ind"]][0]
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == plot1:
            cont, ind = line.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    return fig.canvas

def closeGraphs():
    plt.close("all")