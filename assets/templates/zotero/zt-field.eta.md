title: <%= JSON.stringify(it.title || "") %>
citekey: <%= JSON.stringify(it.citekey || "") %>
authors:
<% if (it.creators && it.creators.length > 0) { %>
<%   it.creators.forEach(function(c) { %>
  - <%= JSON.stringify((c.lastName && c.firstName) ? (c.lastName + ", " + c.firstName) : (c.name || "")) %>
<%   }); %>
<% } else { %>
[]
<% } %>
year: <%= it.date ? (String(it.date).match(/\d{4}/) ? String(it.date).match(/\d{4}/)[0] : String(it.date)) : "" %>
journal: <%= JSON.stringify(it.publicationTitle || "") %>
doi: <%= JSON.stringify(it.DOI || it.doi || "") %>
tags: []
status: "unread"
rating: 
date_added: <%= new Date().toISOString().slice(0, 10) %>
date_read: 