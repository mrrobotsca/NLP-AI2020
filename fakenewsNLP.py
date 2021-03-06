import requests
from bs4 import BeautifulSoup
import pickle
from os import path

#This fonction will only work to https://www.poynter.org/ website structure.
def url_to_fakenews(url):
    '''Returns transcript data specifically from scrapsfromtheloft.com.'''
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    text = [s  for div in soup.select('.post-container .entry-title') for s in div.stripped_strings]
    data = [s for div in soup.select('.post-container .entry-content__text') for s in div.stripped_strings]
    return text

def url_to_data(url):
    '''Returns transcript data specifically from scrapsfromtheloft.com.'''
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    data = [s for div in soup.select('.post-container .entry-content__text') for s in div.stripped_strings]
    return data

# URLs of transcripts in scope
urls = ['https://www.poynter.org/ifcn-covid-19-misinformation/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/2/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/3/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/4/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/5/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/6/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/7/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/8/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/9/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0',
        'https://www.poynter.org/ifcn-covid-19-misinformation/page/10/?covid_countries=0&covid_rating=51174&covid_fact_checkers=0#038;covid_rating=51174&covid_fact_checkers=0']

# # Actually request transcripts (takes a few minutes to run)
# fakenews = [url_to_fakenews(u) for u in urls]
# data = [url_to_data(u) for u in urls]



data=[['Fact-Checked by: FactCrescendo', '2020/06/11 | India', 'Fact-Checked by: Maldita.es', '2020/06/11 | Spain', 'Fact-Checked by: Maldita.es', '2020/06/11 | Spain, Mexico', 'Fact-Checked by: PesaCheck', '2020/06/10 | Kenya', 'Fact-Checked by: Vishvas News', '2020/06/10 | India', 'Fact-Checked by: Vishvas News', '2020/06/10 | India', 'Fact-Checked by: FactCrescendo', '2020/06/10 | Sri Lanka', 'Fact-Checked by: FactCrescendo', '2020/06/10 | Sri Lanka', 'Fact-Checked by: Maldita.es', '2020/06/10 | Spain', 'Fact-Checked by: PesaCheck', '2020/06/10 | Tanzania', 'Fact-Checked by: TEMPO', '2020/06/09 | Indonesia', 'Fact-Checked by: Maldita.es', '2020/06/09 | Spain, India', 'Fact-Checked by: TEMPO', '2020/06/09 | Indonesia', 'Fact-Checked by: Vishvas News', '2020/06/09 | India', 'Fact-Checked by: TEMPO', '2020/06/09 | Indonesia'], ['Fact-Checked by: Agência Lupa', '2020/06/09 | Brazil', 'Fact-Checked by: Agência Lupa', '2020/06/09 | Brazil', 'Fact-Checked by: FactCrescendo', '2020/06/09 | India', 'Fact-Checked by: Agência Lupa', '2020/06/09 | Brazil', 'Fact-Checked by: FactCrescendo', '2020/06/09 | India', 'Fact-Checked by: Agência Lupa', '2020/06/09 | Brazil', 'Fact-Checked by: Facta', '2020/06/09 | Italy', 'Fact-Checked by: PesaCheck', '2020/06/09 | Uganda', 'Fact-Checked by: Maldita.es', '2020/06/09 | Spain', 'Fact-Checked by: PesaCheck', '2020/06/09 | Burundi', 'Fact-Checked by: Chequeado', '2020/06/08 | Argentina', 'Fact-Checked by: Facta', '2020/06/08 | Italy', 'Fact-Checked by: Vistinomer', '2020/06/08 | North Macedonia', 'Fact-Checked by: Maldita.es', '2020/06/08 | Spain', 'Fact-Checked by: Vishvas News', '2020/06/08 | India'], ['Fact-Checked by: Agência Lupa', '2020/06/08 | Brazil', 'Fact-Checked by: Agência Lupa', '2020/06/08 | Brazil', 'Fact-Checked by: Agência Lupa', '2020/06/08 | Brazil', 'Fact-Checked by: Maldita.es', '2020/06/08 | Spain', 'Fact-Checked by: FactCrescendo', '2020/06/08 | India', 'Fact-Checked by: Chequeado', '2020/06/08 | Argentina', 'Fact-Checked by: Vistinomer', '2020/06/06 | North Macedonia', 'Fact-Checked by: La Silla Vacía', '2020/06/05 | Colombia', 'Fact-Checked by: Vishvas News', '2020/06/05 | India', 'Fact-Checked by: Facta', '2020/06/05 | Italy', 'Fact-Checked by: Agência Lupa', '2020/06/05 | Brazil', 'Fact-Checked by: Agência Lupa', '2020/06/05 | Brazil', 'Fact-Checked by: Maldita.es', '2020/06/05 | Spain, Canada', 'Fact-Checked by: Estadão Verifica', '2020/06/05 | Brazil', 'Fact-Checked by: Estadão Verifica', '2020/06/05 | Brazil'], ['Fact-Checked by: Estadão Verifica', '2020/06/05 | Brazil', 'Fact-Checked by: Poligrafo', '2020/06/05 | Portugal', 'Fact-Checked by: PesaCheck', '2020/06/05 | Mali', 'Fact-Checked by: Facta', '2020/06/04 | Italy', 'Fact-Checked by: Maldita.es', '2020/06/04 | Spain', 'Fact-Checked by: TEMPO', '2020/06/04 | Indonesia', 'Fact-Checked by: Agência Lupa', '2020/06/04 | Brazil', 'Fact-Checked by: Agência Lupa', '2020/06/04 | Brazil', 'Fact-Checked by: Chequeado', '2020/06/04 | Argentina, Italy', 'Fact-Checked by: Chequeado', '2020/06/04 | Argentina, Spain, Venezuela, Bolivia', 'Fact-Checked by: Colombiacheck', '2020/06/04 | Colombia', 'Fact-Checked by: AFP', '2020/06/04 | France', 'Fact-Checked by: Facta', '2020/06/04 | Italy', 'Fact-Checked by: Maldita.es', '2020/06/04 | Spain', 'Fact-Checked by: AAP FactCheck', '2020/06/03 | Australia'], ['Fact-Checked by: TEMPO', '2020/06/03 | Indonesia', 'Fact-Checked by: Agência Lupa', '2020/06/03 | Brazil', 'Fact-Checked by: Animal Político', '2020/06/03 | Mexico', 'Fact-Checked by: Agência Lupa', '2020/06/03 | Brazil', 'Fact-Checked by: Vistinomer', '2020/06/03 | North Macedonia', 'Fact-Checked by: Vishvas News', '2020/06/03 | India', 'Fact-Checked by: AFP', '2020/06/03 | France', 'Fact-Checked by: AFP', '2020/06/03 | France', 'Fact-Checked by: AFP', '2020/06/03 | France', 'Fact-Checked by: FactCrescendo', '2020/06/03 | India', 'Fact-Checked by: Estadão Verifica', '2020/06/03 | Brazil', 'Fact-Checked by: Verificado', '2020/06/03 | Mexico', 'Fact-Checked by: PolitiFact', '2020/06/03 | United States', 'Fact-Checked by: India Today', '2020/06/03 | India', 'Fact-Checked by: Facta', '2020/06/03 | Italy'], ['Fact-Checked by: Agência Lupa', '2020/06/02 | Brazil', 'Fact-Checked by: Vishvas News', '2020/06/02 | India', 'Fact-Checked by: PesaCheck', '2020/06/02 | Uganda', 'Fact-Checked by: Agência Lupa', '2020/06/02 | Brazil', 'Fact-Checked by: PesaCheck', '2020/06/02 | Tanzania', 'Fact-Checked by: La Silla Vacía', '2020/06/02 | Colombia', 'Fact-Checked by: Animal Político', '2020/06/02 | Mexico', 'Fact-Checked by: Dubawa', '2020/06/02 | Nigeria', 'Fact-Checked by: La Silla Vacía', '2020/06/02 | Colombia', 'Fact-Checked by: Vishvas News', '2020/06/02 | India', 'Fact-Checked by: Vishvas News', '2020/06/02 | India', 'Fact-Checked by: BOOM FactCheck', '2020/06/02 | India', 'Fact-Checked by: Fatabyyano', '2020/06/02 | Egypt', 'Fact-Checked by: AFP', '2020/06/02 | Canada, United States, Australia, Malawi', 'Fact-Checked by: FactCrescendo', '2020/06/02 | India'], ['Fact-Checked by: BOOM FactCheck', '2020/06/02 | India', 'Fact-Checked by: FactCrescendo', '2020/06/02 | India', 'Fact-Checked by: India Today', '2020/06/02 | India', 'Fact-Checked by: Agência Lupa', '2020/06/01 | Brazil', 'Fact-Checked by: BOOM FactCheck', '2020/06/01 | India', 'Fact-Checked by: Vishvas News', '2020/06/01 | India', 'Fact-Checked by: Facta', '2020/06/01 | Italy', 'Fact-Checked by: Colombiacheck', '2020/06/01 | Colombia', 'Fact-Checked by: Estadão Verifica', '2020/06/01 | Brazil', 'Fact-Checked by: Colombiacheck', '2020/06/01 | Colombia', 'Fact-Checked by: Poligrafo', '2020/06/01 | Portugal', 'Fact-Checked by: Verificado', '2020/06/01 | Mexico', 'Fact-Checked by: PolitiFact', '2020/06/01 | United States', 'Fact-Checked by: Maldita.es', '2020/06/01 | Spain', 'Fact-Checked by: Animal Político', '2020/05/31 | Mexico'], ['Fact-Checked by: Re:Check', '2020/05/31 | Latvia', 'Fact-Checked by: Chequeado', '2020/05/31 | Argentina', 'Fact-Checked by: AFP', '2020/05/31 | Sri Lanka', 'Fact-Checked by: Agencia Ocote', '2020/05/31 | Guatemala', 'Fact-Checked by: Animal Político', '2020/05/30 | Mexico', 'Fact-Checked by: Colombiacheck', '2020/05/30 | Colombia', 'Fact-Checked by: Vishvas News', '2020/05/30 | India', 'Fact-Checked by: FactCrescendo', '2020/05/30 | Sri Lanka', 'Fact-Checked by: Colombiacheck', '2020/05/30 | Colombia', 'Fact-Checked by: FactCrescendo', '2020/05/30 | India', 'Fact-Checked by: FactCrescendo', '2020/05/30 | India', 'Fact-Checked by: Colombiacheck', '2020/05/30 | Colombia', 'Fact-Checked by: India Today', '2020/05/30 | India', 'Fact-Checked by: Facta', '2020/05/29 | Italy', 'Fact-Checked by: GhanaFact', '2020/05/29 | Ghana'], ['Fact-Checked by: Re:Check', '2020/05/29 | Latvia', 'Fact-Checked by: GhanaFact', '2020/05/29 | Ghana', 'Fact-Checked by: FactCrescendo', '2020/05/29 | India', 'Fact-Checked by: FactCrescendo', '2020/05/29 | India', 'Fact-Checked by: Colombiacheck', '2020/05/29 | Colombia', 'Fact-Checked by: Facta', '2020/05/29 | Italy', 'Fact-Checked by: PesaCheck', '2020/05/29 | South Sudan', 'Fact-Checked by: Facta', '2020/05/29 | Italy', 'Fact-Checked by: Maldita.es', '2020/05/29 | Spain', 'Fact-Checked by: FactCrescendo', '2020/05/29 | India', 'Fact-Checked by: La Silla Vacía', '2020/05/29 | Colombia', 'Fact-Checked by: La Silla Vacía', '2020/05/29 | Colombia', 'Fact-Checked by: Science Feedback', '2020/05/29 | United States', 'Fact-Checked by: Poligrafo', '2020/05/29 | Portugal', 'Fact-Checked by: TEMPO', '2020/05/29 | Indonesia'], ['Fact-Checked by: Rappler', '2020/05/29 | Philippines', 'Fact-Checked by: TheJournal.ie', '2020/05/29 | Ireland', 'Fact-Checked by: Newschecker', '2020/05/29 | India', 'Fact-Checked by: Newtral.es', '2020/05/28 | Spain', 'Fact-Checked by: 15min.lt', '2020/05/28 | Lithuania', 'Fact-Checked by: 15min.lt', '2020/05/28 | Lithuania', 'Fact-Checked by: FactCrescendo', '2020/05/28 | India', 'Fact-Checked by: AAP FactCheck', '2020/05/28 | Australia', 'Fact-Checked by: PesaCheck', '2020/05/28 | Kenya', 'Fact-Checked by: Aos Fatos', '2020/05/28 | Brazil', 'Fact-Checked by: La Silla Vacía', '2020/05/28 | Colombia', 'Fact-Checked by: PesaCheck', '2020/05/28 | Kenya', 'Fact-Checked by: Newtral.es', '2020/05/28 | Spain', 'Fact-Checked by: PesaCheck', '2020/05/28 | Tanzania', 'Fact-Checked by: PesaCheck', '2020/05/28 | Kenya']]
fakenews=[['FALSE:', 'People who arrived at Tirur, Kerala (India) from Mumbai in train, escaped from the sight of the authorities to avoid quarantine.', 'FALSE:', 'Claims from Spanish singer Miguel Bosé on the Bill and Melinda Gates foundation, that he made last Tuesday, June 9 through a Twitter thread on his personal account.', 'FALSE:', 'Images of a man dressed in a hospital gown who seems to run away jumping a wall of the building. According to the caption, this man reported that he had gone to the health center to heal a wound in his hand when they assured him that he should be admitted for COVID-19 and that when “they were going to connect a ventilator, he decided to jump from the second floor and escape”.', 'FALSE:', 'World Health Organization announcing that COVID-19 is losing its potency.', 'FALSE:', 'Hot steam and tea cure coronavirus.', 'FALSE:', 'There will be complete lockdown on June 15th in India.', 'FALSE:', 'PCR tests were conducted on a journalist and his crew who attended late Minister Thondaman’s funeral as they had COVID19 symptoms.', 'FALSE:', 'Dr Eliyantha White had developed a special medicine for COVID19 and was planning to use it on Sri Lankan Navy personnel with the approval of the Prime Minister.', 'FALSE:', 'Images and texts that assure that the vice-president of the Spanish government, Pablo Iglesias, assumed the responsibilities of the nursing homes after the declaration of the state of alarm for the coronavirus.', 'FALSE:', 'Tanzania has developed a coronavirus drug called COVIDOL that can cure COVID-19.', 'FALSE:', 'Vodka can reduce the risk of Coronavirus infection.', 'FALSE:', 'A video of a 14-year-old Indian boy named Abhigya Anand who was alleged to have predicted the coronavirus in 2019.', 'FALSE:', 'Swine flu virus is more dangerous than the novel coronavirus.', 'FALSE:', 'UV rays from the sun can cure COVID-19.', 'FALSE:', 'The body in this video is a Covid-19 patient whose internal organs have been removed.'], ['FALSE:', 'The state government of Pernambuco, Brazil, shipped boxes of alcohol-based hand sanitizers to state hospitals, but there were only two bottles and a lot of sand on each box.', 'FALSE:', 'During an interview to an Australian newspaper, a WHO official said the institution never recomended social isolation.', 'FALSE:', 'Kerala (India) temple offers special Puja for curing COVID-19 and a rate card for the specific COVID19 prayer (rituals) has been created by the temple.', 'FALSE:', 'A video of a “baile funk”, a kind of Brazilian party. On the caption, it is stated that the party was from last week, after the Supreme Court suspended police operations on Rio’s favelas during the pandemic.', 'FALSE:', 'DPS (Delhi Public School) is selling masks with its logo printed on it to students for Rs.400 each.', 'FALSE:', 'The WHO stated that asymptomatic cases of COVID-19 do not contribute to the spread the disease.', 'FALSE:', 'A picture claiming that, starting from September, teachers will have to call an ambulance if a student has a fever at school.', 'FALSE:', 'Ugandan President Kaguta Museveni and Prime Minister Ruhakana Rugunda have tested positive for COVID-19.', 'FALSE:', 'A message accompanied by a photo of a poster from the Government delegation in Navarra, Spain, stating “international vaccination center”. According to the message that is circulating, “these ‘International Vaccination’ posters are beginning to be placed in government delegations, it will be the protocol of the new normal” after the quarantine of the coronavirus. It also says that the virus “was only an excuse to get us a mRNA (genetic software) vaccine synchronized to a digital identity.”', 'FALSE:', 'China is now using special glasses instead of laboratory equipment to screen for coronavirus.', 'FALSE:', 'An image of the Argentinian President Alberto Fernández with officials during the pandemic without masks and without respecting social distancing.', 'FALSE:', 'A WhatsApp message claiming that Italian supermarket chain Conad is offering free shopping vouchers for €1.000 in Italy.', 'FALSE:', 'Text claims that the director of the Public Revenue Office of the Republic of North Macedonia, Sanja Lukarevska, tested positive for coronavirus and went to the hairdresser.', 'FALSE:', 'A WhatsApp message that states that COVID-19 means “Certificate of identification of vaccination with artificial intelligence”; which is intended through the disease to carry out an international plan for the control and reduction of populations.', 'FALSE:', 'Drinking pigeon membrane slurry can cure COVID-19.'], ['FALSE:', 'Donald Trump published on his Twitter account that Brazilian president “Javier” Bolsonaro is a “great guy”, but that his COVID-19 policies are leading to a “genocide”.', 'FALSE:', 'The Brazilian Ministry of Health forbade the expression “COVID-19 suspect” to be used on death certificates.', 'FALSE:', 'Former Brazilian presidential candidate Fernando Haddad threw a birthday party, with guests, while advocating for lockdown.', 'FALSE:', 'A message that states that “An asymptomatic person is a HEALTHY person. He is someone who has a virus but his body developed antibodies. This is called” attenuated virus “, which means that he dominated the virus thanks to his healthy lifestyle habits. This person does not spread the virus, but communicates antibodies to the rest of the people and generates herd immunity.', 'FALSE:', 'Video shows a group of Muslim devotees spitting deliberately to spread coronavirus.', 'FALSE:', 'The vaccine against the new coronavirus has existed since 2001.', 'FALSE:', 'Text claims that “two epidemiologists from the Institute of Public Health of the Republic of North Macedonia tested positive for coronavirus.”', 'FALSE:', 'A man says that coronavirus was created to keep people inside homes and install 5G antennas.', 'FALSE:', 'Dr Uma Kumar of AIIMS gave an interview on coronavirus.', 'FALSE:', 'A video where a man accuses the Italian Civil Protection and the government of Regione Piemonte of having distributed protective masks “poisoned” them with zinc pyrithione.', 'FALSE:', 'The Anhembi field hospital, in São Paulo, Brasil is empty. A video allegedly proves it.', 'FALSE:', 'Tasuku Honjo, Nobel prize winner, stated that the SARS-Cov-2 was made in a lab in Wuhan, where he used to work.', 'FALSE:', 'A WhatsApp message that warns about the installation of an application called “COVID-19 ABTraceTogether”. The chain message asks the reader to to unfriend their friends on Facebook as well as delete their contacts’ phone numbers if they intend to use it because by doing so “everyone your contacts will be known “against” your will and knowledge”.', 'FALSE:', 'Boldo tea prevents COVID-19.', 'FALSE:', 'ICU units in Rio de Janeiro are closed because of lack of patients.'], ['FALSE:', 'Azithromycin and ivermectin are efficient medicines to cure COVID-19.', 'FALSE:', 'List of recommendations from US virologist Robert Ray Redfield that has spread on social media.', 'FALSE:', 'Wearing a mask, the exhaled viruses will not be able to escape and will concentrate in the nasal passages, penetrate the olfactory nerves, and then transit to the brain.', 'FALSE:', 'A WhatsApp message claiming that, once installed, the “Immuni” app (the Italian national contact-tracing application), will acquire users’ phonebooks.', 'FALSE:', 'Messages that claim that the Government knows where we are at all times thanks to an application that Google has installed on our phones.', 'FALSE:', 'The severity of the Covid-19 Case in Surabaya, Indonesia is caused by a “global elite conspiracy”.', 'FALSE:', 'Renata Vasconcellos, one of Brazil’s most famous news anchor, contracted COVID-19.', 'FALSE:', 'Maria Virgínia Casagrande, first lady of the Brazilian State of Espirito Santo, was cured of COVID-19 after being treated with a protocol of hydroxychloroquine and azithromycin.', 'FALSE:', '96.3% of the deaths registered in Italy by COVID-19 died from other pathologies.', 'FALSE:', 'The use or abuse of the mask produces hypercapnia or hypoxia.', 'Mostly False:', 'Mayor of Medellín, Colombia, based his decision on schedule to play sports on validated research.', 'FALSE:', 'Vaccines and facemasks “kill” people.', 'FALSE:', 'A text message states that Facebook would have taken advantage of the chaos created by Covid-19 to gain permission to use our personal pictures.', 'FALSE:', 'Pedro Sánchez, President of Spain, said this Wednesday, June 3 in the Congress of Deputies, that “today we have 0 deceased in our country as a result of COVID” and that Pablo Casado should be happy that “we haven’t had any death by COVID-19 over the past two days”.', 'FALSE:', 'A Facebook post makes a series of claims about Italy “defeating” COVID-19 inclduign that it “nothing but intravascular coagulation (thrombosis)”.It also alleges that Italian doctors who performed autopsies “discovered” that COVID-19 “is not a virus” but a bacteria that causes death and the formation of blood clots.'], ['FALSE:', 'This cyclist died due to lack of oxygen he was wearing a mask.', 'FALSE:', 'There were no COVID-19 deaths in Belém, Brazil, on May 30 and May 31.', 'FALSE:', 'The herb named “holy leaf” or “momo” cures COVID-19 and helps patients breathe.', 'FALSE:', 'Madagascar’s president, Andry Rajoelina, accused the WHO of promising bribes if he “poisoned” an alledged local COVID-19 treatment.', 'FALSE:', 'Claim that despite the fact that the crisis headquarters in the North Macedonian town of Stip announced that the textile factories in Stip will be closed due to established cases of coronavirus infections, some of the factories are still working.', 'FALSE:', 'Drinking pigeon membrane slurry can cure COVID-19.', 'FALSE:', 'French “Stopcovid” case-tracking app has been secretly installed on smartphones.', 'FALSE:', 'This table shows death figures in France from January to April.', 'FALSE:', 'A cure for COVID-19 was discovered in Italy.', 'FALSE:', 'Indian Home Minister Amit Shah said that the government transferred financial aid of Rs 530 million into the bank accounts of 410 million people during the coronavirus pandemic, which means Rs 1.29 for each person.', 'FALSE:', 'A federal investigation in the city of Fortaleza, Brazil, made number of daily recorded deaths fall 90%.', 'FALSE:', 'President of Mexico has proposed to collect taxes for having pets to cover social programs by COVID-19.', 'FALSE:', '“She’s just casually carrying a body with 1 hand..? Sure.. More evidence of coronavirus being a complete hoax with props & street theater.”', 'FALSE:', 'Japanese Nobel laureate Dr. Tasuku Honjo has said China manufactured coronavirus and he once worked at the Wuhan lab which later produced it.', 'FALSE:', 'A scientific study about the new coronavirus according to which asymptomatic people would not be contagious. The study was conducted in China and it monitored 455 people who got in touch with a 22-years-old asymptomatic patient who tested positive for Covid-19, claiming that none of them caught the disease'], ['FALSE:', 'After a police raid in Rio, the city administration reduced the official COVID-19 death toll by 1.177', 'FALSE:', 'Italy did not follow WHO protocol and did an autopsy on a corpse that died from Covid-19 and realised that coronavirus is actually not a virus but a bacterium which gets amplified with 5G electromagnetic radiation that also produces inflammation and hypoxia, and multiple other claims.', 'FALSE:', 'Uganda Red Cross Society in partnership with the United States Agency for International Development (USAID).', 'FALSE:', 'A photo of a person carrying an alledged corpse with a single hand. The caption states this was a forged funeral.', 'FALSE:', 'Vodacom is offering Tsh80,000 to M-Pesa users as COVID-19 relief funds.', 'FALSE:', 'Alkaline water cures the coronavirus.', 'FALSE:', 'President of Mexico proposes to collect a tax of 500 pesos for each pet, to pay for social programs related to COVID-19.', 'FALSE:', 'A Facebook page shared a post announcing that the United States of America will grant 5,000 Nigerians free work Visa for two years.', 'FALSE:', 'A beverage with aspirin, lemon and hot water cures the coronavirus.', 'FALSE:', 'Claim that Indian Prime minister Modi said one crore (10 million) COVID-19 positive patients have been treated for free.', 'FALSE:', 'Video shows 106 dead bodies in Delhi’s Loknayak hospital, in India.', 'FALSE:', 'India’s Prime Minister Narendra Modi said in his ‘Mann Ki Baat’ radio address that one crore COVID-19 patients have been treated for free in the country.', 'FALSE:', 'These images show bodies of COVID19 patient dead in the streets in America.', 'FALSE:', 'A video has been shared thousands of times on social media, claiming that circuit boards with “COV-19” inscribed on them are being fitted to 5G towers.', 'FALSE:', 'Indian Prime minister Narendra Modi said 10 million COVID-19 patients have been treated for free in India.'], ['FALSE:', 'India Today Ticker that says PM Modi has stated that India has treated 1 crore (10 million) COVID-19 patients for free.', 'FALSE:', 'Gujarat CM Vijay Rupani said that his government provided ration to 650 million people during the lockdown.', 'FALSE:', 'US President Donald Trump wanted to ruin Americans using coronavirus as a weapon. Thousands of people are protesting on the streets against that.', 'FALSE:', 'There were no COVID-19 deaths in Fortaleza, Brazil, on May 29.', 'FALSE:', 'The video of terrible conditions of a COVID-19 ward is from Delhi’s hospital.', 'FALSE:', 'Video shows 106 dead bodies in Delhi’s Loknayak hospital, in India.', 'FALSE:', 'A picture claiming that Lidl is offering free shopping vouchers for €180 in Italy.', 'FALSE:', 'The coronavirus ‘has been defeated with anti-inflammatories and anticoagulants’.', 'FALSE:', 'Deaths in Brazil by pneumonia are registered as COVID-19.', 'FALSE:', 'WHO has declared COVID-19 an endemic disease.', 'FALSE:', 'The covid-19 pandemic caused the death of 0.003% of the world population.', 'FALSE:', 'The use of masks for COVID-19 causes hypoxia.', 'FALSE:', '“How many of you are aware that the female governor of Michigan is the niece of George Soros?”', 'FALSE:', 'Publications on social networks that claims that a coronavirus outbreak after the protests in the Barrio de Salamanca, Madrid, Spain.', 'False:', 'Video shows the Mexican Air Force throwing bodies of people infected with COVID-19 on the beaches of Acapulco.'], ['FALSE:', 'Facebook posts questioning the existence of the coronavirus, as no supermarket employee has been infected in the world.', 'FALSE:', 'Lionel Messi said “there was a planetary coup d’etat” with the coronavirus pandemic.', 'FALSE:', 'A photo from the funeral of a recently deceased Sri Lankan politician, Arumugam Thondaman, has been shared thousands of times in multiple Facebook posts. The posts claim the image shows one of Thondaman’s daughters violated Sri Lanka’s mandatory coronavirus quarantine policy for travelers by attending the ceremony shortly after returning to the country from overseas.', 'FALSE:', 'A Facebook page posted that temporary hospitals in Guatemala would be closed, as people diagnosed with COVID-19 could isolate themselves at home. A statement they attributed to an authority in the Ministry of Health.', 'false:', 'Salaries of deputies in Guatemala are suspended due to the COVID-19 crisis.', 'FALSE:', 'In recent days, a chain circulated through WhatsApp that urged entering the page colombia.ayudas.xyz to be a beneficiary of government aid.', 'FALSE:', 'Image claims that a family committed suicide in Jodhpur, India with its picture going viral during lockdown.', 'FALSE:', 'Tamil Nadu (India) government approved Thanikasalam Siddha medicine for COVID-19.', 'FALSE:', 'Italian politician asked to take Bill Gates to the International Criminal Court.', 'FALSE:', 'Video shows migrants looting food packets at Hyderabad Railway station, in India.', 'FALSE:', 'Coronavirus can be sexually transmitted.', 'FALSE:', 'Mayor of El Espinal, Colombia ‘bought false tests for COVID-19’.', 'FALSE:', 'Man seen in viral images was a Covid-19 patient who fell in love with his lady doctor. The two got engaged in the same hospital in Egypt.', 'FALSE:', 'A video which would show that the Immuni app (the application for contact tracing sponsored by the Italian government) is already active on our smartphones and, therefore, Italian people are being traced without their consent.', 'FALSE:', 'Chewing raw onions can cure coronavirus.'], ['FALSE:', 'Facebook post claims that the Latvian app Apturi Covid (Stop Covid) which was created to warn people who have been close to  an infected person, will be used so the government can track all the people from the contact list and record their locations.', 'FALSE:', 'A vaccine for the coronavirus has been discovered.', 'FALSE:', 'Indian PM Narendra Modi has been selected as new chairmant of WHO.', 'FALSE:', 'The fifth phase of lockdown will be more harsh and strict in the state of Gujrat, India.', 'FALSE:', '5G towers have a ‘VOC 19’ component and cause coronavirus.', 'FALSE:', 'A picture, allegedly published by the press agency Adnkronos, shows a passenger car with the inscription: “Covid-19 deportation plan”.', 'FALSE:', 'South Sudan had recorded 481 COVID-19 cases by May 20, after the announcement of 134 new cases in Juba.', 'FALSE:', 'An article claiming that wearing protective masks in open spaces would have severe collateral effects that could eventually lead to cancer.', 'FALSE:', 'An excerpt from a document from the Ministry of Health with the following message: “This document of March 5, from the Government of Spain, requires nursing homes to keep the elderly with COVID-19 symptoms, locked in their rooms, preventing them from going to the hospital to be treated. So they died alone! Tremendous! “', 'FALSE:', 'India’s Home Ministry has given permission to reopen schools and educational institutions across India.', 'FALSE:', 'Vickvaporub eliminates coronavirus.', 'FALSE:', 'An Italian deputy says that 96 percent of the deaths of coronavirus are for other diseases.', 'FALSE:', 'A study by Bartomeu Payeras i Cifre shows a direct correlation between 5G networks and COVID-19 outbreaks and “demonstrates clearly the most likely probability that the COVID-19 hypoxic injuries and hospital admissions are directly related to electromagnetic radiation exposure by 5G networks”.', 'FALSE:', 'Portuguese energy company Galp is offering 3 months of free fuel to “help the needy”.', 'FALSE:', 'Covid-19 is just common flu and was produced to make a profit.'], ['FALSE:', 'A female overseas Filipino worker (OFW) in Saudi Arabia was beheaded after testing positive for COVID-19, the disease caused by the novel coronavirus.', 'FALSE:', 'Bill Gates, Melinda Gates, Anthony Fauci and the WHO are being charged with genocide.', 'FALSE:', 'In Italy, the cure for Coronavirus is finally found.', 'FALSE:', 'Google has installed a secret app in phones to spy users.', 'FALSE:', 'A Youtube video shared on facebook claimed that Lithuanian Health Minister banned a “cure from COVID-19” from Lithuania.', 'FALSE:', 'An article shared on Facebook claimed that the virus is fake and proven only by faulty testing.', 'FALSE:', 'Kerala government is providing free quarantine service only to religious minorities.', 'FALSE:', 'An Instagram post claims Microsoft founder Bill Gates said up to 700,000 people could die from a COVID-19 vaccine.', 'FALSE:', 'A Kenyan Facebook page bearing the name and image of Kakamega Governor Wycliffe Oparanya with a post claiming to offer cash relief of Ksh15,000 to Kenyans in distress as a result of the COVID-19 pandemic.', 'FALSE:', 'Rio de Janeiro’s City Hall revised data after Federal Police operation and decreased 1,177 deaths from official COVID-19 records.', 'FALSE:', 'The cure for coronavirus: acetaminophen and gargling mouthwash.', 'FALSE:', 'Scientists in the United States have discovered a coronavirus cure “that works 100 percent”.', 'FALSE:', 'One person has been stabbed during a protest against the government in the neighbourhood of Moratalaz in Madrid.', 'FALSE:', 'Ameera al-Taweel, a former Saudi princess and philanthropist, has partnered with the World Health Organization (WHO) to give out COVID-19 relief money on social media.', 'FALSE:', 'Italian doctors have confirmed that COVID-19 is a bacterial disease and not caused by a virus as claimed by a number of authorities.']]

# print(data)
# print(fakenews)

data_verifier= list(range(0,int(len(data)*len(data[1])/2)))
data_datelocation=list(range(0,int(len(data)*len(data[1])/2)))
data_date=list(range(0,int(len(data)*len(data[1])/2)))
data_location=list(range(0,int(len(data)*len(data[1])/2)))
fakenewsC=list(range(0,int(len(data)*len(data[1])/2)))
c1=0
for i in range(0,len(data)):

    for j in range(0,len(data[2]),2):
        data_verifier[c1]=data[i][j]
        data_datelocation[c1] = data[i][j+1]
        fakenewsC[c1]=fakenews[i][j+1]
        c1=c1+1


# print(data_verifier[0][0:17])
# print(data_verifier[0][17:])
# print(data_datelocation[0][0:10])
# print(data_datelocation[0][13:])
# print(fakenewsC)


for i in range(0,len(data_datelocation)):

    data_date[i]=data_datelocation[i][0:10]
    data_location[i]= data_datelocation[i][13:]
    data_verifier[i]= data_verifier[i][17:]

fakenews_combined = ' '.join(fakenewsC)

# print(fakenews_combined)

# import pandas as pd
import pandas as pd

#creating panda dataframe

data_df = pd.DataFrame(list(zip(data_location, data_date,data_verifier,fakenewsC)),
                  columns=['location', 'date','verifier','fakenews'])

data = data_df.to_dict('index')

#Cleaning text, following thumb-rule, no number, no pontuation...

import re
import string

def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('misleading', '', text)
    text = re.sub('covid', '', text)
    text = re.sub('coronavirus', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

round1 = lambda x: clean_text(x)
data_clean = data_df.copy()
data_clean.fakenews=pd.DataFrame(data_df.fakenews.apply(round1))

# print(data_df)
# print(data_clean.loc[146,'fakenews'])

# Let's pickle it for later use
data_df.to_pickle("corpus.pkl")
data_df.to_csv(r'DATAFRAME.csv')

# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english')
data_cv = cv.fit_transform(data_clean.fakenews)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
# print(data_dtm)


clean_fakenews_combined=clean_text(fakenews_combined)
corpus=[clean_fakenews_combined]
corpus_cv=cv.fit_transform(corpus)
corpus_dtm = pd.DataFrame(corpus_cv.toarray(), columns=cv.get_feature_names())

# Let's pickle it for later use
data_dtm.to_pickle("dtm.pkl")
corpus_dtm.to_pickle("corpus_dtm.pkl")

# Let's also pickle the cleaned data (before we put it in document-term matrix format) and the CountVectorizer object
data_clean.to_pickle('data_clean.pkl')
pickle.dump(cv, open("cv.pkl", "wb"))

from collections import Counter


EDA_data=corpus_dtm.transpose()
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
top = EDA_data[0].sort_values(ascending=False).head(50)
top.to_csv(r'top_words.csv')
top_dict = top.to_dict()
# print(top_dict)
words=[]
for w in top_dict:
    words.append(w)
print(top)

from sklearn.feature_extraction import text
stop_words = text.ENGLISH_STOP_WORDS

from wordcloud import WordCloud

wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)


import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [16, 6]

# wc.generate(clean_fakenews_combined)
wc.fit_words(top)
image = wc.to_svg()
svg = open(path.join(d, 'newsvg.svg'),'w').write(image)
# plt.subplot(3, 4, index + 1)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
# plt.title(full_names[index])

plt.savefig("allwords_wc.svg")
plt.show()
# print(clean_fakenews_combined)
