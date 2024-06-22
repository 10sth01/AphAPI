import requests
import bs4 

def retrieve_page(url):
     
     response = requests.get(url)
     soup = bs4.BeautifulSoup(response.content, 'lxml')
     
     return soup
   
def get_patch_notes():
          
     main_page = retrieve_page('https://www.leagueoflegends.com/en-ph/news/tags/patch-notes/')

     patchNotes = main_page.select("a[class='sc-87e5609-0 ezOpNh sc-8f90eaf7-0 cQWGGy sc-759b9122-5 dIAeui action']")
     
     patchNoteLinks = []
     
     for tag in patchNotes:
          link = tag.get('href')
          if link:
               patchNoteLinks.append("https://www.leagueoflegends.com" + link)
               
     return patchNoteLinks

def get_title(patch_note_page):
     
     patch_note_page = retrieve_page(patch_note_page)
     return patch_note_page.find('h1', class_='title').text.strip()

def get_datePosted(patch_note_page): 
               
     patch_note_page = retrieve_page(patch_note_page)
     return patch_note_page.find('time').text.strip() 

def get_champions():
     
     champion_page = retrieve_page('https://www.leagueoflegends.com/en-us/champions/')
     champions = champion_page.find_all("a", class_="sc-87e5609-0 ezOpNh sc-8f90eaf7-0 cQWGGy")
     champions = [champion.get('aria-label') for champion in champions]
     
     return champions
     
def get_champion_changes(patch_note_page):
     
     patch_note_page = retrieve_page(patch_note_page)
     
     champions = get_champions()
     
     champion_changes = []
     h2_tag = patch_note_page.find('h2', text='Champions')
     
     if h2_tag:
          next_sibling = h2_tag.find_next_sibling()
          while next_sibling:
               if (next_sibling.name == "h3") and (next_sibling.text.strip() in champions):
                    champion_changes.append(next_sibling.text.strip())
               next_sibling = next_sibling.find_next_sibling()
                               
     # champions = patch_note_page.select("h3 > a[rel='noopener noreferrer nofollow']")
     
     # if not champions:
     #           champions = patch_note_page.find_all("h3", class_="change-title")
               
     # champions = [champion.text.strip() for champion in champions]
     
     return champion_changes

def main():
     
     patch_note_links = get_patch_notes()
     
     for link in patch_note_links:
          print(get_title(link))
          print(get_datePosted(link))
          print(get_champion_changes(link))
          print("")
          
if __name__ == "__main__":
     main()
