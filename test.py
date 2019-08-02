import requests


def main():

    filePath = './front_door.jpg'
    url = 'http://ccrc.twnict.com/function/upload_img.php'
    img = {'img':open(filePath, 'rb')}

    req = requests.Request("POST", url, files=img)
    prepared = req.prepare()

    print(prepared.body)
    # print("Post Response: %s" % str(r.content).replace("<br/>","\n"))


if __name__ == "__main__":
    main()

