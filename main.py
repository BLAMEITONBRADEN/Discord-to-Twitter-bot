import discord
import tweepy
import requests
import asyncio

# Replace these with your own API key and secret
consumer_key = 'API_KEY'
consumer_secret = 'API_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Use OAuth to authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Replace this with your bot's token
bot_token = 'TOKEN_HERE'

# Create a Discord client
client = discord.Client()

@client.event
async def on_message(message):
    # Only respond to messages in the specified channel
    if message.channel.id == CHANNEL_ID_HERE:
        # Check if the message starts with the prefix "!"
        if message.content.startswith('!'):
            # Split the message into command and arguments
            command, *args = message.content.split()

            # Check the command and respond accordingly
            if command == '!tweet':
                # Get the text of the tweet (everything after the command)
                tweet_text = ' '.join(args)

                try:
                    # Check if the message has any attached media (images, videos, GIFs)
                    if message.attachments:
                        media_url = message.attachments[0].url

                        # Download the media file
                        response = requests.get(media_url)
                        media_data = response.content

                        # Save the media file to the local filesystem
                        with open('media.jpg', 'wb') as f:
                            f.write(media_data)

                        # Upload the media to Twitter
                        media_id = api.media_upload('media.jpg').media_id

                        # Include the media in the tweet
                        tweet = api.update_status(status=tweet_text, media_ids=[media_id])
                    else:
                        # Post the tweet
                        tweet = api.update_status(tweet_text)

                    # Get the URL of the tweet
                    tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"

                    # Send the URL of the tweet to the Discord channel
                    await message.channel.send(tweet_url)

                except Exception as e:
                    # Create the embed with the error message
                    embed = discord.Embed(title="Error", description=str(e), color=0xff0000)

                    # Send the embed to the Discord channel
                    msg = await message.channel.send(embed=embed)

                    # Delay the deletion of the message by 30 seconds
                    await asyncio.sleep(30)

                    # Delete the message
                    await msg.delete()


# Run the Discord client
client.run(bot_token)
