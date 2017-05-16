import webbrowser
import tweepy

def main():
    try:
        api_key = input('Please input your consuper (API) Key: ')
        api_secret = input('Please input your consumer (API) Secret: ')
        auth = tweepy.OAuthHandler(api_key, api_secret)
        redirect_url = auth.get_authorization_url()
        input('\n\nPress any key and a browser window will open. It will ask you to'
              + ' authorize the bot to your account.\nOnce you do, it will display'
              + 'a PIN number. copy it...')
        webbrowser.open(redirect_url)
        pin = input('And paste it here: ')
        auth.get_access_token(pin)
        tokenfile = open('tokens.py', 'w')
        tokenfile.write('api_key = \'{0}\'\n'.format(api_key)
                        +'api_secret = \'{0}\'\n'.format(api_secret)
                        +'access_token = \'{0}\'\n'.format(auth.access_token)
                        +'access_token_secret = \'{0}\''.format(auth.access_token_secret))
        print('Tokens saved successfuly!')
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

main()

