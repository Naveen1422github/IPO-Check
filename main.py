# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from io import StringIO

# # Base URL
# base_url = "https://www.chittorgarh.com"

# # Function to fetch and parse a URL
# def fetch_soup(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return BeautifulSoup(response.content, "html.parser")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching {url}: {e}")
#         return None

# # Function to extract IPO list from the main page
# def get_ipo_list(main_url):
#     soup = fetch_soup(main_url)
#     if not soup:
#         return []

#     tables = soup.find_all("table", {"class": "table"})
#     if len(tables) <= 1:
#         st.error("IPO table not found on the main page.")
#         return []

#     ipo_table = tables[1]  # Assuming the IPO table is the second table
#     ipo_list = []
#     for row in ipo_table.find("tbody").find_all("tr"):
#         link_tag = row.find("a")
#         if link_tag and link_tag.get("href"):
#             name = link_tag.text.strip()
#             full_link = base_url + link_tag["href"]
#             ipo_list.append({"Company Name": name, "Detail Link": full_link})
#     return ipo_list

# # Function to extract details from an IPO page
# def get_ipo_details(detail_url):
#     soup = fetch_soup(detail_url)
#     if not soup:
#         return {}

#     detail_tables = soup.find_all("table", {"class": "table"})
#     details = {}

#     # Extract retail shares offered
#     if len(detail_tables) > 2:
#         try:
#             details['Retail Shares Offered'] = pd.read_html(StringIO(str(detail_tables[2])))[0]
#         except Exception as e:
#             st.error(f"Error parsing retail shares offered table: {e}")

#     # Extract basis of allotment
#     if len(detail_tables) > 4:
#         try:
#             details['Basis of Allotment'] = pd.read_html(StringIO(str(detail_tables[4])))[0]
#         except Exception as e:
#             st.error(f"Error parsing basis of allotment table: {e}")

#     # Extract GMP data with error handling
#     gmp_tag = soup.find('a', title="IPO GMP")
#     if gmp_tag:
#         gmp_url = gmp_tag.get('href')
#         gmp_soup = fetch_soup(gmp_url)
#         if gmp_soup:
#             try:
#                 gmp_tables = gmp_soup.find_all("table", {"class": "table"})
#                 if gmp_tables:
#                     details['GMP Data'] = pd.read_html(StringIO(str(gmp_tables[0])))[0]
#             except Exception as e:
#                 st.error(f"Error parsing GMP data from {gmp_url}: {e}")

#     # Extract subscription data with error handling
#     subscription_tag = soup.find('a', title="IPO Live Subscription")
#     if subscription_tag:
#         subscription_url = base_url + subscription_tag.get('href')
#         subscription_soup = fetch_soup(subscription_url)
#         if subscription_soup:
#             try:
#                 subscription_tables = subscription_soup.find_all("table", {"class": "table"})
#                 if len(subscription_tables) > 1:
#                     details['Subscription Data'] = pd.read_html(StringIO(str(subscription_tables[1])))[0]
#                 else:
#                     st.warning(f"Subscription table not found at {subscription_url}")
#             except Exception as e:
#                 st.error(f"Error parsing subscription data from {subscription_url}: {e}")

#     return details

# # Streamlit app
# def main():
#     st.title("IPO Data Scraper")

#     main_url = f"{base_url}/"
#     ipo_list = get_ipo_list(main_url)

#     if not ipo_list:
#         st.warning("No IPOs found.")
#         return

#     for ipo in ipo_list:
#         st.header(ipo['Company Name'])
#         st.write(f"Detail Link: [Click here]({ipo['Detail Link']})")

#         details = get_ipo_details(ipo['Detail Link'])

#         # Filter and display retail shares offered
#         if 'Retail Shares Offered' in details:
#             retail_shares = details['Retail Shares Offered']
#             retail_row = retail_shares[retail_shares['Investor Category'].str.contains("Retail Shares Offered", na=False)]
#             st.subheader("Retail Shares Offered")
#             st.write(retail_row)

#         # Filter and display basis of allotment and listing date
#         if 'Basis of Allotment' in details:
#             basis = details['Basis of Allotment']
#             filtered_basis = basis[basis[0].isin(['Basis of Allotment', 'Listing Date'])]
#             st.subheader("Basis of Allotment and Listing Date")
#             st.write(filtered_basis)

#         # Display top 5 entries of GMP data
#         if 'GMP Data' in details:
#             gmp_data = details['GMP Data']
#             st.subheader("Top 5 GMP Data")
#             st.write(gmp_data.head(5))

#         # Display subscription data for Retail Individual
#         if 'Subscription Data' in details:
#             subscription_data = details['Subscription Data']
#             retail_subscription = subscription_data[subscription_data['Investor Category'].str.contains("Retail Individual", na=False)]
#             st.subheader("Retail Individual Subscription Data")
#             st.write(retail_subscription)

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# Base URL
base_url = "https://www.chittorgarh.com"

# Function to fetch and parse a URL
def fetch_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {url}: {e}")
        return None

# Function to extract IPO list from the main page
def get_ipo_list(main_url):
    soup = fetch_soup(main_url)
    if not soup:
        return []

    tables = soup.find_all("table", {"class": "table"})
    if len(tables) <= 1:
        st.error("IPO table not found on the main page.")
        return []

    ipo_table = tables[1]  # Assuming the IPO table is the second table
    ipo_list = []
    for row in ipo_table.find("tbody").find_all("tr"):
        td_elements = row.find_all('td') 

        if len(td_elements) >= 3:
            opening_date = td_elements[1].text.strip()
            closing_date = td_elements[2].text.strip()

        link_tag = row.find("a")
        if link_tag and link_tag.get("href"):
            name = link_tag.text.strip()
            full_link = base_url + link_tag["href"]
            ipo_list.append({"Company Name": name+ "  | Open " + opening_date + " | Close " + closing_date + " |", "Detail Link": full_link})
    return ipo_list

# Function to extract details from an IPO page
def get_ipo_details(detail_url):
    soup = fetch_soup(detail_url)
    if not soup:
        return {}

    detail_tables = soup.find_all("table", {"class": "table"})
    details = {}

    # Extract retail shares offered
    if len(detail_tables) > 2:
        try:
            details['Retail Shares Offered'] = pd.read_html(StringIO(str(detail_tables[2])))[0]
        except Exception as e:
            st.error(f"Error parsing retail shares offered table: {e}")

    # Extract basis of allotment
    if len(detail_tables) > 4:
        try:
            details['Basis of Allotment'] = pd.read_html(StringIO(str(detail_tables[4])))[0]
        except Exception as e:
            st.error(f"Error parsing basis of allotment table: {e}")

    # Extract GMP data with error handling
    gmp_tag = soup.find('a', title="IPO GMP")
    if gmp_tag:
        gmp_url = gmp_tag.get('href')
        gmp_soup = fetch_soup(gmp_url)
        if gmp_soup:
            try:
                gmp_tables = gmp_soup.find_all("table", {"class": "table"})
                if gmp_tables:
                    details['GMP Data'] = pd.read_html(StringIO(str(gmp_tables[0])))[0]
            except Exception as e:
                st.error(f"Error parsing GMP data from {gmp_url}: {e}")

    # Extract subscription data with error handling
    subscription_tag = soup.find('a', title="IPO Live Subscription")
    if subscription_tag:
        subscription_url = base_url + subscription_tag.get('href')
        subscription_soup = fetch_soup(subscription_url)
        if subscription_soup:
            try:
                subscription_tables = subscription_soup.find_all("table", {"class": "table"})
                if len(subscription_tables) > 1:
                    details['Subscription Data'] = pd.read_html(StringIO(str(subscription_tables[1])))[0]
                else:
                    st.warning(f"Subscription table not found at {subscription_url}")
            except Exception as e:
                st.error(f"Error parsing subscription data from {subscription_url}: {e}")

    return details

# Streamlit app
def main():
    st.title("IPO Data Scraper")

    # Display IPO list
    main_url = f"{base_url}/"
    ipo_list = get_ipo_list(main_url)

    if not ipo_list:
        st.warning("No IPOs found.")
        return

    # Dropdown to select IPO
    ipo_names = [ipo['Company Name'] for ipo in ipo_list]
    selected_ipo = st.selectbox("Select an IPO to view details:", ["Select"] + ipo_names)

    if selected_ipo == "Select":
        st.info("Please select an IPO from the dropdown.")
        return

    # Fetch details for the selected IPO
    selected_ipo_data = next((ipo for ipo in ipo_list if ipo['Company Name'] == selected_ipo), None)
    if selected_ipo_data:
        details = get_ipo_details(selected_ipo_data['Detail Link'])

        # Display top 5 entries of GMP data
        if 'GMP Data' in details:
            gmp_data = details['GMP Data']
            st.subheader("Top 5 GMP Data")
            st.write(gmp_data.head(5))

        # Filter and display retail shares offered
        if 'Retail Shares Offered' in details:
            retail_shares = details['Retail Shares Offered']
            retail_row = retail_shares[retail_shares['Investor Category'].str.contains("Retail Shares Offered", na=False)]
            st.subheader("Retail Shares Offered")
            st.write(retail_row)

          # Display subscription data for Retail Individual
        if 'Subscription Data' in details:
            subscription_data = details['Subscription Data']
            retail_subscription = subscription_data[subscription_data['Investor Category'].str.contains("Retail Individual", na=False)]
            st.subheader("Retail Individual Subscription Data")
            st.write(retail_subscription)

        # Filter and display basis of allotment and listing date
        if 'Basis of Allotment' in details:
            basis = details['Basis of Allotment']
            filtered_basis = basis[basis[0].isin(['Basis of Allotment', 'Listing Date'])]
            st.subheader("Basis of Allotment and Listing Date")
            st.write(filtered_basis)


if __name__ == "__main__":
    main()

# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # Base URL
# base_url = "https://www.chittorgarh.com"

# # Function to fetch and parse a URL
# def fetch_soup(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return BeautifulSoup(response.content, "html.parser")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching {url}: {e}")
#         return None

# # Function to extract IPO list from the main page
# def get_ipo_list(main_url):
#     soup = fetch_soup(main_url)
#     if not soup:
#         return []

#     tables = soup.find_all("table", {"class": "table"})
#     if len(tables) <= 1:
#         st.error("IPO table not found on the main page.")
#         return []

#     ipo_table = tables[1]  # Assuming the IPO table is the second table
#     ipo_list = []
#     for row in ipo_table.find("tbody").find_all("tr"):
#         link_tag = row.find("a")
#         if link_tag and link_tag.get("href"):
#             name = link_tag.text.strip()
#             full_link = base_url + link_tag["href"]
#             ipo_list.append({"Company Name": name, "Detail Link": full_link})
#     return ipo_list

# # Function to extract details from an IPO page
# def get_ipo_details(detail_url):
#     soup = fetch_soup(detail_url)
#     if not soup:
#         return {}

#     detail_tables = soup.find_all("table", {"class": "table"})
#     details = {}

#     # Extract retail shares offered
#     if len(detail_tables) > 2:
#         try:
#             details['Retail Shares Offered'] = pd.read_html(str(detail_tables[2]))[0]
#         except Exception as e:
#             st.error(f"Error parsing retail shares offered table: {e}")

#     # Extract basis of allotment
#     if len(detail_tables) > 4:
#         try:
#             details['Basis of Allotment'] = pd.read_html(str(detail_tables[4]))[0]
#         except Exception as e:
#             st.error(f"Error parsing basis of allotment table: {e}")

#     # Extract GMP data with error handling
#     gmp_tag = soup.find('a', title="IPO GMP")
#     if gmp_tag:
#         gmp_url = base_url + gmp_tag.get('href')
#         gmp_soup = fetch_soup(gmp_url)
#         if gmp_soup:
#             try:
#                 gmp_tables = gmp_soup.find_all("table", {"class": "table"})
#                 if gmp_tables:
#                     details['GMP Data'] = pd.read_html(str(gmp_tables[0]))[0]
#             except Exception as e:
#                 st.error(f"Error parsing GMP data from {gmp_url}: {e}")

#     # Extract subscription data with error handling
#     subscription_tag = soup.find('a', title="IPO Live Subscription")
#     if subscription_tag:
#         subscription_url = base_url + subscription_tag.get('href')
#         subscription_soup = fetch_soup(subscription_url)
#         if subscription_soup:
#             try:
#                 subscription_tables = subscription_soup.find_all("table", {"class": "table"})
#                 if len(subscription_tables) > 1:
#                     details['Subscription Data'] = pd.read_html(str(subscription_tables[1]))[0]
#                 else:
#                     st.warning(f"Subscription table not found at {subscription_url}")
#             except Exception as e:
#                 st.error(f"Error parsing subscription data from {subscription_url}: {e}")

#     return details

# # Streamlit app
# def main():
#     st.title("IPO Data Scraper")

#     # Display IPO list
#     main_url = f"{base_url}/"
#     ipo_list = get_ipo_list(main_url)

#     if not ipo_list:
#         st.warning("No IPOs found.")
#         return

#     # Show IPOs in a table with clickable buttons
#     st.subheader("IPO List")
#     if "selected_ipo" not in st.session_state:
#         st.session_state.selected_ipo = None

#     for ipo in ipo_list:
#         if st.button(f"View Details: {ipo['Company Name']}"):
#             st.session_state.selected_ipo = ipo

#     # Display details for the selected IPO
#     if st.session_state.selected_ipo:
#         selected_ipo = st.session_state.selected_ipo
#         st.header(f"Details for {selected_ipo['Company Name']}")
#         details = get_ipo_details(selected_ipo['Detail Link'])

#         # Display Retail Shares Offered
#         if 'Retail Shares Offered' in details:
#             st.subheader("Retail Shares Offered")
#             st.write(details['Retail Shares Offered'])

#         # Display Basis of Allotment and Listing Date
#         if 'Basis of Allotment' in details:
#             st.subheader("Basis of Allotment and Listing Date")
#             st.write(details['Basis of Allotment'])

#         # Display GMP Data
#         if 'GMP Data' in details:
#             st.subheader("GMP Data")
#             st.write(details['GMP Data'].head(5))

#         # Display Subscription Data
#         if 'Subscription Data' in details:
#             st.subheader("Retail Individual Subscription Data")
#             st.write(details['Subscription Data'])

# if __name__ == "__main__":
#     main()
