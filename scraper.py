import requests
from bs4 import BeautifulSoup
import re
import os
import traceback

def get_list_of_applications():
    url = "https://www.citywindsor.ca/residents/planning/land-development/development-applications/current-development-applications"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    applications = []
    # applications are in a table, table columns are: File Name, Address, Application Type, Other Information
    table = soup.find('table')
    if not table:
        print("No table found on the webpage.")
        return []
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) < 4:
            continue  # Skip rows that don't have enough columns
        file_name = cols[0].text.strip() # file name also contains a link to the application
        link = cols[0].find('a')['href'] if cols[0].find('a') else None
        if link:
            file_name = link.split('/')[-1]
        else:
            print("Link not found for" + file_name)
        # if link starts with /, add https://www.citywindsor.ca to the beginning
        if link and link.startswith('/'):
            link = 'https://www.citywindsor.ca' + link

        address = cols[1].text.strip()
        application_type = cols[2].text.strip()
        other_info = cols[3].text.strip()
        pdf_links = []
        # check if cols[3] contains a link to a pdf
        # if 'href' in other_info:
        if cols[3].find('a'):
            pdf_links = [{'url': "https://www.citywindsor.ca" + a['href'] if a['href'].startswith('/') else a['href'], 'name': a.get_text()} for a in cols[3].find_all('a') if a['href'].endswith('.pdf')]
        # other info can contain links to pdfs, we need to extract these links
        applications.append({
            'file_name': file_name,
            'link': link,
            'address': address,
            'application_type': application_type,
            'other_info': other_info,
            'pdf_links': pdf_links
        })
    return applications

def get_application(application):
    # gets individual application
    url = application['link']
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        print("URL:", url)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    # find div with class page
    # page contains div, that div contains two divs, pick second div
    page_div = soup.find('div', class_='page')
    # get the immediate child div of page_div
    content = page_div.find_all('div')[0]
    # get list of immediate child divs, don't include nested divs
    content = content.find_all('div', recursive=False)[1]

    # find all links to pdfs in the content
    pdf_links = content.find_all('a', recursive=True)
    pdf_links = [{'url': ('https://www.citywindsor.ca' + a['href'] if a['href'].startswith('/') else a['href']), 'name': a.get_text()} for a in pdf_links if a['href'].endswith('.pdf')]
    # append pdf links to application
    application['pdf_links'].extend(pdf_links)
    # remove duplicate pdf links
    # application['pdf_links'] = list({v['url']: v for v in application['pdf_links']}.values())
    # get all text in the content div
    content = content.get_text(separator="\n").strip()
    # extract text before "Associated Documents:"
    project_description = content.split("Associated Documents:")[0].strip()
    # extract text after "For general information, call 311. For detailed inquiries, contact:"
    citywindsor_contact = content.split("For general information, call 311. For detailed inquiries, contact:")[-1].strip()
    application['project_description'] = project_description
    application['citywindsor_contact'] = citywindsor_contact
    return application

def sanitize_file_name(file_name):
    # Replace unsafe characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def get_pdfs(application):
    # get all pdf links
    try:
        pdf_links = application['pdf_links']
        application_name = sanitize_file_name(application['file_name'])
        save_dir = os.path.join('pdfs', application_name)
        print(f"Saving PDFs to {save_dir}")
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

        for pdf in pdf_links:
            url = pdf['url']
            file_name = sanitize_file_name(pdf['name']) + '.pdf'
            file_path = os.path.join(save_dir, file_name)

            if os.path.exists(file_path):
                print(f"File already exists, skipping: {file_path}")
            else:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {file_path}")
                else:
                    print(f"Failed to download {url}")
                    continue

            # Update the pdf link with the local file path
            pdf['file_path'] = file_path

        application['pdf_links'] = pdf_links  # Update application with updated pdf links
        return application
    except Exception as e:
        print(f"Error while downloading PDFs: {e}")
        print(e.__traceback__)
        # print complete traceback
        print(traceback.format_exc())
        print(application)
        # quit execution
        exit(1)
        return application

if __name__ == "__main__":
    applications = get_list_of_applications()
    # print(applications[0])
    # print any pdf links
    # for app in applications:
    #     if app['pdf_links']:
    #         print(f"application Name: {app['file_name']}")
    #         print(f"PDF Links:", app['pdf_links'])
    for app in applications:
        if app is None:
            continue
        application = get_application(app)
        if application is None:
            continue
        application = get_pdfs(application)
    # save to json file
    import json
    with open('applications.json', 'w') as f:
        json.dump(applications, f, indent=4)

# https://www.citywindsor.ca/residents/planning/land-development/development-applications/current-development-applications/4170-4190-sixth-concession-road