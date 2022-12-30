#https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot

import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)


#takes a list of tuples (date, rating, rank) as input
#returns a canvas with
def createGraph(data):
    #probably want to start with list of tuples (date, rating, rank)
    #rank might be None

    x = np.sort(np.random.rand(15)) #switch to ordered list of dates
    y = np.sort(np.random.rand(15)) #swtich to ordered list of rating values


    names = np.array(list("ABCDEFGHIJKLMNO")) #switch to ordered list of rating values

    fig,ax = plt.subplots()
    line, = plt.plot(x,y, marker="o")

    annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        x,y = line.get_data()
        annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                            " ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
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

plt.show()