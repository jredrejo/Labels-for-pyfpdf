# coding: utf8

def labels():
    from gluon.contrib.pyfpdf.pdflabels import PDFLabel        
    """
        To create the object, 2 possibilities:
        either pass a custom format via a dictionary
        or use a built-in commercial AVERY or APLI name
    """
    
    # Example of custom format
    #pdf = PDFLabel({'paper-size':'A4', 'metric':'mm', 'marginLeft':1, 'marginTop':1, 'NX':2, 'NY':7, 'SpaceX':0, 'SpaceY':0, 'width':99, 'height':38, 'font-size':14})
    
    pdf = PDFLabel('Avery-L7163')
    pdf.add_page()
    
    # The next three lines are a needed trick if the data to be printed 
    # is collected from some source of data with utf-8 codification:
    import sys
    reload(sys)
    sys.setdefaultencoding( "latin-1" )   
        
    # Print labels
    for i in range(0,20):
        text="%s\n%s\n%s\n%s %s, %s" % ("Laurent %s" % str(i), 'Immeuble Toto', 'av. Fragonard', '06000', 'NICE', 'FRANCE')
        pdf.add_label(text)
        
    response.headers['Content-Type'] = 'application/pdf'
    return pdf.output(dest='S')     
    
def table():
    from gluon.contrib.pyfpdf import FPDF, HTMLMixin
    import os
    response.title = "web2py sample report"
    
    # include a google chart!
    url = "http://chart.apis.google.com/chart?cht=p3&chd=t:60,40&chs=250x100&chl=Hello|World&.png"
    chart = IMG(_src=url, _width="250",_height="100")

    # create a small table with some data:
    rows = [THEAD(TR(TH("Key",_width="70%"), TH("Value",_width="30%"))),
            TBODY(TR(TD("Hello"),TD("60")), 
                  TR(TD("World"),TD("40")))]
    table = TABLE(*rows, _border="0", _align="center", _width="50%")


    # create a custom class with the required functionalities 
    class MyFPDF(FPDF, HTMLMixin):
        def header(self): 
            "hook to draw custom page header"
            logo=os.path.join(request.env.web2py_path,"applications","labels","static","images","logo_pb.png")
            self.image(logo,10,8,33)
            self.set_font('Arial','B',15)
            self.cell(65) # padding
            self.cell(60,10,response.title,1,0,'C')
            self.ln(20)
            
        def footer(self):
            "hook to draw custom page header (printing page numbers)"
            self.set_y(-15)
            self.set_font('Arial','I',8)
            txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
            self.cell(0,10,txt,0,0,'C')
                    
        
    pdf = MyFPDF()
    pdf.add_page()
    
    # The next three lines are a needed trick if the data to be printed 
    # is collected from some source of data with utf-8 codification:
    import sys
    reload(sys)
    sys.setdefaultencoding( "latin-1" )      
      
    #send html to the pdf with required encoding 
    # also, I change the font size for the text (default size is 12)
    pdf.write_html('<font size="10">' + table.xml().decode('UTF-8') + '</font>')
    pdf.write_html(str(XML(CENTER(chart), sanitize=False)))
    response.headers['Content-Type'] = 'application/pdf'        
    #send the PDF as a string
    return pdf.output(dest='S')          
