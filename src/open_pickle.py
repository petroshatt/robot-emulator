import pickle
import matplotlib.pyplot as plt
fig2 = pickle.load(open('fig1.pkl','rb'))
#ax_master = fig2.axes[0]
#for ax in fig2.axes:
#    if ax is not ax_master:
#        ax_master.get_shared_y_axes().join(ax_master, ax)

plt.show()
