from bs4 import BeautifulSoup
import requests
import os

# Step 1: Create a function to retrieve the links of the departments under the college
def get_department_links(college_url):
    print(f'Getting departments for {college_url}.. ')
    html_text = requests.get(college_url)
    soup = BeautifulSoup(html_text.text, 'lxml')

    div_entry = soup.find('div', class_='entry clearfix') or soup.find('div', class_='entry')

    if div_entry:
        ul_element = div_entry.ul
        if ul_element:
            department_links = [a['href'] for li in ul_element.find_all('li') if
                                (a := li.find('a')) and 'href' in a.attrs]
            print('Done with getting departments!')
            return department_links
        else:
            print('Error: Could not find "ul" element within div_entry.')
            return []
    else:
        print(f'Error: Could not find div_entry with class "entry clearfix" or "entry" at {college_url}.')
        return []

# List of college URLs
college_urls = {
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-health-sciences/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-business-and-economics/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-humanities-language-studies-journalism-and-communication/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-natural-sciences/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-performing-and-visual-arts/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-social-sciences/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/college-of-veterinary-medicine-and-agriculture/',
    'http://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/architecture-building-contraction-and-city-development/'
}

# Step 2: Iterate through the list of college URLs
for college_url in college_urls:
    department_urls = get_department_links(college_url)

    # Step 3: Iterate through the retrieved links and scrape the information for each department
    for index, url in enumerate(department_urls):
        html_text = requests.get(url)
        soup = BeautifulSoup(html_text.content, 'lxml')

        # Check if 'div' with class 'entry clearfix' exists
        div_entry = soup.find('div', class_='entry clearfix') or soup.find('div', class_='entry')
        if div_entry:
            # Find 'p' tags within the 'div'
            content_tags = div_entry.find_all('p')[:14]

            content = ''
            for content_tag in content_tags:
                content += content_tag.get_text(strip=True) + " \n"

            # Find 'ul' or 'ol' for general objectives
            general_objectives = div_entry.find('ul') or div_entry.find('ol')
            if general_objectives:
                general_objective = ''
                for li in general_objectives.find_all('li'):
                    general_objective += li.get_text(strip=True) + ' \n'
            else:
                general_objective = 'General objectives not found.'

            # Step 4: Save the scraped information to separate files for each department
            college_name = college_url.split('/')[-2]  # Extract college name from the URL
            directory = f'{college_name}_Departments_Info'
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f'Creating directory.. ')
            file_path = os.path.join(directory, f'{index}.txt')
            with open(file_path, 'w') as f:
                f.write(f"Content:\n{content}\n\nGeneral Objectives:\n{general_objective}\n")

            print(f'File Saved: {file_path}')
        else:
            print(f'Error: Could not find "div_entry" with class "entry clearfix" or "entry" at {url}.')

# content_all = []
# content_all = content_all + content

# print(f'Mission Statement: {mission_statement}')

# with open('home.html', 'r') as html_file:
#     content = html_file.read()
#     soup = BeautifulSoup(content, 'lxml')
#     course_cards = soup.find_all('div', class_='card')
#     for course in course_cards:
#         course_name = course.h5.text
#         course_price = course.a.text.split()[-1]
#         print(f'{course_name} costs {course_price}')

# tags = soup.find_all('h5')
# for tag in tags:
#     print(tag.text)
