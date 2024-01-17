from bs4 import BeautifulSoup
import requests
import os

url = 'http://www.aau.edu.et/quick-links/aau-colleges/'

def get_college_links(college_url):
    print('Getting College info....')
    college_text = requests.get(college_url)
    soup = BeautifulSoup(college_text.text, 'lxml')

    college_entry = soup.find('div', class_='entry clearfix') or soup.find('div', class_='entry')
    if college_entry:
        ul_element = college_entry.ul
        print('ul exists in the college_entry')
        if ul_element:
            College_links = [a['href'] for li in ul_element.find_all('li') if
                             (a := li.find('a')) and 'href' in a.attrs]
            print('Done with getting colleges!')
            modified_links = []
            for link in College_links:
                if not link.startswith('http://www.aau.edu.et'):
                    link = 'http://www.aau.edu.et' + link
                modified_links.append(link)

            # Append the common part to all links outside the loop
            modified_links = modified_links + ['http://www.aau.edu.et/about/mission-vision/']

            return modified_links
        else:
            print('Error: Could not find "ul" element within college_entry.')
            return []
    else:
        print(f'Error: Could not find div_entry with class "menu-sidebar-colleges" in {college_url}.')
        return []


college_links = get_college_links(url)
for index, college_url in enumerate(college_links):
    html_text = requests.get(college_url)
    soup = BeautifulSoup(html_text.content, 'lxml')
    div_entry = soup.find('div', class_='entry clearfix') or soup.find('div', class_='entry')
    if div_entry:
        # Find 'p' tags within the 'div'
        content_tags = div_entry.find_all('p')[:14]

        # Improved content structure with newline characters
        content = '\n'.join([content_tag.get_text(strip=True) for content_tag in content_tags])

        college_name = college_url.split('/')[-3]
        directory = f'{college_name}_College_Info'
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f'Creating directory...')
        file_path = os.path.join(directory, f'{index}.txt')
        with open(file_path, 'w') as f:
            f.write(f"Content:\n{content}\n \n")

        print(f'File Saved: {file_path}')
    else:
        print(f'Error: Could not find "div_entry" with class "entry clearfix" or "entry" at {url}.')
