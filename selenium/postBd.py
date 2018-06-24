import psycopg2


# cursor.execute("SELECT * FROM public.tnved"

class update_session():

    def __init__(self,conn,cr):
        """Constructor"""
        self.session = {}
        self.conn = conn
        self.cr = cr
    # def __del__(self):
    #     print ("ME DELETED")
    #     if connection:
    #         try:
    #             connection.close()
    #             print ("connection close good.")
    #             pass
    #         except Exception as o:
    #             print (o)
    #             pass

    def close_session(self):
        
        sql = """UPDATE public.update_index
                SET state = 'close'
                WHERE id_num={id_num}""".format(id_num=self.session["id_num"])
        self.cr.execute(sql)
        self.conn.commit()
        # connection.close()

    def record_to_object(self,cursor,record):
        colnames = [desc[0] for desc in cursor.description]
        ooo = {}
        for p in range(len(colnames)):
            ooo[colnames[p]] = record[p]

        return ooo

    def find_session(self):   
        sql = "SELECT * FROM public.update_index WHERE state='open' or state='new'"
        self.cr.execute(sql)
        res = self.cr.fetchall()
        if not res: return False
        res = self.record_to_object(self.cr,res[0])
        return res

    def open_session(self):
        
        sql = """SELECT * 
        FROM public.update_index
            """
        self.cr.execute(sql)
        rows = self.cr.rowcount
        sql = """INSERT INTO public.update_index
            (id_num, state)
            VALUES 
            (%s,%s)
            """
        self.cr.execute(sql,(rows+1,"new"))
        self.conn.commit()
        return self.find_session()

    def reg_session(self):
        res = self.find_session()
        if not res:
            res = self.open_session()
        self.session = res
        return res
        

    def update_record_session(self):
        
        sql = """ SELECT * FROMpublic.update_index
            FROM public.update_index 
            ORDER BY id_num 
            DESC LIMIT 1"""
        # sql = "SUPDATE public.update_index SET state = 'state' WHERE id_num = 'id_num';"
        self.cr.execute(sql,("State",1))
        updated_rows = self.cr.rowcount
        # Commit the changes to the database
        self.conn.commit()
        # Close communication with the PostgreSQL database
        # connection.close()
        # results = cursor.fetchall()
        # print (results[0])
        # # connection.commit()
        # cursor.close()


update_index_fields = [
    {"name":"id_num",
    "type":"integer",
    "default":0},
    {"name":"start_time",
    "type":"date",
    "default":""},
    {"name":"state",
    "type":"text",
    "default":""},
    {"name":"balance",
    "type":"json",
    "default":""}
]

class tnved_updater():
    def __init__(self,root_list=[],upload_item={}):
        """Constructor"""
        
        conn = psycopg2.connect(dbname='fgis', user='openpg', password='openpgpwd')
        cr = conn.cursor()
        up = update_session(conn=conn,cr=cr)
        self.root_list = root_list
        self.upload_item = upload_item
        self.conn = conn
        self.сr = cr
        self.update_session = up
        self.session = up.reg_session()
        # upload_session = update_session()
        # up_ob = upload_session.get_session()


    def __del__(self):
        if self.сr:
            self.сr.close()
        if self.conn:
            self.conn.close()
            
    tv_ved_fields = [
        {"name":"id",
        "type":"integer",
        "default":0},
        {"name":"code",
        "type":"character varying",
        "default":""},
        {"name":"label",
        "type":"text",
        "default":""},
        {"name":"load_on_demand",
        "type":"boolean",
        "default":True},
        {"name":"arhive",
        "type":"boolean",
        "default":False},
        {"name":"update_index_id_num",
        "type":"integer",
        "default":0}
    ]

    def record_to_object(self,cursor,record):
        colnames = [desc[0] for desc in cursor.description]
        ooo = {}
        for p in range(len(colnames)):
            ooo[colnames[p]] = record[p]
        return ooo

    def count_to_parse(self):
        record={}
        conn = psycopg2.connect(dbname='fgis', user='openpg', password='openpgpwd')
        cr = conn.cursor()
        sql = "SELECT count(id) FROM public.wait_parse WHERE load_on_demand=True AND parsed=False"
        cr.execute(sql) 
        record["more"] = cr.fetchall()[0]
        sql = "SELECT count(id) FROM public.wait_parse WHERE load_on_demand=False"
        cr.execute(sql) 
        record["done"] = cr.fetchall()[0]

        cr.close()
        conn.close()
        return record

    def record_next_parse(self):
        sql = "SELECT * FROM public.wait_parse WHERE load_on_demand=True AND parsed=False ORDER BY id ASC LIMIT 1"
        self.сr.execute(sql) 
        if not self.сr.rowcount:
            self.update_session.close_session()
            return {}
        record = self.сr.fetchall()[0]
        return self.record_to_object(self.сr,record)  

    def get_data(self,d):
        res = {}
        for f in self.tv_ved_fields:
            if f["name"] in d:
                res[f["name"]] = d[f["name"]]
            else:
                res[f["name"]] = f["default"]
        res["update_index_id_num"] = self.session["id_num"]        
        return res 


  
    def truncate_to_parse(self):
        
        self.сr.execute("TRUNCATE wait_parse")
        self.conn.commit()
 

    def insert_to_parse(self,previous_id=0,data=[]):
        if previous_id:
            sql = "UPDATE public.wait_parse  SET parsed = True WHERE id={id}".format(id=str(previous_id))
            self.сr.execute(sql) 
            self.conn.commit()                    
        names = [i["name"] for i in  self.tv_ved_fields ]
        for d in data:
            o = self.get_data(d)
            sql = "INSERT INTO public.wait_parse "
            sql += "(" + ", ".join(names) + ")"
            sql += " VALUES (" + ", ".join(["%s" for t in o]) + ")"
            q = [o[i["name"]] for i in self.tv_ved_fields ]
            self.сr.execute(sql,tuple(q)) 
            self.conn.commit()

            
    def insert_tnved(self,data = {}):
        try:
            
            names = [i["name"] for i in  self.tv_ved_fields ]
            u = "(" + ", ".join(names) + ")"
            sql = "INSERT INTO public.tnved "
            sql += u
            data = self.get_data(data)
            sql += " VALUES (" + ", ".join(["%s" for t in data]) + ")"
            q = [data[i["name"]] for i in self.tv_ved_fields ]
            try:
                self.сr.execute(sql,tuple(q)) 
            except psycopg2.IntegrityError as o:
                self.conn.rollback()
                raise o
            else:
                self.conn.commit()
                return data
        except Exception as  e:             
            return  e


    def update_tnved(self,data = {}):
        try:
            
            names = [i["name"] for i in  self.tv_ved_fields ]
            u = "(" + ", ".join(names) + ")"
            sql = "INSERT INTO public.tnved "
            sql += u
            data = self.get_data(data)
            sql += " VALUES (" + ", ".join(["%s" for t in data]) + ")"
            q = [data[i["name"]] for i in self.tv_ved_fields ]

            try:
                self.сr.execute(sql,tuple(q)) 
            except psycopg2.IntegrityError as o:
                self.conn.rollback()
                raise o
            else:
                self.conn.commit()
                return data


        except Exception as  e:   
            
            return  e