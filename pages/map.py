import streamlit as st
import requests
import io
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Map", page_icon="️🗺")

st.title("🗺 Map")

hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
st.sidebar.page_link("main.py", label="🔥 Home")
st.sidebar.page_link("pages/map.py", label="🗺️ Map")
st.sidebar.page_link("pages/data.py", label="📊 Data")
st.sidebar.page_link("pages/info.py", label="📜 Info")
st.sidebar.page_link("pages/chatbot.py", label="💬 Chatbot")
st.sidebar.page_link("pages/about.py", label="🔍 About Us")

FIRMS_KEY = st.secrets["FIRMS_KEY"]
url = "https://firms.modaps.eosdis.nasa.gov/api"

countries = {'ABW': 'Aruba', 'AFG': 'Afghanistan', 'AGO': 'Angola', 'AIA': 'Anguilla', 'ALA': 'Aland Islands', 'ALB': 'Albania', 'AND': 'Andorra', 'ARE': 'United Arab Emirates', 'ARG': 'Argentina', 'ARM': 'Armenia', 'ASM': 'American Samoa', 'ATA': 'Antarctica', 'ATF': 'French Southern and Antarctic Lands', 'ATG': 'Antigua and Barbuda', 'AUS': 'Australia', 'AUT': 'Austria', 'AZE': 'Azerbaijan', 'BDI': 'Burundi', 'BEL': 'Belgium', 'BEN': 'Benin', 'BFA': 'Burkina Faso', 'BGD': 'Bangladesh', 'BGR': 'Bulgaria', 'BHR': 'Bahrain', 'BHS': 'Bahamas', 'BIH': 'Bosnia and Herzegovina', 'BLM': 'Saint-Barthelemy', 'BLR': 'Belarus', 'BLZ': 'Belize', 'BMU': 'Bermuda', 'BOL': 'Bolivia', 'BRA': 'Brazil', 'BRB': 'Barbados', 'BRN': 'Brunei Darussalam', 'BTN': 'Bhutan', 'BWA': 'Botswana', 'CAF': 'Central African Republic', 'CAN': 'Canada', 'CHE': 'Switzerland', 'CHL': 'Chile', 'CHN': 'China', 'CIV': "Cote d'Ivoire", 'CMR': 'Cameroon', 'COD': 'Democratic Republic of the Congo', 'COG': 'Republic of Congo', 'COK': 'Cook Islands', 'COL': 'Colombia', 'COM': 'Comoros', 'CPV': 'Cape Verde', 'CRI': 'Costa Rica', 'CUB': 'Cuba', 'CUW': 'Curacao', 'CYM': 'Cayman Islands', 'CYP': 'Cyprus', 'CZE': 'Czech Republic', 'DEU': 'Germany', 'DJI': 'Djibouti', 'DMA': 'Dominica', 'DNK': 'Denmark', 'DOM': 'Dominican Republic', 'DZA': 'Algeria', 'ECU': 'Ecuador', 'EGY': 'Egypt', 'ERI': 'Eritrea', 'ESP': 'Spain', 'EST': 'Estonia', 'ETH': 'Ethiopia', 'FIN': 'Finland', 'FJI': 'Fiji', 'FLK': 'Falkland Islands', 'FRA': 'France', 'FRO': 'Faeroe Islands', 'FSM': 'Federated States of Micronesia', 'GAB': 'Gabon', 'GBR': 'United Kingdom', 'GEO': 'Georgia', 'GGY': 'Guernsey', 'GHA': 'Ghana', 'GIB': 'Gibraltar', 'GIN': 'Guinea', 'GLP': 'Guadeloupe', 'GMB': 'The Gambia', 'GNB': 'Guinea-Bissau', 'GNQ': 'Equatorial Guinea', 'GRC': 'Greece', 'GRD': 'Grenada', 'GRL': 'Greenland', 'GTM': 'Guatemala', 'GUF': 'French Guiana', 'GUM': 'Guam', 'GUY': 'Guyana', 'HKG': 'Hong Kong', 'HMD': 'Heard I. and McDonald Islands', 'HND': 'Honduras', 'HRV': 'Croatia', 'HTI': 'Haiti', 'HUN': 'Hungary', 'IDN': 'Indonesia', 'IMN': 'Isle of Man', 'IND': 'India', 'IOT': 'British Indian Ocean Territory', 'IRL': 'Ireland', 'IRN': 'Iran', 'IRQ': 'Iraq', 'ISL': 'Iceland', 'ISR': 'Israel', 'ITA': 'Italy', 'JAM': 'Jamaica', 'JEY': 'Jersey', 'JOR': 'Jordan', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan', 'KHM': 'Cambodia', 'KIR': 'Kiribati', 'KNA': 'Saint Kitts and Nevis', 'KOR': 'Republic of Korea', 'KOS': 'Kosovo', 'KWT': 'Kuwait', 'LAO': 'Lao PDR', 'LBN': 'Lebanon', 'LBR': 'Liberia', 'LBY': 'Libya', 'LCA': 'Saint Lucia', 'LIE': 'Liechtenstein', 'LKA': 'Sri Lanka', 'LSO': 'Lesotho', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia', 'MAC': 'Macao', 'MAF': 'Saint-Martin', 'MAR': 'Morocco', 'MCO': 'Monaco', 'MDA': 'Moldova', 'MDG': 'Madagascar', 'MDV': 'Maldives', 'MEX': 'Mexico', 'MHL': 'Marshall Islands', 'MKD': 'Macedonia, Former Yugoslav Republic of', 'MLI': 'Mali', 'MLT': 'Malta', 'MMR': 'Myanmar', 'MNE': 'Montenegro', 'MNG': 'Mongolia', 'MNP': 'Northern Mariana Islands', 'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MSR': 'Montserrat', 'MTQ': 'Martinique', 'MUS': 'Mauritius', 'MWI': 'Malawi', 'MYS': 'Malaysia', 'MYT': 'Mayotte', 'NAM': 'Namibia', 'NCL': 'New Caledonia', 'NER': 'Niger', 'NFK': 'Norfolk Island', 'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NIU': 'Niue', 'NLD': 'Netherlands', 'NOR': 'Norway', 'NPL': 'Nepal', 'NRU': 'Nauru', 'NZL': 'New Zealand', 'OMN': 'Oman', 'PAK': 'Pakistan', 'PAN': 'Panama', 'PCN': 'Pitcairn Islands', 'PER': 'Peru', 'PHL': 'Philippines', 'PLW': 'Palau', 'PNG': 'Papua New Guinea', 'POL': 'Poland', 'PRI': 'Puerto Rico', 'PRK': 'Dem. Rep. Korea', 'PRT': 'Portugal', 'PRY': 'Paraguay', 'PSE': 'Palestine', 'PYF': 'French Polynesia', 'QAT': 'Qatar', 'REU': 'Reunion', 'ROU': 'Romania', 'RUS': 'Russian Federation', 'RWA': 'Rwanda', 'SAU': 'Saudi Arabia', 'SDN': 'Sudan', 'SEN': 'Senegal', 'SGP': 'Singapore', 'SGS': 'South Georgia and South Sandwich Islands', 'SHN': 'Saint Helena', 'SJM': 'Svalbard and Jan Mayen', 'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone', 'SLV': 'El Salvador', 'SMR': 'San Marino', 'SOM': 'Somalia', 'SPM': 'Saint Pierre and Miquelon', 'SRB': 'Serbia', 'SSD': 'South Sudan', 'STP': 'Sao Tome and Principe', 'SUR': 'Suriname', 'SVK': 'Slovakia', 'SVN': 'Slovenia', 'SWE': 'Sweden', 'SWZ': 'Swaziland', 'SXM': 'Sint Maarten', 'SYC': 'Seychelles', 'SYR': 'Syria', 'TCA': 'Turks and Caicos Islands', 'TCD': 'Chad', 'TGO': 'Togo', 'THA': 'Thailand', 'TJK': 'Tajikistan', 'TKM': 'Turkmenistan', 'TLS': 'Timor-Leste', 'TON': 'Tonga', 'TTO': 'Trinidad and Tobago', 'TUN': 'Tunisia', 'TUR': 'Turkey', 'TUV': 'Tuvalu', 'TWN': 'Taiwan', 'TZA': 'Tanzania', 'UGA': 'Uganda', 'UKR': 'Ukraine', 'UMI': 'United States Minor Outlying Islands', 'URY': 'Uruguay', 'USA': 'United States', 'UZB': 'Uzbekistan', 'VAT': 'Vatican', 'VCT': 'Saint Vincent and the Grenadines', 'VEN': 'Venezuela', 'VGB': 'British Virgin Islands', 'VIR': 'United States Virgin Islands', 'VNM': 'Vietnam', 'VUT': 'Vanuatu', 'WLF': 'Wallis and Futuna Islands', 'WSM': 'Samoa', 'YEM': 'Yemen', 'ZAF': 'South Africa', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe'}

country = st.selectbox("Select a country", list(countries.values()))

if st.checkbox("Select whole world"):
    country = "the world"

day_range = st.slider("Select a day range", 1, 10, 1)

@st.cache_data
def get_firms_data(c, days):
    if c == "the world":
        response = requests.get(f"{url}/area/csv/{FIRMS_KEY}/VIIRS_SNPP_NRT/world/{days}")

        if response.status_code == 200:
            csv_data = response.text
            df = pd.read_csv(io.StringIO(csv_data))
            return df
        else:
            st.error("Failed to fetch data. Check API key or try again later.")
            return pd.DataFrame()
    else:
        code = list(countries.keys())[list(countries.values()).index(c)]
        response = requests.get(f"{url}/country/csv/{FIRMS_KEY}/VIIRS_SNPP_NRT/{code}/{days}")

        if response.status_code == 200:
            csv_data = response.text
            df = pd.read_csv(io.StringIO(csv_data))
            return df
        else:
            st.error("Failed to fetch data. Check API key or try again later.")
            return pd.DataFrame()

df = get_firms_data(country, day_range)

if df.empty:
    st.warning("No data available for the selected country and day range.")
else:
    if day_range == 1:
        st.markdown(f"<p style='text-align: center;'>FIRMS data for {country}, for the last day.</p>",
                    unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align: center;'>FIRMS data for {country}, for the last {str(day_range)} days.</p>",
                    unsafe_allow_html=True)
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state={"latitude": 0, "longitude": 0, "zoom": 1, "pitch": 30},
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    get_weight="brightness",
                    opacity=0.8,
                    cell_size=100000,
                    # radius scale by zoom
                    get_radius=10000,
                    get_color= [255, 0, 0],
                )
            ],
        )
    )

st.markdown(
    """
    Each red dot indicates an active fire. The brightness of the dot represents the intensity of the fire.
    
    
    **Note:** FIRMS data is provided by [NASA's Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/).
    """
)
