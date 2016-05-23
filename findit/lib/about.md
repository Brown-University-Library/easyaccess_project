easyAccess
==========

'easyAccess' is a service of the [Brown University Library][BUL] that makes it easier to get books and articles.

In many Library, and Article, and Book websites, a link to an article or book may take you to this easyAccess service. Included in that link is a very long string (called an [openurl][openurl]) which contains information about the item you want.

This easyAccess service will inspect that item-information, and do a bunch of lookups on services the Brown University Library subscribes to, and has built, to try to get you right to the item you want.


### Books

If it's a book you're looking for, and we have it in the Library, and it's available, you'll be told that so you can come and get it.

If we don't have the book, or it's not easily available, you'll be able to (with a simple button-click and log-in) request the book, and our easyBorrow service will find it, and borrow it for you. You'll get an initial email with information that it's in-process, and then another email when the book arrives at the Rock for you to pick up.


## Articles

If you're looking for an article, behind the scenes we'll search services we've built and subscribe to to see if we take you directly to the full-text for the article.

If we can't get you immediately to the full-text of the article, our easyArticle service makes it a one-click & log-in process to order it. You'll get an initial email with information that it's in-process, and then another email when a link to the article is ready.


[BUL]: https://library.brown.edu/
[openurl]: https://en.wikipedia.org/wiki/OpenURL


## Examples

Below are examples of book and article links to this easyAccess service.

If you have any questions, feel free to email us at z@z.edu -- and should you run into a problem, all of our pages have a link to report the issue.


#### Article examples

- [Held electronically only. (should redirect to item)
{{ BASE_URL }}?sid=google&auinit=T&aulast=SOTA&atitle=Phylogeny+and+divergence+time+of+island+tiger+beetles+of+the+genus+Cylindera+(Coleoptera:+Cicindelidae)+in+East+Asia&id=doi:10.1111/j.1095-8312.2011.01617.x&title=Biological+journal+of+the+Linnean+Society&volume=102&issue=4&date=2011&spage=715&issn=0024-4066">

- [Held in print only. (should show holdings location)
{{ BASE_URL }}?rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.spage=80&rft.au=Churchland%2C PS&rft.aulast=Churchland&rft.format=journal&rft.date=1983&rft.aufirst=PS&rft.volume=64&rft.eissn=1468-0114&rft.atitle=Consciousness%3A The transmutation of a concept&rft.jtitle=Pacific philosophical quarterly&rft.issn=0279-0750&rft.genre=article&url_ver=Z39.88-2004&rfr_id=info:sid/libx%3Abrown">

- [Article-chapter held at Annex. (should show holdings location, with josiah link)
{{ BASE_URL }}?genre=article&issn=00377686&title=Social%20Compass&volume=14&issue=5%2F6&date=19670901&atitle=Religious%20knowledge%20and%20attitudes%20in%20Mexico%20City.&spage=469&pages=469-482&sid=EBSCO:Academic%20Search%20Premier&aulast=Stryckman,%20Paul">

- [Journal held at annex and has journal-level link, not direct to full text. (should show both, with note that it's not to full text, and josiah link)
{{ BASE_URL }}?rft.issn=0301-0066&rft.externalDocID=19806992&rft.date=2009-01-01&rft.volume=38&rft.issue=6&rft.spage=927&rft.jtitle=Perception&rft.au=Rhodes%2C+Gillian&rft.au=Jeffery%2C+Linda&rft.atitle=The+Thatcher+illusion%3A+now+you+see+it%2C+now+you+don%27t&ctx_ver=Z39.88-2004&rft.genre=article&ctx_enc=info%3Aofi%2Fenc%3AUTF-8&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal">

- [Mutliple full text links. (should take user right to one)
{{ BASE_URL }}?rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/www.isinet.com:WoK:UA&rft.spage=864&rft.issue=5&rft.epage=875&rft.title=JOURNAL%20OF%20ECOLOGY&rft.aulast=De%20Deyn&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft.date=2009&rft.volume=97&url_ver=Z39.88-2004&rft.stitle=J%20ECOL&rft.atitle=Vegetation%20composition%20promotes%20carbon%20and%20nitrogen%20storage%20in%20model%20grassland%20communities%20of%20contrasting%20soil%20fertility&rft.au=Bardgett%2C%20R&rft_id=info:doi/10%2E1111%2Fj%2E1365-2745%2E2009%2E01536%2Ex&rft.auinit=G&rft.issn=0022-0477&rft.genre=article">

- [Not held - request via Illiad. (should display link to request the article from illiad)
{{ BASE_URL }}?atitle=Stalking+the+Wild+Basenji&jtitle=AKC+gazette&pages=&date=2006&issn=&id=&pmid=&volume=&issue=&au=Curry&rfe_dat">

- [Print and online holdings; resolved link not direct to article. (should show both, with note that it's not to full text)
{{ BASE_URL }}?volume=9&genre=article&spage=39&sid=EBSCO:qrh&title=Gay+%26+Lesbian+Review+Worldwide&date=20020501&issue=3&issn=15321118&pid=&atitle=Chaste+Take+on+Those+Naughty+Victorian's.">

- [Direct links and non-direct links. (should ignore non-direct links and redirect to article)
{{ BASE_URL }}?rft.issn=0036-8075&rft.externalDocID=10_1126_science_1074128&rft.date=2002-10-11&rft.volume=298&rft.spage=409&rft.epage=412&rft.issue=5592&rft.pub=American+Association+for+the+Advancement+of+Science&rft.externalDBID=GSCI&rft.atitle=Neural+Correlates+for+Perception+of+3D+Surface+Orientation+from+Texture+Gradient&rft.jtitle=Science+%28New+York%2C+N.Y.%29&rft.au=Taira%2C+Masato&rft.au=Tsutsui%2C+Ken-Ichiro&rft.au=Sakata%2C+Hideo&rft.au=Naganuma%2C+Tomoka&ctx_ver=Z39.88-2004&rft.genre=article&rft_id=info%3Adoi%2F10.1126%2Fscience.1074128&ctx_enc=info%3Aofi%2Fenc%3AUTF-8&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal">

- [Pubmed request - direct-link available. (should redirect to article)
{{ BASE_URL }}?pmid=12611747&sid=demo">

- [Pubmed request - item not held. (should display link to request the article from illiad)
{{ BASE_URL }}?pmid=18496984&sid=Entrez:PubMed">

- [Pubmed request - locally-held and no direct link. (should show local holdings, and W.H.O. link which includes search)
{{ BASE_URL }}?pmid=11234459">

- [Request from Worldcat for a citation that resolves to a journal, not an article. (should -- for now -- redirect to old serial-solutions resolver)
{{ BAE_URL }}?sid=FirstSearch%3AWorldCat&genre=journal&issn=2151-0814&title=Charter+school+law+deskbook.&id=doi%3A&pid=%3Caccession+number%3E436869608%3C%2Faccession+number%3E%3Cfssessid%3E0%3C%2Ffssessid%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E436869608%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F436869608&rft_id=urn%3AISSN%3A2151-0814&rft.jtitle=Charter+school+law+deskbook.&rft.issn=2151-0814&rft.place=Charlottesville++VA&rft.pub=LexisNexis&rft.genre=journal&checksum=25d304e7598efe59760d18e8854b5090&title=Brown University&linktype=openurl&detail=RBN">





    <h5 class="intro">Book Examples</h5>
    <ul>
    <li><a href="{{ BASE_URL }}?sid=FirstSearch:WorldCat&genre=book&isbn=9780439339117&title=Zen+shorts&date=2005&aulast=Muth&aufirst=Jon&auinitm=J&id=doi:&pid=53084041&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&rfe_dat=<accessionnumber>53084041</accessionnumber>&rft_id=info:oclcnum/53084041&rft_id=urn:ISBN:9780439339117&rft.aulast=Muth&rft.aufirst=Jon&rft.auinitm=J&rft.btitle=Zen+shorts&rft.date=2005&rft.isbn=9780439339117&rft.place=New+York&rft.pub=Scholastic+Press&rft.edition=1st+ed.">
        Requestable -- no alternate versions.</a> (should redirect to easyBorrow landing page; should show 'Request' button)</li>
    <!-- <li><a href="{{ BASE_URL }}?sid=FirstSearch%3AWorldCat&genre=book&isbn=9780099598169&title=Zen+and+the+art+of+motorcycle+maintenance+%3A+an+inquiry+into+values&date=2014&aulast=Pirsig&aufirst=Robert&auinitm=M&id=doi%3A&pid=897778210%3Cfssessid%3E0%3C%2Ffssessid%3E%3Cedition%3E40th+anniversary+edition.%3C%2Fedition%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E897778210%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F897778210&rft_id=urn%3AISBN%3A9780099598169&rft.aulast=Pirsig&rft.aufirst=Robert&rft.auinitm=M&rft.btitle=Zen+and+the+art+of+motorcycle+maintenance+%3A+an+inquiry+into+values&rft.date=2014&rft.isbn=9780099598169&rft.edition=40th+anniversary+edition.&rft.genre=book">
        Requestable -- version not available, _should_ show other versions available</a></li> -->
    <li><a href="{{ BASE_URL }}?sid=FirstSearch%3AWorldCat&genre=book&title=Zen&date=1978&aulast=Yoshioka&aufirst=Tōichi&id=doi%3A&pid=6104671%3Cfssessid%3E0%3C%2Ffssessid%3E%3Cedition%3E1st+ed.%3C%2Fedition%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E6104671%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F6104671&rft.aulast=Yoshioka&rft.aufirst=Tōichi&rft.btitle=Zen&rft.date=1978&rft.place=Osaka++Japan&rft.pub=Hoikusha&rft.edition=1st+ed.&rft.genre=book">
        Requestable -- ebook also available.</a> <br/>(should redirect to easyBorrow landing page; should show 'Request' button, and show ebook link)</li>
    <li><a href="{{ BASE_URL }}?sid=FirstSearch%3AWorldCat&genre=book&isbn=9780688002305&title=Zen+and+the+art+of+motorcycle+maintenance%3A+an+inquiry+into+values%2C&date=1974&aulast=Pirsig&aufirst=Robert&auinitm=M&id=doi%3A&pid=673595%3Cfssessid%3E0%3C%2Ffssessid%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E673595%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F673595&rft_id=urn%3AISBN%3A9780688002305&rft.aulast=Pirsig&rft.aufirst=Robert&rft.auinitm=M&rft.btitle=Zen+and+the+art+of+motorcycle+maintenance%3A+an+inquiry+into+values%2C&rft.date=1974&rft.isbn=9780688002305&rft.place=New+York&rft.pub=Morrow&rft.genre=book">
        Not requestable -- local copy available.</a> <br/>(should redirect to easyBorrow landing page; should _not_ show 'Request' button, should show minimal info about available copies, and show the new-josiah bib-link)</li>
    <li><a href="{{ BASE_URL }}?sid=FirstSearch%3AWorldCat&isbn=9781587299803&title=Supplement+to+%22Walt+Whitman%2C+a+descriptive+bibliography%22&date=2011&aulast=Myerson&aufirst=Joel&id=doi%3A&pid=727367664%3Cfssessid%3E0%3C%2Ffssessid%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=unknown&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E727367664%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F727367664&rft_id=urn%3AISBN%3A9781587299803&rft.aulast=Myerson&rft.aufirst=Joel&rft.title=Supplement+to+%22Walt+Whitman%2C+a+descriptive+bibliography%22&rft.date=2011&rft.isbn=9781587299803&rft.place=Iowa+City+%3A&rft.pub=University+of+Iowa+Press%2C&rft.genre=unknown">
        Not requestable -- local copy available; and Hay and ebook and 'other editions' available.</a> <br/>(should redirect to easyBorrow landing page; _not_ show 'Request' button, and show minimal info about available print, ebook, and Hay copies, and minimal info about other-editions available, and show the new-josiah bib-link)</li>
    </ul>


---