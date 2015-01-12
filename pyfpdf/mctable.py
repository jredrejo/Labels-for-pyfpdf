#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# * Software: Table with multicell                                             *
# * Date:     2015-01-11                                                       *
# * License:  LGPL v3.0                                                        *
# *                                                                            *
# * Original Author (PHP):  Copyright (C) 2002 Olivier oliver@fpdf.org         *
# * Published at http://www.fpdf.org/en/script/script3.php                     *
# *                                                                            *
# * Ported to Python 2.6 by jredrejo (jredrejo@debian.org)   January-2015      *
# *****************************************************************************/
try:
    from pyfpdf import FPDF
except:
    from fpdf import FPDF


    def set_fill_color(self,r,g=-1,b=-1):
        "Set color for all filling operations"
        if((r==0 and g==0 and b==0) or g==-1):
            self.fill_color=sprintf('%.3f g',r/255.0)
        else:
            self.fill_color=sprintf('%.3f %.3f %.3f rg',r/255.0,g/255.0,b/255.0)
        self.color_flag=(self.fill_color!=self.text_color)
        if(self.page>0):
            self._out(self.fill_color)
            
def hex2dec(color = "#000000"):
    if color:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return r, g, b
            
class MCTable(FPDF):
    def __init__(self,widths=[],aligns=[]):
        super(MCTable,self).__init__()   
        self.widths=widths
        self.aligns=aligns
        
    def set_widths(self,w):
        """Set the array of column widths"""
        self.widths=w
    
    def set_aligns(self,a):
        """Set the array of column alignments"""
        self.aligns=a
        
    def box_shadow(self, w, h, bgcolor):
        if bgcolor:
            fill_color = self.fill_color
            self.set_fill_color(*bgcolor)
            self.rect(self.x, self.y, w, h, 'F')
            self.fill_color = fill_color
                
    def row(self,data,background_color="ffffff",border=0):
        # Calculate the height of the row
        nb=0
        for i, item in enumerate(data):
            nb=max(nb,self.number_lines(self.widths[i],item))
        h=5*nb
        # Issue a page break first if needed
        self.check_page_break(h)
        bgcolor = hex2dec(background_color)
        # Draw the cells of the row
        for i, item in enumerate(data):
            w=self.widths[i]
            a='L' 
            if len(self.aligns)>i:
                a='L' if not self.aligns[i] else self.aligns[i]
            # Save the current position
            x=self.get_x()
            y=self.get_y()
            # Draw the border
            #self.rect(x,y,w,h)
            # Set the fill color
            self.box_shadow(w, h, bgcolor)
            # Print the text
            self.multi_cell(w,5,item,border,a)
            # Put the position to the right of the cell
            self.set_xy(x+w,y)
        # Go to the next line
        self.ln(h)
        
    def check_page_break(self,h):
        """If the height h would cause an overflow, add a new page immediately"""
        if self.get_y()+h>self.page_break_trigger:
            self.add_page(self.cur_orientation)

    def number_lines(self,w,txt):
        """Computes the number of lines a MultiCell of width w will take"""
        cw=self.current_font['cw']
        if(w==0):
            w=self.w-self.r_margin-self.x
        wmax=(w-2*self.c_margin)*1000.0/self.font_size
        s=txt.replace("\r",'')
        nb=len(s)
        if(nb>0 and s[nb-1]=="\n"):
            nb-=1
        sep=-1
        i=0
        j=0
        l=0
        nl=1
        while(i<nb):
            #Get next character
            c=s[i]
            if(c=="\n"):
                #Explicit line break
                i+=1
                sep=-1
                j=i
                l=0
                nl+=1
                continue
            if(c==' '):
                sep=i
            if self.unifontsubset:
                l += self.get_string_width(c) / self.font_size*1000.0
            else:
                l += cw.get(c,0)
            if(l>wmax):
                #Automatic line break
                if(sep==-1):
                    if(i==j):
                        i+=1
                else:
                    i=sep+1
                sep=-1
                j=i
                l=0
                nl+=1
            else:
                i+=1            

        return nl


if __name__ == "__main__":
    import random
    import string

    def generate_word(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
        
    
    def generate_sentence():
        # Get a random sentence
        nb=random.randint(1,10)
        s=""
        for i in range(nb):
            s +=" "
            s +=generate_word(random.randint(2,7),string.ascii_lowercase )            
        return s[1:]
                
    # Table with 20 rows and 4 columns        
    pdf = MCTable(widths=(30,50,30,40))
    pdf.add_page()
    pdf.set_font('arial', '', 14.0)
    
    for i in range(20):
        col = i % 2 and "#E3E3E3" or "#FFFFFF"
        pdf.row((generate_sentence(),generate_sentence(),generate_sentence(),generate_sentence()),col)
    pdf.output('./table_archive.pdf', 'F')
    
