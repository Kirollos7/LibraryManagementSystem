{
    
    
    'name' : 'Library System Management',
    
    'author' : 'Kirollos',  
    
    'summary' : 'Manage books easily',
    
    
     'website': "http://www.facebook.com", 
    
     'category': 'Uncategorized',
    
     'version': '13.0.1',
    
     'depends': ['base'],
     'application' : True,
     'data': [
    #   'views/views.xml',
        'security/groups.xml' ,
        'security/ir.model.access.csv',
        'views/library_book_view.xml',
        'views/library_book_category_view.xml'
        
        ],
    
    #  'demo': ['demo.xml'], 
    
     
    #  'images':'static/description/icon.png'
    
}