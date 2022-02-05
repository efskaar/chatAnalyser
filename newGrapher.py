from matplotlib.pyplot import * 
import matplotlib

# backends =  ['GTK3Agg', 'GTK3Cairo', 'MacOSX', 'nbAgg', 'Qt4Agg', 'Qt4Cairo',
#   'Qt5Agg', 'Qt5Cairo', 'TkAgg', 'TkCairo', 'WebAgg', 'WX', 'WXAgg',
#    'WXCairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template']

#makes emojis render proberly
matplotlib.rcParams['font.size'] = 15
matplotlib.rcParams["font.monospace"] = ["DejaVu Sans Mono"]
matplotlib.rcParams["font.family"] = "monospace"


class Grapher():
  def __init__(self,filetype='png'):
      self.dpi = 55
      self.backend = {'png':'Agg','svg':'svg'}
      self.filetype = filetype
      matplotlib.use(self.backend[filetype])
      self.goodColors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#42d4f4', '#f032e6', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#000075', '#a9a9a9', '#ffffff', '#000000']
  
  def makePlot(self,dict,filename,path='',border=False):
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    maxValue = max(dict.values())
    length = len(dict.keys())
    keys = list(dict.keys())
    w = 3 #width

    #make it pretty, kinda
    fig, ax = subplots(figsize=(length,5),frameon=False,facecolor=(0,0,0))
    ax.axis('off')
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(0)
    for item in [fig, ax]:
      item.patch.set_visible(False)
    tick_params(top=False,right=False,left=False,bottom=False)

    for i in range(length):
      key = keys[i]
      value = dict[key]
      xStart = ((1+i)*w)-1
      yStart = 0
      xEnd = ((1+i)*w) 
      yEnd = value/maxValue
      ax.add_artist(Rectangle((xStart,yStart),w-0.5,yEnd,linewidth=3,fill=True,color=self.goodColors[i]))
      text(xEnd+0.3,yEnd+0.05,f'{value}',rotation=0,fontsize=25,ha="center",va="center",fontname='Segoe UI Emoji',fontweight="bold")
      text(xEnd+0.3,-0.1,f'{key}',rotation=0,fontsize=30,ha="center",va="center",fontname='Segoe UI Emoji')
    xlim([0,length*w+w])
    ylim([-0.2,1.2])
    subplots_adjust(left=0,right=1, top=1, bottom=0.0) 
    savefig(f'{path:s}{filename}-dpi{self.dpi:d}.{self.filetype}', dpi=self.dpi)
    close()