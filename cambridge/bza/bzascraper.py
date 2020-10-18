import urllib
from BeautifulSoup import BeautifulSoup
urls = [
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bEED10314-1B34-45E0-B9F7-432CE30CD5CC%7d&start=20201022T180000&end=20201022T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b6AAF6C47-B5BB-4165-9675-158E46D56C19%7d&start=20201008T180000&end=20201008T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b2DFB58E5-26BB-4EC7-8D51-DEDF2330DC28%7d&start=20200910T180000&end=20200910T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b082892FE-E1B2-4E10-BEAC-B152B0406209%7d&start=20200924T180000&end=20200924T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b70F35378-B592-46C0-8E84-7CC58ABABF68%7d&start=20200813T180000&end=20200813T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bA33C8EFD-9420-4512-B4EA-BF3174FA2726%7d&start=20200827T180000&end=20200827T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b0066525F-3A66-4248-8024-9DCEB252E827%7d&start=20200709T180000&end=20200709T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b943F88C5-70DC-4BE6-9982-24FD301F33BA%7d&start=20200723T180000&end=20200723T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b8F553611-3B2B-4C99-BFF9-140677A3BBD0%7d&start=20200730T180000&end=20200730T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b406B6F86-0C72-4064-B421-5D826736CAD3%7d&start=20200312T190000&end=20200312T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b4CE573D2-15DC-47EA-9993-7D4D8E3A26B3%7d&start=20200326T190000&end=20200326T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b3595F31D-BE65-457B-B354-C357177FBDC7%7d&start=20200213T190000&end=20200213T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b28DD2A30-AF5F-449D-AB0B-1E75F5B47A0A%7d&start=20200227T190000&end=20200227T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b59438BCF-14FA-4DC0-98B1-DC664BB16BBB%7d&start=20200109T190000&end=20200109T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bC3E7B35A-1052-449D-BAC4-DFF0A032907F%7d&start=20200130T190000&end=20200130T233000',

  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b69B0C6D7-74FB-4403-99A2-E8CE8218D3DE%7d&start=20191205T190000&end=20191205T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b7E8B984D-CF24-4C49-B661-667B78B57DCA%7d&start=20191212T190000&end=20191212T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b994AC147-022F-4455-8863-4A49CBBCF5ED%7d&start=20191107T190000&end=20191107T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bDEFCB44D-41E8-4623-8386-8C162CBD202F%7d&start=20191121T190000&end=20191121T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b3833EEDA-EF9A-4B52-A7FE-A9D7EC1447DC%7d&start=20191010T190000&end=20191010T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b339ADA66-BC16-4F71-869A-B683F1207D12%7d&start=20191024T190000&end=20191024T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b5850E7F9-1B8B-401C-8A45-5DDE64E6E14E%7d&start=20190912T190000&end=20190912T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b82DE8287-382C-4976-800F-D0F4DE35D915%7d&start=20190926T190000&end=20190926T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bBEE37B87-C82F-42BC-8070-91726DB8BEB9%7d&start=20190815T190000&end=20190815T234500',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bC7584EBA-C9B0-4541-9C6C-2D74E857F4EA%7d&start=20190711T190000&end=20190711T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b3D132B2A-200E-4E06-8490-7F085986E24D%7d&start=20190725T190000&end=20190725T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b6833BACF-D5F4-4844-9277-1128CA7E2E03%7d&start=20190613T190000&end=20190613T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bD812CA8C-07BE-4B1E-A58D-EE7534E9328B%7d&start=20190627T190000&end=20190627T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b220B245C-9D56-4C76-9CEB-6A9BC722C70E%7d&start=20190516T190000&end=20190516T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bB5D40A6C-82E9-49EC-A431-B19F36FC0E33%7d&start=20190530T190000&end=20190530T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bF5254D85-46AB-4AAC-B4BE-18EFF0E4C0AE%7d&start=20190411T190000&end=20190411T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bB1FC8D02-415C-4783-8AE7-6C8B84EDBBFD%7d&start=20190425T190000&end=20190425T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bD1340CBF-FB52-4B5C-8658-1E7C5CB2E173%7d&start=20190314T190000&end=20190314T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bC0ABB717-73B2-4AA1-A825-1DEEF6D0EA72%7d&start=20190328T190000&end=20190328T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bC5320098-48A5-4F34-B684-9531DBED0486%7d&start=20190214T190000&end=20190214T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7bBA80E5EB-7956-4856-B7F5-4A5710123695%7d&start=20190228T190000&end=20190228T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b867C5A68-DE41-4F76-8AEB-8C3589E032AF%7d&start=20190110T193000&end=20190110T233000',
  'https://www.cambridgema.gov/inspection/Calendar/view.aspx?guid=%7b69B2C180-9F49-4E7D-A1C0-1305ECEC7ABC%7d&start=20190131T193000&end=20190131T233000',
]

for page in urls:
    u = urllib.urlopen(page)
    bs = BeautifulSoup(u.read())
    for i in bs.findAll("table", attrs={'class':'bza-case'}):
        try:
            petitioner = i.findAll("tr")[2].find("td").find("p")
            if petitioner:
                if "C/O" in petitioner.text:
                    print petitioner.text
        except:
            pass
