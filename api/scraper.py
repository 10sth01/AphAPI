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
               patchNoteLinks.append(link)
               
     for link in patchNoteLinks:
          
          patch_note_page = retrieve_page("https://www.leagueoflegends.com" + link)
          
          title = patch_note_page.find('h1', class_='title').text.strip()
          print(title)
          
          time = patch_note_page.find('time').text.strip()
          print(time)
          
          champions = patch_note_page.select("h3 > a[rel='noopener noreferrer nofollow']")
          
          print("\nChanges:")
          
          if not champions:
               print(f"No changes found for {title}")
               champions = patch_note_page.find_all("h3", class_="change-title")
          
          for champion in champions:
               print(champion.text.strip())
          print("\n")
          
def main():
     get_patch_notes()
     

if __name__ == "__main__":
     main()
