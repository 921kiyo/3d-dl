from slackclient import SlackClient

sc = SlackClient("xoxp-273685211557-273369142960-343515639718-246d19b1bb30d4a9c436d25dced63476")

# print("Testing API")
# print(80 * "=")
# print (sc.api_call("api.test"))

print (sc.api_call("chat.postMessage",channel="CA26521FW",
    text="I cannot be controlled :sunglasses:",username="Botty",icon_url="https://media.licdn.com/dms/image/C5603AQH1O4gyDC2HhA/profile-displayphoto-shrink_800_800/0?e=1528221600&v=alpha&t=j8JQsn43pdhaLFVWCSHgiHMYYFcVsqdW8YkLaVQM_J0",unfurl_links="true"))
