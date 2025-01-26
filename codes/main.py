from requests_html import HTMLSession
import json


def get_tactics_number(table):
    """
    Extracts the tactics numbers from the table.

    Args:
        table (Element): The HTML table element containing the tactics.

    Returns:
        list: A list of tactics numbers.
    """
    numbers = []
    tactics_number = table.find("tr")[1].text.split("\n")
    for numb in tactics_number:
        numbers.append(numb.split("\xa0")[0])
    return numbers


def clean_table(rowdata):
    """
    Cleans the table data by merging rows where necessary.

    Args:
        rowdata (list): The list of rows from the table.

    Returns:
        list: The cleaned list of rows.
    """
    for row in rowdata:
        if row[0] != "":
            x = row[0]
        else:
            row[0] = x + row[1]
            row.pop(1)
    return rowdata


def get_techniques_data(session, url, tactic_techniques):
    """
    Retrieves data for each technique under a tactic.

    Args:
        session (HTMLSession): The HTML session for making requests.
        url (str): The base URL of the website.
        tactic_techniques (list): The list of techniques under a tactic.

    Returns:
        dict: A dictionary containing the data for each technique.
    """
    techniques = {}
    for row in tactic_techniques[1:]:
        if row.find("td")[1].text.startswith("."):
            subtechnique = technique + row.find("td")[1].text
            techniques[subtechnique] = {
                "technique_name": row.find("td")[2].text,
                "description": "",
                "url": url + row.find("td")[1].find("a")[0].attrs["href"][1:],
                "Procedure": "",
                "Mitigation": "",
            }
        else:
            technique = row.find("td")[0].text
            techniques[technique] = {
                "technique_name": row.find("td")[1].text,
                "description": "",
                "url": url + row.find("td")[0].find("a")[0].attrs["href"][1:],
                "Procedure": "",
                "Mitigation": "",
            }
    return techniques


def get_procedures(session, url, technique_response):
    """
    Retrieves procedures for a given technique.

    Args:
        session (HTMLSession): The HTML session for making requests.
        url (str): The base URL of the website.
        technique_response (Response): The response object for the technique.

    Returns:
        list: A list of procedures for the technique.
    """
    procedures = []
    if technique_response.html.find("h2")[0].attrs["id"] == "examples":
        procedure_rows = technique_response.html.find(
            "div.tables-mobile", first=True
        ).find("tr")[1:]
        for procedure_html in procedure_rows:
            procedure = procedure_html.text.split("\n")
            procedure_id = procedure[0]
            procedure_name = procedure[1]
            procedure_description = procedure[2]
            procedure_url = (
                url + procedure_html.find("td")[1].find("a")[0].attrs["href"][1:]
            )

            procedure_data = {
                "id": procedure_id,
                "name": procedure_name,
                "description": procedure_description,
                "url": procedure_url,
                "technique_used": get_techniques_used(session, procedure_url),
            }
            procedures.append(procedure_data)
    return procedures


def get_techniques_used(session, procedure_url):
    """
    Retrieves techniques used in a given procedure.

    Args:
        session (HTMLSession): The HTML session for making requests.
        procedure_url (str): The URL of the procedure.

    Returns:
        list: A list of techniques used in the procedure.
    """
    techniques_used = []
    procedure_response = session.get(procedure_url)
    techniques_used_rows = procedure_response.html.find(
        "table.techniques-used", first=True
    ).find("tr")[1:]
    for technique_html in techniques_used_rows:
        technique = technique_html.text.split("\n")
        if len(technique) == 5:
            technique_id = technique[1] + technique[2]
            technique_name = technique[3]
            technique_use = technique[4]
        elif len(technique) == 4:
            technique_id = technique[1]
            technique_name = technique[2]
            technique_use = technique[3]
        else:
            subtechnique_id = technique_id + technique[0]
            technique_name = technique[1]
            technique_use = technique[2]
            techniques_used.append(
                {
                    "id": subtechnique_id,
                    "name": technique_name,
                    "technique_use": technique_use,
                }
            )
        techniques_used.append(
            {
                "id": technique_id,
                "name": technique_name,
                "technique_use": technique_use,
            }
        )
    return techniques_used


def get_mitigations(session, url, technique_response):
    """
    Retrieves mitigations for a given technique.

    Args:
        session (HTMLSession): The HTML session for making requests.
        url (str): The base URL of the website.
        technique_response (Response): The response object for the technique.

    Returns:
        list: A list of mitigations for the technique.
    """
    mitigations = []
    if technique_response.html.find("h2")[0].attrs["id"] != "examples":
        mitigation_rows = technique_response.html.find("div.tables-mobile")[0].find(
            "tr"
        )[1:]
    else:
        mitigation_rows = technique_response.html.find("div.tables-mobile")[1].find(
            "tr"
        )[1:]

    for mit in mitigation_rows:
        mitigation_id = mit.find("td")[0].text
        mitigation_name = mit.find("td")[1].text
        mitigation_description = mit.find("td")[2].text
        mitigation_url = url + mit.find("td")[1].find("a")[0].attrs["href"][1:]

        mitigations.append(
            {
                "id": mitigation_id,
                "name": mitigation_name,
                "description": mitigation_description,
                "url": mitigation_url,
            }
        )
    return mitigations


if __name__ == "__main__":
    session = HTMLSession()
    url = "https://attack.mitre.org/"
    response = session.get(url)

    table = response.html.find("table.matrix.side", first=True)
    tactics = table.find("tr")[0].text.split("\n")
    tactics_number = get_tactics_number(table)

    for i in range(len(tactics)):
        data = {}
        tactic = tactics[i]
        tactic_number = tactics_number[i]
        tactic_url = (
            url + table.find("tr")[0].find("td")[i].find("a")[0].attrs["href"][1:]
        )
        tactic_response = session.get(tactic_url)
        tactic_text = tactic_response.html.find("div.description-body", first=True).text
        data[tactic] = {
            "description": tactic_text,
            "tactics_number": tactic_number,
            "techniques": {},
        }
        tactic_techniques = tactic_response.html.find("table")[0].find("tr")
        data[tactic]["techniques"] = get_techniques_data(
            session, url, tactic_techniques
        )

        for key, value in data[tactic]["techniques"].items():
            technique_response = session.get(value["url"])
            technique_text = technique_response.html.find(
                "div.description-body", first=True
            ).text
            data[tactic]["techniques"][key]["description"] = technique_text
            procedures = get_procedures(session, url, technique_response)
            data[tactic]["techniques"][key]["Procedure"] = procedures
            mitigations = get_mitigations(session, url, technique_response)
            data[tactic]["techniques"][key]["Mitigation"] = mitigations

        with open(f"{tactic}_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"The {tactic} is done.\n")
