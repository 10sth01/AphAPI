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

def get_items():
     
     items_page = retrieve_page('https://leagueoflegends.fandom.com/wiki/List_of_items')
     items = items_page.find_all("div", class_="item-icon")
     items = [item.get('data-item') for item in items]
     
     return items
     
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
                               
     if not champion_changes: 
          changes = patch_note_page.find_all("h3", class_="change-title")
          for change in changes:
               if change.text.strip() in champions:
                    champion_changes.append(change.text.strip())
     
     return champion_changes

def get_item_changes(patch_note_page):
     
     patch_note_page = retrieve_page(patch_note_page)
     
     items = get_items()
     
     item_changes = []
     h2_tag = patch_note_page.find('h2', text='Items')
     
     if h2_tag: 
          next_sibling = h2_tag.find_next_sibling()
          while next_sibling:
               if (next_sibling.name == "h3") and (next_sibling.text.strip() in items):
                    item_changes.append(next_sibling.text.strip())
               next_sibling = next_sibling.find_next_sibling()

     if not item_changes:
          changes = patch_note_page.find_all("h3", class_="change-title")
          for change in changes:
               if change.text.strip() in items:
                    item_changes.append(change.text.strip())
                    
     return item_changes

def main():
     
     patch_note_links = get_patch_notes()
     
     for link in patch_note_links:
          print(get_title(link))
          print(get_datePosted(link))
          print("Champion Changes")
          print(get_champion_changes(link))
          print("Item Changes")
          print(get_item_changes(link))
          print("")
          
if __name__ == "__main__":
     main()
