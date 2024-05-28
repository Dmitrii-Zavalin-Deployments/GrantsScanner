import json

class HTMLGenerator:
    def __init__(self, data_file):
        self.data_file = data_file

    def generate_html(self, output_file='grants.html'):
        # Read the data from the JSON file
        with open(self.data_file, 'r') as file:
            grants_data = json.load(file)

        # Start of the HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Grant Details</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Grant Details</h1>
            <table>
                <tr>
                    <th>No.</th>
                    <th>Country</th>
                    <th>Max Funding</th>
                    <th>Due Date</th>
                    <th>Requirements</th>
                    <th>Submission Items</th>
                    <th>PDF Link</th>
                    <th>Query</th>
                </tr>
        """

        # Add table rows for each grant
        for i, grant in enumerate(grants_data, start=1):
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{grant.get('Country', 'N/A')}</td>
                    <td>{grant.get('MaxFunding', 'N/A')}</td>
                    <td>{grant.get('DueDate', 'N/A')}</td>
                    <td>{grant.get('Requirements', 'N/A')}</td>
                    <td>{grant.get('SubmissionItems', 'N/A')}</td>
                    <td><a href="{grant.get('PDFLink', '#')}">Details</a></td>
                    <td>{grant.get('Query', 'N/A')}</td>
                </tr>
            """

        # End of the HTML content
        html_content += """
            </table>
        </body>
        </html>
        """

        # Write the HTML content to the output file
        with open(output_file, 'w') as file:
            file.write(html_content)

        print(f"HTML file generated: {output_file}")
