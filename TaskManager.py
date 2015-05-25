from pylab import *
from Tkinter import *
import psutil
import os
import __builtin__
import tkSimpleDialog
import time 


class MultiListbox(Frame):
    def __init__(self, master, lists):
	Frame.__init__(self, master)
	self.lists = []
	for l,w in lists:
	    frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
	    Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
	    lb = Listbox(frame, width=w, height=25, borderwidth=0, selectborderwidth=0,
			 relief=FLAT, exportselection=FALSE)
	    lb.pack(expand=YES, fill=BOTH)
	    self.lists.append(lb)
	    lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Leave>', lambda e: 'break')
	    lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
	    lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
	    lb.bind("<Double-Button-1>", self.OnDouble)
	frame = Frame(self); frame.pack(side=LEFT, fill=Y)
	Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
	sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
	sb.pack(expand=YES, fill=Y)
	self.lists[0]['yscrollcommand']=sb.set
	
    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print "selection:" '%s' % selection 
  	print "selection by" '%s' % __builtin__.myList[int(''.join(map(str,selection)))]
	p = psutil.Process(__builtin__.myList[int(''.join(map(str,selection)))])
	p.terminate()
	mlb.delete(0,END)
    	__builtin__.myList = []
    	for proc in psutil.process_iter():
          pro=proc.pid
          p=psutil.Process(pro)
	  __builtin__.myList.append(pro)        
	  mlb.insert(END, ('%d' % pro, '%s' % p.name(), '%s' % p.username(), '%d' % p.get_memory_percent()))	

    def _select(self, y):
	row = self.lists[0].nearest(y)
	self.selection_clear(0, END)
	self.selection_set(row)
	return 'break'

    def _button2(self, x, y):
	for l in self.lists: l.scan_mark(x, y)
	return 'break'

    def _b2motion(self, x, y):
	for l in self.lists: l.scan_dragto(x, y)
	return 'break'

    def _scroll(self, *args):
	for l in self.lists:
	    apply(l.yview, args)

    def curselection(self):
	return self.lists[0].curselection()

    def delete(self, first, last=None):
	for l in self.lists:
	    l.delete(first, last)

    def get(self, first, last=None):
	result = []
	for l in self.lists:
	    result.append(l.get(first,last))
	if last: return apply(map, [None] + result)
	return result
	    
    def index(self, index):
	self.lists[0].index(index)

    def insert(self, index, *elements):
	for e in elements:
	    i = 0
	    for l in self.lists:
		l.insert(index, e[i])
		i = i + 1

    def size(self):
	return self.lists[0].size()

    def see(self, index):
	for l in self.lists:
	    l.see(index)

    def selection_anchor(self, index):
	for l in self.lists:
	    l.selection_anchor(index)

    def selection_clear(self, first, last=None):
	for l in self.lists:
	    l.selection_clear(first, last)

    def selection_includes(self, index):
	return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
	for l in self.lists:
	    l.selection_set(first, last)
    
def virtual():
	p=psutil.virtual_memory()
	p0= p[2]
	p1= 100-p0
	frac = [p0,p1]
	labels = [p0,p1]
	explode = [0, 0]
	pie(frac, explode, labels, shadow=True)
	title('Virtual Memory')
	show()

def refresh(self):
    while True:
	time.sleep(2)
	self.update()	

if __name__ == '__main__':
    tk = Tk()
    tk.title('Process Explorer')
    proc=psutil.pids()
    Label(tk, text='OPTIONS').pack()
    frame2 = Frame(tk)       
    frame2.pack()
    b1 = Button(frame2,text="Refresh",command=refresh(tk))
    b2 = Button(frame2,text="Exit",command=exit)
    b3 = Button(frame2,text="Virtual Memory",command=virtual)
    b1.pack(side=LEFT); 
    b2.pack(side=LEFT); b3.pack(side=LEFT)
    mlb = MultiListbox(tk, (('Process ID', 10), ('Process Name', 20), ('User', 12), ('Status', 10)))
    mlb.delete(0,END)
    __builtin__.myList = []
    for proc in psutil.process_iter():
        pro=proc.pid
        p=psutil.Process(pro)
	__builtin__.myList.append(pro)        
	mlb.insert(END, ('%d' % pro, '%s' % p.name(), '%s' % p.username(), '%s' % p.status()))
    mlb.pack(expand=YES,fill=BOTH)   
    tk.mainloop()
