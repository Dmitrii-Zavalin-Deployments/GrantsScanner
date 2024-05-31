import os

class HTMLGenerator:
    def generate_html(self, grants_data, output_file='grants.html'):
        # Check if the output file exists and delete it if it does
        if os.path.exists(output_file):
            os.remove(output_file)

        # Read the reviewed links
        with open('data/reviewed_links.txt', 'r') as file:
            reviewed_links = file.read().splitlines()

        # Start of the HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Grant Details</title>
            <style>
                table {{
                    width: 300%; /* Make the table wider than the page */
                    border-collapse: collapse;
                    table-layout: fixed; /* Fixed table layout to manage column widths */
                }}
                table, th, td {{
                    border: 1px solid black;
                    padding: 10px;
                    text-align: left;
                    vertical-align: top; /* Align text to the top of the cell */
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                th:nth-child(1) {{ width: 2%; }} /* Number column */
                th:nth-child(2) {{ width: 8%; }} /* Name column */
                th:nth-child(3), th:nth-child(4), th:nth-child(5), th:nth-child(6) {{ width: 10%; }} /* Funds, Dates, Requirements, Documents columns */
                th:nth-child(7) {{ width: 40%; }} /* Summary column */
                th:nth-child(8) {{ width: 2%; }} /* Link column */
                th:nth-child(9) {{ width: 8%; }} /* Query column */
                .tabcontent {{
                    display: none;
                }}
                .active-tab {{
                    display: block;
                }}
            </style>
        </head>
        <body onload="openTab(event, 'NewLinks')">
            <h1>Grant Details</h1>
            <div class="tab">
                <button class="tablinks" onclick="openTab(event, 'NewLinks')">New Links</button>
                <button class="tablinks" onclick="openTab(event, 'ReviewedLinks')">Reviewed Links</button>
            </div>

            <div id="NewLinks" class="tabcontent">
                <h2>New Links</h2>
                <table>
                    <tr>
                        <th>Number</th>
                        <th>Name</th>
                        <th>Funds</th>
                        <th>Dates</th>
                        <th>Requirements</th>
                        <th>Documents</th>
                        <th>Summary</th>
                        <th>Link</th>
                        <th>Query</th>
                    </tr>
                    {new_links_rows}
                </table>
            </div>

            <div id="ReviewedLinks" class="tabcontent">
                <h2>Reviewed Links</h2>
                <table>
                    <tr>
                        <th>Number</th>
                        <th>Name</th>
                        <th>Funds</th>
                        <th>Dates</th>
                        <th>Requirements</th>
                        <th>Documents</th>
                        <th>Summary</th>
                        <th>Link</th>
                        <th>Query</th>
                    </tr>
                    {reviewed_links_rows}
                </table>
            </div>

            <script>
                function openTab(evt, tabName) {{
                    var i, tabcontent, tablinks;
                    tabcontent = document.getElementsByClassName("tabcontent");
                    for (i = 0; i < tabcontent.length; i++) {{
                        tabcontent[i].className = tabcontent[i].className.replace(" active-tab", "");
                    }}
                    tablinks = document.getElementsByClassName("tablinks");
                    for (i = 0; i < tablinks.length; i++) {{
                        tablinks[i].className = tablinks[i].className.replace(" active", "");
                    }}
                    document.getElementById(tabName).className += " active-tab";
                    if (evt) evt.currentTarget.className += " active";
                }}
                // Call openTab to set the default tab when the page loads
                document.addEventListener('DOMContentLoaded', (event) => {{
                    openTab(null, 'NewLinks');
                }});
            </script>
        </body>
        </html>
        """

        # Function to create rows HTML
        def create_rows_html(grants_list):
            rows_html = ""
            for i, grant in enumerate(grants_list, start=1):
                rows_html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{grant.get('name', 'N/A')}</td>
                        <td>{grant.get('funds', 'N/A')}</td>
                        <td>{grant.get('dates', 'N/A')}</td>
                        <td>{grant.get('requirements', 'N/A')}</td>
                        <td>{grant.get('documents', 'N/A')}</td>
                        <td>{grant.get('summary', 'N/A')}</td>
                        <td><a href="{grant.get('link', '#')}" target="_blank">Details</a></td>
                        <td>{grant.get('query', 'N/A')}</td>
                    </tr>
                """
            return rows_html

        # Categorize grants into new and reviewed
        new_links_grants = []
        reviewed_links_grants = []
        for grant_id, grant in grants_data.items():
            if grant['link'] in reviewed_links:
                reviewed_links_grants.append(grant)
            else:
                new_links_grants.append(grant)

        # Create rows HTML for New and Reviewed Links
        new_links_rows = create_rows_html(new_links_grants)
        reviewed_links_rows = create_rows_html(reviewed_links_grants)

        # Format the HTML content with the rows
        html_content = html_content.format(new_links_rows=new_links_rows, reviewed_links_rows=reviewed_links_rows)

        # Write the HTML content to the output file
        with open(output_file, 'w') as file:
            file.write(html_content)

        print(f"HTML file generated: {output_file}")




