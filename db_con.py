import mysql.connector
import frev



def open_db(obj):
   global mydb
   try:
       mydb = mysql.connector.connect(host=obj.host, user=obj.user, password=obj.password, database=obj.db_name)
       return 0
   except mysql.connector.Error as error:
       return error



def get_client_db_list():
    res=[]
    mycursor2=mydb.cursor()
    sql2="SELECT `client_name` FROM `client` WHERE flag=1"
    mycursor2.execute(sql2)
    result=mycursor2.fetchall()
    for rec in result:
        res.append(str(rec[0]))
    return res


def change_client_flag(client_name):
    cursor1 = mydb.cursor()
    sql = "Update client set flag = 0 where client_name = %s"
    remove = []
    remove.append(str(client_name))
    cursor1.execute(sql, remove)
    mydb.commit()
    pass


def add_client(client_name):
    try:
        mycursor1=mydb.cursor()
        sql1 = "INSERT INTO `client`(`client_name`) VALUES (%s) ON DUPLICATE KEY UPDATE flag=1"
        add=[]
        add.append(str(client_name))
        mycursor1.execute(sql1,add)
        mydb.commit()
        return "Client added"
    except mysql.connector.Error as error:
        return error



def add_to_db(s2, t2):
    mycursor = mydb.cursor()
    cli_flag = 0
    add_flag = 0
    try:
     sql = "INSERT INTO `details`(`account_id`, `transaction_id`, `trans_date`, `trans_post_date`, `cheque_no`, `description`, `type`, `Trans_amt`, `avail_bal`, `client`, `purpose`, `remarks`)" \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     sql1= "INSERT INTO `details`(`account_id`, `transaction_id`, `trans_date`, `trans_post_date`, `cheque_no`, `description`, `type`, `Trans_amt`, `avail_bal`, `purpose`, `remarks`)" \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     s2[2]=frev.change_date_format(s2[2])
     s2[3]=frev.change_date_time_format(s2)
     s2[8]=frev.change_last(s2[8])
     s2[10]=frev.change_last(s2[10])
     s2[11]=frev.change_last(s2[11])
     s2=frev.bal_change(s2)
     s2[0]=t2
     if s2[9]=="Choose a Client":
         s2.remove("Choose a Client")
         cli_flag=1
         mycursor.execute(sql1,s2)
     else:
         mycursor.execute(sql,s2)
     add_flag=1
    except mysql.connector.IntegrityError:
        sql = "UPDATE `details` SET `account_id`=(%s),`transaction_id`=(%s),`trans_date`=(%s),`trans_post_date`=(%s),`cheque_no`=(%s),`description`=(%s),`type`=(%s),"\
              "`Trans_amt`=(%s),`avail_bal`=(%s),`client`=(%s),`purpose`=(%s),`remarks`=(%s) WHERE `account_id`=(%s) AND`transaction_id`=(%s)"

        sql1 = "UPDATE `details` SET `account_id`=(%s),`transaction_id`=(%s),`trans_date`=(%s),`trans_post_date`=(%s),`cheque_no`=(%s),`description`=(%s),`type`=(%s),"\
              "`Trans_amt`=(%s),`avail_bal`=(%s),`purpose`=(%s),`remarks`=(%s) WHERE `account_id`=(%s) AND`transaction_id`=(%s)"

        s2.append(t2)
        s2.append(s2[1])
        if cli_flag:
            mycursor.execute(sql1, s2)
        else:
            mycursor.execute(sql, s2)
        add_flag=1
    except:
        pass
    mydb.commit()
    mycursor.close()
    return add_flag


def close_db():
    global mydb
    mydb.close()