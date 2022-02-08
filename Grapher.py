from matplotlib.pyplot import * 
import matplotlib

class Grapher():
  def __init__(self,filetype='png'):
      self.dpi = 55
      self.backend = {'png':'Agg','svg':'svg'}
      self.filetype = filetype
      matplotlib.use(self.backend[filetype])
      #makes emojis render proberly
      matplotlib.rcParams['font.size'] = 15
      matplotlib.rcParams["font.monospace"] = ["DejaVu Sans Mono"]
      matplotlib.rcParams["font.family"] = "monospace"
      self.goodColors = ['#e6194B','#3cb44b','#FFC107','#4363d8','#42d4f4',
                          '#f032e6','#795548']
  
  def makePlot(self,dData,filename,path=''):
    '''
    Makes a bar plot of dictionary data
    7 Colors are repeated and there is no background for the images

    Args:
      dict dData      : a dictionary with number values
      string filename : can include path in this variable 
      Optional:
        string path : can separately add path
    Returns:
      None
    
    Output:
      image file at given path
    '''
    maxValue = max(dData.values())
    length = len(dData.keys())
    colorLen = len(self.goodColors)
    keys = list(dData.keys())
    w = 3 #width

    #make it pretty, kinda
    fig, ax = subplots(figsize=(length,5),frameon=False,facecolor=(0,0,0))
    ax.axis('off')
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(0)
    for item in [fig, ax]:
      item.patch.set_visible(False)
    tick_params(top=False,right=False,left=False,bottom=False)

    #making the bars and labels
    for i in range(length):
      key = keys[i]
      value = dData[key]
      xStart = ((1+i)*w)-1
      yStart = 0
      xEnd = ((1+i)*w) 
      yEnd = value/maxValue
      ax.add_artist(Rectangle((xStart,yStart),w-0.5,yEnd,linewidth=3,fill=True,color=self.goodColors[i%colorLen]))
      text(xEnd+0.3,yEnd+0.05,f'{value}',rotation=0,fontsize=25,color=self.goodColors[i%colorLen],ha="center",va="center",fontname='Segoe UI Emoji',fontweight="bold")
      text(xEnd+0.3,-0.1,f'{key}',rotation=0,fontsize=30,color=self.goodColors[i%colorLen],ha="center",va="center",fontname='Segoe UI Emoji')
    
    #making it a tight fit to the bars
    xlim([0,length*w+w])
    ylim([-0.2,1.2])
    
    #removing the border created by the view and saving the file
    subplots_adjust(left=0,right=1, top=1, bottom=0.0) 
    savefig(f'{path}{filename}-dpi{self.dpi:d}.{self.filetype}', dpi=self.dpi)
    close()
