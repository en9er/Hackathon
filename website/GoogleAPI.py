import os
from .GDRIVER import Create_Service_Gmail,Create_Service_Sheet,Create_Service_Drive
from googleapiclient.http import MediaFileUpload
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


CLIENT_SECRET_FILE_DRIVE = 'static_files/creds/json/client_secret.json'
CLIENT_SECRET_FILE_SHEET = 'static_files/creds/json/sheet_account.json'
CLIENT_SECRET_FILE_GMAIL = 'static_files/creds/json/client_secret.json'

drive_service = Create_Service_Drive(CLIENT_SECRET_FILE_DRIVE)
sheet_service = Create_Service_Sheet(CLIENT_SECRET_FILE_SHEET)
gmail_service = Create_Service_Gmail(CLIENT_SECRET_FILE_GMAIL)

sheet_id = '1_QhNMv1zjNtpb4HYVZhUZZWx9_qqRsQ-TqzWiMY3KFY'
drive_id = '1EfI8KyGXglFbbUqfLjzThwGVtiQiWcZJ'

currentLine = 1

def Init(driveId, sheetId, init_line):
    sheet_id = sheetId
    drive_id = driveId
    currentLine = init_line

def GetMimetype(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.pdf':
        return 'application/pdf'
    elif ext == '.jpg':
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.bmp':
        return 'image/bmp'
    elif ext == '.doc':
        return 'application/msword'
    elif ext == '.docx':
        return 'application/msword'

def PushRecieptData(mail, name, date, amount, references):
    refs = ""

    for r in references:
        refs += r + ' \n'

    refs = refs[:-1]

    range = 'A' + str(currentLine) + ':E' + str(currentLine)

    sheet_service.spreadsheets().values().batchUpdate(
        spreadsheetId=sheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range,
                "majorDimension": "ROWS",
                "values": [[mail, name, date, amount, refs]]},
        ]
        }
    ).execute()

def UploadFiles(files):
    references = []

    for file in files:
        media = MediaFileUpload(file.name,
                            mimetype=GetMimetype(file.name),
                            resumable=True)
        file_metadata = {
            'name': file.name,
            'parents': [drive_id]
        }
        googleFile = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        references.append('https://drive.google.com/file/d/' + googleFile['id'])
    
    return references
                            

def AddReceipt(mail, name, date, amount, files):
    refs = UploadFiles(files)
    PushRecieptData(mail, name, date, amount, refs)
    global currentLine
    currentLine += 1

def SendGmail(to, subject, message):
    emailMsg = message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = to
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = gmail_service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)

