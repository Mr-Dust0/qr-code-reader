# QR code reader
This Python project allows users to scan a QR code, which contains the file path of a PDF. Upon scanning, the corresponding PDF file is displayed to the user. Additionally, the system logs the time and details of when the PDF was opened to a centralized server which is running the complementary go [webserver](https://github.com/Mr-Dust0/go-log-webserver) to add the logs to the database and display them in an friendly way. This helps administrators monitor and track the files being accessed, providing insights into which projects are currently active and when the file was closed to see how long the project was worked on for.
Features

- QR Code Scanning: Scan QR codes containing file paths to open PDFs.
- PDF Display: Automatically display the PDF file referenced by the QR code.
- Activity Logging: Log each time a PDF is accessed with a timestamp and user details to a central server for tracking purposes.
- Admin Monitoring: Admins can view logs to track which PDFs are being accessed and monitor ongoing projects.
