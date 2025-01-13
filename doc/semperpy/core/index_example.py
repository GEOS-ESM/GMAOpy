from semperpy.core.index import Index

index = Index('title','genre','director','year')
index.insert(dict(duration=120,location='3F'),title='Mr and Mrs Smith',genre='action',director='Doug Liman',year=2005)
index.insert(dict(duration=124,location='2A'),title='Notting Hill',genre='romantic comedy',director='Roger Michell',year=1999)
index.insert(dict(duration=117,location='17C'),title='Four Weddings and a Funeral',genre='romantic comedy',director='Mike Newell',year=1994)
index.insert(dict(duration=122,location='45Z'),title='Man to Man',genre='drama',director='Regis Wargnier',year=2005)
index.insert(dict(duration=96,location='12F'),title='An American Affair',genre='drama',director='William Olsson',year=2009)

