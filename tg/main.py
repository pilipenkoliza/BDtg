import mysql.connector
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Подключение к базе данных
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cookbook",
    port='3309'
)

# Функция для создания таблицы с заданным именем
def create_table(update: Update, context: CallbackContext):
    table_name = "example_table"  # Имя таблицы по умолчанию
    if context.args:  # Если в сообщении есть аргументы, используем их как имя таблицы
        table_name = ' '.join(context.args)
    cursor = db_connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)")
    db_connection.commit()
    update.message.reply_text(f'Таблица {table_name} создана')

# Функция для удаления заданной таблицы
def delete_table(update: Update, context: CallbackContext):
    if context.args:
        table_name = ' '.join(context.args)
        cursor = db_connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        db_connection.commit()
        update.message.reply_text(f'Таблица {table_name} удалена')
    else:
        update.message.reply_text('Пожалуйста, укажите имя таблицы для удаления')

# Функция для переименования таблицы
def rename_table(update: Update, context: CallbackContext):
    if len(context.args) >= 2:
        old_table_name = context.args[0]
        new_table_name = context.args[1]
        cursor = db_connection.cursor()
        cursor.execute(f"ALTER TABLE {old_table_name} RENAME TO {new_table_name}")
        db_connection.commit()
        update.message.reply_text(f'Таблица {old_table_name} переименована в {new_table_name}')
    else:
        update.message.reply_text('Пожалуйста, укажите имя текущей таблицы и новое имя')


# Функция для вставки данных в таблицу
def insert_data(update: Update, context: CallbackContext):
    if len(context.args) >= 3:
        table_name = context.args[0]
        columns = context.args[1]
        values = context.args[2:]
        placeholders = ', '.join(['%s'] * len(values))
        cursor = db_connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        db_connection.commit()
        update.message.reply_text(f'Данные вставлены в таблицу {table_name}')
    else:
        update.message.reply_text('Использование: /insert_data table_name column1, column2 value1, value2')



# Функция для выборки данных из таблицы
def select_data(update: Update, context: CallbackContext):
    if context.args:
        table_name = context.args[0]
        cursor = db_connection.cursor(prepared=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        update.message.reply_text(f'Данные из таблицы {table_name}: {data}')
    else:
        update.message.reply_text('Пожалуйста, укажите имя таблицы для выборки данных')


def main():
    updater = Updater("6952888318:AAHJAWagf7FKdvTtMINhCy2Ux1y2hTLu2VM", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("create_table", create_table, pass_args=True))
    dispatcher.add_handler(CommandHandler("delete_table", delete_table, pass_args=True))
    dispatcher.add_handler(CommandHandler("rename_table", rename_table, pass_args=True))
    dispatcher.add_handler(CommandHandler("insert_data", insert_data, pass_args=True))
    dispatcher.add_handler(CommandHandler("select_data", select_data, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
