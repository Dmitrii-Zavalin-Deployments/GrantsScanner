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
                    width: 100%;
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid black;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .tabcontent {{
                    display: none;
                }}
                .active-tab {{
                    display: block;
                }}
            </style>
        </head>
        <body>
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
                function openTab(evt, tabName) {
                    var i, tabcontent, tablinks;
                    tabcontent = document.getElementsByClassName("tabcontent");
                    for (i = 0; i < tabcontent.length; i++) {
                        tabcontent[i].className = tabcontent[i].className.replace(" active-tab", "");
                    }
                    tablinks = document.getElementsByClassName("tablinks");
                    for (i = 0; i < tablinks.length; i++) {
                        tablinks[i].className = tablinks[i].className.replace(" active", "");
                    }
                    document.getElementById(tabName).className += " active-tab";
                    evt.currentTarget.className += " active";
                }
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
                        <td><a href="{grant.get('link', '#')}">Details</a></td>
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
        
        
        
        