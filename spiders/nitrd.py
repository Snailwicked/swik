import requests


import requests
from lxml import etree
import time
from spiders.fanyi import translation

import pymysql
class DbToMysql(object):

    def __init__(self):
        self.con = pymysql.connect(
            host="180.97.15.173",
            user="wzh",
            password="wzh234287",
            db="bgnet",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.con.close()

    def save_one_data(self,datas):
        sql = "INSERT INTO `bgnet_intelligence` (person_id,collector_id,user_id,title,translat_title,hand_translat_title,type_way,type,translat_type,hand_translat_type,original_link,translat_original_link,hand_translat_original_link,web_site,translat_web_site,hand_translat_web_site,country,translat_country,hand_translat_country,content,translat_content,hand_translat_content,status,create_time,update_time,is_del,longitude,latitude,remark,mark) " \
              "VALUES ('0', NULL, NULL,'{0}' ,'{1}', NULL, 0, 0, NULL, NULL,'{2}', NULL, NULL, '{3}', NULL, NULL, '{4}', NULL, NULL, '{5}', '{6}', NULL, 0, '{7}', NULL, 0, '{8}', '{9}', NULL, NULL)".format(str(datas['title']),str(datas['translat_title']),datas['original_link'],datas['web_site'],datas['country'],str(datas['content']),str(datas['translat_content']),datas['create_time'],datas['longitude'],datas['latitude'])
        print(sql)
        try:
            with self.con.cursor() as cursor:
                print(cursor.execute(sql))
                self.con.commit()
        except Exception as e:
            return -1
        # finally:
        #     self.close()

dbsql = DbToMysql()



# headers = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Referer': 'https://www.nitrd.gov/news/newsroom.aspx',
#     'X-Requested-With': 'XMLHttpRequest',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#     'Sec-Fetch-Mode': 'cors',
# }
#
# params = (
#     ('_', '1570591952492'),
# )
# response = requests.get('https://www.nitrd.gov/news/data/newsarchive.txt', headers=headers, params=params)


cookies = {
    '_ga': 'GA1.2.1192070446.1569492061',
    '__utmc': '239080220',
    '__utmz': '239080220.1570591431.4.4.utmcsr=localhost:63342|utmccn=(referral)|utmcmd=referral|utmcct=/swik/webapplication/templates/index.html',
    '_gid': 'GA1.2.2106858737.1570591431',
    '__utma': '239080220.1192070446.1569492061.1570591431.1570601055.5',
    '__utmt': '1',
    '__utmb': '239080220.4.10.1570601055',
}

headers = {
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.nitrd.gov/events/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('_', '1570601980870'),
)

response = requests.get('https://www.nitrd.gov/events/data/events.txt', headers=headers, params=params, cookies=cookies)

from dateutil.parser import parse as date_parser

import json

result =  [
 {
   "date": "August 29, 2019",
   "PostTitle": "Artificial Intelligence & Wireless Spectrum: Opportunities and Challenges",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=Artificial-Intelligence-Wireless-Spectrum",
   "PostDescription": "Agencies of the NITRD Wireless Spectrum Research & Development (WSRD) Interagency Working Group (IWG) are conducting a workshop focused on the application of existing and new AI techniques in the wireless spectrum context. Wireless spectrum has been managed and utilized over many decades through a complex regulatory framework and a patchwork of policies. The current manual process of assessing spectrum needs is a growing problem due to the high-level of interdependencies in the spectrum domain. Existing and emerging methods for allocating spectrum are often driven by small studies that suffer from inherent biases. As a result, spectrum policies and usage are often sub-optimal and rigid, preventing efficient use of wireless spectrum. As the U.S. moves forward as a leader in 5G technologies and deployment, it critically needs fast and efficient wireless spectrum policy creation, adoption, and management of wireless spectrum. Artificial Intelligence techniques have been successfully applied in many other domains, such as image classification or autonomous navigation, which previously relied on either a model-based approaches or a vital human-in-the-loop element. Despite the differences between multimedia and RF signals, researchers have shown that the judicious integration of Artificial Intelligence techniques can provide similar gains in the wireless spectrum domain.",
   "coverimage": "https://www.nitrd.gov/images/wsrd11.gif",
   "Organizer": "Wireless Spectrum Research & Development (WSRD) Interagency Working Group (IWG)",
   "year": "2019"
 },
 {
   "date": "August 6, 2019",
   "PostTitle": "Future Computing Community of Interest Meeting",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=FC-COI-2019",
   "PostDescription": "The Future Computing (FC) Community of Interest Meeting will explore the computing landscape for the coming decade and beyond, along with emerging and future application drivers, to inform agencies and to identify potential opportunities as well as gaps. It will also examine new software concepts needed for the effective use of advances that come with the future computing systems to ensure that the federal government is poised to respond to unanticipated challenges and opportunities.",
   "coverimage": "https://www.nitrd.gov/images/FC-COI-2019.gif",
   "Organizer": "High End Computing (HEC)\nInteragency Working Group (IWG)",
   "year": "2019"
 },
 {
   "date": "July 17, 2019",
   "PostTitle": "Federal Listening Session on Interoperability of Medical Devices, Data, and Platforms to Enhance Patient Care",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=Medical-Device-Interoperability-2019",
   "PostDescription": "Medical devices, electronic health records (EHRs) and the data generated by and stored in these systems are essential to the practice and advancement of modern medicine and healthcare. If interoperability is enabled between these devices and systems, patient care can be improved using connected and autonomous applications, automated error detection and more rapid development cycles. Achieving safe interoperability will require the system of care delivery to be properly engineered to address both the desired (e.g. new apps and safety interlocks) and undesired (e.g. unsafe interference) emergent properties. Interoperability needs to be engineered for safety.",
   "coverimage": "https://www.nitrd.gov/images/Medical-Interoperability-2019.gif",
   "Organizer": "Health Information Technology Research and Development (Health IT R&D)\nInteragency Working Group (IWG)",
   "year": "2019"
 },
 {
   "date": "June 6, 2019",
   "PostTitle": "Artificial Intelligence and Cybersecurity Workshop",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=AI-CYBER-2019",
   "PostDescription": "The NSTC's NITRD Subcommittee, in collaboration with the NSTC's MLAI Subcommittee, and through the sponsorship of the NSTC's Special Cyber Operations Research & Engineering (SCORE) will hold a workshop to assess the key research challenges and opportunities at the intersection of cybersecurity and artificial intelligence (AI). The NSTC, led by the White House Office of Science and Technology Policy, is the principal means within the Executive Branch to coordinate science and technology policy across the diverse Federal R&D enterprise. The workshop will discuss current and future research activities in this space, including potential research gaps to help the federal government plan future R&D in this area.",
   "coverimage": "https://www.nitrd.gov/images/ai.gif",
   "Organizer": "National Science and Technology Council's (NSTC) Networking and Information Technology Research and Development (NITRD) Subcommittee; NSTC's Machine Learning and Artificial Intelligence (MLAI) Subcommittee",
   "year": "2019"
 },
 {
   "date": "July 3, 2019",
   "PostTitle": "Speaker Series on the Scientific Data Life Cycle",
   "ResourceLink": "https://www.nitrd.gov/news/2019-MAGIC-Data-Life-Cycle-Series.aspx",
   "PostDescription": "Middleware and Grid Interagency Coordination Team (MAGIC) is conducting a series of public meetings to examine different aspects and interconnections of the scientific data life cycle (e.g., gathering, triaging, analyzing, archiving and reusing data). This multi-session series is examining issues such as provenance, verification/quality assurance, tools and services involved in managing complex scientific infrastructure and tools. The issues involved in the data life cycle cuts across scientific domains and need to be addressed to enable cutting edge R&D efforts.",
   "coverimage": "https://www.nitrd.gov/news/images/Data-Life-Cycle.gif",
   "Organizer": "Middleware and Grid Interagency Coordination Team (MAGIC)",
   "year": "2019"
 },
 {
   "date": "November 13, 2018",
   "PostTitle": "SC18 Birds of a Feather: 'What the heck is HEC?'",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=SC18-Birds-of-Feather",
   "PostDescription": "Federal High-End Computing (HEC) is evolving in response to the needs of the HEC community and advancing technological landscape, including rapidly changing architecture, anticipated end to Moore's Law, facing the challenges associated with the data tsunami, and scaling software to newer and more complex platforms. Consequently, the HEC environment is more complex than ever and these factors stress the HEC community in every way. This BoF will provide an overview of the current and emerging federal HEC efforts and seeks to have a candid discussion with the HEC community on how it can be collaboratively cultivated to serve tomorrow's challenges.",
   "coverimage": "https://www.nitrd.gov/images/SC18-BOF.gif",
   "Organizer": "High End Computing (HEC)\nInteragency Working Group (IWG)\n",
   "year": "2018"
 },
 {
   "date": "October 30, 2018",
   "PostTitle": "The Convergence of High Performance Computing, Big Data, and Machine Learning",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=HPC-BD-Convergence",
   "PostDescription": "An evolving scientific and technological landscape requires computing platforms for HPC, BD, and ML to be more integrated, but convergence can strain traditional paradigms of computing and software development. Science-based simulation increasingly relies on embedded machine learning models to interpret results from massive outputs as well as to steer computations. Likewise, science-based models are being combined with data-driven models to represent complex systems and phenomena. This process is not seamless and there are numerous challenges including the need for: innovative distributed computing and workflow architectures, new software capabilities that incorporate simulation and analytics, and advanced workforce training. This workshop will bring together experts from the Federal agencies, academia and the private sector to discuss these challenges and opportunities, facilitate information sharing and collaboration, and identify research needs. The National Strategic Computing Initiative (NSCI) and the national Big Data R&D Initiative have highlighted the rapid development of hardware and software for extreme-scale and big data computing, while the National Artificial Intelligence Research and Development Plan, and other government Artificial Intelligence and ML initiatives, have highlighted the ubiquitous use of ML and related techniques across a variety of domains.",
   "coverimage": "https://www.nitrd.gov/images/HPC-BD-2018.png",
   "Organizer": "High End Computing (HEC)\nInteragency Working Group (IWG); Big Data Interagency Working Group (IWG)",
   "year": "2018"
 },
 {
   "date": "September 13, 2018",
   "PostTitle": "Security from a Wireless Spectrum Perspective: Technology Innovation and Policy Research Needs",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=WSRD-Workshop-X",
   "PostDescription": "Communications over the wireless medium pose security threats that are yet to be fully understood. It is currently possible for attackers that are within the wireless range to hijack or intercept an unprotected connection without being detected. With the advent of sophisticated cognitive radios, and wireless devices, and applications such as the Internet of Things (IOT), drones, small satellites, driverless cars, and wireless healthcare devices, the security threat of attacks occurring is rapidly increasing. As 5G, low-power wide area networks, and other emerging systems are deployed, security issues are expected to increase unless new protective technologies and policies are in place.",
   "coverimage": "https://www.nitrd.gov/images/wsrdx.jpg",
   "Organizer": "Wireless Spectrum Research & Development (WSRD) Interagency Working Group (IWG)",
   "year": "2018"
 },
 {
   "date": "April 4, 2018",
   "PostTitle": "MAGIC Containerization and Virtualization Speaker Series",
   "ResourceLink": "https://nitrd.gov/news/containerization_virtualization.aspx",
   "PostDescription": "MAGIC is conducting an in-depth examination of the impact of and opportunities for virtualization and containerization technologies and services on computing ecosystems. The effort was divided into 4 sessions: (1) various packages that are in common use; (2) adoption and usage of container technologies in science communities; (3) adoption and deployment by resource providers; and (4) discussion of research and operational deployment challenges.",
   "coverimage": "https://www.nitrd.gov/news/images/Virtualization.jpg",
   "Organizer": "Middleware and Grid Interagency Coordination Team (MAGIC)",
   "year": "2018"
 },
 {
   "date": "November 15, 2017",
   "PostTitle": "Supercomputing (SC) 2017 Panel - Blurring the Lines: High-End Computing and Data Science",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/images/2/2f/SC17Panel_Blurring_the_Lines.pdf",
   "PostDescription": "High-End Computing (HEC) encompasses both massive computational and big data capability to solve computational problems of significant importance that are beyond the capability of small- to medium-scale systems. Data science includes large-scale data analytics and visualization across multiple scales of data from a multitude of sources. Increasingly on-demand and real-time data intensive computing, enabling real-time analysis of simulations, data-intensive experiments and streaming observations, is pushing the boundaries of computing and resulting in a convergence of traditional HEC and newer cloud computing environments. This panel will explore challenges and opportunities at the intersection of high-end computing and data science.",
   "coverimage": "https://www.nitrd.gov/nitrdgroups/skins/vector/images/hec.jpg",
   "Organizer": "High End Computing (HEC) Interagency Working Group (IWG)",
   "year": "2017"
 },
 {
   "date": "October 4, 2017",
   "PostTitle": "Open Knowledge Network: Enabling the Community to Build the Network",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=Open_Knowledge_Network",
   "PostDescription": "The vision of OKN is to create an open knowledge graph of all known entities and their relationships, ranging from the macro (e.g., have there been unusual clusters of earthquakes in the US in the past six months?) to the micro (e.g., what is the best combination of chemotherapeutic drugs for a 56 y/o female with stage 3 brain cancer.) OKN is meant to be an inclusive, open, community activity resulting in a knowledge infrastructure that could facilitate and empower a host of applications and open new research avenues including how to create trustworthy knowledge networks/graphs. A workshop took place in October 2017 at NIH. This workshop examined current OKN-related projects within Federal Agencies, how those projects can collaborate with private sector efforts, and potential next steps. The workshop focused on particular domains, and discuss how to enable an open contributing community. The presentations are available below.",
   "coverimage": "https://www.nitrd.gov/news/images/Open-Knowledge-Network-Workshop-Report-2018-slide.gif",
   "Organizer": "Big Data Interagency Working Group (IWG)",
   "year": "2017"
 },
 {
   "date": "September 18, 2017",
   "PostTitle": "Operationalizing Software-Defined Networks",
   "ResourceLink": "https://www.nitrd.gov/nitrdgroups/index.php?title=OperationalizingSDN",
   "PostDescription": "The Large Scale Networking (LSN) Workshop on Operationalizing SDN was held from September 18 until September 20 in Washington, D.C. The workshop is in sequel to two previous workshops in 2013 and 2015, with the purpose to invite participants from the academia, industry, open source software communities, and government agencies to discuss the current state and forward pathways for the realization of an open, innovative, multi-domain and inter-operable SDN as an operational infrastructure. The workshop intends to facilitate an objective and constructive dialogue among different SDN stakeholder communities. It will provide input for LSN to identify opportunities and strategies towards the next important milestones for operational SDN. This workshop was co-organized by the LSN IWG and Clemson University (NSF Award CNS-1747856).",
   "coverimage": "https://www.nitrd.gov/nitrdgroups/skins/vector/images/lsn.jpg",
   "Organizer": "Large Scale Networking (LSN)\nInteragency Working Group (IWG)",
   "year": "2017"
 }]
for item in result:
    # if item.get("year") == "2019":
    data = {}
    try:
        html = requests.get(item.get("ResourceLink")).text
        html_tree = etree.HTML(html)
    except:
        continue
    data["title"] = str(item.get("PostTitle")).replace("'", "").replace("\"", "")
    data["translat_title"] = translation(data["title"])
    timeArray = time.localtime(int(time.mktime(
        date_parser(str(item.get("date")+" 00:00:00")).timetuple())))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    data["create_time"] = otherStyleTime
    data["content"] = str(item.get("PostDescription")).replace("'","").replace("\"","")

    try:
        data["translat_content"] = translation(data["content"])
    except:
        data["translat_content"] = ""

    data["country"] = "美国"
    data["original_link"] = item.get("ResourceLink")
    data["longitude"] = 138.250000
    data["web_site"] = "总统科技顾问委员会"
    data["latitude"] = 36.204824
    print(data)

    dbsql.save_one_data(data)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.nitrd.gov/events/data/events.txt?_=1570601980870', headers=headers, cookies=cookies)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.nitrd.gov/news/data/newsarchive.txt?_=1570591952492', headers=headers)
