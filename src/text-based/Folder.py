# External Libraries
import imaplib  # Used in exception catching

def ViewFolders(conn):
    folders = conn.list_folders()
    print 'FOLDERS'
    for flags, delimiter, folder_name in folders:
        print '- %s' % folder_name, "\n"
    return folders


def SelectFolder(conn):

    folders = conn.list_folders()

    folderName = raw_input("Choose a folder: ")
    folderName = folderName.upper()

    b_folder_found = False

    for flags, delimiter, folder_name in folders:
        if folderName in [folder_name]:
            conn.close_folder
            conn.select_folder(folderName)
            print "Folder Set To: ", folderName
            return folderName
    if not b_folder_found:
        raise ReferenceError("Could not select folder")
    print "FOLDER NOT FOUND"
    return


def new_folder(conn):
    create = raw_input("Folder Name: ")
    create = create.upper()
    try:
        conn.create_folder(create)
        print "Folder ", create, " created..."
    except imaplib.IMAP4.error as inst:
        print "Error: "
        print inst.args

def delete_folder(conn):
    delete = raw_input("Folder to Delete: ")
    delete = delete.upper()
    try:
        conn.delete_folder(delete)
        print "Folder ", delete, " deleted..."
    except imaplib.IMAP4.error as inst:
        print "Error: "
        print inst.args
