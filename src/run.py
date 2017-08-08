import plugins
import telebot


google = plugins.GoogleSearch()
yandex = plugins.YandexSearch()

bot = telebot.AsyncTeleBot(token='%token%')


@bot.message_handler(regexp='gooq:.*$')
def google_search(message):
    query = message.text.replace('gooq:', '')
    bot.send_message(message.chat.id, "Wait...")

    results = google.search(query, 10)
    results_rows = []

    for row in results:
        results_rows.append(
            "{title}\n{uri}\n\n{delimiter}".format(title=row.get('title'), uri=row.get('uri'), delimiter='#'*10)
        )

    bot.send_message(message.chat.id, "\n\n".join(results_rows), disable_web_page_preview=True)


@bot.message_handler(regexp='yaq:.*$')
def yandex_search(message):
    query = message.text.replace('yaq:', '')
    bot.send_message(message.chat.id, "Wait...search in yandex")

    results = yandex.search(query)

    results_rows = []
    for row in results:
        results_rows.append(
            "{title}\n{uri}\n@{description}\n\n{delimiter}".format(
                title=row.get('title'),
                uri=row.get('uri'),
                description=row.get('description'),
                delimiter='#' * 10
            )
        )

    bot.send_message(message.chat.id, "\n\n".join(results_rows), disable_web_page_preview=True)


bot.polling()

