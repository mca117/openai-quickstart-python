import os
import openai
import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, url_for

example_letter = '''Dear [Polician name],\n\n
I am writing to you with profound concern and an urgent appeal regarding the dire and rapidly deteriorating situation in Gaza. As you are well aware, UN experts have issued an unequivocal warning that time is running out to prevent a genocide and a humanitarian catastrophe in this besieged region.\n

The relentless Israeli airstrikes and attacks against the Palestinian people, especially the assaults on the Jabalia refugee camp, represent a glaring violation of international law and fundamental human rights. Almost 10,000 Palestinians have been killed by Israeli military forces. Almost 4,000 of those massacred are children. Israeli forces just bombed another hospital, AlShifa, sheltering 30,000 people. The consequences of these actions are dire and inhumane, affecting innocent civilians, including women, children, persons with disabilities, and older individuals, who are enduring unimaginable hardships.\n

Canada's commitment to 'Never Again' against genocide is not merely a slogan but a solemn promise that is being broken. I implore you to exercise your leadership and take immediate and decisive actions to address this crisis. We urge you to use your voice and influence to call for an immediate ceasefire to prevent further suffering and loss of innocent lives.\n

Canada must pressure Israel and its allies to cease their disastrous course of action and ensure that urgently needed humanitarian aid reaches those who need it most. Canada should also demand the protection of UN and humanitarian workers, hospitals, and schools providing life-saving services to the people of Gaza, as per international law.\n

As a global superpower committed to international human rights law, Canada must fulfill its commitment and uphold international law rather than be complicit in yet another genocide. This demands a strong condemnation of the racist inaction that the world witnesses, revealing that some lives are considered unworthy of protection.\n

Our government's inaction is not merely a diplomatic failure but a stark reflection of racism that should be vehemently condemned. Furthermore, our prime minister must actively challenge the narrative that attempts to justify these actions with the notion of a 'right to defend,' particularly when the death toll has reached thousands. The question becomes who, in reality, is Israel defending themselves against? The lives of Palestinians are not worth any less.\n

We implore you to prioritize human rights over power and bilateral relationships, as the voices of Canadian people of conscience remain unheard. \n

The gravity of this situation leaves no room for equivocation or delay. I urge you to utilize your authority to protect the lives and rights of all Palestinians in Gaza.\n\n
Sincerely,\n
[name given]'''

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        call_to_action = request.form["call_to_action"]
        article_url = request.form["background_information"]  # Get the article URL
        background_information = scrape_article_content(article_url)  # Scrape article content

        response = openai.Completion.create(
            prompt = generate_prompt(background_information, call_to_action),
            model="gpt-3.5-turbo-instruct",
            max_tokens=200,
            temperature=0.6,
        )
        result = response['choices'][0]['text']
        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def scrape_article_content(url):
    if url.startswith("http"):
        # Use requests to get the HTML content from the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find and extract the relevant content, modify this based on the website structure
            # Here, we assume the main article content is in <p> tags, adjust as needed
            article_content = "\n".join([p.text for p in soup.find_all("p")])

            return article_content
        else:
            return "Failed to fetch article content"
    else:
        return url  # Return the provided text if it's not a URL
    

def generate_prompt(background_information, call_to_action):
    return """Your a human rights activist that stands up for the right of Human life in atrocities around teh world. Write a 400 word or less letter directed to the your local Minister of Parliament to demand a given call_to_action and background_information on the topic.
    some examples are shown bellow:
background_information: Time has run out to prevent genocide in Gaza. Over 11,100 civilians have been killed by the Israeli regime, including more than 4,000 children. Gaza’s two largest hospitals, Al-Shifa and Al-Quds, have both closed, leading patients and babies to die. Israeli snipers continue to fire at anyone near Al-Shifa Hospital, trapping thousands inside. UN experts have issued a stark warning about Israel's unrelenting attacks on the besieged Gaza Strip, flagging it as a genocide, clear breach of international law and a grave threat to the Palestinian people. We must act urgently to halt this crisis.
Demand that Canadian Prime Minister Justin Trudeau take immediate and decisive action to halt the violence and support a ceasefire in Gaza. We cannot afford to wait any longer. The lives of innocent civilians, including women, children, persons with disabilities, and older persons, are being sorely neglected by Canadian leaders who once promised: "Never Again." 
call_to_action: Urgently call for an immediate ceasefire in Gaza to prevent further suffering and loss of life.
letter: 
Dear [Polician name],\n\n
I am writing to you with profound concern and an urgent appeal regarding the dire and rapidly deteriorating situation in Gaza. As you are well aware, UN experts have issued an unequivocal warning that time is running out to prevent a genocide and a humanitarian catastrophe in this besieged region.\n

The relentless Israeli airstrikes and attacks against the Palestinian people, especially the assaults on the Jabalia refugee camp, represent a glaring violation of international law and fundamental human rights. Almost 10,000 Palestinians have been killed by Israeli military forces. Almost 4,000 of those massacred are children. Israeli forces just bombed another hospital, AlShifa, sheltering 30,000 people. The consequences of these actions are dire and inhumane, affecting innocent civilians, including women, children, persons with disabilities, and older individuals, who are enduring unimaginable hardships.\n

Canada's commitment to 'Never Again' against genocide is not merely a slogan but a solemn promise that is being broken. I implore you to exercise your leadership and take immediate and decisive actions to address this crisis. We urge you to use your voice and influence to call for an immediate ceasefire to prevent further suffering and loss of innocent lives.\n

Canada must pressure Israel and its allies to cease their disastrous course of action and ensure that urgently needed humanitarian aid reaches those who need it most. Canada should also demand the protection of UN and humanitarian workers, hospitals, and schools providing life-saving services to the people of Gaza, as per international law.\n

As a global superpower committed to international human rights law, Canada must fulfill its commitment and uphold international law rather than be complicit in yet another genocide. This demands a strong condemnation of the racist inaction that the world witnesses, revealing that some lives are considered unworthy of protection.\n

Our government's inaction is not merely a diplomatic failure but a stark reflection of racism that should be vehemently condemned. Furthermore, our prime minister must actively challenge the narrative that attempts to justify these actions with the notion of a 'right to defend,' particularly when the death toll has reached thousands. The question becomes who, in reality, is Israel defending themselves against? The lives of Palestinians are not worth any less.\n

We implore you to prioritize human rights over power and bilateral relationships, as the voices of Canadian people of conscience remain unheard. \n

The gravity of this situation leaves no room for equivocation or delay. I urge you to utilize your authority to protect the lives and rights of all Palestinians in Gaza.\n\n
Sincerely,\n
[name given]

---

background_information: 
Since 2016 a large network of concentration camps has been established in East Turkistan (Xinjiang) in Western China, and more than 2 million Uyghur people have been imprisoned. Hundreds of thousands of children have been forcefully taken from their parents and detained in concentration camps where they are subject to abuse and torture.  Women and girls have been forcefully sterilized and forced to abort even full-term babies. Torture, gang rape and forced organ harvesting are happening in these concentration camps. 
call_to_action: 
1. call_to_action: Acknowledge the Uyghur genocide\n
2. Introduce the Uyghur Forced Labour Prohibition Act\n
3. Commit to the resettlement of Uyghur Refugees\n
4. Stop CPP investments in Chinese corporations supporting genocide\n
5. Implement Transparency and Foreign Lobbyist Registration Act\n
letter: 
Dear [Polition name],\n\n
Since 2016 a large network of concentration camps has been established in East Turkistan (Xinjiang) in Western China and more than 2 million Uyghur people have been imprisoned. Hundreds of thousands of children have been forcefully taken from their parents and detained in concentration camps where they are subject to abuse and torture.  Women and girls have been forcefully sterilized and forced to abort even full-term babies. Torture, gang rape and forced organ harvesting is happening in these concentration camps. \n
In January 2021, the US State Department declared that the Chinese government is committing genocide and crimes against humanity against the Uyghur people in East Turkistan (Xinjiang) through the use of concentration camps, forced sterilization and child separation. In February 2021 Canada’s parliament passed a motion declaring that China’s treatment of the Uyghur people constitutes genocide. \n
We call upon the Canadian Government to:\n
1. Acknowledge the ongoing Uyghur genocide and introduce measures to address this on a domestic and global level.\n
The Government’s failure to respect and acknowledge the unanimous vote by the parliament acknowledging Uyghur Genocide has weakened our ability to uphold a rules-based international order. It has prevented Canada’s ability to fulfill its internationally binding legal obligation to stop the genocide, punish those responsible for the crime of genocide as well as properly utilize the Responsibility to Protection Doctrine. If Canada is genuinely committed to human rights in particular and international law in general - then we must reach out to other like-minded countries and build an international coalition to name the crime of Uyghur genocide and take appropriate, orchestrated, and unified actions. As a global leader, Canada must acknowledge the Uyghur genocide and take initiative by raising corresponding measures in proper forums, including International Criminal Court, International Court of Justice and at the UN Security council.\n
2. Introduce the Uyghur Forced Labour Prohibition Act\n
At the recent G7 Summit in Cornwall, United Kingdom, the world’s leading democracies stood united against forced labor, including in Xinjiang, and committed to ensure global supply chains are free from the use of forced labor. Cotton and related products manufactured and processed in east Turkistan make up 90% of China’s total export and 30% of the global supply. Tomato products made in East Turkistan are a quarter of the total global supply. Despite the Prime Minister’s official commitment to ban products and supply chains using Uyghur forced labour from the global and Canadian Market; Global Affairs Canada released an advisory on January 12, 2021, with very weak enforceable measures. Canada has been actively importing Cotton, Tomatoes and Solar panels that are made by Uyghur forced labour and not a single shipment has been seized by the CBSA. The United States passed The Uyghur Forced Labor Prevention Act on July 14th, 2021. Canada must follow suit and stand by the commitment made at the G7 summit by passing the Uyghur Forced Labour Prohibition Act and boycotting products made by Uyghur forced labour.  \n
3. The Government of Canada must commit to the resettlement of Uyghur refugees. \n
In 2006, Canada spearheaded the introduction of the Responsibility to Protection Doctrine to the Geneva Convention. This doctrine expanded the responsibilities of party states from stopping, preventing, and punishing genocide to also include the protection of the victims of genocide. Therefore, Canada has a legal responsibility to act with international allies in adopting effective measures and procedures to stop genocide, prevent genocide, punish those responsible for the crime of genocide and offer assistance to the victims of genocide. \n
The United States Congress has included the Uyghur Refugee Settlement through Priority 2 category as part of the Uyghur Human Rights Protection Act , which provides legal ground for the victims of Uyghur genocide and victims of all forms of persecution to settle in the United States, therefore bypassing the ineffective UNHCR process. Canada should also include the settlement of the Uyghur refugees trapped in unsafe third countries to Canada as part of the projected refugee settlement program announced by the Minister of Immigration. \n
4. Stop CPP investments in Chinese corporations supporting genocide.\n
Canada Pension Plan Fund represents nearly $500 billion CAD in assets and is managed by the CPP Investment Board (CPPIB). Recently the CPPIB decided to invest in Chinese companies that are blacklisted and sanctioned by the US due to their deep involvement in China’s genocidal policy against Uyghurs. This makes every single Canadian complicit in the genocide by financially contributing into blacklisted and sanctioned companies involved in the genocide of the Uyghur people.\n
Bill C-231 proposed a number of amendments to ensure CPP funds are not invested in companies violating human rights or producing arms or ammunition prohibited by international law or benefitting individuals or acts of corruption under the Corruption of Foreign Public Officials Act. Unfortunately, this bill has been tabled in the House and defeated in March 2021. Canadian Parliament must pass legislation ensuring CPP funds are not invested in organizations promoting genocide. \n
5. Implement Transparency and Foreign Lobbyist Registration Act \n
The United States and Australia have passed Foreign Agent Registration Act or similar legislation to ensure foreign countries do not influence national policies, state owned enterprises, universities, and other strategic national interests. Both Australia and the US require “agents of foreign principals who are engaged in political activities” to disclose their actions. The Canadian Coalition on Human Rights in China has called on the Liberal government to set up a similar register for former politicians and public servants who assume paid roles for foreign governments and companies. Lack of similar legislation in Canada has enabled foreign influence in state backed investments and other entities in Canada’s political, social, academic and media spheres thereby extending China’s control and influence in Canada. The recent Senate rejection of the Uyghur Genocide motion by Senator Yuen Pau Woo is an example of this influence in our government. Canadian taxpayers deserve transparency from their leaders and should know who is representing China’s interest in Canada.\n
We can no longer be complicit in the ongoing atrocity crimes by remaining silent. Canada must act and join the US and other nations and stop the ongoing genocide.\n
Thank you for your crucial attention to these matters. \n\n
Sincerely,\n
[name given]

---

background_information: {}
call_to_action: {}
letter:
""".format(
        background_information, call_to_action
    )
